  # add_library('pdf')
import datetime
import random as rd
import itertools

scaler=3
resolution=10
ow=oh=resolution
w=resolution*90
h=resolution*100

print(w,h)

all_col    =[
            #  [255,142,106,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
            [245,240,219,255],
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
            # [248,208,135,255],
            # [0,0,0,255],
            # [191,41,0,255],
            [246,249,211,255],
            [67,136,249,255],
            [232,221,200,255],
            # [222,228,229,255],
            # [129,20,14,255],
            # [11,82,2,255],
            # [133,175,154,255],
            #  [183,39,47 ,255],
            [214,200,132,255],
            [180,91,38,255],
            # [33,140,218,255],
            [219,115,19,255],
            [103,102,58,255],
            [44,81,21,255],
            [43,95,128,255],
            [190,61,44,255],
            [144,166,112,255],
            [140,204,248,255],
            [248,190,181,255],
            [248,208,135,255],
            [0,0,0,255],
            # [191,41,0,255],
            # [246,249,211,255],
            # [151,165,176,255],
            # [103,135,30,255],
            # [25,122,199,255],
            # [0,0,0,255],
            # [239,199,77,255],
            # [240,240,240,255],
            [226, 145, 37,255]
            ]

# all_col = rd.sample(all_col,7)

background_col=(245,240,219)

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def setup():
    # size(w,h,PDF, ''.join('expand_test'+timestamp+'.pdf'))
    size(w,h)
    background(*background_col)
    noLoop()
    # blendMode(DARKEST)
    
def add_midpoint(p1, p2, anchor, depth, expand_scale):
    p1x,p1y=p1[0], p1[1]
    p2x,p2y=p2[0], p2[1]
    
    center = floor(p1x+(p2x-p1x)/2), floor(p1y+(p2y-p1y)/2)
    length_fragment=dist(p1x,p1y,p2x,p2y)/2
    if length_fragment>1:
        atan_3=atan2(center[1]-anchor[1],center[0]-anchor[0])
        expand_angle=rd.gauss(mu=degrees(atan_3),sigma=10)
    
        target=PVector().fromAngle(radians(expand_angle)).mult(length_fragment*random(expand_scale))
        newpx=int(center[0]+target.x)
        newpy=int(center[1]+target.y)
            
        return ((newpx, newpy, center), p2)
    else:
        # print(length_fragment,p2)
        # print("p2:", p2)
        return (p1, p2)

def expand(list_of_points,reference,expand_scale,depth=1):
    
    if depth==0:
        return list_of_points
    
    start=(list_of_points[0][0],list_of_points[0][1])
    extender=[start]
    
    # print("in expand:", list_of_points)
    
    for i in range(0,len(list_of_points[1:]),1):
        # print(i)
        p1=list_of_points[i]
        p2=list_of_points[i+1]
        try:
            anchor=list_of_points[i][2]
        except IndexError:
            anchor=reference
        # print("points:", p1,p2)
        extender.extend(add_midpoint(p1=p1,p2=p2, anchor=anchor, depth=depth, expand_scale=expand_scale))
        # print("Extender: ", extender)
    
    return expand(list_of_points=extender
              , reference=reference
              , expand_scale=expand_scale
              , depth=depth-1)

def polygon_points(x,y,n,r,a,boomfactor):
    interval=floor(360/n)
    points=[]
    xoff=yoff=0
    for p in range(0+a,360+a,interval):
        xnoise=map(xoff,0,1,boomfactor[0],boomfactor[0]+1)
        ynoise=map(yoff,0,1,boomfactor[1],boomfactor[1]+1)
        xp=x+cos(radians(p))*r*xnoise
        yp=y+sin(radians(p))*r*ynoise
        points.append((int(xp),int(yp)))
        xoff+=0.01
        yoff+=0.01
    
    first_point=points[0]
    points.append(first_point)
    
    return points    

