// Детектор отказа на основе двустороннего контроля пересылки (BFD).
// Реализация к разделу 3.4 диссертации. Измерительная обвязка для эксперимента Э3.
//
// Оба узла запускают один и тот же двоичный файл. Каждый узел периодически
// отправляет контрольные сообщения и следит за приёмом встречных. Отказ
// признаётся после k подряд не полученных сообщений, возврат — после m
// подряд полученных (несимметричные правила, раздел 3.4).
//
// Сборка:   go build -o detector detector.go
// Запуск:   ./detector -listen :4000 -peer 192.168.1.20:4000 -tau 26ms -k 5 -m 3 -log node1.jsonl
package main

import (
	"encoding/binary"
	"encoding/json"
	"flag"
	"fmt"
	"net"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"
)

const msgSize = 24 // seq(8) + wallNano(8) + magic(8)
const magic uint64 = 0x42464400444554 // маркер для отбрасывания посторонних пакетов

type event struct {
	WallNano  int64   `json:"t_wall_ns"`     // системное время события
	MonoMicro int64   `json:"t_mono_us"`     // монотонное время от старта, мкс
	Event     string  `json:"event"`         // sent | recv | down | up
	Seq       uint64  `json:"seq,omitempty"`
	GapMs     float64 `json:"gap_ms,omitempty"`      // с последнего приёма
	LastRecv  int64   `json:"last_recv_mono_us,omitempty"`
	Missed    int     `json:"missed,omitempty"`
}

type logger struct {
	mu   sync.Mutex
	enc  *json.Encoder
	f    *os.File
	t0   time.Time
}

func newLogger(path string, t0 time.Time) (*logger, error) {
	f, err := os.Create(path)
	if err != nil {
		return nil, err
	}
	return &logger{enc: json.NewEncoder(f), f: f, t0: t0}, nil
}

func (l *logger) log(e event) {
	e.WallNano = time.Now().UnixNano()
	e.MonoMicro = time.Since(l.t0).Microseconds()
	l.mu.Lock()
	_ = l.enc.Encode(e)
	l.mu.Unlock()
}

func (l *logger) close() { _ = l.f.Sync(); _ = l.f.Close() }

func main() {
	listen := flag.String("listen", ":4000", "адрес приёма")
	peer := flag.String("peer", "", "адрес встречного узла (обязательно)")
	tau := flag.Duration("tau", 26*time.Millisecond, "период контрольных сообщений τ")
	k := flag.Int("k", 5, "пороговое число подряд не полученных сообщений")
	m := flag.Int("m", 3, "число подтверждающих сообщений для возврата")
	logPath := flag.String("log", "detector.jsonl", "файл протокола")
	flag.Parse()

	if *peer == "" {
		fmt.Fprintln(os.Stderr, "не задан -peer")
		os.Exit(2)
	}

	t0 := time.Now()
	lg, err := newLogger(*logPath, t0)
	if err != nil {
		fmt.Fprintln(os.Stderr, "протокол:", err)
		os.Exit(1)
	}
	defer lg.close()

	laddr, err := net.ResolveUDPAddr("udp", *listen)
	if err != nil {
		fmt.Fprintln(os.Stderr, "listen:", err)
		os.Exit(1)
	}
	paddr, err := net.ResolveUDPAddr("udp", *peer)
	if err != nil {
		fmt.Fprintln(os.Stderr, "peer:", err)
		os.Exit(1)
	}
	conn, err := net.ListenUDP("udp", laddr)
	if err != nil {
		fmt.Fprintln(os.Stderr, "сокет:", err)
		os.Exit(1)
	}
	defer conn.Close()

	var (
		mu       sync.Mutex
		lastRecv = time.Since(t0) // монотонное время последнего приёма
		up       = false          // начальное состояние — «путь неработоспособен»
		consecOK = 0
	)

	// приём встречных сообщений
	go func() {
		buf := make([]byte, 64)
		for {
			n, _, err := conn.ReadFromUDP(buf)
			if err != nil || n < msgSize {
				continue
			}
			if binary.BigEndian.Uint64(buf[16:24]) != magic {
				continue
			}
			seq := binary.BigEndian.Uint64(buf[0:8])
			now := time.Since(t0)

			mu.Lock()
			gapDur := now - lastRecv
			gap := gapDur.Seconds() * 1000
			// «подряд полученные»: пропуск разрывает серию
			if gapDur > time.Duration(1.5*float64(*tau)) {
				consecOK = 1
			} else {
				consecOK++
			}
			lastRecv = now
			becameUp := false
			if !up && consecOK >= *m {
				up = true
				becameUp = true
			}
			mu.Unlock()

			lg.log(event{Event: "recv", Seq: seq, GapMs: gap})
			if becameUp {
				lg.log(event{Event: "up", Seq: seq})
				fmt.Printf("[%8.3f с] ВОЗВРАТ: путь работоспособен\n", time.Since(t0).Seconds())
			}
		}
	}()

	// отправка контрольных сообщений
	go func() {
		var seq uint64
		out := make([]byte, msgSize)
		t := time.NewTicker(*tau)
		defer t.Stop()
		for range t.C {
			seq++
			binary.BigEndian.PutUint64(out[0:8], seq)
			binary.BigEndian.PutUint64(out[8:16], uint64(time.Now().UnixNano()))
			binary.BigEndian.PutUint64(out[16:24], magic)
			_, _ = conn.WriteToUDP(out, paddr)
			lg.log(event{Event: "sent", Seq: seq})
		}
	}()

	// контроль истечения предельного времени ожидания
	go func() {
		// проверка чаще периода, чтобы разрешающая способность не ухудшала измерение
		t := time.NewTicker(*tau / 4)
		defer t.Stop()
		deadline := time.Duration(*k) * *tau
		for range t.C {
			now := time.Since(t0)
			mu.Lock()
			idle := now - lastRecv
			becameDown := false
			lr := lastRecv
			if up && idle > deadline {
				up = false
				consecOK = 0 // сброс только в момент перехода, не на каждом тике
				becameDown = true
			}
			mu.Unlock()

			if becameDown {
				lg.log(event{
					Event:    "down",
					GapMs:    idle.Seconds() * 1000,
					LastRecv: lr.Microseconds(),
					Missed:   *k,
				})
				fmt.Printf("[%8.3f с] ОТКАЗ: не получено %d сообщений подряд, простой канала %.1f мс\n",
					now.Seconds(), *k, idle.Seconds()*1000)
			}
		}
	}()

	fmt.Printf("детектор запущен: τ=%v, k=%d, m=%d, предельное время ожидания %v\n",
		*tau, *k, *m, time.Duration(*k)**tau)
	fmt.Printf("приём %s, встречный узел %s, протокол %s\n", *listen, *peer, *logPath)

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
	<-sig
	fmt.Println("\nостановлен")
}
