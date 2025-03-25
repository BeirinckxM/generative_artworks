import datetime
import random as rd

w =2000
h =2400
ow = 80
oh = 80

color_list=[[191,0,13],
            [246,246,196],
            [233,112,69],
            [46,88,141],
            [0,0,0]]

color_list2=[[34,137,216,255],
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
    background(color(255))
    noLoop()
    #blendMode(DIFFERENCE);
    

def draw():
    
    def ezel_inv(w,ow,h,oh):
        noStroke()
        fill(255)
        rect(0,0,w,oh)
        rect(0,0,ow,h)
        rect(0,h-oh,w,oh)
        rect(w-ow,0,ow,h)
    
    def calc_flow_matrix():
        xoff=0
        arr=list()
        for ix in range(ow,w-ow):
            yoff=0
            xoff+=0.0005
            cols=list()
            for jy in range(oh,h-oh):
                yoff+=0.0005
                noise_val=noise(xoff,yoff)
                angle = map(noise_val, 0.0, 1.0, 0.0, 180)
                cols.append(angle)
            arr.append(cols)
        
        return arr
    
    # def calc_range(min_=50,it=0):
    #     lw=int(random(ow,w-ow))
    #     if (lw+min_) > (w-ow):
    #         hi=int(random(lw+min_,w-ow))
    #         return lw,hi
    #     else:
    #         return ow,w
             
    mat=calc_flow_matrix()
    cl2=rd.choice(color_list2)
    #for y in range(oh,h,4):
    #    strokeWeight(2)
    #    stroke(color(cl2[0],cl2[1],cl2[2]))
        #line(ow,y,w-ow,y)
            
    
    def squiggly(startx,starty,jump,turn,right,it,linesize=10):
        x=startx
        y=starty
        #print(x,y)
        if right:
            luni=sorted([rd.uniform(0,1) for i in range(2)])
            xoff=0
            while (ow+turn)<x<(w-(ow+turn)) and (oh+turn)<y<(h-(oh+turn)):
                n=noise(xoff)*linesize
                strokeWeight(1)
                if it==5:
                    break
                    print("THE END")
                #print(x,y)
                cf=rd.uniform(0,1)
                if cf<luni[0]:
                    x=x+jump
                    y=y+jump
                    angle=mat[x-ow][y-oh]
                    if bool:
                        line(x+jump,y+jump,x+cos(radians(angle))*linesize,y+sin(radians(angle))*linesize)
                    else:
                        line(x+jump,y+jump,w-ow,y-sin(radians(angle))*linesize)
                elif cf>luni[1]:
                    x=x+jump
                    y=y
                    angle=mat[x-ow][y-oh]
                    #line(x+jump,y-jump,x+jump+n,y-jump-linesize)
                    if rd.uniform(0,1)>luni[1]:
                        line(x+jump,y-jump,x+cos(radians(angle))*linesize+n,y+sin(radians(angle))*linesize)
                    else:
                        line(x+jump,y-jump,x+cos(radians(angle))*linesize+n,y-sin(radians(angle))*linesize)
                else:
                    x=x+jump
                    y=y-jump
                    angle=mat[x-ow][y-oh]
                    if bool:
                        line(x+jump,y-jump,x+cos(radians(angle))*linesize+n,y+sin(radians(angle))*linesize)
                    else:
                        line(ow,y-jump,x+jump,y-sin(radians(angle))*linesize)
                    #point(x+jump,y)
                xoff+=0.02
            else:
                if (oh+turn)<y<(h-(oh+turn)):
                    jump=-(jump)
                    it+=1
                    squiggly(x+jump,y+jump,jump=jump,turn=10,right=True,it=it,linesize=liness)
            #endShape()
    
    for s in range(10):
        #cs=[int(random(255)) for i in range(4)]
        cl=rd.choice(color_list)
        print(cl)
        stroke(color(cl[0],cl[1],cl[2],int(random(255))))
        jump=1
        x=int(random(ow+jump+1,w-ow-jump-1))
        y=int(random(oh+jump+1,h-oh-jump-1))
        liness=random(50)
        bool=(rd.uniform(0,1)>.5)
        print(bool)
        squiggly(x,y,jump=jump,turn=10,right=True,it=0,linesize=liness)  
        
        
    ezel_inv(w=w,ow=ow,h=h,oh=oh)
    
    filename= ''.join('rw'+timestamp+'.jpg')

    save(filename)
