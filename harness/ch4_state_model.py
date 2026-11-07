#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка модели главы 4 (черновой расчёт к плану, 07.11.2026).

Проверяется:
  1) доля утраченных при отказе соединений при асинхронной периодической синхронизации
     с периодом θ и задержкой d: q(θ) = E_A[∫_0^{A+d} S(x) dx] / T_с, A ~ U(0; θ),
     S — функция выживания длительности соединения (доля активных соединений моложе
     A + d в стационарном потоке); приближение q ≈ (θ/2 + d)/T_с верно лишь при
     θ + d много меньше длительности самых коротких соединений (первая версия плана
     принимала его без оговорки — моделирование это опровергло);
  2) долговременная доля оборванных отказами соединений η = λ·T_с·q(θ);
  3) предельный переход: q = 0 даёт (3.11).
Метод — событийное моделирование потока соединений (пуассоновский поток, смесь
коротких и длительных соединений по профилю таблицы 2.3), отказ в случайной фазе.
ВСЕ ПАРАМЕТРЫ ИЛЛЮСТРАТИВНЫ; результаты измерениями не являются.
"""
import math
import random

SEED = 20261107
rnd = random.Random(SEED)

LAM_C = 100.0          # 1/с, интенсивность установления соединений на экземпляр
P_LONG, T_LONG = 0.2, 600.0   # доля и длительность длительных соединений (табл. 2.3)
T_SHORT = 1.0          # с, средняя длительность коротких (показательное распределение)
T_C = (1 - P_LONG) * T_SHORT + P_LONG * T_LONG


def duration():
    return T_LONG if rnd.random() < P_LONG else rnd.expovariate(1 / T_SHORT)


def one_failure(theta, d, horizon=1500.0):
    """Отказ в момент horizon; возвращает (активных, утрачено)."""
    t, active, lost = 0.0, 0, 0
    t_fail = horizon
    phase = rnd.random() * theta            # фаза отказа внутри периода синхронизации
    last_sync = t_fail - phase              # момент последней отправки изменений
    effective = last_sync - d               # записи, созданные позже, у резерва отсутствуют
    while True:
        t += rnd.expovariate(LAM_C)
        if t >= t_fail:
            break
        if t + duration() > t_fail:          # соединение живо в момент отказа
            active += 1
            if t > effective:
                lost += 1
    return active, lost


def q_exact(theta, d, m=2000):
    """q(θ) по точной формуле: среднее по фазе A ~ U(0; θ) от ∫_0^{A+d} S(x) dx / T_с."""
    def I(a):   # ∫_0^a S(x) dx для смеси: показательные короткие + детерминированные длинные
        return (1 - P_LONG) * T_SHORT * (1 - math.exp(-a / T_SHORT)) + P_LONG * min(a, T_LONG)
    return sum(I((i + 0.5) / m * theta + d) for i in range(m)) / m / T_C


def check(theta, d, n=300):
    """Доверительный интервал — по отказам: утраты при одном отказе зависимы (общая фаза)."""
    A = L = 0
    r = []
    for _ in range(n):
        a, l = one_failure(theta, d)
        A += a
        L += l
        r.append(l / a)
    q_sim = L / A
    m = sum(r) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in r) / (n - 1))
    return q_sim, q_exact(theta, d), (theta / 2 + d) / T_C, A / n, L, 1.96 * sd / math.sqrt(n)


if __name__ == "__main__":
    print(f"T_с = {T_C:.1f} с; активных на экземпляр λ_с·T_с = {LAM_C * T_C:.0f}")
    for theta, d in ((0.01, 0.0005), (1.0, 0.0005), (10.0, 0.0005), (60.0, 0.0005)):
        q_sim, q_ex, q_lin, act, nl, ci = check(theta, d)
        print(f"θ = {theta:>6} с: q моделирование {q_sim:.3e} ± {ci:.1e} ({nl} событий), точная {q_ex:.3e} "
              f"(расх. {abs(q_sim - q_ex) / q_ex * 100:4.1f} %, в ДИ: {abs(q_sim - q_ex) <= ci}), "
              f"линейное прибл. {q_lin:.3e}")
    lam = 1 / (365 * 86400)
    for theta in (0.01, 1.0):
        print(f"η(θ = {theta} с) = λ·T_с·q = {lam * T_C * q_exact(theta, 0.0005):.2e}")
