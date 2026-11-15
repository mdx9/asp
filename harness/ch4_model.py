#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Расчёты главы 4: доля утраченных соединений, частота синхронизации, служебная нагрузка.

Все параметры — ИЛЛЮСТРАТИВНЫЕ (раздел 4.2, таблица 4.2), результатами измерений не являются.
Формулы: (4.2) доля утраченных q(θ); (4.3) оценка сверху (малое окно); (4.4) замкнутый вид для профиля;
(4.5) задержка с повторами; (4.6) коэффициент простоя; (4.8) долговременная доля оборванных;
(4.9)–(4.10) нагрузка на канал и процессор; (4.11) θ*; (4.12)–(4.13) реализуемость.
Запуск из корня репозитория: python3 harness/ch4_model.py
"""
import math

Y = 365 * 86400
LAM = 1 / Y                 # 1/с, интенсивность отказов узла (Tн = 1 год, как в главе 3)
LAM_C = 100.0               # 1/с, установление соединений на экземпляр
P_LONG, T_LONG = 0.2, 600.0 # доля и длительность длительных соединений (таблица 2.3)
T_SHORT = 1.0               # с, средняя длительность коротких соединений (показательный закон)
T_C = (1 - P_LONG) * T_SHORT + P_LONG * T_LONG
D = 0.5e-3                  # с, задержка доставки изменений резервному экземпляру
T_U = 1.0                   # с, время повторного установления оборванного соединения (как c_ν гл. 3)
T_O, T_R = 25e-3, 1.6e-3    # с, время обнаружения и перенаправления (таблица 3.8, внутриплощ.)
E_REC = 32                  # байт, запись об изменении (формат метода, раздел 4.3)
H_MSG = 62                  # байт, заголовки сообщения: Ethernet 18 + IPv4 20 + UDP 8 + собственный 16
M_PAY = 1456                # байт, полезная нагрузка сообщения: 1500 − 28 − 16
C_MSG, C_REC = 5e-6, 0.2e-6 # с, затраты процессора на сообщение и на запись
U_MAX = 0.01                # допустимая доля одного ядра
THETA_MIN = 1e-3            # с, наименьший реализуемый период таймера


def I(a):
    """∫_0^a S(x) dx для смеси показательных коротких и детерминированных длительных соединений."""
    return (1 - P_LONG) * T_SHORT * (1 - math.exp(-a / T_SHORT)) + P_LONG * min(a, T_LONG)


def q(theta, d=D, m=4000):
    """(4.1): q = E_A[∫_0^{A+d} S] / T_с, A ~ U(0; θ)."""
    return sum(I((i + 0.5) / m * theta + d) for i in range(m)) / m / T_C


def q_lin(theta, d=D):
    """(4.2): приближение малого окна."""
    return (theta / 2 + d) / T_C


def msg_rate(theta):
    """Средний темп пакетов изменений: полные пакеты плюс один неполный за период, 1/с."""
    return 1 / theta + 2 * LAM_C * E_REC / M_PAY


def B(theta):
    """(4.9): нагрузка на канал, бит/с."""
    return 8 * (2 * LAM_C * E_REC + H_MSG * msg_rate(theta))


def U(theta):
    """(4.10): доля ядра процессора."""
    return C_MSG * msg_rate(theta) + 2 * LAM_C * C_REC


def theta_star(q_max):
    """(4.9): наибольший θ, при котором q(θ) ≤ q_доп (бисекция по точной формуле)."""
    if q(0.0) > q_max:
        return None
    lo, hi = 0.0, 1000.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if q(mid) <= q_max else (lo, mid)
    return lo


def theta_U():
    """(4.12): наименьший период, при котором U(θ) ≤ U_доп."""
    den = U_MAX - 2 * LAM_C * (C_REC + C_MSG * E_REC / M_PAY)
    return C_MSG / den if den > 0 else float("inf")


def lam_c_max():
    """(4.13): предельный темп установления соединений на экземпляр."""
    return U_MAX / (2 * (C_REC + C_MSG * E_REC / M_PAY))


def k_star(c_nu, p, tau=10e-3, lam=LAM):
    """(3.24)."""
    v = math.log(lam * tau ** 2 / (c_nu * (1 - p) ** 2)) / math.log(p)
    return max(1, math.ceil(v))


if __name__ == "__main__":
    print(f"T_с = {T_C:.1f} с, активных на экземпляр {LAM_C * T_C:.0f}")
    print("\n(4.1) против (4.2):")
    for th in (1e-3, 1e-2, 0.1, 1.0, 10.0, 60.0):
        print(f"  θ = {th:g} с: q = {q(th):.3e}, малое окно {q_lin(th):.3e}, "
              f"расхождение {(q_lin(th) / q(th) - 1) * 100:.1f} %")
    print(f"\nбез переноса q = 1; q(∞) → {q(1e5):.4f}")
    print(f"\nθ_U = {theta_U() * 1e3:.3f} мс (U_доп = {U_MAX:.0%}), θ_min = {THETA_MIN * 1e3:.1f} мс")
    print("\nТаблица 4.3:")
    for qm in (1e-3, 1e-4, 1e-5, 5e-6):
        th = theta_star(qm)
        lb = max(theta_U(), THETA_MIN)
        if th is None or th < lb:
            print(f"  q_доп = {qm:g}: θ* = {th * 1e3 if th else float('nan'):.3f} мс < нижней границы "
                  f"{lb * 1e3:.2f} мс — асинхронная синхронизация недостаточна")
            continue
        print(f"  q_доп = {qm:g}: θ* = {th * 1e3:.2f} мс, q = {q(th):.2e}, сохранено {(1 - q(th)) * 100:.4f} %, "
              f"B = {B(th) / 1e3:.1f} кбит/с, U = {U(th) * 100:.3f} %, η = {LAM * T_C * q(th):.2e}")
    print("\n(4.4): вклады в простой, с/год (внутриплощадочный канал, таблица 3.8):")
    base = LAM * (T_O + T_R) * Y
    for name, qq in (("без переноса", 1.0), ("θ = 10 мс", q(0.01)), ("θ = 1 с", q(1.0))):
        print(f"  {name}: λ(Tо+Tр) = {base:.4f}, λ·q·Tу = {LAM * qq * T_U * Y:.4f}, "
              f"сумма {base + LAM * qq * T_U * Y:.4f}")
    print("\nЦена ложного срабатывания и пороговое число по (3.24):")
    for ch, p in (("внутриплощадочный", 2.09e-4), ("межплощадочный", 3.96e-3)):
        c_no = T_R + T_U
        c_yes = T_R + q(0.01) * T_U
        print(f"  {ch}: c_ν без переноса {c_no:.4f} с → k* = {k_star(c_no, p)}; "
              f"с переносом {c_yes * 1e3:.3f} мс → k* = {k_star(c_yes, p)}")
    print("\nНагрузка и процессор по θ:")
    for th in (1e-3, 1e-2, 0.1, 1.0):
        print(f"  θ = {th:g} с: B = {B(th) / 1e3:.1f} кбит/с, U = {U(th) * 100:.3f} %")


# ---------------------------------------------------------------- дополнения (v54)
def q_closed(theta, d=D):
    """(4.2) в замкнутом виде для смеси при θ + d ≤ T_LONG."""
    tk, p = T_SHORT, P_LONG
    short = (1 - p) * tk * (1 - (tk / theta) * (math.exp(-d / tk) - math.exp(-(theta + d) / tk)))
    return (short + p * (theta / 2 + d)) / T_C


def q_general(theta, surv_int, tc, d=D, m=4000):
    return sum(surv_int((i + 0.5) / m * theta + d) for i in range(m)) / m / tc


def dist_family(tc):
    """Три распределения с одинаковым средним: показательное, логнормальное (σ = 1,5), Парето (α = 1,5)."""
    from math import erf, exp, log, sqrt
    exp_I = lambda a: tc * (1 - math.exp(-a / tc))
    s = 1.5
    mu = log(tc) - s * s / 2
    def ln_S(x):
        return 1.0 if x <= 0 else 0.5 * (1 - erf((log(x) - mu) / (s * sqrt(2))))
    def ln_I(a, n=4000):
        return sum(ln_S((i + 0.5) / n * a) for i in range(n)) * a / n
    al = 1.5
    xm = tc * (al - 1) / al
    def par_I(a):
        if a <= xm:
            return a
        return xm + xm ** al * (a ** (1 - al) - xm ** (1 - al)) / (1 - al)
    return {"показательное": exp_I, "логнормальное σ = 1,5": ln_I, "Парето α = 1,5": par_I}


def d_eff(d, p_s, t_rep):
    """Задержка с учётом повторов при надёжной доставке: d + t_повт·p_s/(1 − p_s)."""
    return d + t_rep * p_s / (1 - p_s)


def lam_sweep():
    """Смена связывающего ограничения с ростом темпа установления соединений."""
    global LAM_C
    keep = LAM_C
    out = []
    for lc in (1e2, 1e3, 1e4, 1.5e4):
        LAM_C = lc
        th4, th5 = theta_star(1e-4), theta_star(1e-5)
        out.append((lc, theta_U(), th4, U(th4), B(th4), th5, theta_U() <= th5))
    LAM_C = keep
    return out


if __name__ == "__main__":
    print("\n--- дополнения v54 ---")
    for th in (1e-3, 1e-2, 0.1, 1.0, 10.0):
        print(f"  замкнутый вид θ = {th:g}: {q_closed(th):.4e} против численного {q(th):.4e}")
    print("\nчувствительность к распределению длительности (T_с одинаково = 120,8 с):")
    fam = dist_family(T_C)
    for th in (0.01, 1.0, 10.0, 60.0):
        row = [f"{name}: {q_general(th, f, T_C, m=400):.3e}" for name, f in fam.items()]
        print(f"  θ = {th:g} с: " + "; ".join(row) + f"; малое окно {q_lin(th):.3e}")
    print("\nзадержка с повторами (t_повт = 10 мс):")
    for ps in (0.0, 1e-3, 1e-2, 0.1):
        de = d_eff(D, ps, 0.01)
        print(f"  p_с = {ps:g}: d_эфф = {de * 1e3:.3f} мс; θ*(1e-4) = {2 * (1e-4 * T_C - de) * 1e3:.2f} мс (малое окно)")
    n_tab = LAM_C * T_C
    print(f"\nобъём таблицы: {n_tab:.0f} записей × {E_REC} Б = {n_tab * E_REC / 1024:.0f} КиБ; полная пересылка "
          f"при 1 Гбит/с {n_tab * E_REC * 8 / 1e9 * 1e3:.2f} мс, при 100 Мбит/с {n_tab * E_REC * 8 / 1e8 * 1e3:.1f} мс")
    print("\nсмена связывающего ограничения по темпу установления (q_доп = 1e-4):")
    print(f"  предельный темп (4.13): {lam_c_max():.0f} 1/с")
    for lc, thu, th4, u4, b4, th5, ok5 in lam_sweep():
        print(f"  λс = {lc:g}: θ_U = {thu * 1e3:.3f} мс; q_доп=1e-4: θ* = {th4 * 1e3:.2f} мс, U = {u4 * 100:.3f} %, "
              f"B = {b4 / 1e6:.3f} Мбит/с; q_доп=1e-5: θ* = {th5 * 1e3:.2f} мс, реализуемо: {ok5}")
    for tc in (1.0, 10.0, 120.8, 600.0):
        print(f"  T_с = {tc:g} с: q_min ≈ d/T_с = {D / tc:.1e}; θ*(1e-4) ≈ {2 * (1e-4 * tc - D) * 1e3:.2f} мс")
    print(f"\nдвойной отказ: вероятность отказа резерва за время восстановления резервирования Tп = 300 с: "
          f"λ·Tп = {LAM * 300:.2e}")


# ---------------------------------------------------------------- планирование Э4 (v54)
def loss_moments(theta, d=D, m=4000):
    """Число утраченных при отказе: смесь Пуассона, m(A) = λс·∫_0^{A+d} S; возвращает E m и Var m."""
    vals = [LAM_C * I((i + 0.5) / m * theta + d) for i in range(m)]
    em = sum(vals) / m
    vm = sum((v - em) ** 2 for v in vals) / m
    return em, vm


def reps_needed(theta, delta, z=1.96):
    """(4.15): число отказов для относительной полуширины δ доверительного интервала."""
    em, vm = loss_moments(theta)
    return z * z * (em + vm) / (delta * em) ** 2


if __name__ == "__main__":
    print("\n--- планирование Э4 ---")
    for th in (0.01, 0.1, 1.0):
        em, vm = loss_moments(th)
        hw30 = 1.96 * math.sqrt((em + vm) / 30) / em
        print(f"  θ = {th:g}: E m = {em:.3f}, Var m = {vm:.3f}, полуширина при 30 отказах {hw30 * 100:.0f} %, "
              f"n(δ=0,2) = {reps_needed(th, 0.2):.0f}, n(δ=0,3) = {reps_needed(th, 0.3):.0f}")


# ---------------------------------------------------------------- дополнения (v54, часть 3)
def p_no_loss(theta, d=D, m=4000):
    """(4.8а): вероятность отказа без единой утраты: среднее e^{−m(A)} по фазе."""
    return sum(math.exp(-LAM_C * I((i + 0.5) / m * theta + d)) for i in range(m)) / m


if __name__ == "__main__":
    print("\n--- вероятность отказа без утрат (4.8а) ---")
    for th in (1e-3, 0.01, 0.1, 1.0):
        print(f"  θ = {th:g}: P(N = 0) = {p_no_loss(th):.3f}, E N = {LAM_C * T_C * q(th):.2f}")
    print("\n--- θ* в зависимости от d ---")
    for dd in (0.1e-3, 0.5e-3, 1e-3, 2e-3, 5e-3):
        row = []
        for qd in (1e-3, 1e-4, 1e-5):
            if q(0.0, d=dd) > qd:
                row.append("—")
                continue
            lo, hi = 0.0, 1000.0
            for _ in range(70):
                mid = (lo + hi) / 2
                lo, hi = (mid, hi) if q(mid, d=dd, m=600) <= qd else (lo, mid)
            row.append(f"{lo * 1e3:.2f}" if lo >= THETA_MIN else f"{lo * 1e3:.2f}<θmin")
        print(f"  d = {dd * 1e3:g} мс: " + " | ".join(row))
