import numpy as np, json
def fit_h(src,dst):
    A=[]
    for (X,Z),(u,v) in zip(src,dst):
        A.append([X,Z,1,0,0,0,-u*X,-u*Z,-u]); A.append([0,0,0,X,Z,1,-v*X,-v*Z,-v])
    _,_,Vt=np.linalg.svd(np.array(A,float)); H=Vt[-1].reshape(3,3); return H/H[2,2]
def apply(H,X,Z):
    p=H@np.array([X,Z,1.0]); return p[0]/p[2],p[1]/p[2]
def inv(H,u,v):
    return apply(np.linalg.inv(H),u,v)
def solve(xlines,zlines,iters=8,H0=None):
    """xlines: list of (Xft, px_u, px_v_measured_row); zlines: (Zft, px_v, px_u_measured_col).
    Unknown other coord found iteratively."""
    H=H0
    for _ in range(iters):
        src=[];dst=[]
        for X,u,v in xlines:
            Z=inv(H,u,v)[1] if H is not None else 0
            src.append((X,Z));dst.append((u,v))
        for Z,v,u in zlines:
            X=inv(H,u,v)[0] if H is not None else 0
            src.append((X,Z));dst.append((u,v))
        H=fit_h(src,dst)
    res=[]
    for (X,Z),(u,v) in zip(src,dst):
        uu,vv=apply(H,X,Z); res.append(round(float(np.hypot(uu-u,vv-v)),1))
    return H,res
