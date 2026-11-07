# -*- coding: utf-8 -*-
"""Статья 1, алгоритм 1 и таблица 2: выбор (τ, k) при τ ≥ τ_min с округлением к набору RFC 7419.
Параметры — по опубликованным данным (см. verification.md), λ = 1/год иллюстративно."""
import math
Y=365*86400.0; lam=1/Y
SET=[0.0033,0.010,0.020,0.050,0.100,1.0]           # общеупотребительные периоды [RFC 7419]
C=lambda k,p:(1-p)*(k-0.5)*p**k
def Kp(k,tau,p,Tr,c):
    To=(k-0.5)*tau; nu=(1-p)*p**k/tau
    return (lam*(To+Tr)+nu*c)*Y, To, nu*Y
def algorithm1(p,Tr,c,taumin=0.010,nu_max=None,kmax=12):
    best=None
    for k in range(1,kmax+1):
        tstar=math.sqrt(C(k,p)*c/lam)/(k-0.5)
        cand=[t for t in SET if t>=taumin]
        # округление: ближайшее значение набора не меньше τ_min, предпочтительно вниз от τ*
        lower=[t for t in cand if t<=tstar]; tau=max(lower) if lower else min(cand)
        d,To,nuY=Kp(k,tau,p,Tr,c)
        if nu_max is not None and nuY>nu_max: continue
        r=dict(k=k,tau=tau,To=To,nuY=nuY,down=d,bound=("τ_min" if tstar<taumin else "компромисс"),tstar=tstar)
        if best is None or d<best["down"]: best=r
    return best
if __name__=="__main__":
    print("штатно, резервирование: Tо=50 с:", [(Tr,round((lam*(50+Tr))*Y,2)) for Tr in (1.0,0.05)])
    for Tr in (1.0,0.05):
        for p in (1e-4,1e-3,1e-2):
            for c in (Tr,1.0) if Tr<1 else (Tr,):
                r=algorithm1(p,Tr,c)
                print(f"Tр={Tr} c_ν={c} p={p:g}: k={r['k']} τ={r['tau']*1e3:g} мс Tо={r['To']*1e3:.1f} мс ν={r['nuY']:.3g}/год "
                      f"простой={r['down']:.4f} с/год ({r['bound']}, τ*={r['tstar']*1e3:.3g} мс) выигрыш={(lam*(50+Tr))*Y/r['down']:.0f}")
