import datetime
import random as rd

w =1000
h =800
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

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def setup():
    size(w,h)
    background(color(255,248,241))
    noLoop()
    #img = loadImage("IMG_20211118_211047.jpg");
    #img = loadImage("IMG_20211118_211103.jpg");
    #image(img, 0, 0);
    blendMode(DIFFERENCE);

def draw():
    #img = loadImage("IMG_20211118_211047.jpg");
    img = loadImage("IMG_20211118_211103.jpg");
    image(img, 0, 0);
    
    # def draw_circle(xcenter,ycenter, r,interval):
    #     stroke(0)
    #     strokeWeight(6)
    #     rd=random(20)
    #     print(rd)
    #     points_list=[(xcenter + sin(radians(d))*r,ycenter + cos(radians(d))*r+random(20)) for d in range(0,360,interval)]
    #     points_list=points_list+points_list[0:3]      
    #     beginShape()
    #     for x,y in points_list:
    #         curveVertex(int(x),int(y))
    #     endShape()
    
    # #draw_circle(w/2,h/2,50)         

    # for i in range(ow,w,40):
    #     for y in range(oh,h,40):
    #         c=rd.choice(color_list)
    #         fill(color(c[0],c[1],c[2]))
    #         draw_circle(i,y,random(10,40),interval=int(random(5,30)+1)) 
                        
    # cells=50
    # cell_countx=w/cells
    # cell_county=h/cells
    
    # xoff=0
    # step=0.1
    # r=10
    # for x in range(0,w,cell_countx):
    #     yoff=0
    #     for y in range(0,h,cell_county):
    #         n=noise(xoff,yoff)
    #         c=255*n
    #         fill(c)
    #         #circle(x,y,r)
    #         yoff+=step
    #     xoff+=step

    # def draw_circle(xcenter,ycenter, r,interval):
    #     stroke(0)
    #     strokeWeight(6)
    #     xpoints_list=[xcenter + sin(radians(d))*r for d in range(0,360,interval)]
    #     ypoints_list=[ycenter + cos(radians(d))*r for d in range(0,360,interval)]
    #     factors=[random(1,2) for i in range(len(xpoints_list))]
    #     ypoints_list=[a*b for a,b in zip(ypoints_list,factors)]
    #     points_list=zip(xpoints_list,sorted(ypoints_list))
    #     points_list=points_list+points_list[0:3]    
    #     beginShape()
    #     for x,y in points_list:
    #         curveVertex(int(x),int(y))
    #     endShape()
        
    # draw_circle(w/2,h/2,r=20,interval=15)
    
    def draw_circle(xc,yc,r,co=rd.choice(color_list)):
        a,b,c,d=co
        add_=add2_=0
        point_list=list()
        xoff=yoff=0
        rlist=[int(random(1,10)) for i in range(2)]
        for d in range(int(random(1000,10000))):
            if d%rlist[0]==0:
                add_+=1
            if d%rlist[1]==0:
                add2_+=2
                yoff+=0.002
            x=xc + sin(radians(d))*(r+add_)
            y=yc + cos(radians(d))*(r-(r-add2_)/r)
            strokeWeight(3)
            if d%2==0:
                n=noise(xoff,yoff)
                stroke(color(int((a*n)),int((b*n)),int((c*n))))
                point(x,y)
                xoff+=0.02
    
    xoff=yoff=0
    for i in range(oh,h,int(random(2,10))):
        n3=noise(xoff)*(w-ow)
        draw_circle(xc=n3,yc=i,r=random(20))
        xoff+=0.2
        yoff+=0.03
        
    def plume(startx,starty,stroke_length,pressure,amount):
        for i in range(stroke_length):
            lift=(i>(stroke_length/random(1,8)))
            for j in range(int(amount)):
                x = round(randomGaussian() * (i*pressure))
                point(startx+x,starty+i)
            if lift:
                pressure-=(pressure/(stroke_length-i))     
        # line(0,starty,w,starty)
        # line(0,starty+stroke_length,w,starty+stroke_length)    
   
    for jj in range(int(random(1,1))):
        for strokes in range(int(random(50,200))):
            xs = random(40,w-40)+round(randomGaussian() * random(20,40))
            a,b,c,d=rd.choice(color_list)
            stroke(color(a,b,c,d))
            
            plume(startx=xs,
                starty=random(-40,h-40), 
                stroke_length=int(random(300,700)), 
                pressure=random(0,1), 
                amount=int(random(10,80)))
            
    def ezel(top,sides,c=255):
        stroke(0)
        line(sides,top,w-sides+2,top)
        line(w-sides+2,top,w-sides+2,h-top+2)
        line(w-sides+1,h-top+2,sides,h-top+2)
        line(sides,h-top+2,sides,top)
        
    #ezel(41,41)
    filter(BLUR, 2);
    
    filename= ''.join('bollekes'+timestamp+'.jpg')

    save(filename)
