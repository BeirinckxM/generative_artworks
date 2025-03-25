add_library('pdf')
import datetime
import random as rd
import itertools

scaler=1
resolution=10
ow=oh=resolution*3*scaler
w=resolution*50*scaler
h=resolution*80*scaler

all_col    =[[198,26,26],
            [24,134,168],
            [141,175,155],
            [238,223,96],
            [238,119,0],
            [171,169,153],
            [244,92,86],
            [203,226,201],
            [253,235,131],
            [255,200,200],
            [41, 121, 222],
            [254, 242, 169],
            [170, 215, 211],
            [225, 60, 15],
            [207, 42, 41],
            [79, 145, 223],
            [226, 238, 225],
            [40, 133, 147],
            [136, 180, 168],
            [254, 252, 247],
            [14, 105, 109],
            [251, 60, 13],
            [235, 244, 188],
            [91, 191, 84],
            [182, 44, 53],
            [246, 172, 135],
            [231, 232, 224],
            [56, 165, 197],
            [250, 128, 13],
            [250, 89, 74],
            [250, 247, 125],
            [253, 234, 79],
            [230, 247, 248],
            [234, 221, 30],
            [218, 134, 115],
            [245, 242, 231],
            [137, 200, 122],
            [0,0, 0]        
]  

background_col=(245,240,219)

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def setup():
    # size(w,h,PDF, ''.join('fuzzy_circle'+timestamp+'.pdf'))
    size(w,h)
    background(*background_col)
    noLoop()
    blendMode(REPLACE)

def draw():

    print("Starting")

    x=w/2
    y=h/2
    circle(x,y,10)
    yoff=0
    for y in range(int(random(h))):
        angle=noise(yoff)*360
        #print(angle)
        r=50
        stroke(0)
        noFill()
        circle(x,y,10)
        xt=x+cos(radians(angle))*r
        yt=y+sin(radians(angle))*r
        #line(x,y,xt,yt)
        circle(xt,yt,10)
        if rd.uniform(0,1) > .9:
            for a in range(int(angle-90), int(angle+90)):
                xt=x+cos(radians(a))*r
                yt=y+sin(radians(a))*r
                stroke(color(255,0,0))
                point(xt,yt)
            
        yoff+=0.01
    
    filename= ''.join('twomblyesk'+timestamp+'.jpg')
    # save(filename)
    print("End of Program")
    # exit()
    
