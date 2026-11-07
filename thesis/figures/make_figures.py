"""Рисунки 1.2, 2.2–2.6, 3.2, 3.3, 3.5, 3.6, 3.7 (рисунок 1.1 — 1_1_nfv_arch.dot, graphviz).

Запуск из корня репозитория: python3 thesis/figures/make_figures.py
Палитра — категориальная, проверена validate_palette.js (синий, оранжевый, бирюзовый,
жёлтый, розовый); серии различаются также типом линии, маркером или штриховкой.
Данные: 1.2, 3.5 — параметры платформы (таблица 1.3, (1.3)); 2.3 — (3.17) при k = 5,
τ = 26 мс (таблица 2.4); 2.5 — harness/e1_example.py (ДАННЫЕ ПОРОЖДЕНЫ); 2.6 — таблица 2.9;
3.2 — (3.7), (3.11) при Tн = 1 год, Tп = 300 с (таблица 3.2); 3.6, 3.7 — harness/synth.py (ДАННЫЕ ПОРОЖДЕНЫ).
"""
import contextlib
import io
import math
import pathlib
import runpy

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

ROOT = pathlib.Path(__file__).resolve().parents[2]   # корень репозитория
OUT = pathlib.Path(__file__).resolve().parent
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": INK2,
                     "axes.linewidth": 0.6, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.labelcolor": INK, "legend.frameon": False, "savefig.dpi": 200,
                     "savefig.bbox": "tight"})


def ru(x, _=None):
    if x == 0:
        return "0"
    if abs(x) >= 1e4 or abs(x) < 1e-2:
        e = int(math.floor(math.log10(abs(x) * (1 + 1e-12))))
        m = x / 10 ** e
        return f"$10^{{{e}}}$" if abs(m - 1) < 1e-9 else f"{m:g}·$10^{{{e}}}$".replace(".", ",")
    return f"{x:g}".replace(".", ",")


F = FuncFormatter(ru)


def clean(ax, grid="x"):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if grid:
        ax.grid(True, axis=grid, color=GRID, lw=0.6)
        ax.set_axisbelow(True)


# ---------------------------------------------------------------- 1.2
def fig_1_2():
    fig, ax = plt.subplots(figsize=(9, 3.2))
    To, wait = 47.5, 300.0
    ax.barh(1, To, left=0, height=0.45, color=C[0])
    ax.barh(1, wait, left=To, height=0.45, color=C[1])
    ax.barh(1, 25, left=To + wait, height=0.45, color="white", edgecolor=C[2], hatch="///", lw=1)
    ax.text(To / 2, 0.70, "$T_о$ ≈ 47,5 с\n(40–55 с)", ha="center", va="top", color=INK, fontsize=9)
    ax.text(To + wait / 2, 1, "ожидание перед вытеснением 300 с", ha="center", va="center", color="white")
    ax.text(To + wait + 12.5, 1.30, "выбор узла,\nзапуск, готовность\n(условно)", ha="center", va="bottom",
            fontsize=8, color=INK2)
    ax.annotate("", xy=(To + wait + 25, 0.55), xytext=(To, 0.55),
                arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.8))
    ax.text(To + (wait + 25) / 2, 0.42, "$T_п$", ha="center", va="top", color=INK)
    # события
    for x, lab, ha in ((0, "отказ узла ", "right"), (To, " узел признан\n недостижимым", "left"),
                       (To + wait, "вытеснение\nэкземпляров", "center")):
        ax.axvline(x, color=INK2, lw=0.6, ls=":", ymin=0.12)
        ax.text(x, 1.95, lab, ha=ha, va="bottom", fontsize=8.5, color=INK)
    ax.text(380, 1, "≈ 347,5 с\n+ запуск", ha="left", va="center", fontsize=11, fontweight="bold", color=INK)
    # публикации сведений об узле (период 10 с) до отказа
    for t in range(-30, 1, 10):
        ax.plot(t - 4, 0.15, marker="|", ms=9, color=C[0])
    ax.text(-36, 0.15, "обновления сведений\nоб узле, период 10 с", ha="right", va="center", fontsize=8, color=INK2)
    ax.set_xlim(-110, 445)
    ax.set_ylim(0, 2.6)
    ax.set_yticks([])
    ax.set_xticks([0, 50, 100, 150, 200, 250, 300, 350])
    ax.set_xlabel("Время с момента отказа, с")
    clean(ax)
    ax.spines["left"].set_visible(False)
    fig.savefig(OUT / "1_2_timeline.png")
    plt.close(fig)


