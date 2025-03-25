add_library('pdf')

w=800
h=1000
ow=oh=70

import datetime
import random as rd

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
            [133,175,154,255],
            [131,240,213,255],
            [208,232,183,255],
            [255,178,77,255],
            [247,247,170,255],
            [162,191,100,255],
            [216,66,7,255]
            ]

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename= ''.join('paths'+timestamp+'.pdf')

def setup():
    #size(w,h,PDF,filename)
    size(w,h)
    noLoop()
    background(245,240,238)
    
def draw():
    
    for n in range(1):
        _limit = 0
        x=int(random(ow,w-ow))
        y=int(random(oh,h-oh))
        r=1
        zoff=random(1)
    
        angle=0
        noisepower=10
        noiseScale=3000
        strokescale=500
        type=rd.choice((-1,1))
        beginShape()
        while (0<x<w) and (0<y<h) and _limit < 5000:
            _limit +=1
            
            prex=x
            prey=y
            
            
            angle=noise(x/noiseScale,y/noiseScale,zoff)*noisepower
            x+=cos(angle)*r*type
            y+=sin(angle)*r*type
        
            strokeweight=noise(x*n/strokescale,y*n/strokescale,zoff)*4
            
            strokeWeight(strokeweight)
            stroke(0)
        
            zoff+=0.009
            noFill()
            stroke(color(*rd.choice(color_list)))
            #line(prex,prey,x,y)
            #vertex(x,y)
            rb=map(noise(zoff),0,1,0,30)
            circle(x,y,rb)
            
            
        endShape(OPEN)
        
        
    def ezel_inv(w,ow,h,oh):
        noStroke()
        fill(255)
        rect(0,0,w,oh)
        rect(0,0,ow,h)
        rect(0,h-oh,w,oh)
        rect(w-ow,0,ow,h)
    
    def ezel(top,sides,c=255):
        stroke(0)
        strokeWeight(4)
        line(sides,top,w-sides,top)
        line(w-sides,top,w-sides,h-top)
        line(w-sides,h-top,sides,h-top)
        line(sides,h-top,sides,top)

    ezel_inv(w=w,ow=ow,h=h,oh=oh)
    
    ezel(top=oh,sides=ow)

    print("End of Program")
    #exit()    
