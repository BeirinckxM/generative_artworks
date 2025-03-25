add_library('pdf')
import datetime
import time
import random as rd
# from collections import Counter

resolution=15
ow=oh=resolution
w=ow+resolution*50-ow
h=oh+resolution*58-oh

print("Canvas Size:", w,h,w*h)

all_col    =[[241, 78, 27],
            [8, 63, 88],
]  

background_col=(239,234,212)

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

square_size=resolution*20

print(square_size*square_size)

def setup():
    # size(w,h,PDF, ''.join('collage'+timestamp+'.pdf'))
    size(w,h)
    background(*background_col)
    noLoop()
 
    # blendMode(REPLACE)
    
    # global cg1
    # global cg2
    
    # cg1=createGraphics(square_size,square_size)
    # cg2=createGraphics(w,h)
    
def ezel_inv(w,ow,h,oh):
    noStroke()
    fill(color(*background_col))
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
    
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

def recursive_line(x,y,r,rminus,aim,spread,stem_size,branch_alpha,depth,fib):
    
    # Get points where splits happen
    if fib==False:
        # fibn=list(fib(depth))
        fibn=set([int(random(depth)) for i in range(depth/2)])
        print(fibn)
    else:
        fibn=fib
        
    # depth can not be higher than the line length left
    if depth > floor(r/rminus):
        depth = floor(r/rminus)
    
    # Where is the line drawn to?
    dangle = rd.gauss(mu=aim,sigma=20)
    destination=PVector().fromAngle(radians(dangle)).mult(rminus*(depth+1))
    destx,desty=x+destination.x , y+destination.y  
    dx,dy=destx-x,desty-y
    
    if aim:
        # print(aim)
        destination_angle=rd.gauss(mu=aim,sigma=spread)
    else:
        
        # destination_angle=int(degrees(atan2(dy,dx)))
        destination_angle=int(rd.gauss(mu=270,sigma=spread*1.5))
        
    # direction_angle=rd.gauss(mu=destination_angle,sigma=spread)
    target=PVector().fromAngle(radians(destination_angle)).mult(r)
    newx,newy=int(x+target.x),int(y+target.y)
    strokeWeight(max(stem_size,0))
    # stroke(color(stem_size*40,stem_size*20,stem_size*50))
    stroke(color(178,140,83,branch_alpha))
    line(x,y,newx,newy)
    
    if depth==0:
        if rd.uniform(0,1) > .2:
            fill(color(random(40,80),random(80,140),random(30,60)))
        else:
            fill(color(random(230,255),random(230,255),random(230,255)))
        noStroke()
        circle(newx,newy,int(resolution/5))
        
    if depth > 0 and r>0:
        r-=rminus
        # if (depth in fibn) or (depth in (18,20,16)):
        if (depth in (fibn)):
            branches=int(random(2,4))
            # stem_size-=1
            for i,branch in enumerate(range(branches)):
                if i==0:
                    aim=destination_angle
                else:
                    stem_size-=1
                    branch_alpha=max(70,branch_alpha-depth)
                    aim=False
                
                recursive_line(newx,newy,r,rminus,aim,spread,stem_size,branch_alpha,depth=depth-1,fib=fibn)
            noStroke()
            fill(color(255,0,0))
            # circle(newx,newy,5)
        else:
            fill(color(255,255,255))
            noStroke()
            # circle(newx,newy,5)
            aim=destination_angle
            recursive_line(newx,newy,r,rminus,aim,spread,stem_size,branch_alpha,depth=depth-1,fib=fibn)
    
    

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################   
         
def draw():
   

    # stroke(0)  
    # _split=int((w-2*ow)/2)
    # for x in range(0,w,_split):
    #     for y in range(0,h,_split):  
    #         xp=x+int(_split/2)
    #         yp=y+int(_split/2)        
    #         recursive_line(x=xp,y=yp,r=int(resolution),rminus=2,aim=270
    #                   ,spread=25,stem_size=6,depth=8,fib=False,branch_alpha=255)
    
    # list_of_sprouts = [int(random(w)) for i in range(4)]
    list_of_sprouts = [int(w/2)]
    for p in list_of_sprouts:        
        recursive_line(x=p,y=h,r=int(resolution*4),rminus=2,aim=270
                      ,spread=20,stem_size=8,depth=18,fib=False,branch_alpha=255)
            
    ezel_inv(w=w,ow=ow,h=h,oh=oh)
    ezel(top=oh,sides=ow)

    filename= ''.join('tree'+timestamp+'.jpg')
    # save(filename)
    print("End of Program")
    # exit()
    
    
    
