add_library('pdf')

import datetime
import random as rd


w=1000
h=1200
resolution=10
ow=oh=80

color_list=[[114,11,11,255],
            [210,4,4,255],
            [0,48,208,255],
            [11,35,115,255],
            [11,84,115,255],
            [89,156,185,255],
            [89,185,147,255],
            [8,98,62,255],
            [190,61,44,255],
            [169,183,127,255],
            [247,252,202,255],
            [252,212,102,255],
            [252,112,102,255],
            [0,0,0,255],
            [191,41,0,255],
            [246,249,211,255],
            [67,136,249,255],
            [232,221,200,255],
            [222,228,229,255],
            [129,20,14,255],
            [11,82,2,255],
            [133,175,154,255],
            [255,142,106,255],
            [27,128,118,255],
            [84,84,77,255],
            [140,48,17,255],
            [239,231,183,255],
            [239,212,63,255],
            [44,81,21,255],
            [43,95,128,255],
            [190,61,44,255],
            [144,166,112,255],
            [140,204,248,255],
            [248,190,181,255],
            [248,208,135,255]]

#color_list=["AF1313", "720B0B"]

colsel=[rd.choice(color_list) for i in range(7)]

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename = ''.join('fields' + timestamp + '.pdf')

def setup():
    size(w,h,PDF,filename)
    background(color(255,255,250))
    noLoop()
    #blendMode(DIFFERENCE);

def draw():
    
    def ezel_inv(w,ow,h,oh):
        noStroke()
        fill(color(255,255,250))
        rect(0,0,w,oh)
        rect(0,0,ow,h)
        rect(0,h-oh,w,oh)
        rect(w-ow,0,ow,h)
    
    def ezel(top,sides,c=color(255,255,250)):
        stroke(0)
        strokeWeight(3)
        line(sides,top,w-sides,top)
        line(w-sides,top,w-sides,h-top)
        line(w-sides,h-top,sides,h-top)
        line(sides,h-top,sides,top)
        
    def circle_points(x, y, r, angle):
    
        x = x+ sin(radians(angle)) * r
        y = y+ cos(radians(angle)) * r
    
        point(x,y)
        #return list(x, y)
    
    def weird_skribble(x,y,r,n,dens):

        gaussarray=[int(randomGaussian() * dens) for p in range(n)]
        point_array=list()
        #beginShape()
        for i in range(n):
            x = x+ sin(radians(gaussarray[i])) * r
            y = y+ cos(radians(gaussarray[i])) * r
            point_array.append((x,y))
        
        return(point_array)
        #endShape()
        
    
    def gaussian_circle(x,y,r,n,dens,sig,shift):

        gaussarray=[int(rd.gauss(mu=dens, sigma=sig)) for p in range(n)]
        for i in range(n):
            xs = x+ sin(radians(shift+gaussarray[i])) * r
            ys = y+ cos(radians(shift+gaussarray[i])) * r
            strokeWeight(1)
            point(xs,ys)
            #noStroke()
            #fill()
            #square(x,y,5)
    
    n_skribbles=rd.randint(40,60)
    ra=40
    #r=rd.randint(30,120)
    
    # background
    # backn=20
    # for ib in range(backn):
    #     gauss_p_list_background=weird_skribble(x=rd.randint(ow*2,w-ow)
    #                                 ,y=rd.randint(oh,h-oh)
    #                                 ,r=100
    #                                 ,n=5
    #                                 ,dens=100)
    #     for pb in range(len(gauss_p_list_background)):
    #         xb=gauss_p_list_background[pb][0]
    #         yb=gauss_p_list_background[pb][1]
    #         colub=[200,200,200,255]
    #         #backcol=[x+rd.randint(0,100) for x in colub]
    #         stroke(color(*colub))
    #         shift=rd.randint(1,200)
    #         gaussian_circle(x=xb,y=yb,r=1,n=50,dens=80,sig=rd.randint(20,40),shift=shift)
        
    # details
    # gauss_p_list_start=weird_skribble(x=rd.randint(ow*2,w-ow*2)
    #                                   ,y=rd.randint(oh,h/4)
    #                                   ,r=200
    #                                   ,n=n_skribbles
    #                                   ,dens=300)
    
    for xx in range(ow,w-ow,100):
        for yy in range(oh,h-oh,100):

            #r=rd.randint(30,120)
            ra=rd.randint(20,50)
            npieces=rd.randint(20,60)
            xi=xx
            yi=yy
            #print(xi,yi)
            gauss_p_list=weird_skribble(x=xi,y=yi,r=30,n=npieces,dens=400)
            shift=rd.randint(1,200)
            colug=rd.choice(colsel)
            for p in range(len(gauss_p_list)):
                r=rd.randint(1,4)
                xi=gauss_p_list[p][0]
                yi=gauss_p_list[p][1]
                stroke(color(*colug))
                #line(xi,yi,xi+rd.randint(-20,20),yi-rd.randint(100,300))
                strokeWeight(3)
                point(xi,yi)
                for rs in range(ra):
                    reds=[x+rd.randint(0,40) for x in colug]
                    #print(reds)
                    colu=rd.choice(colsel)
                    #noStroke()
                    stroke(color(*reds))
            
                    gaussian_circle(x=xi,y=yi,r=r,n=50,dens=50,sig=rd.randint(10,30),shift=shift)
                    r+=1
                shift+=8

            
    ezel_inv(w=w,ow=ow,h=h,oh=oh)
    
    ezel(top=oh,sides=ow)

    print("End of Program")
    exit()

    #save(filename)