# ---------------------------------------------------------------- 2.2
def fig_2_2():
    fig, axes = plt.subplots(2, 1, figsize=(9, 3.8), sharex=True)
    f0, f1, step = 3.0, 9.0, 0.5
    for ax, title in zip(axes, ("разомкнутая схема", "замкнутая схема")):
        ax.axvspan(f0, f1, color="#f6dccf", lw=0)
        ax.set_yticks([])
        ax.set_ylim(0, 1)
        ax.text(-0.3, 0.5, title, ha="right", va="center", fontsize=10)
        clean(ax, grid=None)
        ax.spines["left"].set_visible(False)
    a = axes[0]
    ok = fail = 0
    t = 0.0
    while t <= 12:
        bad = f0 <= t < f1
        a.plot(t, 0.5, "x" if bad else "o", color=C[1] if bad else C[0], ms=7 if bad else 5, mew=1.5)
        fail += bad
        t += step
    a.annotate("", xy=(f1, 0.85), xytext=(f0, 0.85), arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.8))
    a.text((f0 + f1) / 2, 0.92, f"перерыв покрыт запросами: {fail} без ответа", ha="center", va="bottom", fontsize=8.5)
    b = axes[1]
    t, tmo = 0.0, 4.0
    while t <= 12:
        if f0 <= t < f1:
            b.plot(t, 0.5, "x", color=C[1], ms=7, mew=1.5)
            b.plot([t, t + tmo], [0.5, 0.5], color=C[1], lw=1, ls="--")
            t += tmo
        else:
            b.plot(t, 0.5, "o", color=C[0], ms=5)
            t += step
    b.text((f0 + f1) / 2, 0.92, "источник ждёт ответа и новых запросов не порождает: 2 без ответа",
           ha="center", va="bottom", fontsize=8.5)
    axes[1].set_xlabel("Время, с")
    axes[0].plot([], [], "o", color=C[0], label="ответ получен")
    axes[0].plot([], [], "x", color=C[1], mew=1.5, label="ответ не получен")
    axes[0].fill_between([], [], color="#f6dccf", label="отказ экземпляра")
    axes[0].legend(ncol=3, loc="lower center", bbox_to_anchor=(0.5, 1.25), fontsize=9)
    fig.savefig(OUT / "2_2_load_scheme.png")
    plt.close(fig)


# ---------------------------------------------------------------- 2.3
def fig_2_3():
    k, tau = 5, 0.026
    n = lambda p: (1 - p) * p ** k / tau * 3600
    P = [0.005 + i * 0.345 / 300 for i in range(301)]
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.axvspan(0.10, 0.30, color="#dbe8f8", lw=0, label="назначенный диапазон 0,10–0,30")
    ax.plot(P, [n(p) for p in P], color=C[0], lw=2, label="ожидаемое число за 1 ч, (3.17)")
    pts = [0.10, 0.15, 0.20, 0.25, 0.30]
    ax.plot(pts, [n(p) for p in pts], "o", color=C[0], mfc="white", mew=1.5, ms=6)
    ax.axhline(30, color=C[1], lw=1, ls="--")
    ax.plot(0.193, 30, "D", color=C[1], ms=6)
    ax.annotate("30 наблюдений за 1 ч\nпри p = 0,193", xy=(0.193, 30), xytext=(0.035, 60), fontsize=8.5,
                color=INK, arrowprops=dict(arrowstyle="->", color=INK2, lw=0.8))
    ax.set_yscale("log")
    ax.set_ylim(1e-6, 1e3)
    ax.set_xlim(0, 0.35)
    ax.yaxis.set_major_formatter(F)
    ax.xaxis.set_major_formatter(F)
    ax.set_xlabel("Вероятность потери контрольного сообщения p")
    ax.set_ylabel("Ложных срабатываний за 1 ч")
    clean(ax, grid="y")
    ax.legend(loc="lower right", fontsize=9)
    fig.savefig(OUT / "2_3_false_positive_rate.png")
    plt.close(fig)


