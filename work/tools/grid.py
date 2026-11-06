import sys,json,numpy as np
sys.path.insert(0,'/shared/user/home/neonplan_work/tools')
from calib import *
from PIL import Image,ImageDraw,ImageFont
Image.MAX_IMAGE_PIXELS=None
CAL=json.load(open('/shared/user/home/neonplan_work/calib.json'))
_im={}
def grid(n,X0,Z0,X1,Z1,out,maxw=1600,step=1):
    H=np.array(CAL[n])
    if n not in _im: _im[n]=Image.open(f'/shared/user/home/neonplan_work/src/{n}.png').convert('RGB')
    im=_im[n]
    us=[apply(H,X,Z)[0] for X in (X0,X1) for Z in (Z0,Z1)]; vs=[apply(H,X,Z)[1] for X in (X0,X1) for Z in (Z0,Z1)]
    bx=(int(min(us)),int(min(vs)),int(max(us)),int(max(vs)))
    c=im.crop(bx).copy(); d=ImageDraw.Draw(c,'RGBA')
    f=ImageFont.load_default(size=26)
    for X in np.arange(np.ceil(X0),X1+1e-9,step):
        a=apply(H,X,Z0);b=apply(H,X,Z1); m=(X%5==0)
        d.line([(a[0]-bx[0],a[1]-bx[1]),(b[0]-bx[0],b[1]-bx[1])],fill=(255,0,0,150 if m else 70),width=3 if m else 1)
        d.text((a[0]-bx[0]+3,8),f'{X:g}',fill=(255,0,0,255),font=f)
    for Z in np.arange(np.ceil(Z0),Z1+1e-9,step):
        a=apply(H,X0,Z);b=apply(H,X1,Z); m=(Z%5==0)
        d.line([(a[0]-bx[0],a[1]-bx[1]),(b[0]-bx[0],b[1]-bx[1])],fill=(0,0,255,150 if m else 70),width=3 if m else 1)
        d.text((8,a[1]-bx[1]+2),f'{Z:g}',fill=(0,0,255,255),font=f)
    s=min(1,maxw/c.size[0]); c=c.resize((int(c.size[0]*s),int(c.size[1]*s)),Image.LANCZOS)
    c.save(f'/shared/user/home/neonplan_work/crops/{out}.png')
if __name__=='__main__':
    n=sys.argv[1]; a=list(map(float,sys.argv[2:6])); grid(n,*a,sys.argv[6],int(sys.argv[7]) if len(sys.argv)>7 else 1600)
