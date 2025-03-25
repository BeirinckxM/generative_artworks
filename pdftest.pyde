add_library('pdf')

import datetime
import random as rd

w=150
h=180
ow=oh=10

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

colsel=[rd.choice(color_list) for i in range(10)]

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename= ''.join('bolpack'+timestamp+'.pdf')

def setup():
    size(w,h,PDF,filename)
    #size(w,h)
    cback=color(245,236,213)
    background(cback)
    noLoop()

def draw():
    
    # Flow matrix of angles
    def calc_flow_matrix(rstep,nstep=0.0005):
        xoff=0
        arra=list()
        for ix in range(0,w,rstep):
            yoff=0
            xoff+=nstep
            cols=list()
            for jy in range(0,h,rstep):
                yoff+=nstep
                noise_val=noise(xoff,yoff)
                angle = map(noise_val, 0.0, 1.0, 0.0, 360)
                cols.append(angle)
            arra.append(cols)
        
        return arra

    # Beams to draw on the graphics buffer
    def beam(xs,ys,hbeam,hooks,hooksize,hook_range):
        
        wbeam=(hooks*hooksize)
        
        random_list=[int(random(hook_range)) for i in range(hooks)]
    
        pg.fill(color(*rd.choice(color_list)))
        pg.beginShape()
        pg.noStroke()
        stroke(0)
    
        pg.vertex(xs,ys)
        for i,inc in enumerate(range(xs,xs+wbeam,hooksize)):
            pg.curveVertex(inc,ys-random_list[i-1])
        #curveVertex(xs+wbeam,ys)
        pg.curveVertex(xs+wbeam,ys)
    
        pg.vertex(xs+wbeam,ys)
        pg.vertex(xs+wbeam,ys)
        
        #curveVertex(xs+wbeam,ys+hbeam)
        pg.curveVertex(xs+wbeam,ys+hbeam)
        for i,inc in enumerate(range(xs+wbeam,xs,-hooksize)):
            pg.curveVertex(inc,ys+hbeam-random_list[len(random_list)-(i+1)])
        pg.curveVertex(xs,ys+hbeam)
        #curveVertex(xs,ys+hbeam)
        pg.vertex(xs,ys+hbeam)
        pg.vertex(xs,ys)
        pg.endShape()
   
    pg=createGraphics(w,h)
    pg.beginDraw() 
    pg.background(245)
    pg.stroke(random(100))
    
    for y in range(h):
        for x in range(w):
            pg.point(int(random(w)),y)   
            
    for pi in range(int(random(5, 20))): 
        #alpha(int(random(50)))
        beam(xs=int(random(-w/2,w)),ys=int(random(0,h)),
             hbeam=int(random(120,900)),hooks=int(random(30)),
             hooksize=int(random(50,300)),hook_range=int(random(200)))
    pg.endDraw()
    
    pg.loadPixels()
    
    gridw = gridh = 20
    
    cell_width = float(w)/gridw
    cell_height = float(w)/gridh
    
    def get_grid_position(x, y):
        return x/cell_width + y/cell_height * gridw 

     
    def circle_pack(n,protect=1000,rstart=14,rdelta=1,rmin=8):
        circles=list()
        
        protection=0
        
        while len(circles) < n:
            new_circle=(int(random(w)),int(random(h)),rstart)
            
            grid_position = int(get_grid_position(new_circle[0],new_circle[1]))
            
            overlapping=False
            print(rstart)
            
            for j in range(len(circles)):
                other = circles[j]
                d = dist(new_circle[0],new_circle[1], other[0], other[1])
                if d < (new_circle[2]+other[2])/2:
                    protection+=1
                    overlapping=True
                    if protection in [lim for lim in range(0,protect,protect/10)]:
                        print(protection)
                        if rstart>rmin:
                            rstart-=rdelta
            
            if not overlapping:
                protection=0
                circles.append(new_circle)

            if protection==protect:
                print("Protection: limit reached")
                break
                    
        for cd in range(len(circles)):
            #fill(pg.pixels[circles[cd][0]+circles[cd][1]*width])
            x=circles[cd][0]
            y=circles[cd][1]
            rr=circles[cd][2]
            
            c=color(pg.pixels[x+y*width])
            angle=mat1[int(x/r)-1][int(y/r)-1]
            pushMatrix()
            translate(x,y)
            rotate(radians(angle)) 
            noStroke()
            swing=int(random(4,10))
            a = (c >> 24) & 0xFF
            re = (c >> 16) & 0xFF 
            gr = (c >> 8) & 0xFF   
            bl = c & 0xFF          
            fill(int(random(re-swing,re+swing)), int(random(gr-swing,gr+swing)), int(random(bl-swing,bl+swing)), a)
            arc(0,0,rr,rr,0,PI)
            fill(int(random(re-swing,re+swing)), int(random(gr-swing,gr+swing)), int(random(bl-swing,bl+swing)), int(random(70)))
            #fill(color(255,255,255))
            arc(0,0,rr,rr,PI,2*PI)
            popMatrix()
                
    r=int(random(8,12))
    
    mat1=calc_flow_matrix(rstep=r,nstep=0.006)

    # for y in range(0,h,r):
    #     for x in range(0,w,r):
    #         c=color(pg.pixels[x+y*width])
    #         angle=mat1[int(x/r)-1][int(y/r)-1]
    #         pushMatrix()
    #         translate(x,y)
    #         if ang > 0.5:
    #             rotate(radians(angle)) 
    #         else:
    #             rotate(radians(random(360)))
    #         noStroke()
    #         #stroke(100)
    #         swing=int(random(4,10))
    #         a = (c >> 24) & 0xFF
    #         re = (c >> 16) & 0xFF 
    #         gr = (c >> 8) & 0xFF   
    #         bl = c & 0xFF          
    #         fill(int(random(re-swing,re+swing)), int(random(gr-swing,gr+swing)), int(random(bl-swing,bl+swing)), a)
    #         arc(0,0,r,r,0,PI)
    #         fill(int(random(re-swing,re+swing)), int(random(gr-swing,gr+swing)), int(random(bl-swing,bl+swing)), int(random(70)))
    #         #fill(color(255,255,255))
    #         arc(0,0,r,r,PI,2*PI)
    #         popMatrix()
    
    circle_pack(n=20000,protect=500)
    
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
    exit()
