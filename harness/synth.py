#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ГЕНЕРАТОР МОДЕЛЬНЫХ ДАННЫХ для отработки структуры раздела 3.5.

ВНИМАНИЕ. Выдаваемые значения НЕ ЯВЛЯЮТСЯ РЕЗУЛЬТАТАМИ ИЗМЕРЕНИЙ.
Это синтетические данные, порождённые статистической моделью, и служат
исключительно для отработки формы представления результатов, проверки
обработки и вёрстки таблиц и рисунков. Перед любым использованием работы
по назначению они подлежат замене на протоколы натурного эксперимента,
получаемые обвязкой из этого же каталога (detector.go, run_experiment.sh).

Модель порождения времени обнаружения отражает три реальных эффекта:
  1) фаза отказа внутри периода τ — равномерна, даёт разброс [(k-1)τ, kτ];
  2) дрожание планировщика и сетевого стека — нормальная добавка;
  3) выбросы — редкие задержки планирования, тяжёлый правый хвост.
"""
import json
import math
import random
import statistics as st

SEED = 20260903
random.seed(SEED)

TAU_MS, K, M = 26.0, 5, 3
P_LOSS = 0.01
Y_SEC = 365 * 24 * 3600
N_REP = 30

JITTER_SD = 2.4      # мс, дрожание планировщика и сетевого стека
OUTLIER_P = 0.04     # доля выбросов
OUTLIER_ADD = (25, 90)   # мс, добавка выброса

TR_METHOD_MS = (1.6, 0.5)    # прямая запись в таблицу распределения: среднее, СКО
TR_PLATFORM_MS = (1120, 180)  # через интерфейс управления платформы


def detect_times(tau, k, n=N_REP):
    """Время обнаружения: фаза + дрожание + выбросы."""
    out = []
    for _ in range(n):
        phase = random.random() * tau          # момент отказа внутри периода
        base = k * tau - phase                 # от отказа до истечения ожидания
        v = base + random.gauss(0, JITTER_SD)
        if random.random() < OUTLIER_P:
            v += random.uniform(*OUTLIER_ADD)
        out.append(max(v, 0.1))
    return out


def lognormalish(mean, sd, n=N_REP):
    return [max(random.gauss(mean, sd), 0.05) for _ in range(n)]


def ci95(xs):
    n = len(xs)
    if n < 2:
        return float("nan")
    t = 2.045 if n <= 30 else 2.0
    return t * st.stdev(xs) / math.sqrt(n)


def fmt(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def nu_model(tau_ms, k, p=P_LOSS):
    """Интенсивность ложных признаний по (3.18), 1/с."""
    return (1 - p) * (p ** k) / (tau_ms / 1000.0)


# ---------- Э3, часть 1: время обнаружения по способам внесения отказа ----------
scenarios = [
    ("остановка процесса", "предлагаемый метод", TAU_MS, K),
    ("разрыв связности", "предлагаемый метод", TAU_MS, K),
    ("обесточивание узла", "предлагаемый метод", TAU_MS, K),
]
table36 = []
for name, mech, tau, k in scenarios:
    d = detect_times(tau, k)
    tr = lognormalish(*TR_METHOD_MS)
    full = [a + b for a, b in zip(d, tr)]
    table36.append({
        "способ": name, "механизм": mech, "n": len(d),
        "To_ms": st.mean(d), "To_ci": ci95(d),
        "Tr_ms": st.mean(tr), "full_ms": st.mean(full),
        "To_min": min(d), "To_max": max(d), "raw": d,
    })

# Штатный механизм. Время обнаружения порождается по соотношению (1.3)
# раздела 1.3: T_о = 50 − U(0;10) + U(0;5), диапазон 40–55 с, среднее 47,5 с (версия 1.32+).
# Несогласованность моментов отказа, передачи сведений о состоянии (10 с) и
# проверки их контроллером (5 с). Вытеснение экземпляров — через 300 с.
std_det = [50.0 - random.uniform(0, 10) + random.uniform(0, 5) for _ in range(N_REP)]
std_tr = [x / 1000 for x in lognormalish(*TR_PLATFORM_MS)]
std_full = [a + 300 + b for a, b in zip(std_det, std_tr)]
table36.append({
    "способ": "обесточивание узла", "механизм": "штатный", "n": N_REP,
    "To_ms": st.mean(std_det) * 1000, "To_ci": ci95(std_det) * 1000,
    "Tr_ms": st.mean(std_tr) * 1000, "full_ms": st.mean(std_full) * 1000,
    "To_min": min(std_det) * 1000, "To_max": max(std_det) * 1000, "raw": std_det,
})

# ---------- Э2: проверка модели при разных настройках ----------
# Периоды взяты из набора общеупотребительных значений RFC 7419:
# 10 / 20 / 50 / 100 мс (3,3 мс ниже реализуемого предела, часть 4). Пороговое число подобрано так, чтобы
# охватить время обнаружения от 25 до 250 мс.
settings = [(100.0, 3), (50.0, 4), (20.0, 5), (10.0, 6), (10.0, 3)]
lam_exp = 0.1  # 1/с, повышенная интенсивность внесения отказов
table35 = []
for tau, k in settings:
    d = detect_times(tau, k)
    tr = lognormalish(*TR_METHOD_MS)
    To_m, Tr_m = st.mean(d) / 1000, st.mean(tr) / 1000
    nu = nu_model(tau, k)
    kp_calc = lam_exp * (To_m + Tr_m) + nu * Tr_m
    # измеренный простой: сумма фактических интервалов + шум учёта
    kp_meas = lam_exp * st.mean([a / 1000 + b / 1000 for a, b in zip(d, tr)])
    kp_meas *= random.uniform(0.96, 1.07)
    table35.append({
        "tau": tau, "k": k, "To_calc": (k - 0.5) * tau, "To_meas": st.mean(d),
        "To_ci": ci95(d), "Tr_meas": st.mean(tr),
        "kp_meas": kp_meas, "kp_calc": kp_calc,
        "dev": abs(kp_meas - kp_calc) / kp_calc * 100,
    })

# ---------- Э3, часть 2: ложные признания отказа ----------
# Интенсивность ложных срабатываний при эксплуатационном p = 0,01 составляет
# доли события в год, поэтому измеряется при заведомо завышенных потерях, а
# закон (3.18) проверяется по показателю степени: ln ν линеен по ln p с
# наклоном k. Окно наблюдения подбирается под ~30 событий на точку.
def poisson(lmbda):
    """Число событий пуассоновского потока (метод Кнута)."""
    if lmbda > 500:
        return max(0, int(round(random.gauss(lmbda, math.sqrt(lmbda)))))
    l, kk, pp = math.exp(-lmbda), 0, 1.0
    while True:
        kk += 1
        pp *= random.random()
        if pp <= l:
            return kk - 1


table37 = []
# Пять точек по диапазону, назначенному в разделе 2.3: 0,10–0,30 с шагом 0,05.
# Окно наблюдения подобрано так, чтобы на каждой точке было не менее 30 событий.
for p, hours in ((0.10, 30.0), (0.15, 5.0), (0.20, 1.2), (0.25, 0.45), (0.30, 0.15)):
    nu_s = (1 - p) * (p ** K) / (TAU_MS / 1000.0)
    secs = hours * 3600
    observed = poisson(nu_s * secs)
    nu_obs = observed / secs
    table37.append({
        "p": p, "hours": hours, "n_fp": observed,
        "nu_meas_h": nu_obs * 3600, "nu_calc_h": nu_s * 3600,
        "nu_meas_s": nu_obs, "nu_calc_s": nu_s,
    })

# проверка показателя степени: наклон ln ν по ln p должен равняться k
_lp = [math.log(r["p"]) for r in table37 if r["n_fp"] > 0]
_ln = [math.log(r["nu_meas_s"]) for r in table37 if r["n_fp"] > 0]
_n = len(_lp)
_mx, _my = sum(_lp) / _n, sum(_ln) / _n
SLOPE = sum((x - _mx) * (y - _my) for x, y in zip(_lp, _ln)) / sum((x - _mx) ** 2 for x in _lp)
NU_OPER = (1 - P_LOSS) * (P_LOSS ** K) / (TAU_MS / 1000.0) * Y_SEC  # расчёт по (3.18) при p=0,01
# экстраполяция подобранной прямой ln ν = a + SLOPE·ln p на p = 0,01 (раздел 3.5)
NU_EXTRAP = math.exp(_my + SLOPE * (math.log(P_LOSS) - _mx)) * Y_SEC

# ---------- Э3, часть 4: реализуемый период, естественная вероятность потери,
# ---------- служебная нагрузка ----------
# Период считается реализуемым, пока средний фактический промежуток между
# отправками отличается от ожидаемого при дрожании 0,875·τ не более чем на 5 %.
TAU_MIN_TRUE = 4.2          # мс, предел реализации на стенде
tau_min_meas = [TAU_MIN_TRUE + random.gauss(0, 0.25) for _ in range(N_REP)]
TAU_MIN = st.mean(tau_min_meas)
TAU_MIN_CI = ci95(tau_min_meas)
# Ближайшее общеупотребительное значение не ниже измеренного предела
TAU_COMMON = [3.3, 10.0, 20.0, 50.0, 100.0, 1000.0]
TAU_MIN_USABLE = min(t for t in TAU_COMMON if t >= TAU_MIN)

# Естественная вероятность непринятия контрольного сообщения при τ = τ_min набора (10 мс):
# потеря либо запаздывание сверх периода. Измеряется раздельно по каналам.
def p_natural(mean, rel_sd=0.22, n=N_REP):
    return [max(random.gauss(mean, mean * rel_sd), 0.0) for _ in range(n)]

p_intra = p_natural(2.1e-4)
p_inter = p_natural(4.3e-3)
P_INTRA, P_INTRA_CI = st.mean(p_intra), ci95(p_intra)
P_INTER, P_INTER_CI = st.mean(p_inter), ci95(p_inter)

# Служебная нагрузка на наиболее нагруженном узле стенда:
# S сессий, по каждой 1/τ сообщений в секунду в каждую сторону, L = 90 байт.
L_BYTES, S_STAND = 90, 3
def overhead_mbit(tau_ms, s=S_STAND, l=L_BYTES):
    return 2 * s / (tau_ms / 1000.0) * l * 8 / 1e6

B_CALC = overhead_mbit(TAU_MS)
B_MEAS = B_CALC * random.uniform(1.02, 1.09)   # учёт повторных передач и служебных кадров

if __name__ == "__main__":
    print("=" * 72)
    print("МОДЕЛЬНЫЕ ДАННЫЕ — НЕ РЕЗУЛЬТАТЫ ИЗМЕРЕНИЙ")
    print(f"зерно генератора {SEED}; подлежат замене протоколами эксперимента")
    print("=" * 72)

    print("\n--- Таблица 3.5 (Э2) ---")
    for r in table35:
        _t = fmt(r['tau'], 0 if float(r['tau']).is_integer() else 1)
        print(f"| {_t} | {r['k']} | {fmt(r['To_calc'])} | {fmt(r['To_meas'])} "
              f"| {fmt(r['Tr_meas'],2)} | {fmt(r['kp_meas']*1000,2)} | {fmt(r['kp_calc']*1000,2)} "
              f"| {fmt(r['dev'])} |")

    print("\n--- Таблица 3.6 (Э3, часть 1) ---")
    for r in table36:
        u = 1000 if r["механизм"] == "штатный" else 1
        print(f"| {r['способ']} | {r['механизм']} | {r['n']} | "
              f"{fmt(r['To_ms']/u, 1 if u>1 else 1)} | {fmt(r['Tr_ms']/u,2)} | "
              f"{fmt(r['full_ms']/u,1)} | ±{fmt(r['To_ci']/u)} |")

    print("\n--- Таблица 3.7 (Э3, часть 2) ---")
    for r in table37:
        _h = fmt(r['hours'], 0 if float(r['hours']).is_integer() else 2)
        print(f"| {fmt(r['p']*100,0)} | {_h} | {r['n_fp']} | "
              f"{fmt(r['nu_meas_h'],2)} | {fmt(r['nu_calc_h'],2)} |")
    print(f"\nпоказатель степени по наклону ln ν(ln p): {fmt(SLOPE,2)} при k = {K}")
    print(f"p = 0,01: экстраполяция прямой ν = {fmt(NU_EXTRAP,3)} 1/год, расчёт по (3.18) ν = {fmt(NU_OPER,3)} 1/год")

    print("\n--- Э3, часть 4: реализуемый период, вероятность потери, нагрузка ---")
    print(f"  наименьший реализуемый период: {fmt(TAU_MIN,2)} ± {fmt(TAU_MIN_CI,2)} мс; "
          f"ближайшее общеупотребительное значение не ниже — {fmt(TAU_MIN_USABLE,1)} мс")
    print(f"  вероятность непринятия при τ = {fmt(TAU_MIN_USABLE,0)} мс:")
    print(f"    внутриплощадочный канал  {P_INTRA:.2e} ± {P_INTRA_CI:.1e}")
    print(f"    межплощадочный канал     {P_INTER:.2e} ± {P_INTER_CI:.1e}")
    print(f"  служебная нагрузка при {S_STAND} сессиях и τ = {fmt(TAU_MS,0)} мс: "
          f"расчёт {fmt(B_CALC,3)} Мбит/с, измерено {fmt(B_MEAS,3)} Мбит/с "
          f"({fmt(B_MEAS/1000*100,3)} % канала 1 Гбит/с)")

    all_d = table36[0]["raw"]
    print(f"\nсводка по времени обнаружения (τ=26 мс, k=5), n={len(all_d)}:")
    print(f"  среднее {fmt(st.mean(all_d))} мс, медиана {fmt(st.median(all_d))} мс, "
          f"ДИ ±{fmt(ci95(all_d))} мс")
    print(f"  границы модели [{fmt((K-1)*TAU_MS)}; {fmt(K*TAU_MS)}] мс, "
          f"расчёт {fmt((K-0.5)*TAU_MS)} мс")
    inside = sum(1 for x in all_d if (K-1)*TAU_MS <= x <= K*TAU_MS)
    print(f"  в границах модели {inside} из {len(all_d)}")

    with open("synth_data.json", "w", encoding="utf-8") as f:
        json.dump({"seed": SEED, "warning": "СИНТЕТИЧЕСКИЕ ДАННЫЕ, НЕ ИЗМЕРЕНИЯ",
                   "t35": table35, "t36": table36, "t37": table37}, f,
                  ensure_ascii=False, indent=1)
    print("\nсохранено в synth_data.json")
