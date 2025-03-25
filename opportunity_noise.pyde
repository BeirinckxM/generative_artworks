add_library('pdf')
import datetime
import random as rd
import math
import itertools

resolution=10
ow=oh=resolution
w=resolution*50
h=resolution*60

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
    blendMode(REPLACE)
    
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
    
def rotating_fan(object, rota, sigma, r=40):
    # Starting from arctan angle and deviating with sigma
    for d in range(rota-sigma,rota+sigma):
        xc = sin(gaussian_angle)*r
        yc = cos(gaussian_angle)*r
        current_color=retrieve_cgo_val(pixel_object=object, coordinates=(xc,yc))
        if current_color != (255.0,255.0,255.0,255.0):
            pass
        
    
def fan(x,y,r,a,s,d):
    
    n=r*2+d
    
    stroke(0)
    strokeWeight(0)
    pushMatrix()
    translate(x,y)
    for i in range(int(r)):
        r-=1
        for p in range(int(n)):
            gaussian_angle=rd.gauss(mu=a,sigma=s)
            xc = sin(gaussian_angle)*r
            yc = cos(gaussian_angle)*r
            object.point(xc,yc)
    popMatrix()    

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
    
def create_pathlike(object,cset, mean):
        object.beginDraw()
        object.pushMatrix()
        object.background(255)
        object.fill(0)  
        object.stroke(0)   
        path_list=[]
        for p in cset:
            x,y = p[0],p[1]
            diffx,diffy=x-mean[0],y-mean[1]
            sa=atan2(diffx,diffy)
            
            xoff=random(1)
            nstep=0.002
            x_range=int(random(100))
            path = []
            for yi in range(y,h):
                noise_val=noise(xoff)
                xmove = map(noise_val, 0.0, 1.0, 0, x_range)
                xp,yp=x+xmove,yi
                object.circle(xp,yp,10)  
                xoff+=nstep
                path.append((xp,yp))
            path_list.append(path)
        object.popMatrix()
        object.endDraw()
        
        return path_list
    
def retrieve_cgo_val(pixel_object, coordinates):
    cval=get_rgba(pixel_object.pixels[coordinates[0]+coordinates[1]*width])
    
    return cval        
    

def get_gaussian_coordset(n=20,mux=w/2,muy=h*1/4,sx=w/5,sy=h/9):
    xset=[int(rd.gauss(mu=mux,sigma=sx)) for i in range(n)]
    yset=[int(rd.gauss(mu=muy,sigma=sy)) for i in range(n)]
    cset=zip(xset,yset)    
    
    mean = (sum([p[0] for p in cset])/len(cset),sum([p[1] for p in cset])/len(cset))

    return (mean, cset)


def draw():
    
    print("Starting")
    
    cg1=createGraphics(w,h)
    
    meanc, cset = get_gaussian_coordset(n=int(random(5,15)))
    print(meanc, cset)
    path_list = create_pathlike(object=cg1,cset=cset, mean=meanc)
    
    # cg1.updatePixels()
    
    image(cg1,0,0)
    cg1.updatePixels()
    
    # for p in cset:
    #     x,y = p[0], p[1]
    #     gettest = cg1.get(x,y)
    #     c=get_rgba(gettest)
    #     print(c)
    
    # for x in range(w):
    #     for y in range(h):
    #         current_color = retrieve_cgo_val(pixel_object=cg1, coordinates=(x,y))
    #         if current_color != (255.0,255.0,255.0,255.0):
    #             probability = 0.99
    #         else:
    #             probability = 0.90
    #         chance=rd.uniform(0,1)>probability
    #         if chance:
    #             r=random(200,255)
    #             g=random(200,255)
    #             b=random(220,255)
    #             a=random(200,255)
    #             c=color(r,g,b,a)
    #         else:
    #             c=random(0,10)
    #         stroke(c)
    #         # print(x)
    #         # print(y)
    #         point(x,y)
            
    # for p in path_list:
    #     for _point in p:
    #         # pass
    #         x,y=_point[0],_point[1]
    #         stroke(color(255,240,240,200))
    #         strokeWeight(1)
    #         point(x,y)       
        
        
    # ezel_inv(w=w,ow=ow,h=h,oh=oh)
    # ezel(top=oh,sides=ow)

    # filename= ''.join('white_blue'+timestamp+'.jpg')
    # save(filename)
    print("End of Program")
    # exit()
    
    
    