def generate_points(type="random",loc=(w/2,h/2), n=4, bbox=(100,100)):
    if type=="random":
        rangex=(loc[0],loc[0]+bbox[0])
        rangey=(loc[1],loc[1]+bbox[1])
        points=[(int(random(*rangex)),int(random(*rangey))) for p in range(n)]
        
    if type=="rect":
        x1,y1=loc
        x2,y2=loc[0]+bbox[0],loc[1]
        x3,y3=loc[0]+bbox[0],loc[1]+bbox[1]
        x4,y4=loc[0],loc[1]+bbox[1]
        points=[(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
        
    meanx=sum([p[0] for p in points])/len(points)
    meany=sum([p[1] for p in points])/len(points)
    points.append(points[0])
    ref=(meanx,meany)
    
    return points,ref

def lerp_shape2mean(list_of_points,mean,iters):
    new_list=[]
    for p in list_of_points:
        distance=dist(p[0],p[1],mean[0],mean[1])
        lerps=int(distance/iters[0])
        if lerps>0:
            step=iters[1]*lerps/float(distance)
            x = lerp(p[0],mean[0],step)
            y = lerp(p[1],mean[1],step)
            #print(x,y)
            new_list.append((int(x),int(y)))
        else:
            new_list.append(p)
            
    return new_list

def fill_polygon(list_of_points):
    beginShape()
    for p in list_of_points:
        noStroke()
        vertex(p[0],p[1])
    endShape(CLOSE)
    
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

def draw():
    print("Started code execution" )
    
    
    xt,yt=w/2-200,h/2-200
    # print(xt,yt)
    xiter=50
    yiter=50
    
    
    # for n in range(7):
    xoff=0
    for x in range(0,w,xiter):
        yoff=0
        xoff+=0.2
        for y in range(0,h,yiter):
            yoff+=0.1
            noise_val=noise(xoff,yoff)
            angle = map(noise_val, 0.0, 1.0, 0.0, 360)
        # for hh in range(30):
            spanner=10
            # print(x,y)
            # noFill()
            # stroke(0)
            # rect(x,y,xiter,yiter)
            # bbox_x,bbox_y=(int(xiter),int(xiter)),(int(yiter),int(yiter/2))
            # print(bbox_x,bbox_y)
            xt,yt=x,y
            # xt,yt=x,y
            iters=1
            rt=20
            # rt=1
            # ps,ref=random_points(loc=(xt,yt),n=10,bbox=(resolution*random(10,20),resolution*random(10,20)))
            pushMatrix()
            translate(xt,yt)
            rotate(radians(angle))
            ps,ref=generate_points(type="rect",loc=(int(spanner/2),(spanner/2)),n=10,bbox=(xiter-spanner,yiter-spanner))
            # print(ps)
            fill(255,255,0)
            # fill_polygon(ps)
            fill(255,0,0)
            # circle(ref[0],ref[1],5)
            # r,g,b,a=random(10,50),0,0,10
            r,g,b,a=rd.choice(all_col)
            r+=int(random(-8,8))
            g+=int(random(-8,8))
            b+=int(random(-8,8))
            a=20
            fill(color(r,g,b,a))
            
            for bib in range(rt):
            
                t2=lerp_shape2mean(list_of_points=ps
                                ,mean=ref
                                ,iters=(rt,bib))
                
                for c in range(iters):
                    
                    t=expand(list_of_points=t2
                    ,reference=ref
                    ,expand_scale=0.3
                    ,depth=6)
        
                    # if rd.uniform(0,1)>0.5:
                    #     stroke(color(r,g,b,a))
                    # else:
                    #     noStroke()
                    beginShape()
                    for pt in t:
                        # print("pt:", pt)
                        # noFill()
                        noStroke()
                        # circle(pt[0],pt[1],5)
                        fill(color(r,g,b,a))
                        # stroke(255)
                        # stroke(color(r,g,b,a))
                        vertex(pt[0],pt[1]) 
                        # stroke(color(255,255,255))
                        # if len(pt)>2:
                        # # stroke(0)
                        #     line(pt[0],pt[1],pt[2][0],pt[2][1])
                    endShape(CLOSE)
            popMatrix()
    
    ezel_inv(w=w,ow=ow,h=h,oh=oh)
    ezel(top=oh,sides=ow)
    
    filename= ''.join('drops'+timestamp+'.jpg')
    print("End of Program")
    # save(filename)
    # exit()
    
    
