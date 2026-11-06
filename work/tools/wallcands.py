import sys,json,numpy as np
sys.path.insert(0,'/shared/user/home/neonplan_work/tools')
from calib import *; from walls import segments
CAL=json.load(open('/shared/user/home/neonplan_work/calib.json'))
def cands(n,box,gmin=0.22,gmax=0.42,minov=1.0,minlen=40):
    H=np.array(CAL[n]); S=segments(n,box,minlen)
    def ft(k,c,s,e):
        if k=='h': a=inv(H,s,c); b=inv(H,e,c); return (a[1]+b[1])/2,a[0],b[0]
        a=inv(H,c,s); b=inv(H,c,e); return (a[0]+b[0])/2,a[1],b[1]
    out={}
    for k in 'hv':
        L=sorted(ft(k,*x[:3]) for x in S[k])
        W=[]
        for i,(c,s,e) in enumerate(L):
            for (c2,s2,e2) in L[i+1:]:
                if c2-c>gmax: break
                if c2-c<gmin: continue
                ov=min(e,e2)-max(s,s2)
                if ov>=minov: W.append((round((c+c2)/2,3),round(max(s,s2),2),round(min(e,e2),2),round((c2-c)*12,1)))
        # merge collinear
        W.sort(key=lambda w:(round(w[0]*20),w[1]))
        M=[]
        for w in W:
            if M and abs(M[-1][0]-w[0])<0.06 and w[1]<=M[-1][2]+0.6:
                m=M[-1]; M[-1]=(m[0],m[1],max(m[2],w[2]),m[3])
            else: M.append(w)
        out[k]=M
    return out
if __name__=='__main__':
    n=sys.argv[1]; box=list(map(int,sys.argv[2:6]))
    o=cands(n,box); json.dump(o,open(f'/shared/user/home/neonplan_work/wc_{n}.json','w'))
    for k in 'hv':
        print('HORIZONTAL (z, x0..x1, gap in)' if k=='h' else 'VERTICAL (x, z0..z1, gap in)')
        for w in sorted(o[k]): print(f"  {w[0]:7.2f}  {w[1]:6.2f}..{w[2]:6.2f}  {w[3]}")
