# -*- coding: utf-8 -*-
"""Статья 1, раздел 4.3(б): имитация сессии двустороннего контроля пересылки.
ДАННЫЕ ПОРОЖДЕНЫ МОДЕЛЬЮ, НЕ ИЗМЕРЕНЫ. Ложное признание — серия из ≥ k подряд непринятых сообщений,
отсчитываемая с первого непринятого после принятого (правило RFC 5880, k = Detect Mult).
Модели непринятия: независимая (Бернулли, p) и пачечная Гилберта — Эллиотта с той же средней p
и средней длиной пачки b сообщений (в «плохом» состоянии сообщение теряется, в «хорошем» — нет)."""
import numpy as np, math
rng=np.random.default_rng(20261106)
def runs_ge_k(lost,k):
    x=np.concatenate(([0],lost.astype(np.int8),[0])); d=np.diff(x)
    starts=np.flatnonzero(d==1); ends=np.flatnonzero(d==-1)
    return int(np.sum((ends-starts)>=k))
def bern(n,p): return rng.random(n)<p
def gilbert(n,p,b):
    r=1.0/b; q=p*r/(1-p)                     # P(Х→П)=q, P(П→Х)=r, стационарная доля П = p
    # длительности пребывания — геометрические; строим поток чередованием
    out=np.zeros(n,bool); i=0; bad=rng.random()<p
    while i<n:
        L=rng.geometric(r if bad else q)
        if bad: out[i:i+L]=True
        i+=L; bad=not bad
    return out
k=5; N=2_000_000; R=30
print("p  | модель | ν/сообщение: имитация (среднее ± ДИ 95 %) | расчёт (1-p)p^k | отношение")
res=[]
for p in (0.10,0.15,0.20,0.25,0.30):
    th=(1-p)*p**k
    for name,gen in (("незав.",lambda: bern(N,p)),("пачеч. b=2",lambda: gilbert(N,p,2.0))):
        v=np.array([runs_ge_k(gen(),k)/N for _ in range(R)])
        m=v.mean(); h=2.045*v.std(ddof=1)/math.sqrt(R)
        res.append((p,name,m,h,th)); print(f"{p:.2f} | {name:10s} | {m:.4e} ± {h:.1e} | {th:.4e} | {m/th:.3f}")
# наклон log ν по log p для независимой модели
P=np.array([r[0] for r in res if r[1]=="незав."]); M=np.array([r[2] for r in res if r[1]=="незав."])
sl=np.polyfit(np.log(P),np.log(M),1)[0]; th_sl=np.mean([k-p/(1-p) for p in P])
print(f"наклон: имитация {sl:.3f}, расчёт (среднее k − p/(1−p)) {th_sl:.3f}")
