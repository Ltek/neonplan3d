import sys,json,numpy as np
sys.path.insert(0,'/shared/user/home/neonplan_work/tools')
from calib import *; from lines import img
CAL=json.load(open('/shared/user/home/neonplan_work/calib.json'))
def runs_at(n,orient,pos_guess,along,win=0.6,step=0.01):
    """orient 'v' = vertical wall (scan along X at Z=along). returns dark runs (start,end) in ft"""
    H=np.array(CAL[n]); im=img(n); r=[];cur=None
    for p in np.arange(pos_guess-win,pos_guess+win,step):
        X,Z=(p,along) if orient=='v' else (along,p)
        u,v=apply(H,X,Z); d=im[int(round(v)),int(round(u))]
        if d and cur is None: cur=[p,p]
        elif d: cur[1]=p
        elif cur is not None: r.append(tuple(cur)); cur=None
    if cur: r.append(tuple(cur))
    return r
def snap(n,orient,guess,a,b,gmin=0.2,gmax=0.55,samples=9,win=0.6):
    res=[]
    for along in np.linspace(a,b,samples+2)[1:-1]:
        R=[((s+e)/2) for s,e in runs_at(n,orient,guess,along,win)]
        best=None
        for i in range(len(R)):
            for j in range(i+1,len(R)):
                g=R[j]-R[i]
                if gmin<=g<=gmax:
                    c=(R[i]+R[j])/2
                    if best is None or abs(c-guess)<abs(best[0]-guess): best=(c,g)
        if best: res.append(best)
    if not res: return None
    cs=np.array([c for c,_ in res]); med=np.median(cs); ok=[r for r in res if abs(r[0]-med)<0.05]
    return round(float(np.mean([c for c,_ in ok])),3), round(float(np.mean([g for _,g in ok]))*12,1), len(ok), len(res)
if __name__=='__main__':
    n=sys.argv[1]
    for spec in sys.argv[2:]:
        o,g,a,b=spec.split(':'); print(spec, snap(n,o,float(g),float(a),float(b)))
