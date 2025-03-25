add_library('pdf')
import datetime
import random as rd
# from collections import OrderedDict

resolution=15
ow=oh=resolution
w=ow+resolution*50+ow
h=oh+resolution*60-oh

all_col    =[[198,26,26],
            [24,134,168],
            [0,0,0],
            [0,0,0],
            [0,0,0],
            [0,0,0],
            [0,0,0],
            [0,0,0],
            [0,0,0],
            [141,175,155],
            [58, 97, 87],
            [117, 143, 170],
            [29, 19, 49],
            [9, 62, 61],
            [191, 42, 23],
            [226, 187, 63],
            [204, 212, 213]     
]  

background_col=(245,240,219)

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def setup():
    # size(w,h,PDF, ''.join('rotfan'+timestamp+'.pdf'))
    size(w,h)
    background(*background_col)
    noLoop()
    # blendMode(REPLACE)
    
    global cg1
    cg1=createGraphics(w,h)
    
def ezel_inv(w,ow,h,oh):
    noStroke()
    fill(245)
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

def get_rgba(value):
    rgba=(red(value), green(value), blue(value), alpha(value))
    
    return rgba  

def retrieve_cgo_val(pixel_object, coordinates):
    cval=get_rgba(pixel_object.pixels[coordinates[0]+coordinates[1]*width])
    return cval

def retrieve_cgo_val2(coordinates):
    cval=get_rgba(pixels[coordinates[0]+coordinates[1]*width])
    return cval
    
def rotating_gap_seeker(x,y,r):
    
    print("rotator start:", x,y)
    
    loadPixels()
    center_color=pixels[x+y*(width)]
    center_color=get_rgba(center_color)
    if center_color != (245.0, 240.0, 219.0, 255.0):
        pass
        
    pushMatrix()
    
    translate(x,y)
    # stroke(color(random(255),random(255),random(255)))
    stroke(150)
    fill(0)
    arcdict = dict()
    ongoing=0
    arcnumber=0
    range_start=0
    range_end=360
    
    iter_resolution = float(1)
    iter_angles= [float(iter_angle) / iter_resolution for iter_angle in range(int(range_end*iter_resolution+1))]
    # print(iter_angles[-1]+1)
    
    for d in iter_angles:

       xc = int(cos(radians(d))*r)
       yc = int(sin(radians(d))*r)
       # lerp_points = [] 
       if arcnumber not in arcdict.keys():
          arcdict[arcnumber]=dict()
       arcdict[arcnumber]["coord"]=(x,y)
       arcdict[arcnumber]["radius"]=r
       # print(ongoing,d)
       
       for l in range(int(r)):
           
          ratio = float(l)/float(r)
          xlerp = int(lerp(0, xc, ratio));
          ylerp = int(lerp(0, yc, ratio));
          xlook = min((x+xlerp), w-1)
          ylook = min((y+ylerp), h-1)
          c=pixels[xlook+ylook*(width)]
          c=get_rgba(c)
          
          if (c == (245.0, 240.0, 219.0, 255.0) and d < (range_end)) or d == iter_angles[-1]+1:
              
             # lerp_points.append((xlerp,ylerp))
             
             if l == int(r-1):
                # print(ongoing,d)
                if ongoing==0:
                   # print("hit", arcnumber, d)
                   arcdict[arcnumber]["start_p"]=(xlook,ylook)
                   arcdict[arcnumber]["start_a"]=radians(d)
                   # print(arcdict)
                   ongoing=1
                   
                # for p in lerp_points:
                    
                #    point(p[0],p[1])
                   
          else:
              if ongoing==1:
                arcdict[arcnumber]["end_p"]=(xlook,ylook)
                arcdict[arcnumber]["end_a"]=radians(d)
                # print("end", arcnumber, d)
                arcnumber+=1
                ongoing=0
              break
    popMatrix()
    # updatePixels()
    
    # print(arcdict)
    return arcdict

