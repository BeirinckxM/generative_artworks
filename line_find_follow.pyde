
add_library('pdf')
import datetime
import time
import random as rd
import sys

print("Recursion Limit:", sys.getrecursionlimit())
sys.setrecursionlimit(1000) 
print("Recursion Limit:", sys.getrecursionlimit())
# from collections import Counter

resolution=30
ow=oh=resolution
w=ow+resolution*50-ow
h=oh+resolution*58-oh

print("Canvas Size:", w,h,w*h)

all_col    =[[241, 78, 27],
            [8, 63, 88],
]  

background_col=(239,234,212)

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

square_size=resolution*20

print(square_size*square_size)

def setup():
    # size(w,h,PDF, ''.join('collage'+timestamp+'.pdf'))
    size(w,h)
    background(*background_col)
    noLoop()
 
    # blendMode(REPLACE)
    
    global cg1
    global cg2
    
    cg1=createGraphics(w,h)
    cg2=createGraphics(w,h)
    
def ezel_inv(w,ow,h,oh):
    noStroke()
    fill(color(*background_col))
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
    
def gaussian_boom(pixel_object, x,y,wid,hei,a):
    pixel_object.pushMatrix()
    pixel_object.translate(x,y)
    pixel_object.rotate(radians(a))
    for iy in range(hei):
        nps = abs((hei/2)-iy)
        for ix in range(nps):
            px=rd.gauss(mu=0,sigma=wid/2)
            py=iy
            pixel_object.strokeWeight(1)
            pixel_object.noStroke()
            pixel_object.fill(color(0,0,0,2))
            pixel_object.circle(px,py,20)
    pixel_object.popMatrix()
            
def get_rgba(value):
    rgba=(int(red(value)), int(green(value)), int(blue(value)), int(alpha(value)))
    return rgba  

def retrieve_cgo_val(pixel_object, coordinates):
    cval=get_rgba(pixel_object.pixels[coordinates[0]+coordinates[1]*width])
    return cval

def line_gauss_path(pixel_object,x,y,destination,r,spread,lookback,dest_init=False,form_shape=2):
    destx,desty=destination
    destx=min(destx,w-1)
    desty=min(desty,h-1)
    distance=round(dist(x,y,destx,desty))
    dx,dy=destx-x,desty-y
    destination_angle=round(degrees(atan2(dy,dx)))
    # print(dx,dy,destination_angle,distance,x,y,destx,desty)
    
    if dest_init==False:
        dest_init=(distance,destination_angle)
        
    try:
        distance_covered=100-distance/dest_init[0]*100
    
        on_track = (dest_init[1]-90 <= destination_angle <= dest_init[1]+90)
        # print(distance_covered, on_track)
        if distance_covered < 10 and on_track:
            ratio=.5
            mu=(destination_angle)
            # print(distance,distance_covered,dest_init)
        elif 10<distance_covered<90 and on_track:
            ratio=random(0.05,.90)
            mu=(destination_angle+lookback)/2
        else:
            ratio=0.1
            mu=destination_angle
            # r=distance
            # print("braep" )
    
        if distance<r:
            r=distance
        
        direction_angle=rd.gauss(mu=mu,sigma=spread*ratio)
        target=PVector().fromAngle(radians(direction_angle)).mult(r)
        # print(r, target, direction_angle) 
        lookback=direction_angle
        newx,newy=min(round(x+target.x),w-1),min(round(y+target.y),h-1)
        if (x != destx or y != desty):
            if form_shape==1:
                pixel_object.noStroke()
                pixel_object.vertex(newx,newy)
            elif form_shape==2:
                pixel_object.line(x,y,newx,newy)
            elif form_shape==3:
                pixel_object.point(newx,newy)
            elif form_shape==4:
                pixel_object.noStroke()
                pixel_object.square(newx,newy,10)
            line_gauss_path(pixel_object,newx,newy,destination,r,spread,lookback, dest_init,form_shape=form_shape)
        # else:
        #     print("reached endpoint: ", x, y)
    except ZeroDivisionError:
        print("Did not draw anything")
        pass
        
        
def calc_flow_matrix(w,h,rstep,nstep=0.06,min_val=0, max_val=360):
    xoff=random(10)
    arra=list()
    for ix in range(0,w,rstep):
        yoff=0
        cols=list()
        
        for jy in range(0,h,rstep):
            yoff+=nstep
            noise_val=noise(xoff,yoff)
            angle = map(noise_val, 0.0, 1.0, min_val, max_val)
            cols.append(angle)
            
        xoff+=nstep
        arra.append(cols)
    
    return arra   

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################   
         
def draw():
    
    cg1.beginDraw()

    for boom in range(10):
        x,y=int(random(w)),int(random(h))
        a=int(random(360))
        wid=int(random(resolution*5,resolution*30))
        hei=int(random(resolution*5,resolution*30))
        pixel_object=cg1
        gaussian_boom(pixel_object, x,y,wid,hei,a)
        
    cg1.endDraw()
    cg1.loadPixels()
    
    cg2.beginDraw()
    
    gridsize=resolution*2
    field = calc_flow_matrix(w,h,gridsize,nstep=0.2,min_val=0, max_val=360)
    wix,wiy=int(random(1,10)),int(random(1,10))
    for py in range(0,h,gridsize*wix):
        # list_connect=[]
        for px in range(0,w,gridsize*wiy):
            cg2.stroke(color(0,0,0))
            c=retrieve_cgo_val(cg1, (px,py))
            br=c[-1]
            angle_adjust=map(br,0,255,0,6)
            elaborate=int(random(1,2)*angle_adjust)
            angle_opts = [0, 90, -90, 45,-45]
            angle=[field[px/gridsize][py/gridsize]+z for z in angle_opts]
            angle=rd.choice(angle)
            r=gridsize/2
            target=PVector().fromAngle(radians(angle)).mult(r)
            newx,newy=round(px+target.x),round(py+target.y)
            # cg2.circle(px,py,5)
            t=[int(random(20)),0]
            xmult,ymult=rd.sample(t,2)
            # xmult,ymult=0,0
            newx,newy=newx+xmult*gridsize,newy+ymult*gridsize
            # list_connect.append((newx,newy))
            for j in range(elaborate):
                cg2.strokeWeight(random(1,5))
                line_gauss_path(pixel_object=cg2
                                ,x=px
                                ,y=py
                                ,destination=(newx,newy)
                                ,r=10
                                ,spread=5
                                ,lookback=False
                                ,dest_init=False
                                ,form_shape=2) 
     
    cg2.endDraw()               
    image(cg2,0,0)
    
              
    ezel_inv(w=w,ow=ow,h=h,oh=oh)
    ezel(top=oh,sides=ow)

    filename= ''.join('line_find_follow'+timestamp+'.jpg')
    save(filename)
    print("End of Program")
    # exit()
    
    
    
