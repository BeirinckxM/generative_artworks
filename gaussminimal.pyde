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
filename= ''.join('gaussminimal'+timestamp+'.pdf')

def setup():
    size(w,h,PDF,filename)
    #size(w,h)
    noLoop()
    background(245,240,238)
    
def draw():
    
    cellw=int(w/10)
    cellh=int(h/9)

    def calc_flow_matrix(wee,haa,rstep,nstep=0.0005):
        xoff=0
        arra=list()
        for ix in range(0,wee,rstep):
            yoff=0
            xoff+=nstep
            cols=list()
            for jy in range(0,haa,rstep):
                yoff+=nstep
                noise_val=noise(xoff,yoff)
                angle = map(noise_val, 0.0, 1.0, 0.0, 360)
                cols.append(angle)
            arra.append(cols)
        
        return arra
    
    def circle_pack(n,protect=1000,rstart=cellw*int(random(4)),rdelta=20,rmin=50):
        circles=list()
        
        protection=0
        
        while len(circles) < n:
            new_circle=(int(random(w)),int(random(h)),rstart)
            
            overlapping=False
            #print(rstart)
            
            for j in range(len(circles)):
                other = circles[j]
                d = dist(new_circle[0],new_circle[1], other[0], other[1])
                if d < (new_circle[2]+other[2])/2:
                    protection+=1
                    overlapping=True
                    if protection in [lim for lim in range(0,protect,protect/10)]:
                        #print(protection,rstart)
                        if rstart>rmin:
                            rstart-=rdelta
            
            if not overlapping:
                protection=0
                circles.append(new_circle)

            if protection==protect:
                print("Protection: limit reached")
                break
                    
        for cd in range(len(circles)):
            x=circles[cd][0]
            y=circles[cd][1]
            rr=circles[cd][2]
            
            amount=rr/4 
            pushMatrix()
            translate(x,y-rr*int(random(2)))
            strw=1
            angle=random(30,100)
            switch=int(random(0,y+rr))
            switch2=int(random(0,y+rr))
            #arswiff = calc_flow_matrix(wee=rr*2, haa=rr*2, rstep=1,nstep=0.0005)
            divisor = rr/9
            _alpha=0
            for z in range(rr**int(random(4))):
                if z==1:
                    divisor*=random(1,4)
                if z > switch:
                    _alpha+=10
                    _alpha=sorted([0, _alpha, 255])[1]
                    angle +=1
                else:
                    angle -=4
                    _alpha-=5
                    _alpha=sorted([0, _alpha, 255])[1]
                    
                if z > switch2:
                    rr +=6 
                else:
                    rr -=int(random(-1,1))
                    c=rd.choice(color_list)
                for np in range(amount):
                    xg=randomGaussian()*divisor
                    yg=tan(radians(sorted([-180, angle, 360])[1]))*xg+z
                    stroke(color(c[0],c[1],c[2],_alpha+random(-50,50)))
                    if (.55 < rd.uniform(0,1) < .57):
                        strokeWeight(strw*random(5))
                    else:
                        strokeWeight(strw)
                    point(xg,yg)
            popMatrix()
    
    circle_pack(n=20,protect=1000)
        
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
