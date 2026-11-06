import numpy as np, json, sys, cv2
sys.path.insert(0,'/shared/user/home/neonplan_work/tools')
from lines import img
def segments(name,box,minlen=70):
    x0,y0,x1,y1=box
    a=(img(name)[y0:y1,x0:x1]).astype(np.uint8)*255
    out={}
    for k,ker in (('h',(minlen,1)),('v',(1,minlen))):
        m=cv2.morphologyEx(a,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_RECT,ker))
        n,lab,st,cen=cv2.connectedComponentsWithStats(m,8)
        L=[]
        for i in range(1,n):
            x,y,w,h,ar=st[i]
            if k=='h': L.append((float(round(y0+y+h/2-0.5,1)),int(x0+x),int(x0+x+w),int(h)))
            else: L.append((float(round(x0+x+w/2-0.5,1)),int(y0+y),int(y0+y+h),int(w)))
        out[k]=sorted(L)
    return out
def walls(L,gmin=14,gmax=48,minov=50):
    res=[]
    for i,(c,s,e,t) in enumerate(L):
        for (c2,s2,e2,t2) in L[i+1:]:
            if c2-c>gmax: break
            if c2-c<gmin: continue
            ov=min(e,e2)-max(s,s2)
            if ov>=minov: res.append((round((c+c2)/2,1),max(s,s2),min(e,e2),round(c2-c,1)))
    return res
if __name__=='__main__':
    name=sys.argv[1]; box=list(map(int,sys.argv[2:6]))
    S=segments(name,box)
    json.dump(S,open(f'/shared/user/home/neonplan_work/segs_{name}.json','w'))
    print(len(S['h']),len(S['v']))
