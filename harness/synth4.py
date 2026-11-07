#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ГЕНЕРАТОР МОДЕЛЬНЫХ ДАННЫХ части 1 эксперимента Э4 (раздел 4.5).

ВНИМАНИЕ. Значения НЕ ЯВЛЯЮТСЯ РЕЗУЛЬТАТАМИ ИЗМЕРЕНИЙ: это событийное моделирование потока
соединений и отказов при иллюстративных параметрах таблицы 4.2, выполненное тем же порядком
обработки, что предписан программе Э4: оценка отношением сумм, доверительный интервал по отказам,
проверка по критерию К4. Подлежит замене протоколом натурного эксперимента.
Запуск из корня репозитория: python3 harness/synth4.py
"""
import math
import pathlib
import random
import runpy
import contextlib
import io

HERE = pathlib.Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    sm = runpy.run_path(str(HERE / "ch4_state_model.py"))
SEED = 20261108
sm["rnd"].seed(SEED)

PLAN = ((0.01, 30), (0.1, 50), (1.0, 30))
D = 0.0005

if __name__ == "__main__":
    print(f"Э4, часть 1 — модельные данные (зерно {SEED}); НЕ ИЗМЕРЕНИЯ")
    for theta, n in PLAN:
        A = L = 0
        ratios = []
        zero = 0
        for _ in range(n):
            a, l = sm["one_failure"](theta, D)
            A += a
            L += l
            ratios.append(l / a)
            zero += (l == 0)
        q_hat = L / A
        m = sum(ratios) / n
        sd = math.sqrt(sum((x - m) ** 2 for x in ratios) / (n - 1))
        from scipy import stats
        t = stats.t.ppf(1 - 0.025 / 2, n - 1)   # уровень 0,975 на точку: групповой 0,95 для двух точек К4
        hw = t * sd / math.sqrt(n)
        qc = sm["q_exact"](theta, D)
        ok = abs(q_hat - qc) <= hw
        role = "контрольная" if theta < 0.05 else "К4"
        print(f"θ = {theta:g} с ({role}), отказов {n}: утрачено {L} из {A} ({L / n:.2f} на отказ, без утрат {zero}); "
              f"q̂ = {q_hat:.3e} ± {hw:.2e} ({hw / q_hat * 100:.0f} %, t = {t:.3f}); расчёт (4.2) {qc:.3e}; "
              f"{'в интервале' if ok else 'ВНЕ интервала'}")
