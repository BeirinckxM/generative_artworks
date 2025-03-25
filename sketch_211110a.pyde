import datetime
import random as rd

w = 1300
h = 1000
ow = 80
oh = 80

color_list=[[34,137,216,255],
            [245,246,231,255],
            [231,243,246,255],
            [201,59,59,255],
            [59,201,182,255],
            [4,128,58,255],
            [44,149,227,255],
            [28,133,211,255],
            [113,152,180,255],
            [44,149,227,255],
            [167,140,250,255],
            [203,47,66,255],
            [47,100,158,255],
            [40,147,130,255],
            [230,232,159,255],
            [207,44,65,255],
            [160,180,113,255],
            [232,221,200,255],
            [222,228,229,255],
            [129,20,14,255],
            [11,82,2,255],
            [133,175,154,255]]

color_list2=[[202,10,10,255],
            [18,82,166,255],
            [18,127,166,255],
            [86,92,100,255]]

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def setup():
    size(w,h)
    background(color(255,248,241))
    noLoop()

def draw():
    def skribbles(size=10, corners=4):
    
        startx=random(ow,w-ow)
        starty=random(oh,h-oh)
        
        beginShape()
        colors=rd.choice(color_list2)
        fill(color(*colors))
        vertex(startx,starty)
        for corener in range(corners-1):
            vertex(constrain(random(startx-size,startx+size),ow,w-ow),constrain(random(starty-size,starty+size),oh,h-oh))
        vertex(startx,starty)
        endShape()
    
    def ezel(weight):
        stroke(0)
        strokeWeight(weight)
        line(ow,oh,w-ow,oh)
        line(w-ow,oh,w-ow,h-oh)
        line(ow,h-oh,w-ow,h-oh)
        line(ow,oh,ow,h-oh)
    
    xcenter=random(ow,w-ow)
    ycenter=random(oh,h-oh)
    r=20
    xpos=random(ow,w-ow)
    
    for xc in range(int(random(ow,w-ow)),w-ow,40):
        colors=rd.choice(color_list)
        fill(color(*colors))
        strokeWeight(int(random(1,3)))
        beginShape()
        for rot in range(20):
            r+=random(0,20)
            for d in range(360):
                x = xc + sin(radians(d))*r
                y = ycenter + rot*cos(radians(d))*r
                x=constrain(x,ow,w-ow)
                y=constrain(y,oh,h-oh)
                xpos=(x<w/2)
                stroke(0)
                point(x,y)
                #print(y)
                #curveVertex(x,y)
        endShape(CLOSE)
        
    for balk in range(100):
        strokeWeight(1)
        colors=rd.choice(color_list)
        fill(color(*colors))
        hii=int(random(-100,2000))
        wii=int(random(-10,30))
        balkx=random(ow,xcenter)
        balky=ycenter
        beginShape()
        vertex(balkx,balky)
        vertex(balkx,constrain(balky+hii,oh,h-oh))
        vertex(constrain(balkx+wii,ow,h-ow),constrain(balky+hii,oh,h-oh))
        vertex(constrain(balkx+wii,ow,h-ow),balky)
        endShape(CLOSE)
        
        cf=rd.uniform(0,1)
        if cf>.9:
            circle(random(ow+30,w-ow-30),random(oh,h-oh),random(10,30))
    
    #for obj in range(int(random(10,40))):
        #skribbles(size=int(random(10,20)),corners=int(random(1,5)))
    
    ezel(weight=5)
    
    filename= ''.join('skeoot'+timestamp+'.jpg')

    save(filename)
