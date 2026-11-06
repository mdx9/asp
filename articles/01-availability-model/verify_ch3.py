# -*- coding: utf-8 -*-
"""Пересчёт всех чисел разделов 3.2–3.3 (таблицы 3.2, 3.3, граничный оптимум, пороги p, (3.23)).
Иллюстративные параметры главы 3: Tн = 1 год, Tр = 1 с, Tп = 300 с, p = 0,01, τ_min = 10 мс."""
import math
from scipy.optimize import brentq
Y=365*86400.0
lam=1/Y; Tr=1.0; Tp=300.0
C=lambda k,p:(1-p)*(k-0.5)*p**k
print("== таблица 3.2")
for To in (40,10,5,2,1,0.5,0.1):
    s=(To+Tp); r1=To+1; r05=To+0.05
    print(f"{To:5} single {s:7.1f}  Tr1 {r1:6.2f} доля {1/(To+1)*100:5.1f}%  Tr0.05 {r05:6.2f} доля {0.05/(To+0.05)*100:5.2f}%")
print("Gmax", 1+40/1, 1+40/0.05, " бюджет одиночн. To<", 315.36-300)
print("E при 40,1:",40/41,1/41," при 0.1:",0.1/1.1,1/1.1)
print("== таблица 3.3 (p=0.01)")
p=0.01
for k in range(2,7):
    c=C(k,p); To=math.sqrt(c*Tr/lam); tau=To/(k-0.5); nu=c/To
    down=(lam*(To+Tr)+nu*Tr)*Y
    print(f"k={k} To*={To:.4f} c  tau={tau*1e3:.1f} мс nu={nu*Y:.4f}/год простой={down:.3f} с/год реализуемо={tau>=0.01}")
def down(k,tau,p,Tr=1.0):
    To=(k-0.5)*tau; nu=(1-p)*p**k/tau
    return (lam*(To+Tr)+nu*Tr)*Y, To, nu*Y
print("граница k=6 tau=10мс:", down(6,0.01,0.01))
print("== совместный оптимум при tau_min=10мс по p")
def best(p,taumin=0.01):
    res=[]
    for k in range(1,15):
        c=C(k,p); To=math.sqrt(c*Tr/lam); tau=max(To/(k-0.5),taumin)
        d,To2,nu=down(k,tau,p); res.append((d,k,tau,To2,nu))
    return min(res)
for p in (1e-4,1e-3,1e-2,3e-2):
    d,k,tau,To,nu=best(p); print(f"p={p:g}: k={k} tau={tau*1e3:.2f}мс To={To*1e3:.1f}мс простой={d:.4f} nu={nu:.4g}/год")
print("== порог p, с которого внутр. оптимум реализуем (tau*>=10мс)")
for k in (4,5,6):
    f=lambda p: math.sqrt(C(k,p)*Tr/lam)/(k-0.5)-0.01
    print(k, brentq(f,1e-6,0.4))
print("== округление k=5:", [round(down(5,t,0.01)[0],3) for t in (0.020,0.026336,0.050)])
c5=C(5,0.01); To5=math.sqrt(c5*Tr/lam); print("tau* k5", To5/4.5)
print("== (3.23): To>=", c5/(1/Y), c5/(0.1/Y), " To*",To5, "отн", c5/(0.1/Y)/To5)
print("граница k6: 1 ЛС в", 1/down(6,0.01,0.01)[2],"лет")
print("== уточнение 3.1: To=2с k=5,k=3")
for k in (5,3):
    To=2; nu=C(k,0.01)/To; print(k,(lam*(To+Tr)+nu*Tr)*Y)
print("== чувствительность к p: x3 ->",C(5,0.03)/C(5,0.01)," x10->",C(5,0.1)/C(5,0.01))
