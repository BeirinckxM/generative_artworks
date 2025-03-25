add_library('pdf')
import datetime
import time
# import math
import random as rd
# from collections import Counter

resolution=40
ow=oh=resolution
w=ow+resolution*120-ow
h=oh+resolution*100-oh

print(w,h,w*h)

all_col    =[[241, 78, 27],
            [8, 63, 88],
            [158, 37, 38],
            [207, 83, 27],
            [194, 27, 20],
            [34, 84, 63],
            [41, 64, 90],
            [33, 51, 44],
            [10, 56, 113],
            [3, 98, 127],
            [255, 255, 255],
            [232,221,200,255],
            [222,228,229,255],
            [129,20,14,255],
            [11,82,2,255],
            [133,175,154,255]     
]  

# color_list = [((185.0, 12.0, 32.0, 255.0)),(0.0, 0.0, 0.0, 255.0),(9.0, 72.0, 118.0, 255.0)]

background_col=(239,234,212)

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

square_size=resolution*60

print(square_size*square_size)

def setup():
    # size(w,h,PDF, ''.join('collage'+timestamp+'.pdf'))
    size(w,h)
    background(*background_col)
    noLoop()
 
    # blendMode(REPLACE)
    
    global cg1
    global cg2
    global cg3
    
    cg1=createGraphics(square_size,square_size)
    cg2=createGraphics(w,h)
    # cg3=createGraphics(w+2*ow,h+2*oh)
    
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

def pick_color(k=3):
    return rd.sample(all_col,k)

def get_rgba(value):
    rgba=(red(value), green(value), blue(value), alpha(value))
    
    return rgba  

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

def retrieve_cgo_val(pixel_object, coordinates, pobw):
    cval=get_rgba(pixel_object.pixels[coordinates[0]+coordinates[1]*pobw])
    return cval
    

