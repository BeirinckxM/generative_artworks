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
    
    def rotating_ellipse(x,y,angle):
        pushMatrix()
        translate(w/2,h/2)
        rotate(radians(angle))
        noFill()
        ellipse(x,y,100,200)
        popMatrix()
   
    angle=0
    x=0
    y=0
    for i in range(90):
        rotating_ellipse(x,y,angle)
        angle+=1
        print(x,y)
        
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
    
