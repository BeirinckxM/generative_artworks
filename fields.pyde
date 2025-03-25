add_library('pdf')

import datetime
import random as rd


w=1000
h=1200
resolution=10
ow=oh=80

color_list=[[255,142,106,255],
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
            [248,208,135,255],
            [0,0,0,255],
            [191,41,0,255],
            [246,249,211,255],
            [67,136,249,255],
            [232,221,200,255],
            [222,228,229,255],
            [129,20,14,255],
            [11,82,2,255],
            [133,175,154,255]]

#colsel=[rd.choice(color_list) for i in range(3)]

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename = ''.join('fields' + timestamp + '.pdf')

def setup():
    size(w,h,PDF,filename)
    background(255)
    noLoop()
    #blendMode(DIFFERENCE);

def draw():
    
    def ezel_inv(w,ow,h,oh):
        noStroke()
        fill(255)
        rect(0,0,w,oh)
        rect(0,0,ow,h)
        rect(0,h-oh,w,oh)
        rect(w-ow,0,ow,h)
    
    def ezel(top,sides,c=255):
        stroke(0)
        strokeWeight(10)
        line(sides,top,w-sides,top)
        line(w-sides,top,w-sides,h-top)
        line(w-sides,h-top,sides,h-top)
        line(sides,h-top,sides,top)
        
    def create_field(st,en,his,hi,n,dim,dens):
        polu=rd.choice(color_list)
        if dim in (1,3):
            wi=en-st
        elif dim in (2,4):
            wi=hi
        for xs in range(wi):
            enc=0
            for i in range(n):
                gaussval=randomGaussian() * dens
                if dim==1:
                    if 0<(hi+gaussval)<hi:
                        stroke(0)
                        strokeWeight(1)
                        xoo=st+xs
                        yoo=his+hi+gaussval
                        pgcol=color(pg.pixels[int(xoo+yoo*width)])
                        if enc==0 and pgcol == -1:                
                            point(xoo,yoo)
                            if enc==1:
                                break
                        else: 
                            stroke(color(*polu))
                            strokeWeight(2)
                            point(xoo,yoo)
                            enc+1
                elif dim==2:
                    if 0<(en-st+gaussval)<en-st:
                        stroke(0)
                        strokeWeight(1)
                        xoo=en+gaussval
                        yoo=his+xs       
                        pgcol=color(pg.pixels[int(xoo+yoo*width)])                    
                        if pgcol == -1:                
                            point(xoo,yoo)
                        else: 
                            stroke(color(*polu))
                            strokeWeight(2)
                            point(xoo,yoo)
                elif dim==3:
                    if 0<(hi-gaussval)<hi:
                        stroke(0)
                        strokeWeight(1)
                        xoo=st+xs
                        yoo=his+gaussval     
                        pgcol=color(pg.pixels[int(xoo+yoo*width)])                  
                        if pgcol == -1:                
                            point(xoo,yoo)
                        else: 
                            stroke(color(*polu))
                            strokeWeight(2)
                            point(xoo,yoo)
                elif dim==4:
                    if 0<(en-st+gaussval)<en-st:
                        stroke(0)
                        strokeWeight(1)
                        xoo=st-gaussval
                        yoo=his+xs      
                        pgcol=color(pg.pixels[int(xoo+yoo*width)])                  
                        if pgcol == -1:                
                            point(xoo,yoo)
                        else: 
                            stroke(color(*polu))
                            strokeWeight(2)
                            point(xoo,yoo)
     
    n_lines=int(random(4,10))
    n_colors=int(random(10,20))
    steps=3 
    straight=.7
    circles=.2                

    pg=createGraphics(w,h)
    pg.beginDraw() 
    pg.background(255)
    strokeWeight(1)
    for i in range(n_lines):
        type=rd.uniform(0,1)
        if type>straight:
            print("straight")
            pg.stroke(0)
            pg.strokeWeight(20)
            linex=int(random(-w/2,w))
            liney=int(random(-h/2,h))
            pg.line(linex,liney,linex,liney+int(random(h-liney)))
            #line(*lineco)
        elif type>circles:
            print("bezier")
            pg.beginShape()
            pg.strokeWeight(20)
            pg.vertex(int(random(ow,w)),int(random(oh,h)))
            for i in range(int(random(3,8))):
                pg.bezierVertex(int(random(-w/2,w)),int(random(-h/2,h)),
                                int(random(-w/2,w)),int(random(-h/2,h)),
                                int(random(-w/2,w)),int(random(-h/2,h)))
            pg.endShape()
        else:
            print("circle")
            pg.fill(255)
            pg.strokeWeight(20)
            pg.stroke(0 )
            r=int(random(w/2))
            linex=int(random(-w/2,w))
            liney=int(random(-h/2,h))
            for ci in range(int(random(6))):
                r-=(r/5)
                pg.fill(255)
                pg.circle(linex,liney,r)
    pg.endDraw()
    
    pg.loadPixels()
    print("pooop")
                    
    ws=500
    hs=150
    
    for y in range(oh,h-oh,hs+5):
        for x in range(ow,w-ow,ws+5):
            noStroke()
            colu=rd.choice(color_list)
            fill(color(*colu))
            #rect(x,y,ws,hs)
            stroke(0)
            dimr=rd.randint(1,4)
            densr=rd.randint(30,80)
            enr=rd.randint(100,300)
            _str=rd.randint(100,300)
            hir=rd.randint(60,300)
            nr=rd.randint(50,100)
            #print(dimr)
            create_field(st=x,en=(x+min(ws,w-ow-x-5)),his=y,hi=hs,n=nr,dim=dimr,dens=densr)
        
        
    #ezel_inv(w=w,ow=ow,h=h,oh=oh)
    
    #ezel(top=oh,sides=ow)

    print("End of Program")
    exit()

    #save(filename)
