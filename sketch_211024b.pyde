import datetime
import os
import random as rd

w = int(random(1000,1600))
h = int(random(1000,1200))

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

ABUNCHOFCOLORS = [[44,149,227],
                  [28,133,211],
                  [113,152,180],
                  [44,149,227],
                  [167,140,250],
                  [203,47,66],
                  [47,100,158],
                  [40,147,130],
                  [230,232,159],
                  [207,44,65],
                  [160,180,113],
                  [232,221,200],
                  [222,228,229],
                  [129,20,14],
                  [11,82,2],
                  [133,175,154],
                  [255,251,212],
                  [229,251,203],
                  [255,192,166],
                  ]
    
def setup():
    size(w,h)
    background(255)
    noLoop()
        
def draw():
    def ezel(top,sides,c=255):
        stroke(0)
        line(sides,top,w-sides+2,top)
        line(w-sides+2,top,w-sides+2,h-top+2)
        line(w-sides+1,h-top+2,sides,h-top+2)
        line(sides,h-top+2,sides,top)
        
    
    def drawline(x0, y0, x1, y1):
    
        dx = abs(x1-x0)
        dy = abs(y1-y0) 
        sx = sy = 0
            
        #sx = 1 if x0 < x1 else -1
        #sy = 1 if y0 < y1 else -1
            
        if (x0 < x1): 
            sx = 1 
        else: 
            sx = -1
        if (y0 < y1):
            sy = 1 
        else: 
            sy = -1
        
        err = dx - dy
            
        while (True):
        
            point(x0, y0)
        
            if (x0 == x1) and (y0 == y1): 
                break
        
            e2 = 2 * err
            if (e2 > -dy):
                err = err - dy
                x0 = x0 + sx
        
            if (x0 == x1) and (y0 == y1):
                break
    
            if (e2 <  dx):
                err = err + dx
                y0 = y0 + sy 
            
    # drawline(50,250,250,500)
        
    def draw_circle(xcenter,ycenter, r):
        for d in range(360):
            x = xcenter + sin(radians(d))*r
            y = ycenter + cos(radians(d))*r
            stroke(0)
            strokeWeight(1)
            point(x,y)
            
            

    def plume(startx,starty,stroke_length,pressure,amount):
        for i in range(stroke_length):
            lift=(i>(stroke_length/random(1,8)))
            for j in range(int(amount)):
                x = round(randomGaussian() * (i*pressure))
                point(constrain(startx+x, 40, w-40),constrain(starty+i, 40, h-40))
            if lift:
                pressure-=(pressure/(stroke_length-i))     
        # line(0,starty,w,starty)
        # line(0,starty+stroke_length,w,starty+stroke_length)    
   
    for jj in range(int(random(1,1))):
        for strokes in range(int(random(200,400))):
            xs = random(40,w-40)+round(randomGaussian() * random(20,40))
            a,b,c=rd.choice(ABUNCHOFCOLORS)
            stroke(color(a,b,c))
            
            plume(startx=xs,
                starty=random(-40,h-40), 
                stroke_length=int(random(20,400)), 
                pressure=random(0,1), 
                amount=int(random(10,80)))
    ezel(41,41)
    filename= ''.join('noisywaves'+timestamp+'.jpg')
    
    save(filename)
        
        
        
