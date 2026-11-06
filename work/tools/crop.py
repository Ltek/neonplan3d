import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
# usage: crop.py SRC x0 y0 x1 y1 out [maxw]  (full-res pixel coords)
src,x0,y0,x1,y1,out=sys.argv[1:7]; mw=int(sys.argv[7]) if len(sys.argv)>7 else 1600
im=Image.open(f'/shared/user/home/neonplan_work/src/{src}.png')
c=im.crop((int(x0),int(y0),int(x1),int(y1)))
s=min(1,mw/c.size[0]); c=c.resize((int(c.size[0]*s),int(c.size[1]*s)),Image.LANCZOS)
c.save(f'/shared/user/home/neonplan_work/crops/{out}.png'); print(c.size,s)