# ---------------------------------------------------------------- 2.4
def fig_2_4():
    fig = plt.figure(figsize=(10, 4.6))
    ax = fig.add_axes([0.03, 0.30, 0.94, 0.66])
    ev = [(0, "отказ", 0), (2.2, "изменение\nсостояния", 1), (3.6, "назначение\nузла", 1),
          (5.0, "запуск\nпроцесса", 2), (6.6, "экземпляр\nготов", 2), (7.4, "обслуживание\nвосстановлено", 3)]
    src = [("маяк", C[0]), ("журнал контроллера", C[1]), ("журнал узла размещения", C[2]), ("измеритель", C[3])]
    ax.axhline(0, color=INK2, lw=0.8)
    for x, lab, s in ev:
        ax.plot(x, 0, "o", ms=10, color=src[s][1], mec="white", mew=1.5, zorder=3)
        ax.text(x, -0.35, lab, ha="center", va="top", fontsize=8.5)

    def br(x0, x1, y, lab, col):
        ax.plot([x0, x0, x1, x1], [y - 0.12, y, y, y - 0.12], color=col, lw=1.6)
        ax.text((x0 + x1) / 2, y + 0.06, lab, ha="center", va="bottom", fontsize=9, color=INK)
    br(0, 2.2, 0.55, "$T_о$", C[0])
    br(2.2, 3.6, 0.55, "$T_{п1}$", C[4])
    br(3.6, 5.0, 0.55, "$T_{п2}$", C[4])
    br(5.0, 6.6, 0.55, "$T_{п3}$", C[4])
    br(2.2, 6.6, 1.15, "$T_п$ — по меткам разных узлов, входит рассогласование часов", C[4])
    br(0, 7.4, 1.85, "$T_в$ — по часам измерителя, рассогласование часов не входит", C[3])
    ax.set_xlim(-0.6, 8.2)
    ax.set_ylim(-1.2, 2.4)
    ax.axis("off")
    for i, (lab, col) in enumerate(src):
        ax.plot([], [], "o", color=col, ms=8, label=lab)
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.10), fontsize=9, title="источник метки времени",
              title_fontsize=9)
    # врезка: Э1.2, иной масштаб
    b = fig.add_axes([0.03, 0.02, 0.94, 0.20])
    b.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.0,rounding_size=0.03",
                               transform=b.transAxes, fc="#f4f3f0", ec="none"))
    b.axhline(0.45, xmin=0.08, xmax=0.92, color=INK2, lw=0.8)
    for x, lab, col in ((0.2, "экземпляр признан\nнеготовым", C[1]), (0.8, "трафик на него\nне направляется", C[3])):
        b.plot(x, 0.45, "o", ms=9, color=col, mec="white", mew=1.5, transform=b.transAxes)
        b.text(x, 0.12, lab, ha="center", va="center", fontsize=8.5, transform=b.transAxes)
    b.annotate("", xy=(0.8, 0.75), xytext=(0.2, 0.75), xycoords="axes fraction",
               arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.8))
    b.text(0.5, 0.80, "$T_р = T_в − T_о$ по (2.4а) — сценарий Э1.2, масштаб миллисекунд", ha="center",
           va="bottom", fontsize=9, transform=b.transAxes)
    b.axis("off")
    fig.savefig(OUT / "2_4_measurement.png")
    plt.close(fig)


