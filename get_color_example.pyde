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
    noFill()
    stroke(0)
    circle(x,y,200)
    
    # print(hex(get(x,y)), red(get(x,y)), green(get(x,y)), blue(get(x,y)), alpha(get(x,y)))
    
    def get_rgba(value):
        rgba=(red(value), green(value), blue(value), alpha(value))
        return rgba
    
    # x=0
    # y=h/2
    # while get_rgba(value=get(x,y)) != (0.0,0.0,0.0,255.0):
    #     point(x,y)
    #     x+=1
    
    line(800,0,800,h)
    
    for n in range(3):    
        for y in range(0,h,int(random(50))):
            x=0
            while get_rgba(value=get(x,y)) == (245,240,219,255) and ((0<=x<w) and (0<=y<h)):
                # print(get_rgba(value=get(x,y)))
                point(x,y)
                x+=1
    
    # Does get work on cg objects?
    pg1=createGraphics(w,h)
    pg1.beginDraw()
    pg1.pushMatrix()
    pg1.translate(w/2,h/2)
    pg1.background(255)
    pg1.stroke(color(0,0,0))
    pg1.fill(0)
    pg1.circle(w/2,h/2,200)
    pg1.popMatrix()
    pg1.endDraw()
    
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
    
    ezel(top=oh,sides=ow)
    
    # x1=0
    # y1=h/2+10
    
    # rgba=get_rgba(value=pg1.get(x1,y1)) 
    # print(rgba)
    # for y1 in range(0,h,50):
    #     x1=ow+1
    #     while get_rgba(value=pg1.get(x1,y1)) != (0,0,0,255) and ((ow<x1<w-ow) and (oh<y1<h-oh)):
    #         print(get_rgba(value=pg1.get(x1,y1)))
    #         point(x1,y1)
    #         x1+=1

    # ezel_inv(w=w,ow=ow,h=h,oh=oh)
    
    ezel(top=oh,sides=ow)
    
    # filename= ''.join('boxes'+timestamp+'.jpg')
    # save(filename)
    print("End of Program")
    # exit()
    
