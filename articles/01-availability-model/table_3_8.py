# -*- coding: utf-8 -*-
"""Таблица 3.8 при цене ложного признания c_ν как параметре (решение Р2).
Совместный оптимум по (τ, k) при τ ≥ τ_min: для каждого k τ = max(τ*, τ_min), τ* из (3.21).
Входные p, τ_min, T_р — МОДЕЛЬНЫЕ значения раздела 3.5 (synth.py), не измерения."""
import math
Y=365*86400; lam=1/Y; Tr=1.6e-3; taumin=0.010
chan={"внутриплощадочный":1.95e-4,"межплощадочный":4.80e-3}
C=lambda k,p:(1-p)*(k-0.5)*p**k
def at(p,k,tau,c):
    To=(k-0.5)*tau; nu=(1-p)*p**k/tau
    return dict(k=k,tau=tau,To=To,nuY=nu*Y,down=(lam*(To+Tr)+nu*c)*Y,ratio=nu*c/(lam*To))
def best(p,c):
    rows=[]
    for k in range(1,12):
        ts=math.sqrt(C(k,p)*c/lam)/(k-0.5)
        rows.append(at(p,k,max(ts,taumin),c)|{"interior":ts>=taumin,"tau_star":ts})
    return min(rows,key=lambda r:r["down"])
for c in (1.6e-3, 31.6e-3, 1.0):
    for name,p in chan.items():
        r=best(p,c)
        print(f"c_ν={c*1e3:7.1f} мс {name:18s} k={r['k']} τ={r['tau']*1e3:.1f} мс ({'внутр.' if r['interior'] else 'граница'}, τ*={r['tau_star']*1e3:.2f}) "
              f"To={r['To']*1e3:.1f} мс ν={r['nuY']:.4g}/год простой={r['down']:.4f} с/год νc/λTo={r['ratio']:.2g}")
p=4.8e-3
for c in (1.6e-3,1.0):
    r=at(p,3,taumin,c); print(f"межпл. k=3, τ=10 мс, c_ν={c*1e3} мс: ν={r['nuY']:.1f}/год простой={r['down']:.3f}")
