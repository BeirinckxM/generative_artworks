add_library('pdf')
import datetime
import random as rd

resolution=12
ow=oh=resolution*2
w=resolution*70
h=resolution*80

color_list=[[198,26,26],
            [24,134,168],
            [141,175,155],
            [238,223,96],
            [238,119,0],
            [171,169,153],
            [244,92,86],
            [203,226,201],
            [253,235,131],
            [255,255,255],
            
]


timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def setup():
    size(w,h,PDF, ''.join('kkkk'+timestamp+'.pdf'))
    # size(w,h)
    background(245,240,219)
    noLoop()
    #blendMode(DIFFERENCE)

def draw():
    
    def ezel_inv(w,ow,h,oh):
        noStroke()
        fill(245)
        rect(0,0,w,oh)
        rect(0,0,ow,h)
        rect(0,h-oh,w,oh)
        rect(w-ow,0,ow,h)
    
    def ezel(top,sides,c=255):
        stroke(0)
        strokeWeight(3)
        line(sides,top,w-sides,top)
        line(w-sides,top,w-sides,h-top)
        line(w-sides,h-top,sides,h-top)
        line(sides,h-top,sides,top)
    
    print("Starting")
    
    def calc_flow_matrix(w,h,rstep,nstep=0.06):
        xoff=0
        arra=list()
        for ix in range(0,w,rstep):
            yoff=0
            cols=list()
            
            for jy in range(0,h,rstep):
                yoff+=nstep
                noise_val=noise(xoff,yoff)
                angle = map(noise_val, 0.0, 1.0, 100, 255)
                cols.append(angle)
                
            xoff+=nstep
            arra.append(cols)
        
        return arra
    
    def random_angles(w,h,rstep=1):
        arra=list()
        for ix in range(0,w,rstep):
            cols=list()
            for jy in range(0,h,rstep):
                angle=random(360)
                cols.append(angle)
            arra.append(cols)
        return arra
        
    def make_paper(alphamatrix,angles,granelength=4,granedens=.5,bl=1,ez=1):
        mw, mh = len(alphamatrix), len(alphamatrix[0])
        for ix in range(0,mw,ez):
            for iy in range(0,mh,ez):
                if rd.uniform(0,1) > granedens:
                    angle=angles[ix][iy]
                    x2=sin(angle)*granelength+ix
                    y2=cos(angle)*granelength+iy
                    strokeWeight(0)
                    if bl:
                        r,g,b=random(200,230), random(200,230), random(200,230)
                        a=alphamatrix[ix][iy]
                        stroke(color(r,g,b,a))
                        # line(ix,iy,x2,y2)
                    else:
                        r=g=b=0
                        a=alphamatrix[ix][iy]
                        a=a/255*3
                        stroke(color(r,g,b,a))
                        # if rd.uniform(0,1) > .5:
                            # line(ix,iy,x2,y2)
                        # else:
                    noFill()
                    arc(ix,iy,int(random(4)),int(random(4)),radians(angle-random(180)),radians(angle))
                    
    matalp=calc_flow_matrix(w=w,h=h,rstep=1)
    matang=random_angles(w=w,h=h,rstep=1)

    make_paper(alphamatrix=matalp,angles=matang,granelength=(random(1,3)),granedens=.4,ez=4)
    make_paper(alphamatrix=matalp,angles=matang,granelength=(random(1,3)),granedens=.5,bl=0,ez=4)
                
    def make_linegrid(w,h,gridw,gridh,alpha_,linew):
        strokeWeight(1)
        for x in range(0,w,gridw):
            for y in range(0,h):
                r,g,b=93,120,177
                for i in range(linew):
                    a=random(alpha_)
                    stroke(color(r,g,b,a))
                    point(x+i,y)
                    
        for y in range(0,h,gridh):
            for x in range(0,w):
                for i in range(linew):
                    a=random(alpha_)
                    stroke(color(r,g,b,a))
                    point(x,y+i)
                
    make_linegrid(w=w,h=h,gridw=int(resolution),gridh=int(resolution),alpha_=100,linew=2)          
    
    ezel(top=oh,sides=ow)
    
    def calc_flow_matrix(w,h,rstep,nstep=0.06):
        xoff=0
        arra=list()
        for ix in range(0,w,rstep):
            yoff=0
            cols=list()
            
            for jy in range(0,h,rstep):
                yoff+=nstep
                noise_val=noise(xoff,yoff)
                angle = map(noise_val, 0.0, 1.0, 0, 40)
                cols.append(angle)
                
            xoff+=nstep
            arra.append(cols)
        
        return arra
    matalp=calc_flow_matrix(w=w,h=h,rstep=1,nstep=0.005)
    
    def _circle(x,y,rx,ry,rotator):
        pushMatrix()
        translate(x,y)
        rotate(rotator)
        for a in range(360):
            xc=cos(a)*rx
            yc=sin(a)*ry
            stroke(matalp[int(x)][int(y)])
            point(xc,yc)
        popMatrix()
        
    def path_maker(x,y,leng,stop_condition=1,dim=(w/3,h/4)):
        type=rd.choice((-1,1))
        nscale=2000
        npower=60
        zoff=random(1)
        r=1
        for i in range(leng):
            angle=noise(x/nscale, y/nscale, zoff) * npower
            x+=cos(angle)*r*type
            y+=sin(angle)*r*type
            # stroke(0)
            _circle(x=x,y=y,rx=noise(x/nscale)*dim[0],ry=noise(y/nscale)*dim[1],rotator=noise(zoff))
            zoff+=0.01
            
    for blob in range(10):       
        path_maker(x=random(w),y=random(h),leng=int(random(400,1000)),stop_condition=1,dim=(w/8,h/8))
    
    #path_maker(x=w/4,y=h/2,leng=1000,stop_condition=1)

    # ezel_inv(w=w,ow=ow,h=h,oh=oh)
    
    # ezel(top=oh,sides=ow)
    
    # filename= ''.join('boxes'+timestamp+'.jpg')
    # save(filename)
    print("End of Program")
    exit()
    
