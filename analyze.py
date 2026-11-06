#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Обработка протоколов эксперимента Э3 (раздел 3.5).

Вход:
  detector.jsonl  — протокол детектора (события recv/down/up)
  inject.log      — моменты внесения отказов, по одному unix-времени в нс на строку

Выход: время обнаружения по повторностям, среднее, медиана, доверительный
интервал 0,95, границы, число ложных признаний отказа.

Использование:
  python3 analyze.py detector.jsonl inject.log --tau 26 --k 5
"""
import argparse
import json
import math
import statistics as st
import sys

T_CRIT = {  # двусторонние критические значения t при доверительной вероятности 0,95
    5: 2.571, 10: 2.228, 15: 2.145, 20: 2.093, 25: 2.064,
    30: 2.045, 40: 2.021, 50: 2.010, 60: 2.001, 100: 1.984,
}


def t_crit(n):
    if n < 2:
        return float("nan")
    df = n - 1
    keys = sorted(T_CRIT)
    for k in keys:
        if df <= k:
            return T_CRIT[k]
    return 1.960  # нормальное приближение при большом объёме выборки


def load(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("detector_log")
    ap.add_argument("inject_log")
    ap.add_argument("--tau", type=float, required=True, help="период τ, мс")
    ap.add_argument("--k", type=int, required=True, help="пороговое число k")
    ap.add_argument("--window", type=float, default=5000.0,
                    help="окно сопоставления отказа и обнаружения, мс")
    a = ap.parse_args()

    events = load(a.detector_log)
    downs = [e for e in events if e["event"] == "down"]
    ups = [e for e in events if e["event"] == "up"]

    with open(a.inject_log, encoding="utf-8") as f:
        injections = [int(x.strip()) for x in f if x.strip()]

    matched, unmatched_down, missed_inj = [], list(downs), []
    for inj in injections:
        best, best_dt = None, None
        for d in unmatched_down:
            dt = (d["t_wall_ns"] - inj) / 1e6  # мс
            if 0 <= dt <= a.window and (best_dt is None or dt < best_dt):
                best, best_dt = d, dt
        if best is None:
            missed_inj.append(inj)
        else:
            matched.append(best_dt)
            unmatched_down.remove(best)

    print(f"Протокол:            {a.detector_log}")
    print(f"Внесено отказов:     {len(injections)}")
    print(f"Обнаружено:          {len(matched)}")
    print(f"Не обнаружено:       {len(missed_inj)}")
    print(f"Ложных признаний:    {len(unmatched_down)}")
    print(f"Возвратов в работу:  {len(ups)}")
    print()

    lo_model, mid_model, hi_model = (a.k - 1) * a.tau, (a.k - 0.5) * a.tau, a.k * a.tau
    print(f"Расчёт по (3.16):    T_o = (k-1/2)τ = {mid_model:.1f} мс, "
          f"границы [{lo_model:.1f}; {hi_model:.1f}] мс")

    if len(matched) < 2:
        print("\nНедостаточно повторностей для статистической обработки "
              "(требуется не менее 30 согласно разделу 3.5).")
        return 0

    n = len(matched)
    mean, med = st.mean(matched), st.median(matched)
    sd = st.stdev(matched)
    ci = t_crit(n) * sd / math.sqrt(n)
    inside = sum(1 for x in matched if lo_model <= x <= hi_model)

    print(f"\nВремя обнаружения, {n} повторностей:")
    print(f"  среднее:           {mean:.1f} мс")
    print(f"  доверит. интервал: ±{ci:.1f} мс (0,95)")
    print(f"  медиана:           {med:.1f} мс")
    print(f"  СКО:               {sd:.1f} мс")
    print(f"  минимум/максимум:  {min(matched):.1f} / {max(matched):.1f} мс")
    print(f"  в границах модели: {inside} из {n} ({100*inside/n:.0f} %)")

    dev = abs(mean - mid_model) / mid_model * 100
    print(f"\nРасхождение с расчётом: {dev:.1f} %")
    print(f"Критерий К2 (не более 20 %): {'ВЫПОЛНЕН' if dev <= 20 else 'НЕ ВЫПОЛНЕН'}")

    if n < 30:
        print(f"\nВНИМАНИЕ: {n} повторностей — раздел 3.5 требует не менее 30.")

    print("\nСтрока для таблицы 3.6:")
    print(f"| — | предлагаемый метод | {n} | {mean/1000:.4f} | — | — | ±{ci:.1f} мс |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
