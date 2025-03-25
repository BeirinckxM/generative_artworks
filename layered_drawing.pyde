add_library('pdf')
import datetime
import random as rd
import math
import itertools

resolution=10
ow=oh=resolution
w=resolution*70
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
    
def create_pathlike(object):
        object.beginDraw()
        object.pushMatrix()
        object.background(255)
        
        randx,randy,obj_size=random(ow,w-ow), random(oh,h-oh), random(oh,h-oh)
        object.fill(0)  
        object.circle(randx,randy,obj_size)   
        object.popMatrix()
        object.endDraw()
        
def retrieve_cgo_val(pixel_object, coordinates):
    cval=get_rgba(pixel_object.pixels[coordinates[0]+coordinates[1]*width])
    
    return cval        
    
    
    

def draw():
    
    print("Starting")
    
    cg1=createGraphics(w,h)

    create_pathlike(object=cg1)
    
    # image(cg1, 0, 0)
    # g=1
    # for x in range(ow,w-ow,20):
    #     f=1
    #     for y in range(oh,h-oh,2):
    #         pushMatrix()
    #         translate(x,y)
    #         for p in range(50):
    #             rc=rd.gauss(mu=90,sigma=40)
    #             xc = sin(radians(rc))*20+f
    #             yc = cos(radians(rc))*20+g
    #             point(xc,yc)
    #         f+=rd.choice([1,-1])
    #         g+=rd.choice([1,-1])
    #         popMatrix()
    
    def fan(mu,sigma,n=100):
        for p in range(n):
            gaussian_angle=rd.gauss(mu=mu,sigma=sigma)
            xc = sin(radians(gaussian_angle))*10
            yc = cos(radians(gaussian_angle))*10
            point(xc,yc)
        
    
    x=w/2
    y=h/2
    
    def fan(x,y,r,a,s):
        stroke(0)
        pushMatrix()
        translate(x,y)
        rm=r
        n=r*2
        for i in range(int(r)):
            r-=1
            for p in range(int(n)):
                gaussian_angle=rd.gauss(mu=a,sigma=s)
                xc = sin(radians(gaussian_angle))*r
                yc = cos(radians(gaussian_angle))*r
                diffx=map(xc,0,r,0,1)
                diffy=map(yc,0,r,0,1)
                diff=diffx
                # print(diff)
                stroke(0)
                strokeWeight(0)
                # stroke(255*(1-diff))
                point(xc,yc)
                # stroke(255*(1-diff))
                # line(0,0,xc,yc)
        popMatrix()
    
    nn=10
    xset=[int(rd.gauss(mu=w/2,sigma=random(w/2))) for i in range(nn)]
    yset=[int(rd.gauss(mu=h/2,sigma=random(h/2))) for i in range(nn)]
    cset=zip(xset,yset)
    
    def expand(speed=5):
        # all_points=[(int(random(w)), int(random(h)))]
        set_start=(int(random(w)), int(random(h)))
        all_points=[set_start]
        passed_points=[[]]
        
        def expand_add(depth=0,max_depth=10):
            # speed=int(random(10,40))
            points=list(set(all_points) - set(passed_points[0]))
            passed_points[0]=points
            # print(depth, len(points))
            # points=list(set(all_points) - set(passed_points))
            angles=[int(random(360)) for a in range(int(random(2,4)))]
            g=100*depth/max_depth
            f=100
            # binned=sorted(set(points), key=lambda x: x[0])
            # bin=20
            # binned=[binned[max(0,i-bin):i] for i in range(bin,len(binned),bin)]
            # if binned:
            #     binned=binned[0]
            #     # print(binned)
            # else:
            #     binned=points
            while depth < max_depth:
                for j,p in enumerate(points):
                    # print(points)
                    xs,ys=points[j][0],points[j][1]
                    a=rd.choice(angles)
                    strokeWeight(1)
                    stroke(color(random(50),f,0,255*depth/max_depth))
                    fill(color(random(50),f,0,255))
                    target=PVector().fromAngle(PI/2-radians(a)).mult(speed)
                    # print(target)
                    xoff=random(10)
                    yoff=0
                    for i in range(0,speed,3):
                        yoff+=0.1
                        noise_val=noise(xoff,yoff)*4
                        xlerp=int(lerp(xs,int(xs+target.x+noise_val),(float(i)+1)/speed))
                        ylerp=int(lerp(ys,int(ys+target.y+noise_val),(float(i)+1)/speed))
                        if get_rgba(get(xlerp,ylerp)) == (245.0, 240.0, 219.0, 255.0):
                            all_points.append((xlerp,ylerp))
                            # print(i, all_points)
                            point(xlerp,ylerp)
                            # square(xlerp,ylerp,5)
                        
                _depth=depth+1

                return expand_add(depth=_depth)
                
        expand_add(depth=0)
    
    for px,py in cset:       
        expand(speed=20)
        fan(x=px,y=py,r=random(50,160),a=random(360),s=random(30,60))  
                
            
    # q = [(int(random(w)),int(random(h))) for n in range(10)]   
    # s = sorted(q, key=lambda x: x[0])
    
    # f = [s[max(0,i-2):i] for i in range(2,len(s),2)]
    # print(q)
    # print(s)
    # print(f)
        
        
    ezel_inv(w=w,ow=ow,h=h,oh=oh)
    ezel(top=oh,sides=ow)
    
    # stroke(0)
    # x,y=w/2,h/2
    # point(x,y)
    # # updatePixels()
    # print(get_rgba(get(x,y)))
    # print(get_rgba(get(x+10,y)))
            

    # filename= ''.join('white_blue'+timestamp+'.jpg')
    # save(filename)
    print("End of Program")
    # exit()
    
    
