add_library('pdf')
import datetime
import random as rd


resolution=5
ow=oh=resolution
w=resolution*60
h=resolution*70

all_col    =[[198,26,26],
            [24,134,168],
            [141,175,155]      
]  

background_col=(245,240,219)

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def setup():
    # size(w,h,PDF, ''.join('dottu'+timestamp+'.pdf'))
    size(w,h)
    background(*background_col)
    noLoop()
    
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

def draw_circle(xcenter,ycenter, r):
    pushMatrix()
    translate(xcenter,ycenter)
    for d in range(360):
        x = sin(radians(d))*r
        y = cos(radians(d))*r
        target=PVector().fromAngle(PI/2-radians(d)).mult(50)
        multy=-1
        if rd.uniform(0,1) > 0.2:
            multy=multy*-1
            print(multy)
        line(x,y,x+target.x*multy,y+target.y*multy)
        stroke(0)
        strokeWeight(1)
        #point(x,y)
    popMatrix()

def get_rgba(value):
    rgba=(red(value), green(value), blue(value), alpha(value))
    return rgba

def retrieve_cgo_val(coordinates):
    cval=get_rgba(pixels[coordinates[0]+coordinates[1]*width])
    
    return cval     

def circ(x,y,r):
    mainr=r
    stroke(0)
    strokeWeight(1)
    pushMatrix()
    translate(x,y)
    for j in range(r):
        for i in range(360):
            # print(r,mainr,(float(r)/float(mainr)))
            gaussian_angle=radians(i)
            xc = sin(gaussian_angle)*r/2
            yc = cos(gaussian_angle)*r/2
            if rd.uniform(0,1) < (float(r)/float(mainr))/2:
                point(xc,yc)
        r-=1
    popMatrix() 
    
def calc_flow_matrix(w,h,rstep,nstep=0.06,max_val=360):
    xoff=random(10)
    arra=list()
    for ix in range(0,w,rstep):
        yoff=0
        cols=list()
        
        for jy in range(0,h,rstep):
            yoff+=nstep
            noise_val=noise(xoff,yoff)
            angle = map(noise_val, 0.0, 1.0, 0, max_val)
            cols.append(angle)
            
        xoff+=nstep
        arra.append(cols)
    
    return arra          

def warping_executor(field,length_line=5):
    warp_dict=dict()
    for x in range(w):
        for y in range(h):
            c=retrieve_cgo_val(coordinates=(x,y))
            # print(c)
            if c != (245.0, 240.0, 219.0, 255.0):
                target=PVector().fromAngle(radians(field[x][y])).mult(length_line)
                warp_dict[(x,y)]=(x+target.x,y+target.y)
                
    return warp_dict   

def draw():

    # pixel_base=pixels
    # print(pixels)
    
    warper=calc_flow_matrix(w=w,h=h,rstep=1,nstep=0.06,max_val=360)
    circ(x=w/2,y=h/2,r=300)
    # x1,y1,x2,y2 = w/2,100,w/2,700
    # line(x1,y1,x2,y2)
    
    loadPixels()
    
    # updatePixels()
    
    d=warping_executor(field=warper,length_line=5)
    
    print(len(d))
    
    for k,v in d.items():
        x1,y1=k[0],k[1]
        # print(k, v)
        x2,y2=int(v[0]),int(v[1])
        line(x1,y1,x2,y2)
        
    updatePixels()

    d=warping_executor(field=warper,length_line=40)
    
    print(len(d))
    
    for k,v in d.items():
        x1,y1=k[0],k[1]
        # print(k, v)
        x2,y2=int(v[0]),int(v[1])
        line(x1,y1,x2,y2)    
    # filename= ''.join('white_blue'+timestamp+'.jpg')
    # save(filename)
    print("End of Program")
    # exit()
    
    