# ---------------------------------------------------------------- 2.5
def fig_2_5():
    import numpy as np
    from scipy import stats
    with contextlib.redirect_stdout(io.StringIO()):
        g = runpy.run_path(str(ROOT / "harness" / "e1_example.py"))
    data = [("$T_о$, с", g["To_c"]), ("$T_{п1}$, с", g["Tp1"]), ("$T_{п2}$, с", g["Tp2"]),
            ("$T_{п3}$, с", g["Tp3"]), ("$T_р$, с", g["Tr_c"]), ("$T_в$, с", g["Tv"])]
    fig, axes = plt.subplots(2, 3, figsize=(10, 4.6))
    rng = np.random.default_rng(1)
    for ax, (name, x) in zip(axes.flat, data):
        n = len(x)
        normal = stats.shapiro(x).pvalue > 0.05
        col = C[0] if normal else C[1]
        y = rng.uniform(-0.25, 0.25, n)
        ax.plot(x, y, "o", ms=4.5, color=col, alpha=0.85, mec="white", mew=0.5)
        if normal:
            m = x.mean()
            e = stats.t.ppf(0.975, n - 1) * x.std(ddof=1) / math.sqrt(n)
            lo, hi = m - e, m + e
        else:
            m = float(np.median(x))
            xs = np.sort(x)
            lo, hi = xs[9], xs[20]   # порядковые статистики 10 и 21 при n = 30, P = 0,957
        ax.axvspan(lo, hi, color=col, alpha=0.15, lw=0)
        ax.axvline(m, color=INK, lw=1.4)
        ax.set_title(name, fontsize=10, loc="left")
        ax.set_yticks([])
        ax.set_ylim(-0.5, 0.5)
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",")))
        clean(ax)
        ax.spines["left"].set_visible(False)
    axes[0, 0].plot([], [], "o", color=C[0], label="нормальность подтверждена — среднее и ДИ по Стьюденту")
    axes[0, 0].plot([], [], "o", color=C[1], label="нормальность отвергнута — медиана и ДИ по порядковым статистикам")
    fig.legend(*axes[0, 0].get_legend_handles_labels(), loc="upper center", ncol=1, fontsize=9,
               bbox_to_anchor=(0.5, 1.07))
    fig.tight_layout()
    fig.savefig(OUT / "2_5_distributions.png")
    plt.close(fig)


# ---------------------------------------------------------------- 2.6
def fig_2_6():
    rows = [  # (подпись, значение, группа, вид отказа)
        ("отказ узла, по умолчанию [13]", 300.852, 0, "узел"),
        ("отказ узла, отзывчивая конфигурация [13]", 3.974, 0, "узел"),
        ("специализированное средство [13]", 3.346, 0, "узел"),
        ("отказ узла, по умолчанию [13]", 38.582, 1, "узел"),
        ("отказ узла, отзывчивая конфигурация [13]", 0.872, 1, "узел"),
        ("отказ экземпляра [13]", 0.730, 1, "экземпляр"),
        ("отказ процесса [13]", 0.579, 1, "экземпляр"),
        ("отказ узла, медиана [4]", 5.87, 2, "узел"),
    ]
    groups = ["без резервирования", "с резервированием", "перенос состояния"]
    fig, ax = plt.subplots(figsize=(9, 4.4))
    y, ticks, labels, pos = 0, [], [], {}
    for gi, gname in enumerate(groups):
        ax.text(0.32, y - 0.35, gname, ha="left", va="center", fontsize=9, color=C[gi], fontweight="bold")
        y -= 0.5
        for lab, v, g, kind in rows:
            if g != gi:
                continue
            y -= 1
            mk = "o" if kind == "узел" else "s"
            ax.plot(v, y, mk, ms=8, color=C[gi], mec="white", mew=1)
            ax.text((7.5 if g == 2 else v) * 1.18, y, ru(v) + " с", va="center", fontsize=8.5)
            ticks.append(y)
            labels.append(lab)
            pos[(lab, g)] = (v, y)
        y -= 0.8
    ax.errorbar([5.87], [pos[("отказ узла, медиана [4]", 2)][1]], xerr=[[5.87 - 4.5], [7.5 - 5.87]],
                fmt="none", ecolor=C[2], capsize=3, lw=1)
    (v0, y0), (v1, y1) = pos[("отказ узла, по умолчанию [13]", 0)], pos[("отказ узла, по умолчанию [13]", 1)]
    ax.annotate("", xy=(v1, y1 + 0.15), xytext=(v0, y0 - 0.15),
                arrowprops=dict(arrowstyle="->", color=INK2, lw=0.8, connectionstyle="arc3,rad=-0.25"))
    ax.text(110, (y0 + y1) / 2, "тот же вид отказа:\nв 7,8 раза", fontsize=8.5, color=INK2, ha="center")
    ax.set_yticks(ticks, labels, fontsize=8.5)
    ax.set_xscale("log")
    ax.set_xlim(0.3, 1200)
    ax.xaxis.set_major_formatter(F)
    ax.set_xlabel("Перерыв обслуживания, с (логарифмическая шкала)")
    ax.plot([], [], "o", color=INK2, label="отказ узла")
    ax.plot([], [], "s", color=INK2, label="отказ экземпляра или процесса")
    ax.legend(loc="lower right", fontsize=9)
    clean(ax)
    fig.savefig(OUT / "2_6_published.png")
    plt.close(fig)