def draw_dict(arc_meta):
    
    def gaussian_fill(x,y,start_a,end_a,r, confined=1):
        
        angle_window=(degrees(end_a)-degrees(start_a))
        mu=degrees(start_a)+angle_window/2
        sigma=angle_window/3
        # print(mu,sigma)
        n=r*30*(angle_window/360)
        # stroke(0)
        stroke_color=color(*rd.choice(all_col))
        stroke(stroke_color)
        strokeWeight(0)
        pushMatrix()
        translate(x,y)
        for i in range(int(r)):
            r-=1
            for p in range(int(n)):
                gaussian_angle=rd.gauss(mu=mu,sigma=sigma)
                xc = cos(radians(gaussian_angle))*r
                yc = sin(radians(gaussian_angle))*r
                if degrees(start_a) <= gaussian_angle <= degrees(end_a):
                    point(xc,yc)
                # elif confined != 1:
                #     point(xc,yc)
                    
        popMatrix()    
    
    for k,d in arc_meta.items():
        if "start_p" in d.keys():
            centerx, centery = d["coord"]
            radius=d["radius"]
            start_angle, end_angle = d["start_a"], d["end_a"]
            # print(ax,ay,radius,asa, degrees(asa), aea, degrees(aea))
            fill(color(255,0,0))
            stroke(color(255,0,0))
            # if abs(degrees(start_angle)-degrees(end_angle)) > 20:
                # arc(centerx,centery,2*radius,2*radius,start_angle,end_angle)
            gaussian_fill(x=centerx,y=centery,start_a=start_angle,end_a=end_angle
                          ,r=radius, confined=1)
            
def partition_rectangle(x1, y1, x2, y2, depth, rect_counter=[1]):
    
    if depth == 0:
        # Generate a unique key based on the counter
        rect_key = "rect"  + str(rect_counter[0])
        rect_counter[0] += 1
        rect_width=int(abs(x2-x1))
        rect_height=int(abs(x2-x1))
        surface=rect_width*rect_height
        circle_center=(int(int(x1)+rect_width/2),int(int(y1)+rect_height/2))
        return {rect_key: [(int(x1), int(y1))
                          ,(int(x2), int(y2))
                          ,surface
                          ,rect_width
                          ,rect_height
                          ,circle_center]}
    
    # Decide randomly to split horizontally or vertically
    split_horizontally = rd.choice([True, False])
    
    # Dictionary to store rectangles
    rectangles = {}

    if split_horizontally:
        # Split horizontally by choosing a random y-coordinate between y1 and y2
        y_split = rd.uniform(y1, y2)
        # Recurse on top and bottom halves
        top_half = partition_rectangle(x1, y_split, x2, y2, depth - 1, rect_counter)
        bottom_half = partition_rectangle(x1, y1, x2, y_split, depth - 1, rect_counter)
        rectangles.update(top_half)
        rectangles.update(bottom_half)
    else:
        # Split vertically by choosing a random x-coordinate between x1 and x2
        x_split = rd.uniform(x1, x2)
        # Recurse on left and right halves
        left_half = partition_rectangle(x1, y1, x_split, y2, depth - 1, rect_counter)
        right_half = partition_rectangle(x_split, y1, x2, y2, depth - 1, rect_counter)
        rectangles.update(left_half)
        rectangles.update(right_half)
    
    return rectangles   

def connect_with_loop():
    pass

def get_gaussian_coordset(n=20,mux=w/2,muy=h*1/3,sx=w/5,sy=h/6):
    xset=[int(rd.gauss(mu=mux,sigma=sx)) for i in range(n)]
    yset=[int(rd.gauss(mu=muy,sigma=sy)) for i in range(n)]
    cset=zip(xset,yset)    
    
    mean = (sum([p[0] for p in cset])/len(cset),sum([p[1] for p in cset])/len(cset))

    return (mean, cset)  

def rectangle_overlay(x,y,rect_width,rect_height, block_size):
    if block_size == 0:
        return
    for yblock in range(0,rect_height,block_size*2):
        fill(*background_col)
        noStroke()
        rect(x,y+yblock,rect_width,block_size)

def calc_flow_matrix(w,h,rstep,nstep=0.06,max_val=360):
    xoff=random(10)
    arra=list()
    for ix in range(0,w,rstep):
        yoff=0
        cols=list()
        
        for jy in range(0,h,rstep):
            yoff+=nstep
            noise_val=noise(xoff,yoff)
            angle = map(noise_val, 0.0, 1.0, 0, max_val)
            cols.append(angle)
            
        xoff+=nstep
        arra.append(cols)
    
    return arra        

def warping_executor(field,length_line=5):
    warp_dict=dict()
    for x in range(w):
        for y in range(h):
            c=retrieve_cgo_val2(coordinates=(x,y))
            # print(c)
            if c != (245.0, 240.0, 219.0, 255.0):
                target=PVector().fromAngle(radians(field[x][y])).mult(length_line)
                warp_dict[(x,y)]=(x+target.x,y+target.y, c)
                
    return warp_dict         

