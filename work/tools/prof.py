import sys,numpy as np
sys.path.insert(0,'/shared/user/home/neonplan_work/tools')
from calib import *; from lines import img
import json
CAL=json.load(open('/shared/user/home/neonplan_work/calib.json'))
def Hs(n): return np.array(CAL[n])
def profile(n,axis,fixed,a,b,step=0.02,half=0.15):
    """axis='x': walk X from a..b at Z=fixed; returns list of (pos, darkness) ; averaged over +-half ft perpendicular"""
    H=Hs(n); im=img(n); out=[]
    for p in np.arange(a,b,step):
        vals=[]
        for q in np.linspace(fixed-half,fixed+half,7):
            X,Z=(p,q) if axis=='x' else (q,p)
            u,v=apply(H,X,Z); vals.append(im[int(round(v)),int(round(u))])
        out.append((round(float(p),3),float(np.mean(vals))))
    return out
def edges(n,axis,fixed,a,b,half=0.15):
    pr=profile(n,axis,fixed,a,b,half=half)
    s=''.join('#' if d>0.5 else '.' for _,d in pr)
    # list dark runs in feet and inches
    runs=[];i=0
    while i<len(pr):
        if pr[i][1]>0.5:
            j=i
            while j+1<len(pr) and pr[j+1][1]>0.5: j+=1
            runs.append((pr[i][0],pr[j][0])); i=j+1
        else: i+=1
    return runs
if __name__=='__main__':
    n,ax,f,a,b=sys.argv[1],sys.argv[2],*map(float,sys.argv[3:6])
    h=float(sys.argv[6]) if len(sys.argv)>6 else 0.15
    for r in edges(n,ax,f,a,b,h): print(f"{r[0]:8.3f} .. {r[1]:8.3f}  ({(r[1]-r[0])*12:4.1f} in)")