# ---------------------------------------------------------------- 3.2
def fig_3_2():
    Tp, To0 = 300.0, 50.0
    To = [10 ** (-3 + 5 * i / 400) for i in range(401)]
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.plot(To, [t + Tp for t in To], color=C[0], lw=2, label="одиночный экземпляр, $T_п$ = 300 с")
    ax.plot(To, [t + 1.0 for t in To], color=C[1], lw=2, ls="--", label="резервирование, $T_р$ = 1 с")
    ax.plot(To, [t + 0.05 for t in To], color=C[2], lw=2, ls="-.", label="резервирование, $T_р$ = 0,05 с")
    for v, col in ((Tp, C[0]), (1.0, C[1]), (0.05, C[2])):
        ax.axhline(v, color=col, lw=0.6, ls=":")
    ax.axvline(To0, color=INK2, lw=0.8)
    ax.text(To0 * 0.9, 2e3, "штатное\n$T_о^0$ = 50 с", ha="right", va="top", fontsize=8.5, color=INK2)
    for x, y in ((50, 350), (50, 51), (50, 50.05)):
        ax.plot(x, y, "o", color=INK, ms=4)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-3, 100)
    ax.set_ylim(0.03, 3e3)
    ax.xaxis.set_major_formatter(F)
    ax.yaxis.set_major_formatter(F)
    ax.set_xlabel("Время обнаружения $T_о$, с")
    ax.set_ylabel("Простой обслуживания, с/год")
    ax.legend(loc="center left", bbox_to_anchor=(0.01, 0.55), fontsize=9)
    clean(ax, grid="both")
    fig.savefig(OUT / "3_2_saturation.png")
    plt.close(fig)


# ---------------------------------------------------------------- 3.5
def fig_3_5():
    fig, ax = plt.subplots(figsize=(10, 4.2))
    x0 = 1e-2
    ax.barh(2, 50 - x0, left=x0, height=0.5, color=C[0])
    ax.barh(2, 300, left=50, height=0.5, color=C[1])
    ax.text(0.7, 2, "обнаружение 50 с", ha="center", va="center", color="white", fontweight="bold")
    ax.text(120, 2.33, "ожидание переразмещения 300 с", ha="center", va="bottom", color=INK2, fontweight="bold")
    ax.text(1200, 2, "350 с", va="center", fontsize=13, fontweight="bold")
    ax.barh(1, 0.119 - x0, left=x0, height=0.5, color=C[0])
    ax.barh(1, 1.0, left=0.119, height=0.5, color=C[1])
    ax.text(0.04, 1.33, "обнаружение 0,119 с", ha="center", va="bottom", color=INK2, fontweight="bold")
    ax.text(0.35, 0.67, "перенаправление 1 с (иллюстр.)", ha="center", va="top", color=INK2, fontweight="bold")
    ax.text(1200, 1, "1,12 с", va="center", fontsize=13, fontweight="bold")
    ax.barh(0.1, 300, left=1.119, height=0.32, color=C[2])
    ax.text(18, -0.18, "переразмещение — вне критического пути", ha="center", va="top", color=INK2,
            fontweight="bold")
    ax.set_yticks([2, 1], ["штатный механизм,\nодиночная\nконфигурация", "предлагаемый\nметод,\nрезервирование"])
    ax.set_xscale("log")
    ax.set_xlim(x0, 9000)
    ax.set_ylim(-0.6, 2.7)
    ax.xaxis.set_major_formatter(F)
    ax.set_xlabel("Время с момента отказа, с (логарифмическая шкала)")
    clean(ax)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.savefig(OUT / "3_5_timeline.png")
    plt.close(fig)


