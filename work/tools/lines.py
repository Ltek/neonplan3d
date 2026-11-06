import numpy as np, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
_c={}
def img(name):
    if name not in _c: _c[name]=np.array(Image.open(f'/shared/user/home/neonplan_work/src/{name}.png'))<140
    return _c[name]
def groups(idx,gap=2):
    g=[]
    for c in idx:
        if g and c-g[-1][-1]<=gap: g[-1].append(c)
        else: g.append([c])
    return [(round(float(np.mean(x)),1),len(x)) for x in g]
def hlines(name,x0,x1,y0,y1,frac=0.9):
    a=img(name)[y0:y1,x0:x1]; p=a.sum(1)
    return groups([y0+i for i,v in enumerate(p) if v>=frac*(x1-x0)])
def vlines(name,x0,x1,y0,y1,frac=0.9):
    a=img(name)[y0:y1,x0:x1]; p=a.sum(0)
    return groups([x0+i for i,v in enumerate(p) if v>=frac*(y1-y0)])
if __name__=='__main__':
    f=sys.argv[1]; n=sys.argv[2]; a=list(map(int,sys.argv[3:7])); fr=float(sys.argv[7]) if len(sys.argv)>7 else 0.9
    print((hlines if f=='h' else vlines)(n,*a,frac=fr))