def guass_blob(pixel_object, location, type, blob_size, xmu, xsigma,ymu,ysigma, taper):
    ysize,xsize=blob_size[1], blob_size[0]
    yvalues= [rd.gauss(ymu,ysigma) for y in range(ysize)]
    locx,locy=location
    xsig_iter=0
    factor1=int(random(2,5))
    factor2=int(random(2,10))
    factor3=int(random(2))
    xoff=0
    yoff=0
    for i,yval in enumerate(sorted(yvalues)):
        yoff+=0.01
        if taper or type[1]=="geom1":
            if i < (len(yvalues)/2):
                xsig_iter+=1
            else:
                xsig_iter-=1
            # print(xsig_iter)
        else:
            xsig_iter=xsigma
            
        for it in range(xsize):
            xoff+=0.01
            xval=rd.gauss(xmu,xsig_iter)
            px,py=int(locx+xval),int(locy+yval)
            
            frag_list = []
            if type[0]=="line":
                if type[1]=="referenced":
                    if factor3==1:
                        x1,y1,x2,y2=type[2]
                    else:
                        x2,y2,x1,y1=type[2]
                        
                    if px>=locx:
                        frag_scale=dist(x1,y1,locx,locy)/(blob_size[0])
                        # frag_scale=float((px-locx))/(locx+1)
                        atan_val = atan2((py-y1),(int(px-x1)))
                    else:
                        frag_scale=dist(x2,y2,locx,locy)/(blob_size[0])
                        # frag_scale=float((px-locx))/(locx+1)
                        atan_val = atan2((py-y2),(int(px-x2)))
                    # print(frag_scale)
                        
                    angle = atan_val
                    target=PVector().fromAngle(angle).mult(type[3]*frag_scale)
                    newpx=int(px+target.x)
                    newpy=int(py+target.y)
                    pixel_object.line(px,py,newpx,newpy)
                    
                elif type[1]=="random":
                    x1,y1,x2,y2=int(random(w)),int(random(h)),int(random(w)),int(random(h))
                    if px>=locx:
                        frag_scale=float((abs(px)-locx))/(locx)
                        atan_val = atan2((py-y1),(int(px-x1)))
                    else:
                        frag_scale=float(locx-abs(px))/(locx)
                        atan_val = atan2((py-y2),(int(px-x2)))
                        
                    angle = atan_val
                    target=PVector().fromAngle(angle).mult(resolution*frag_scale)
                    newpx=int(px+target.x)
                    newpy=int(py+target.y)
                    pixel_object.line(px,py,newpx,newpy)
                        
                elif type[1]=="geom1":
                    if px>=locx:
                        frag_scale=float((px-locx))/(locx+1)
                    else:
                        frag_scale=float(locx-px)/(locx+1)
                        
                    newpx=locx+sin(xval*frag_scale)*(xval*factor1)
                    newpy=locy+cos(yval*frag_scale)*(xval*factor2)
                    pixel_object.point(newpx,newpy)
                    
                elif type[1]=="geom_ref":
                    x1,y1,x2,y2=type[2]
                    if px>=locx:
                        r=dist(x1,y1,locx,locy)
                        # frag_scale=float((px-locx))/(locx+1)
                        atan_val = atan2((py-y1),(int(px-x1)))
                        newpx=x1+sin(atan_val)*(xval)
                        newpy=y1+cos(atan_val)*(xval)
                    else:
                        r=dist(x2,y2,locx,locy)
                        # frag_scale=float((px-locx))/(locx+1)
                        atan_val = atan2((py-y2),(int(px-x2)))
                        newpx=x2+sin(atan_val)*(r)
                        newpy=y2+cos(atan_val)*(r)
                    # print(frag_scale)

                    pixel_object.point(newpx,newpy)
                    
            elif type[0]=="point1":
                displacex=map(noise(yoff),0,1,0,resolution*2)
                pixel_object.point(px+displacex,py)
            
            elif type[0]=="point2":
                r=dist(px,py,locx,locy)
                r=int(blob_size[1]/2)
                midcircle=(locx,int(locy+blob_size[1]/2))
                angle = map(noise(i*0.1),0,1,0,360)
                newpx=midcircle[0]+sin(radians(angle))*(r)
                newpy=yval+cos(radians(angle))*(r)
                pixel_object.point(newpx,newpy)
                
            elif type[0]=="circle":
                frag_scale=dist(px,py,locx,locy)/w
                if rd.uniform(0,1) >0.99:
                    pixel_object.fill(color(int(random(10,60)),0,0,100))
                    pixel_object.circle(px,py,resolution*frag_scale)
                # else:
                #     pixel_object.noFill()
                # pixel_object.circle(px,py,resolution*frag_scale)
    
    
    
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################   
         
def draw():
    
    cg2.beginDraw()    
    xiter=int(random(resolution,resolution*10))
    yiter=int(random(resolution,resolution*10))
    cg2.stroke(color(int(random(10,60)),0,0,100))
    cg2.fill(color(int(random(10,60)),0,0,50))
    cg2.strokeWeight(1)
    x=0
    y=int(h/2)
    print(xiter,yiter)
    for x in range(0,w,xiter):
        for y in range(0,h,yiter):
            xt=(x-xiter,x+xiter)
            yt=(y-yiter,y+yiter)
            print(x,y)
            choice=rd.sample(["line", "point2","point1", "circle", "geom" ],1)
            choice2=rd.sample(["geom1", "geom_ref", "referenced" ],1)
            if rd.uniform(0,1) > 0.3:
                guass_blob(pixel_object=cg2
                        ,location=(x,y)
                        ,type=(choice[0], choice2[0]
                            , (int(random(*xt)),int(random(*yt)),int(random(*xt)),int(random(*yt)))
                            , random(resolution/2)
                            )
                        # ,type=("circle",10)
                        # ,type=("circle",10)
                        ,blob_size=(int(random(resolution*10)),int(random(resolution*30)))
                        ,xmu=int(random(resolution*2)),xsigma=int(random(resolution,resolution*20))
                        ,ymu=int(random(resolution*2)),ysigma=int(random(resolution,resolution*20))
                        ,taper=int(random(2))
                        )
    cg2.endDraw() 
    
    image(cg2,0,0)
    
    ezel_inv(w=w,ow=ow,h=h,oh=oh)
    ezel(top=oh,sides=ow)

    filename= ''.join('wolk'+timestamp+'.jpg')
    save(filename)
    print("End of Program")
    exit()
    
    
    
