"""Рисунки 2–5 статьи 1. Данные — по формулам (2)–(7) и таблицам 3, 4 (сценарии
mc_insensitivity.py, sim_session.py). Цветное исполнение; серии различаются и типом линии или маркера."""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, LogLocator

plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 10, "axes.linewidth": 0.6,
                     "lines.linewidth": 1.2, "xtick.direction": "in", "ytick.direction": "in",
                     "legend.frameon": False, "savefig.dpi": 300,
                     "mathtext.fontset": "custom", "mathtext.rm": "Liberation Serif",
                     "mathtext.it": "Liberation Serif:italic"})
YEAR = 365.25 * 86400
# категориальная палитра (проверена validate_palette.js); тип линии сохранён как второй признак
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
W, H = 15 / 2.54, 8 / 2.54

def ru(x, _=None):
    if x == 0: return "0"
    if abs(x) >= 1e4 or abs(x) < 1e-3:
        e = int(math.floor(math.log10(abs(x)))); m = x / 10 ** e
        return f"$10^{{{e}}}$" if abs(m - 1) < 1e-9 else f"{m:g}·$10^{{{e}}}$".replace(".", ",")
    return f"{x:g}".replace(".", ",")
F = FuncFormatter(ru)

def logaxes(ax):
    for a in (ax.xaxis, ax.yaxis):
        a.set_major_formatter(F); a.set_minor_formatter(FuncFormatter(lambda *_: ""))
    ax.grid(True, which="major", lw=0.3, color="0.8")

# Рисунок 2 — избыточный простой λTо + νcν от периода при разных k
lam, c, p, tmin = 1 / YEAR, 1.0, 1e-3, 0.010
fig, ax = plt.subplots(figsize=(W, H))
taus = [10 ** (-3 + 3 * i / 400) for i in range(401)]
styles = ["-", "--", "-.", ":", (0, (5, 1, 1, 1, 1, 1))]
for (k, ls), col in zip(zip(range(2, 7), styles), C):
    y = [(lam * (k - .5) * t + (1 - p) * p ** k / t * c) * YEAR for t in taus]
    ax.plot([t * 1e3 for t in taus], y, color=col, ls=ls, lw=1.5, label=f"k = {k}")
ax.axvspan(1, tmin * 1e3, color="0.92", lw=0)
ax.axvline(tmin * 1e3, color="k", lw=0.6)
ax.text(tmin * 1e3 * 0.93, 3e3, "τ < τ$_\\mathrm{min}$\nнедопустимо", ha="right", va="top", fontsize=9)
ax.set_xscale("log"); ax.set_yscale("log"); logaxes(ax)
ax.set_xlim(1, 1000); ax.set_ylim(1e-3, 1e4)
ax.set_xlabel("Период τ, мс"); ax.set_ylabel("λT$_\\mathrm{о}$ + νc$_\\mathrm{ν}$, с/год")
ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, 1.13), fontsize=9)
fig.tight_layout(); fig.savefig("figures/fig2_tau_k.png"); plt.close(fig)

# Рисунок 3 — выигрыш против штатного обнаружения (ν = 0), формула (3)
To0 = 50.0
fig, ax = plt.subplots(figsize=(W, H))
To = [10 ** (-3 + 5 * i / 400) for i in range(401)]
for (Tr, ls), col in zip(((1.0, "-"), (0.05, "--")), C):
    ax.plot(To, [(To0 + Tr) / (t + Tr) for t in To], color=col, ls=ls, lw=1.5,
            label=f"T$_\\mathrm{{р}}$ = {ru(Tr)} с")
    gmax = 1 + To0 / Tr
    ax.axhline(gmax, color="0.5", lw=0.6, ls=":")
    ax.text(1.2e-3, gmax * 1.12, f"G$_{{\\mathrm{{max}}}}$ = {ru(gmax)}", fontsize=9)
for (Tr, To_, g, mk), col in zip(((1.0, (.025, .035, .055), (50, 49, 48), "o"), (0.05, (.025, .035, .055), (666, 588, 476), "s")), C):
    ax.plot(To_, g, mk, color=col, mfc="white", mew=1.5, ms=6)