# ---------------------------------------------------------------- 3.3
def fig_3_3():
    YEAR = 365 * 86400   # как в тексте главы 3
    lam, p, c, Tr, tmin = 1 / YEAR, 0.01, 1.0, 1.0, 0.010
    ramp = {2: "#b7d3f6", 3: "#86b6ef", 4: "#5598e7", 5: "#2a78d6", 6: "#184f95"}
    To = [10 ** (-2.5 + 5 * i / 500) for i in range(501)]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axhline(315.4, color="#6b6a66", lw=1.6, ls=(0, (6, 3)))
    ax.text(4e-3, 360, "бюджет 99,999 % — 315,4 с/год", color="#6b6a66", fontsize=10)
    ax.axhline(1.0, color="#6b6a66", lw=0.8, ls=":")
    ax.text(230, 1.08, "предел λ$T_р$ = 1 с/год", color="#6b6a66", fontsize=9, ha="right")
    for k in range(2, 7):
        Ck = (1 - p) * (k - 0.5) * p ** k
        y = [(lam * (t + Tr) + Ck / t * c) * YEAR for t in To]
        ax.plot(To, y, color=ramp[k], lw=2.4)
        t_opt = math.sqrt(Ck * c / lam)
        y_opt = (lam * (t_opt + Tr) + Ck / t_opt * c) * YEAR
        ok = t_opt / (k - 0.5) >= tmin
        ax.plot(t_opt, y_opt, "o" if ok else "x", color=ramp[k], ms=9 if ok else 9,
                mec="white" if ok else ramp[k], mew=1.5 if ok else 2.5, zorder=4)
    lab = {2: (90, 230), 3: (11, 36), 4: (1.2, 6.5), 5: (0.2, 2.2), 6: (3.4e-3, 2.8)}
    for k, (x, y) in lab.items():
        ax.text(x, y, f"$k$ = {k}", color=ramp[k], fontsize=12, fontweight="bold")
    t6 = 5.5 * tmin
    C6 = (1 - p) * 5.5 * p ** 6
    y6 = (lam * (t6 + Tr) + C6 / t6 * c) * YEAR
    ax.plot(t6, y6, "s", color=C[1], ms=10, zorder=5)
    ax.annotate("$k$ = 6, τ = τ$_{min}$ = 10 мс:\n$T_о$ = 55 мс, простой 1,06 с/год", xy=(t6, y6 * 1.08),
                xytext=(7e-3, 18), color=C[1], fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=C[1], lw=1.2, connectionstyle="arc3,rad=0.15"))
    ax.plot([], [], "o", color="#6b6a66", label="внутренний оптимум (3.22) реализуем")
    ax.plot([], [], "x", color="#6b6a66", mew=2.5, label="внутренний оптимум требует τ < τ$_{min}$")
    ax.plot([], [], "s", color=C[1], label="совместный оптимум: граница τ = τ$_{min}$")
    ax.legend(loc="upper right", fontsize=10)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(10 ** -2.5, 250); ax.set_ylim(0.8, 4000)
    ax.xaxis.set_major_formatter(F); ax.yaxis.set_major_formatter(F)
    ax.set_xlabel("Время обнаружения отказа $T_о$, с"); ax.set_ylabel("Простой обслуживания, с/год")
    clean(ax, grid="both")
    fig.savefig(OUT / "3_3_optimum.png")
    plt.close(fig)


# ---------------------------------------------------------------- 3.6, 3.7
def _synth():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(str(ROOT / "harness" / "synth.py"))


