add_library('pdf')
import datetime
import random as rd

resolution=10
ow=oh=resolution*3
w=resolution*90
h=resolution*100

color_list=[[198,26,26],
            [24,134,168],
            [141,175,155],
            [238,223,96],
            [238,119,0],
            [171,169,153],
            [244,92,86],
            [203,226,201],
            [253,235,131],
            [255,255,255],
            
]

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def setup():
    # size(w,h,PDF, ''.join('kkkk'+timestamp+'.pdf'))
    size(w,h)
    background(245,240,219)
    noLoop()
    #blendMode(DIFFERENCE)

def draw():
    
    print("Starting")
    
    x=w/2
    y=h/2
    xoff,yoff,zoff=0,0,0
    r=1
    stroke(0)
    noFill()
    
    for p in range(10000):
        spreader=5
        nval=noise(xoff/spreader,yoff/spreader,zoff/spreader)
        angle=map(nval,0,1,0,360)
        x+=cos(angle)*r
        y+=sin(angle)*r
        
        point(x,y)
        
        xoff+=0.001
        yoff+=0.001
        zoff+=0.001
        
        
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

    # ezel_inv(w=w,ow=ow,h=h,oh=oh)
    
    ezel(top=oh,sides=ow)
    
    # filename= ''.join('boxes'+timestamp+'.jpg')
    # save(filename)
    print("End of Program")
    # exit()
    