ax.set_xscale("log"); ax.set_yscale("log"); logaxes(ax)
ax.set_xlim(1e-3, 100); ax.set_ylim(0.8, 3000)
ax.set_xlabel("Время обнаружения T$_\\mathrm{о}$, с"); ax.set_ylabel("Выигрыш G")
ax.legend(loc="center right", fontsize=9)
fig.tight_layout(); fig.savefig("figures/fig3_gain.png"); plt.close(fig)

# Рисунок 4 — отклонение расчёта от моделирования, таблица 3
shape = [0.7, 1.0, 1.5]; K = 0.01852; ci = [0.00008, 0.00006, 0.00004]
d1 = [0.02, 0.04, 0.05]; d2 = [1.90, 1.93, 1.94]
fig, ax = plt.subplots(figsize=(W, H * 0.9))
x = range(3)
ax.bar([i - 0.18 for i in x], d1, 0.32, color=C[0], label="выражение (1)")
ax.bar([i + 0.18 for i in x], d2, 0.32, color="white", edgecolor=C[1], hatch="///", lw=1.0,
       label="приближение первого порядка")
for i in x:
    h = 100 * ci[i] / K
    ax.plot([i - .42, i + .42], [h, h], color="k", lw=0.8, ls="--")
ax.plot([], [], color="k", lw=0.8, ls="--", label="полуширина ДИ 95 %")
for i in x:
    ax.text(i - 0.18, d1[i] + 0.05, ru(d1[i]), ha="center", fontsize=9)
    ax.text(i + 0.18, d2[i] + 0.05, ru(d2[i]), ha="center", fontsize=9)
ax.set_xticks(list(x), [f"форма {ru(s)}" for s in shape])
ax.yaxis.set_major_formatter(F); ax.set_ylabel("Отклонение от моделирования, %")
ax.set_ylim(0, 2.4); ax.grid(True, axis="y", lw=0.3, color="0.8"); ax.set_axisbelow(True)
ax.legend(fontsize=9, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.14))
fig.tight_layout(); fig.savefig("figures/fig4_insensitivity.png"); plt.close(fig)

# Рисунок 5 — интенсивность ложных признаний, таблица 4 и формулы (5), (7)
k, b = 5, 2
P = [0.10, 0.15, 0.20, 0.25, 0.30]
ind = [9.98e-6, 6.42e-5, 2.554e-4, 7.363e-4, 1.696e-3]; ind_ci = [0.95e-6, 0.20e-5, 0.055e-4, 0.071e-4, 0.010e-3]
bur = [3.120e-3, 4.678e-3, 6.227e-3, 7.832e-3, 9.370e-3]
pp = [0.08 + 0.24 * i / 200 for i in range(201)]
fig, ax = plt.subplots(figsize=(W, H))
ax.plot(pp, [(1 - q) * q ** k for q in pp], "-", color=C[0], lw=1.5, label="расчёт по (5), независимые")
ax.plot(pp, [q / b * (1 - 1 / b) ** (k - 1) for q in pp], "--", color=C[1], lw=1.5, label="расчёт по (7), пачечные, b = 2")
ax.errorbar(P, ind, yerr=ind_ci, fmt="o", color=C[0], mfc="white", mew=1.5, ms=6, capsize=2, lw=0.8,
            label="моделирование, независимые")
ax.plot(P, bur, "s", color=C[1], ms=5.5, label="моделирование, пачечные")
ax.set_yscale("log"); logaxes(ax); ax.xaxis.set_major_formatter(F)
ax.set_xlim(0.08, 0.32); ax.set_ylim(3e-6, 3e-2)
ax.set_xlabel("Вероятность непринятия p"); ax.set_ylabel("ν на одно сообщение")
ax.legend(fontsize=9, loc="lower right")
fig.tight_layout(); fig.savefig("figures/fig5_bursty.png"); plt.close(fig)
print("ok")
