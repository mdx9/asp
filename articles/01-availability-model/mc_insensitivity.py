# -*- coding: utf-8 -*-
"""Имитационная проверка нечувствительности (3.5) к виду распределений.
ДАННЫЕ ПОРОЖДЕНЫ МОДЕЛЬЮ, НЕ ИЗМЕРЕНЫ. Отказы — процесс восстановления Вейбулла по наработке,
ложные признания — пуассоновский поток по наработке, Tо ~ U(30;45) с, Tп — логнормальное, среднее 300 с, CV 0,5.
Наработка сжата до Tн = 2·10^4 с, чтобы Kп ≈ 0,018 и погрешность приближения (3.7) была различима."""
import numpy as np, math
def sim(rng, Tn, shape, To_lo, To_hi, Tp_mean, Tp_cv, nu, n_fail):
    scale=Tn/math.gamma(1+1/shape)
    s2=math.log(1+Tp_cv**2); mu=math.log(Tp_mean)-s2/2
    # отказы — процесс восстановления по накопленной наработке (узел заменяется при отказе);
    # ложные признания — пуассоновский поток по наработке, часы отказа не сбрасывают
    gaps=scale*rng.weibull(shape,n_fail); U=gaps.sum()
    nfa=rng.poisson(nu*U)
    down=(rng.uniform(To_lo,To_hi,n_fail)+rng.lognormal(mu,math.sqrt(s2),n_fail)).sum()
    down+=rng.lognormal(mu,math.sqrt(s2),nfa).sum()
    return down/(U+down)
rng=np.random.default_rng(20261106)
Tn=2e4; To=(30,45); Tp=300; nu=1/2e5; lam=1/Tn; ToM=37.5
f37=lam*(ToM+Tp)+nu*Tp; f35=1-1/(1+f37)
print(f"расчёт: (3.5)={f35:.5f} (3.7)={f37:.5f}")
for shape in (1.0,0.7,1.5):
    r=np.array([sim(rng,Tn,shape,*To,Tp,0.5,nu,20000) for _ in range(30)])
    m=r.mean(); h=2.045*r.std(ddof=1)/math.sqrt(30)
    print(f"Вейбулл k={shape}: Kп={m:.5f}±{h:.5f}  откл (3.5) {100*(f35/m-1):+.2f}%  (3.7) {100*(f37/m-1):+.2f}%")
