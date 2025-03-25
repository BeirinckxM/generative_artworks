add_library('pdf')

import datetime
import random as rd

w = 1200
h = 1400
ow = 0
oh = 0

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename = ''.join('lineswitch' + timestamp + '.pdf')

cback = color(245,245,245)

def setup():
    size(w, h, PDF, filename)
    #size(w, h)
    background(cback)
    noLoop()

def draw():

    def calc_flow_matrix(wee, haa, rstep, nstep=0.0005, value=(0, 360)):
        xoff = 0
        arra = list()
        for ix in range(0, wee, rstep):
            yoff = 0
            xoff += nstep
            cols = list()
            for jy in range(0, haa, rstep):
                yoff += nstep
                noise_val = noise(xoff, yoff)
                angle = map(noise_val, 0.0, 1.0, value[0], value[1])
                cols.append(angle)
            arra.append(cols)

        return arra
    
    reso=200
    spawnfield = calc_flow_matrix(wee=w, haa=h,
                                  rstep=reso, nstep=0.0005, 
                                  value=(0, 1))
    maxp=40
    
    duos=list()
    for xfield in range(0,w,reso):
        for yfield in range(0,h,reso):
            pushMatrix()
            translate(xfield,yfield)
            allpoints=[(int(x),int(y)) for x in range(reso) for y in range(reso)]
            np=1+int(spawnfield[xfield/reso][yfield/reso] * maxp)
            samples=rd.sample(allpoints,np)
            duos.append((xfield,yfield,samples[0]))
            #print(xfield)
            for p in set(samples):
                stroke(color(0,0,0,100))
                strokeWeight(1)
                x=p[0]
                y=p[1]
                line(x,y,x,y+int(random(30,60)))
            popMatrix()
            if len(duos)>0:
                xs=xfield-reso+duos[xfield/reso-1][2][0]
                ys=yfield-reso+duos[xfield/reso-1][2][1]
                xe=xfield+duos[xfield/reso][2][0]
                ye=yfield+duos[xfield/reso][2][1]
                line(xs,ys,xe,ye)


    def ezel_inv(w, ow, h, oh):
        noStroke()
        fill(cback)
        rect(0, 0, w, oh)
        rect(0, 0, ow, h)
        rect(0, h - oh, w, oh)
        rect(w - ow, 0, ow, h)

    def ezel(top, sides, c=cback):
        stroke(0)
        strokeWeight(5)
        line(sides, top, w - sides, top)
        line(w - sides, top, w - sides, h - top)
        line(w - sides, h - top, sides, h - top)
        line(sides, h - top, sides, top)

    ezel_inv(w=w, ow=ow, h=h, oh=oh)

    ezel(top=oh, sides=ow)

    print("End of Program")
    exit()
