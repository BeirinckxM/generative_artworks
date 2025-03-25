add_library('pdf')

import datetime
import random as rd
from collections import Counter

r_split=250
w=5*r_split
h=6*r_split
ow=oh=50

color_list=[ "#4D5571",
            "#252E4D",
            "#254D3A",
            "#790B12",
            "#65746A",
            "#8B9357",
            "#C1CE6C",
            "#6CA9CE",
            "#009FFF",
            "#FFEA00",
            "#F5A800",
            "#E8E7E5",
            "#D80209",
            "#07B269",
            "#236C4D",
            "#A6D1EA",
            "#B7E8E7",
            "#F0EAA9",
            "#F27E78",
            "#232050",
            "#374D33",
            "#478D9D",
            "#6B9B2F",
            "#FF98B0","#C5E3C3","#D7E3C3","#FFAA00","#CE000E","#EDE58B","#EDAC8B",
            "#1279C6","#12C2C6","#AF6900","#C2D1A6","#315783","#44BF08"]

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename= ''.join('lineswitch'+timestamp+'.pdf')

cback=color(245,245,213)

def setup():
    size(w,h,PDF,filename)
    #size(w,h)
    background(cback)
    noLoop()

def draw():
    
    n_lines=int(random(4,12))
    n_colors=int(random(10,20))
    steps=1
    
    colsel=[rd.choice(color_list) for i in range(n_colors)]
    rd.shuffle(colsel)
    
    straight=.8
    circles=.3
    
    pg=createGraphics(w,h)
    pg.beginDraw() 
    pg.background(255)
    strokeWeight(1)
    for i in range(n_lines):
        type=rd.uniform(0,1)
        if type>straight:
            print("straight")
            pg.stroke(0)
            linex=int(random(-w/2,w))
            liney=int(random(-h/2,h))
            pg.line(linex,liney,linex,liney+int(random(h-liney)))
            #line(*lineco)
        elif type>circles:
            print("bezier")
            pg.beginShape()
            pg.noFill()
            pg.vertex(int(random(ow,w)),int(random(oh,h)))
            for i in range(int(random(3,8))):
                pg.bezierVertex(int(random(-w/2,w)),int(random(-h/2,h)),
                                int(random(-w/2,w)),int(random(-h/2,h)),
                                int(random(-w/2,w)),int(random(-h/2,h)))
            pg.endShape()
        else:
            print("circle")
            r=int(random(w/2))
            linex=int(random(-w/2,w))
            liney=int(random(-h/2,h))
            for ci in range(int(random(6))):
                r-=(r/5)
                pg.noFill()
                pg.circle(linex,liney,r)
    pg.endDraw()
    
    pg.loadPixels()
    
    # #image(pg, 0, 0)
    # _split=int(random(2,4))
    # c_follower=0
    # for y in range(0,h/_split,steps):
    #     for x in range(0,w,steps):
    #         #print("left to right:", x,y)
    #         pgcol=color(pg.pixels[x+y*width])
    #         if x==0:
    #             c_follower=0
    #             countblack=0
    #         if pgcol != -1:
    #             countblack+=1
    #         else:
    #             if countblack != 0:
    #                 if c_follower < n_colors:
    #                     c_follower+=1
    #                 countblack=0    
    #         stroke(colsel[c_follower-1])
    #         if rd.uniform(0,1) > .5:
    #             strokeWeight(steps)
    #             point(x,y)
                
    # c_follower=n_colors            
    # for y in range(h/_split,h,steps):
    #     for x in range(w-1,-1,-steps):
    #         #print("right to left:", x,y)
    #         pgcol=color(pg.pixels[x+y*width])
    #         if x==w-1:
    #             c_follower=n_colors
    #             countblack=0
    #         if pgcol != -1:
    #             countblack+=1
    #         else:
    #             if countblack != 0:
    #                 if c_follower > 0:
    #                     c_follower-=1
    #                 countblack=0    
    #         stroke(colsel[c_follower-1])
    #         if rd.uniform(0,1) > .5:
    #             strokeWeight(steps)
            
    #             point(x,y)
    
    # def circle_pack(n,protect=500):
    #         circles=list()
            
    #         protection=0
    
    #         r=500
            
    #         while len(circles) < n:
    #             new_circle=(int(random(w)),int(random(h)),r)
    #             overlapping=False
                
    #             for j in range(len(circles)):
    #                 other = circles[j]
    #                 d = dist(new_circle[0],new_circle[1], other[0], other[1])
    #                 if d < (new_circle[2]+other[2])/2:
    #                     protection+=1
    #                     overlapping=True
    #                     if protection in [lim for lim in range(0,protect,protect/5)]:
    #                         r-=10
                
    #             if not overlapping:
    #                 protection=0
    #                 circles.append(new_circle)

    #             if protection==protect:
    #                 print("Protection: limit reached")
    #                 break
                    
    #         return circles
                
    #list_to_draw=circle_pack(n=200)
    
    #for spots in list_to_draw:
    for xs in range(r_split/2,w,r_split):
        for ys in range(r_split/2,h,r_split):
            fill(cback)
            noStroke()
            xcenter=xs
            ycenter=ys  
            circle(xcenter,ycenter,r_split)      
            r=0
            step=float(1)
            #countblack=0
            for circle_r in range(0,r_split):
                r+=1
                if circle_r%200==0:
                    step=step/2
                points_to_draw=[j * step for j in range(0,int(360*(1/step)))]
                
                for i,d in enumerate(points_to_draw):
                    x = int(constrain(xcenter + sin(radians(d))*r/2,0,w))-1
                    y = int(constrain(ycenter + cos(radians(d))*r/2,0,h))-1
                    pgcol=color(pg.pixels[x+y*width])
                    if y==ycenter-1:
                        c_follower=0
                        countblack=0
                    if pgcol != -1:
                        countblack+=1
                    else:
                        if countblack != 0:
                            if c_follower < n_colors:
                                c_follower+=1
                            countblack=0    
                    stroke(colsel[c_follower-1])
                    if rd.uniform(0,1) > .5:
                        strokeWeight(steps)
                        point(x,y)

    def ezel_inv(w,ow,h,oh):
        noStroke()
        fill(255)
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

    ezel_inv(w=w,ow=ow,h=h,oh=oh)
    
    ezel(top=oh,sides=ow)

    print("End of Program")
    exit()
