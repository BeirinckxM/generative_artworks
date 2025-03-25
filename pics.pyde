#add_library('pdf')

w=1000
h=865
ow=oh=70

import datetime
import random as rd

color_list=[
            ]

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename= ''.join('pics'+timestamp+'.jpg')

def setup():
    size(w,h)
    noLoop()
    background(245,240,238)
    
def draw():
    #1644336588712
    #adk
    #Unknown.jpeg
    #_DSC5568
    # photoa=loadImage("A.jpeg")
    # photob=loadImage("B.jpeg")
    # photoc=loadImage("C.jpeg")
    # #photod=loadImage("D.jpeg")
    nblocks=100
    # ncurves=5
    # mainImage = createGraphics(1000,865)
    # mainImage.beginDraw()
    # image(photob, 0, 0)
    # for i in range(nblocks):
    #     photo=rd.choice([photoa, photob, photoc])
    #     maskImage = createGraphics(1000,865)
    #     maskImage.beginDraw()
    #     maskImage.beginShape()
    #     coinf=rd.uniform(0,1)
    #     if coinf >.5:
    #         for j in range(ncurves):
    #             maskImage.curveVertex(rd.randint(0,w),rd.randint(0,h))
    #     # elif coinf > .50:
    #     #     maskImage.ellipse(rd.randint(0,w), rd.randint(0,h), rd.randint(0,w),rd.randint(0,h))
    #     elif coinf > .0: 
    #         maskImage.rect(rd.randint(0,w), rd.randint(0,h), rd.randint(0,w),rd.randint(0,h))
    #     else:
    #         pass
        
    #     maskImage.endShape(CLOSE)
    #     maskImage.endDraw()
    #     photo.mask(maskImage)
    #     mainImage.image(photo, 0, 0)
    # mainImage.endDraw()
    
    #image(mainImage,0,0)
    
    pttest1=loadImage("gy2.jpg")
    pttest=loadImage("j.jpg")
    image(pttest,0,0)
    
    for i in range(0,nblocks):
        xr=rd.randint(0,w)
        yr=rd.randint(0,h)
        block=rd.randint(50,300)
        photo=rd.choice([pttest])

        if rd.uniform(0,1)>.5:
            #copy(photo1,i,j,block,block,i,j,block,block)
            pass
        else:
            ran=rd.randint(0,150)
            if rd.uniform(0,1)>.5:
                dir=1
            else:
                dir=0
            for z in range(0,ran,rd.randint(3,10)):
                if dir:
                    copy(photo,xr,yr,block,block,xr+z,yr,block,block)
                else:
                    copy(photo,xr,yr,block,block,xr,yr+z,block,block)
            #rect(0,0,10,10)
            #image(photo1,xr,yr)
        
        
    print("End of Program")
    save(filename)   