def draw():

    # circle(200,200,50)
    # circle(350,280,50)
    # circle(400,500,50)
    
    meanc, cset = get_gaussian_coordset(n=int(random(7,14)))
    circle_color=color(*rd.choice(all_col))
    
    for p in cset:
        fill(circle_color)
        stroke(circle_color)
        circle(p[0],p[1],random(20,60))
    
    rectangles = partition_rectangle(ow, oh, w-ow, h-oh, int(random(3,6))) 
    print(rectangles)
    rectangles_by_size = sorted(rectangles.values(), key=lambda x: x[2])
    print(rectangles_by_size)
    
    cg1.beginDraw()
    cg1.background(255)        
    
    for k,v in rectangles.items():
        # print(v)
        xr1,yr1 = v[0]
        xr2,yr2 = v[1]
        wid,hei=int(abs(xr2-xr1)), int(abs(yr2-yr1))
        noFill()
        stroke(150)
        # noStroke()
        strokeWeight(1)
        if (wid > w/10) and (hei > h/10):
            cg1.fill(0)  
            cg1.stroke(0)               
            cg1.rect(xr1,yr1,wid,hei)
            center=(xr1+wid/2,yr1+hei/2)
            # print(center)
            r=min(wid/2,hei/2)
            arc_meta=rotating_gap_seeker(x=center[0],y=center[1],r=r)
            draw_dict(arc_meta=arc_meta)
            if rd.uniform(0,1) > 0.7:
                rectangle_overlay(x=xr1,y=yr1,rect_width=wid,rect_height=hei, block_size=int(r/20))
            
    cg1.endDraw()
    cg1.loadPixels()
    # image(cg1,0,0)
    
    stroke(circle_color)
    strokeWeight(1)
    # alpha(random(255))
    # yplacing=calc_flow_matrix(w,h,rstep=1,nstep=0.05, max_val=2)
    alpha_field=calc_flow_matrix(w,h,rstep=1,nstep=0.02, max_val=100)
    
    stroke_color=rd.choice(all_col)
    for py in range(0,h,1):
        for px in range(0,w):
            xline=px
            yline=py
            cval = retrieve_cgo_val(pixel_object=cg1, coordinates=(xline,yline))
            av=200 + rd.randint(-1,1)*int(alpha_field[xline][yline])
            if cval == (255.0,255.0,255.0,255.0):
                    # av=200 + rd.randint(-1,1)*int(alpha_field[xline][yline])
                    r,g,b=stroke_color
                    stroke(color(r,g,b,av))
                    # stroke(0)
                    point(xline,yline)
                    
    
    
    loadPixels()
    
    # updatePixels()
    
    warper=calc_flow_matrix(w=w,h=h,rstep=1,nstep=0.003,max_val=360)
    d=warping_executor(field=warper,length_line=10)
    
    print(len(d))
    
    for k,v in d.items():
        stroke(color(*background_col))
        x1,y1=k[0],k[1]
        point(x1,y1)
        # print(k, v)
        x2,y2=int(v[0]),int(v[1])
        stroke(color(*v[2]))
        point(x2,y2)
        # line(x1,y1,x2,y2)  
        
    warper=calc_flow_matrix(w=w,h=h,rstep=1,nstep=0.003,max_val=360)
    d=warping_executor(field=warper,length_line=10)
    
    print(len(d))
    
    for k,v in d.items():
        stroke(color(*background_col))
        x1,y1=k[0],k[1]
        point(x1,y1)
        # print(k, v)
        x2,y2=int(v[0]),int(v[1])
        stroke(color(*v[2]))
        point(x2,y2)
        # line(x1,y1,x2,y2)      
        
    warper=calc_flow_matrix(w=w,h=h,rstep=1,nstep=0.002,max_val=360)
    d=warping_executor(field=warper,length_line=10)
    
    print(len(d))
    
    for k,v in d.items():
        stroke(color(*background_col))
        x1,y1=k[0],k[1]
        point(x1,y1)
        # print(k, v)
        x2,y2=int(v[0]),int(v[1])
        stroke(color(*v[2]))
        point(x2,y2)
        # line(x1,y1,x2,y2)       
        
    # warper=calc_flow_matrix(w=w,h=h,rstep=1,nstep=0.06,max_val=360)
    # d=warping_executor(field=warper,length_line=20)
    
    # print(len(d))
    
    # for k,v in d.items():
    #     stroke(color(*background_col))
    #     x1,y1=k[0],k[1]
    #     point(x1,y1)
    #     # print(k, v)
    #     x2,y2=int(v[0]),int(v[1])
    #     stroke(color(*v[2]))
    #     point(x2,y2)
    #     # line(x1,y1,x2,y2)   
            
        
    ezel_inv(w=w,ow=ow,h=h,oh=oh)
    ezel(top=oh,sides=ow)

    filename= ''.join('rotfan'+timestamp+'.jpg')
    save(filename)
    print("End of Program")
    # exit()
    
    
    
