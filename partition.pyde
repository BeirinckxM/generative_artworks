import datetime
import random as rd

w=2200
h=1800
ow=80
oh=80

resolution=10

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
            [133,175,154,255]]

color_list2=[[233,130,49],
             [87,138,206],[133,185,206],
             [180,206,172],[206,121,117],[233,219,138]]

colsel=[rd.choice(color_list2)[:3]+[int(random(0,100))] for i in range(5)]
#colsel=color_list2
print(colsel)

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def setup():
    size(w,h)
    noLoop()
    background(255)
    
def draw():
    
    def calc_flow_matrix(rstep,nstep=0.007):
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
    
    def plume(startx,starty,stroke_length,pressure,amount,no,de):
        for i in range(stroke_length):
            lift=(i>(no * stroke_length/de))
            for j in range(int(amount)):
                x = round(randomGaussian() * (i*pressure))
                point(startx+x,starty+i)
            if lift:
                pressure-=(pressure/(stroke_length-i))     
   
            
    mat1=calc_flow_matrix(rstep=resolution)
    print(len(mat1[0]), len(mat1))
        
    for y in range(0,h,resolution):
        for i in range(0,w,resolution):
            chance=(rd.uniform(0,1)>.5)
            strokeWeight(1)
            stroke(color(*rd.choice(colsel)))
            pushMatrix()
            translate(i,y)
            angle=mat1[int(i/resolution)-1][int(y/resolution)-1]
            rotate(radians(angle))
            if chance:
                plume(0,0,stroke_length=int(100),pressure=random(.3,.4),amount=20,no=random(7),de=random(10))
            #line(0,0,0,y+200)
            popMatrix()
            
            if not chance:
                beginShape()
                #fill(color(*rd.choice(colsel)))
                noFill()
                y1=int(random(h))
                x1=int(random(w))
                y2=y1
                x2=x1
                for i in range(20):
                    step_length=resolution
                    pushMatrix()
                    translate(x2,y2)
                    strokeWeight(3)
                    stroke(color(*rd.choice(color_list)))
                    angle=mat1[int(x2/resolution)-1][int(y2/resolution)-1]
                        #rotate(radians(angle))
                    target=PVector().fromAngle(angle).mult(resolution)
                    curveVertex(x2,y2)
                    x2=constrain(x2+target.x,0,w)
                    y2=constrain(y2+target.y,0,h)
                    popMatrix()
                    #point(x,y)
                endShape()
            
    def ezel_inv(w,ow,h,oh):
        noStroke()
        fill(255)
        rect(0,0,w,oh)
        rect(0,0,ow,h)
        rect(0,h-oh,w,oh)
        rect(w-ow,0,ow,h)
    
    ezel_inv(w,ow,h,oh)
            
    filename= ''.join('bloom'+timestamp+'.jpg')

    save(filename)
