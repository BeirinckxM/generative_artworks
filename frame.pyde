add_library('pdf')

import datetime
import random as rd


w=500
h=600
resolution=15
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
    #size(w,h,PDF,filename)
    size(w,h)
    background(255)
    noLoop()

def draw():
    
    
    def sinewave(x,y,a=1,r=20, col=rd.choice(color_list)):
        angle, tracker = 0, 0
        col_sequence = []
        x=x
        seq=0
        list_of_switches = []
        for i,ri in enumerate([r]):
            x=0
            angle=0
            #print(i)
            store_y = [(x,y)]
            at=0
            while x <= w:
                xi=x
                yi=y+a*sin(radians(angle))*ri
                c=color(pg.pixels[min(int(xi),w)+min(int(yi),h)*width])
                if c != -1 and (store_y[-1][0]+10 < int(xi)):
                    store_y.append((int(xi),int(yi)))
                    #print("switch", xi, yi, tracker) 
                    tracker = abs(tracker - 1)
                    #print(store_y)
                    stroke(color(*col))
                point(int(xi),int(yi))
                angle+=.5
                x+=.5
            else:
                seq+=1
                first=0
            
    
    pg=createGraphics(w,h)
    pg.beginDraw() 
    pg.background(255)
    for lines in range(0,h,100):
        pg.stroke(0)
        line(0,lines,w,lines)
        pg.line(0,lines,w,lines)
    pg.endDraw()
    
    pg.loadPixels()
    
    for lines in range(0,h,100):
        for sinew in range(20):
            sinewave(x=0,y=lines+sinew,a=1,r=25, col=col)
    
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
        
        
    #ezel_inv(w=w,ow=ow,h=h,oh=oh)
    
    #ezel(top=oh,sides=ow)

    print("End of Program")
    #exit()

    #save(filename)
