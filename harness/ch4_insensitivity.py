#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка (4.5б): доля потерянной нагрузки не зависит от вида распределений длительностей пребывания.

Моделирование процесса восстановления с чередованием по графу рисунка 4.1 при завышенных
интенсивностях (иначе события редки); длительности пребывания — показательные, детерминированные
и логнормальные с коэффициентом вариации 2 при одинаковых средних. Параметры иллюстративны.
"""
import math
import random

LAM, NU = 1e-2, 5e-3          # 1/с, завышенные интенсивности отказов и ложных признаний
T_O, T_R, T_U, QQ = 2.0, 0.5, 10.0, 0.3


def sampler(kind, mean, rnd):
    if kind == "показательное":
        return rnd.expovariate(1 / mean)
    if kind == "детерминированное":
        return mean
    cv = 2.0
    s2 = math.log(1 + cv * cv)
    return rnd.lognormvariate(math.log(mean) - s2 / 2, math.sqrt(s2))


def run(kind, cycles=400000, seed=7):
    rnd = random.Random(seed)
    t_total = lost = 0.0
    for _ in range(cycles):
        up = rnd.expovariate(LAM + NU)
        t_total += up
        if rnd.random() < LAM / (LAM + NU):
            a, b = sampler(kind, T_O, rnd), sampler(kind, T_R, rnd)
            lost += a + b
            t_total += a + b
        else:
            b = sampler(kind, T_R, rnd)
            lost += b
            t_total += b
        c = sampler(kind, T_U, rnd)
        lost += QQ * c
        t_total += c
    return lost / t_total


if __name__ == "__main__":
    num = LAM * (T_O + T_R) + NU * T_R + (LAM + NU) * QQ * T_U
    den = 1 + LAM * (T_O + T_R) + NU * T_R + (LAM + NU) * T_U
    k_exact = num / den
    print(f"(4.5б): {k_exact:.5f}; первое приближение (4.6): {num:.5f}")
    for kind in ("показательное", "детерминированное", "логнормальное CV = 2"):
        k = run(kind)
        print(f"  {kind}: {k:.5f} (отклонение {abs(k - k_exact) / k_exact * 100:.2f} %)")