def fig_3_6():
    g = _synth()
    tau, k = g["TAU_MS"], g["K"]
    x = g["table36"][0]["raw"]          # остановка процесса, n = 30
    m, e = sum(x) / len(x), g["ci95"](x)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(x, bins=[104 + 1.5 * i for i in range(20)], color=C[0], ec="white", lw=1.2)
    ax.axvspan(m - e, m + e, color=C[1], alpha=0.18, lw=0)
    for v in ((k - 1) * tau, k * tau):
        ax.axvline(v, color=INK, ls=(0, (5, 4)), lw=1.6)
    ax.axvline((k - 0.5) * tau, color=C[1], lw=2.2)
    ax.axvline(m, color=C[1], ls=(0, (5, 4)), lw=2.2)
    top = ax.get_ylim()[1] * 1.6
    ax.set_ylim(0, top)
    f1 = lambda v: f"{v:.0f}"
    ax.text((k - 1) * tau + 1, top * 0.9, f"$(k-1)τ$ = {f1((k - 1) * tau)} мс", color=INK)
    ax.text(k * tau - 1, top * 0.9, f"$kτ$ = {f1(k * tau)} мс", color=INK, ha="right")
    ax.text((k - 0.5) * tau - 0.4, top * 0.74, "расчёт $(k-\\frac{1}{2})τ$ = " + f"{(k - 0.5) * tau:.1f}".replace(".", ",") + " мс",
            color=C[1], ha="right", fontweight="bold")
    ax.text(m + e + 0.4, top * 0.55, f"среднее\n{m:.1f} ± {e:.1f} мс".replace(".", ","), color=C[1], fontweight="bold")
    ax.set_xlabel("Время обнаружения отказа, мс")
    ax.set_ylabel("Число повторностей")
    clean(ax, grid="y")
    fig.savefig(OUT / "3_6_detect_hist.png")
    plt.close(fig)


def fig_3_7():
    g = _synth()
    from scipy import stats
    t37, k, tau = g["table37"], g["K"], g["TAU_MS"] / 1000
    slope, mx, my = g["SLOPE"], g["_mx"], g["_my"]
    fig, ax = plt.subplots(figsize=(9, 5.4))
    ps = [0.008 * (0.4 / 0.008) ** (i / 200) for i in range(201)]
    ax.plot(ps, [(1 - p) * p ** k / tau for p in ps], color=C[1], ls=(0, (6, 3)), lw=2.4,
            label=f"расчёт по (3.18) при $k$ = {k}")
    ax.plot(ps, [math.exp(my + slope * (math.log(p) - mx)) for p in ps], color=C[0], lw=2,
            label=f"аппроксимация, наклон {slope:.2f}".replace(".", ","))
    for r in t37:
        n, T = r["n_fp"], r["hours"] * 3600
        lo = stats.chi2.ppf(0.025, 2 * n) / 2 / T if n else 0
        hi = stats.chi2.ppf(0.975, 2 * n + 2) / 2 / T
        ax.errorbar(r["p"], r["nu_meas_s"], yerr=[[r["nu_meas_s"] - lo], [hi - r["nu_meas_s"]]],
                    fmt="o", ms=8, color=C[0], mec="white", mew=1.2, capsize=5, lw=1.6)
    ax.plot([], [], "o", color=C[0], label="модельные «измерения» с пуассоновскими границами")
    nu_ex = math.exp(my + slope * (math.log(0.01) - mx))
    nu_c = (1 - 0.01) * 0.01 ** k / tau
    ax.plot([0.01], [nu_ex], "s", color=C[0], ms=8, mec="white")
    ax.plot([0.01], [nu_c], "D", color=C[1], ms=7, mec="white")
    ax.annotate(f"$p$ = 0,01: экстраполяция {g['NU_EXTRAP']:.3f}".replace(".", ",") +
                f", расчёт {g['NU_OPER']:.3f} события в год".replace(".", ","),
                xy=(0.0105, nu_ex), xytext=(0.016, 3e-8), color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="-", color=INK2, lw=1))
    ax.axvline(0.01, color=INK2, lw=0.8, ls=":")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.008, 0.4)
    ax.set_ylim(1e-9, 0.3)
    ax.xaxis.set_major_formatter(F)
    ax.yaxis.set_major_formatter(F)
    ax.set_xlabel("Вероятность непринятия контрольного сообщения $p$")
    ax.set_ylabel("Интенсивность ложных признаний отказа, с$^{-1}$")
    ax.legend(loc="upper left", fontsize=9)
    clean(ax, grid="both")
    fig.savefig(OUT / "3_7_false_positive.png")
    plt.close(fig)


if __name__ == "__main__":
    for f in (fig_1_2, fig_2_2, fig_2_3, fig_2_4, fig_2_5, fig_2_6, fig_3_2, fig_3_3, fig_3_5,
              fig_3_6, fig_3_7):
        f()
        print("готово:", f.__name__)
