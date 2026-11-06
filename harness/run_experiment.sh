#!/usr/bin/env bash
# Эксперимент Э3, часть 1: время обнаружения отказа.
# Запускается на узле-наблюдателе — узле, направляющем трафик (раздел 3.4).
# Встречный узел (на стенде — С2, объект внесения отказа) несёт второй
# экземпляр детектора. Стенд описан в разделе 2.1 и в README.md.
#
# Способ внесения отказа задаётся переменной MODE:
#   process — завершение процесса детектора на встречном узле по SSH (kill -9)
#   pause   — приостановка процесса (SIGSTOP): отказ О3 раздела 2.3, воспроизводит
#             зависание; сигнал не перехватывается и не игнорируется
#   link    — разрыв связности через nftables на стороне наблюдателя
#   power   — снятие электропитания через контроллер управления сервера
#             (Redfish ForceOff, раздел 2.1); заполнить POWER_OFF_CMD / POWER_ON_CMD
#
# Использование:
#   MODE=process PEER=192.168.1.20 REPS=30 ./run_experiment.sh

set -euo pipefail

MODE="${MODE:-process}"
PEER="${PEER:?укажите PEER=<адрес встречного узла>}"
PEER_USER="${PEER_USER:-$USER}"
REPS="${REPS:-30}"
TAU="${TAU:-26ms}"
K="${K:-5}"
M="${M:-3}"
SETTLE="${SETTLE:-3}"      # с, ожидание установления сессии
RECOVER="${RECOVER:-5}"    # с, ожидание восстановления между повторностями
OUT="${OUT:-run-$(date +%Y%m%d-%H%M%S)}"

POWER_OFF_CMD="${POWER_OFF_CMD:-echo 'ЗАПОЛНИТЕ POWER_OFF_CMD'}"
POWER_ON_CMD="${POWER_ON_CMD:-echo 'ЗАПОЛНИТЕ POWER_ON_CMD'}"

mkdir -p "$OUT"
DET_LOG="$OUT/detector.jsonl"
INJ_LOG="$OUT/inject.log"
: > "$INJ_LOG"

echo "режим=$MODE  повторностей=$REPS  τ=$TAU  k=$K  m=$M"
echo "каталог результатов: $OUT"

./detector -listen :4000 -peer "$PEER:4000" -tau "$TAU" -k "$K" -m "$M" \
           -log "$DET_LOG" > "$OUT/detector.out" 2>&1 &
DET_PID=$!
trap 'kill $DET_PID 2>/dev/null || true' EXIT
sleep "$SETTLE"

start_peer() {
  case "$MODE" in
    process|pause)
             ssh "$PEER_USER@$PEER" "pkill -9 -f '^./detector' || true; nohup ./detector -listen :4000 -peer $(hostname -I | awk '{print $1}'):4000 -tau $TAU -k $K -m $M -log /tmp/peer.jsonl >/dev/null 2>&1 &" ;;
    link)    sudo nft delete table inet e3 2>/dev/null || true ;;
    power)   eval "$POWER_ON_CMD" ;;
  esac
}

inject_failure() {
  case "$MODE" in
    process) ssh "$PEER_USER@$PEER" "pkill -9 -f '^./detector' || true" ;;
    pause)   ssh "$PEER_USER@$PEER" "pkill -STOP -f '^./detector' || true" ;;
    link)    sudo nft add table inet e3 2>/dev/null || true
             sudo nft add chain inet e3 out '{ type filter hook output priority 0; }' 2>/dev/null || true
             sudo nft add rule inet e3 out ip daddr "$PEER" drop ;;
    power)   eval "$POWER_OFF_CMD" ;;
  esac
}

for i in $(seq 1 "$REPS"); do
  printf "повторность %2d/%d: " "$i" "$REPS"
  start_peer
  sleep "$SETTLE"

  # фаза отказа внутри периода τ рандомизируется: без этого отказ всегда
  # приходится на одну и ту же точку цикла и среднее смещается к kτ
  # вместо расчётного (k − 1/2)τ (см. README, «Фаза внесения отказа»)
  sleep "$(awk -v s="$RANDOM" -v t="${TAU%ms}" 'BEGIN{srand(s); printf "%.6f", rand()*t/1000}')"

  # момент внесения отказа фиксируется непосредственно перед действием
  date +%s%N >> "$INJ_LOG"
  inject_failure
  printf "отказ внесён, ожидание обнаружения... "

  sleep "$RECOVER"
  echo "готово"
done

kill $DET_PID 2>/dev/null || true
sleep 1

echo
echo "обработка результатов:"
python3 analyze.py "$DET_LOG" "$INJ_LOG" --tau "${TAU%ms}" --k "$K" | tee "$OUT/report.txt"
echo
echo "протоколы сохранены в $OUT — приложить к диссертации как протокол измерений"
