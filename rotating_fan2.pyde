add_library('pdf')
import datetime
import time
import random as rd
# from collections import Counter

resolution=30
ow=oh=resolution
w=ow+resolution*50+ow
h=oh+resolution*60-oh

all_col    =[[241, 78, 27],
            [158, 37, 38],
            [207, 83, 27],
            [194, 27, 20],
            [10, 56, 113],
            [3, 98, 127],
            [255, 255, 255],
            [255,142,106,255],
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
            [133,175,154,255]     
]  

color_list = [((185.0, 12.0, 32.0, 255.0)),(0.0, 0.0, 0.0, 255.0),(9.0, 72.0, 118.0, 255.0)]

background_col=(239,234,212)

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def setup():
    size(w,h,PDF, ''.join('rotfan'+timestamp+'.pdf'))
    # size(w,h)
    background(*background_col)
    noLoop()
    noSmooth()
    # blendMode(REPLACE)
    
    global cg1
    global cg2
    cg1=createGraphics(w,h)
    cg2=createGraphics(w,h)
    
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

def pick_color(k=3):
    return rd.sample(all_col,k)

def get_rgba(value):
    rgba=(red(value), green(value), blue(value), alpha(value))
    
    return rgba  

def retrieve_cgo_val(pixel_object, coordinates):
    cval=get_rgba(pixel_object.pixels[coordinates[0]+coordinates[1]*width])
    return cval

def rotating_gap_seeker(pixel_object,x,y,r,pigment=0,nested=True):
    
    print("Rotator start:", x, y, r)
    
    if not nested: 
        pixel_object.beginDraw()
        pixel_object.background(*background_col)
    
    pixel_object.loadPixels()
    center_color=pixel_object.pixels[x+y*(width)]
    center_color=get_rgba(center_color)
    if center_color[0:3] != background_col:
        print("Rotator could not be drawn")
        pass
    pixel_object.pushMatrix()
    pixel_object.translate(x,y)
    
    arcdict = dict()
    ongoing=0
    arcnumber=0
    range_start=0
    range_end=360
    
    iter_resolution = float(1)
    iter_cut_end=float(1)/iter_resolution
    iter_angles= [float(iter_angle) / iter_resolution for iter_angle in range(range_start,int(range_end*iter_resolution+iter_cut_end))]
    # print(iter_angles)
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
          c=cg1.pixels[xlook+ylook*(width)]
          c=get_rgba(c)
          
          if (c[0:3] == background_col and d < (iter_angles[-1])):
              
             # lerp_points.append((xlerp,ylerp))
             
             if l == int(r-1):
                # print(ongoing,d)
                if ongoing==0:
                   arcdict[arcnumber]["start_point"]=(xlook,ylook)
                   arcdict[arcnumber]["start_angle"]=radians(d)
                   arcdict[arcnumber]["start_angle_degree"]=d
                   ongoing=1
                   
                # for p in lerp_points:
                   # point(p[0],p[1])
                   
          else:
              if ongoing==1:
                arcdict[arcnumber]["end_point"]=(xlook,ylook)
                arcdict[arcnumber]["end_angle"]=radians(d)
                arcdict[arcnumber]["end_angle_degree"]=d
                arcnumber+=1
                ongoing=0
              break
          
    pixel_object.popMatrix()
    # updatePixels()
    if not nested: 
        pixel_object.endDraw()
    
    # print(arcdict)
    return arcdict

def draw_dict(pixel_object,arc_meta,nested=True):
    
    def gaussian_fill(x,y,start_a,end_a,r, confined=1):
        
        angle_window=(degrees(end_a)-degrees(start_a))
        mu=degrees(start_a)+angle_window/2
        sigma=angle_window/3
        # print(mu,sigma)
        n=r*resolution*10*(angle_window/360)
        # n=1
        # stroke(0)
        stroke_color=color(0,0,0)
        
        if not nested: 
            pixel_object.beginDraw()
            pixel_object.background(*background_col)
            
        pixel_object.stroke(stroke_color)
        pixel_object.fill(0)
        pixel_object.strokeWeight(0)
        pixel_object.pushMatrix()
        pixel_object.translate(x,y)
        
        # for i in range(0,int(r)):
        #     for p in range(int(n)):
        #         # gaussian_angle=radians(rd.gauss(mu=mu,sigma=sigma))
        #         gaussian_angle=radians(random(360))
        #         xc = ceil(cos(gaussian_angle)*r)
        #         yc = ceil(sin(gaussian_angle)*r)
        #         if degrees(start_a) <= degrees(gaussian_angle) < degrees(end_a):
        #             pixel_object.point(xc,yc)
        #     r-=1
        for enum,i in enumerate(range(0,int(r),resolution)):
            fill_inter=255*enum/float(r/resolution)
            # print(enum, int(r/resolution))
            pixel_object.fill(255-fill_inter)
            # pixel_object.strokeWeight(int(resolution/5))
            if enum == 0:
                pixel_object.strokeWeight(int(random(resolution/6,resolution/4)))
                pixel_object.stroke(0)
            else:
                pixel_object.noStroke()
            pixel_object.circle(0,0,r-i)
        
        pixel_object.popMatrix() 
        
        if not nested: 
            pixel_object.endDraw() 
        

    
    for k,d in arc_meta.items():
        if "start_point" in d.keys():
            centerx, centery = d["coord"]
            radius=d["radius"]
            start_angle, end_angle = d["start_angle"], d["end_angle"]

            gaussian_fill(x=centerx,y=centery,start_a=start_angle,end_a=end_angle
                          ,r=radius, confined=1)

def pixels2pdf(pixel_object):
    # pixel_object.updatePixels()
    for x in range(0,w):
        for y in range(0,h):
            c=retrieve_cgo_val(pixel_object=pixel_object, coordinates=(x,y))
            stroke(color(*c))
            point(x,y)
            
def partition_rectangle(x1, y1, x2, y2, depth, rect_counter=[1], apply=0):
    
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

def draw_circle_range(pixel_object,xcenter,ycenter, r, _range):
    pixel_object.pushMatrix()
    pixel_object.translate(xcenter,ycenter)
    # stroke(0)
    s=_range[0]
    e=_range[1]
    # print(s,e)
    for d in range(s,e, 1):
        # print(d)
        x = ceil(cos(radians(d))*r)
        y = ceil(sin(radians(d))*r)
        pixel_object.point(x,y)
        #point(x,y)
    pixel_object.popMatrix()

def connect_circles(pixel_object,x1, y1, r1, x2, y2, r2, c=(255,0,0), strokew=5, nested=True):
    def find_common_tangents(x1, y1, r1, x2, y2, r2):
        r1=r1/2
        r2=r2/2
        
        # Step 1: Calculate the distance between the centers
        d = dist(x1,y1,x2,y2)
        
        # Check if circles are too close or too far for common tangents to exist
        if d < abs(r1 - r2):
            pass
            print("No tangents exist - one circle is within the other.")
        if d == 0 and r1 == r2:
            pass
            print("No tangents exist - circles are identical.")
        
        # Step 2: Calculate angles for tangents
        angle_between_centers = atan2(y2 - y1, x2 - x1)
        angle_external = acos((r1 - r2) / d)
    
        # Function to calculate tangent points on both circles for a given angle
        def tangent_points(angle):
            # Tangent point on the first circle
            tx1 = floor(x1 + r1 * cos(angle))
            ty1 = floor(y1 + r1 * sin(angle))
            
            # Tangent point on the second circle
            tx2 = floor(x2 + r2 * cos(angle))
            ty2 = floor(y2 + r2 * sin(angle))
            
            return (tx1, ty1, tx2, ty2, angle)
            
        # Step 3: Calculate the tangent points for all four tangents
        tangents = {}
        
        # External tangents
        tangents['c1'] = tangent_points(angle_between_centers + angle_external)
        tangents['c2'] = tangent_points(angle_between_centers - angle_external)
    
        return tangents

    tangents=find_common_tangents(x1, y1, r1, x2, y2, r2)
    
    print("Tangents: ", tangents )

    def looparaound(d):
        angle1=False
        angle1_2 = degrees(atan2(y1 - y2, x1 - x2))
        angle2_1 = degrees(atan2(y2 - y1, x2 - x1))
        print("Angles direction:", angle1_2, angle2_1)
        color_surplus=rd.sample(all_col,1)[0]
        if not nested: 
            pixel_object.beginDraw() 
        
        pixel_object.stroke(color(*c))
        pixel_object.strokeWeight(strokew)
        
        for k,v in d.items():
            
            point1_x,point1_y,point2_x,point2_y, angle2 = v
            angle2=degrees(angle2)
            pixel_object.line(point1_x,point1_y,point2_x,point2_y)
            pixel_object.strokeWeight(strokew/2)
            pixel_object.stroke(*color_surplus)
            pixel_object.line(point1_x,point1_y,point2_x,point2_y)
            pixel_object.stroke(color(*c))
            pixel_object.strokeWeight(strokew)
            if angle1:
                print("Angles: ", angle1, angle2)
                angle_small=min(angle2,angle1)
                angle_big=max(angle2,angle1)
                if angle_small < angle2_1 < angle_big:
                    print(angle_small, angle2_1, angle_big, angle_small+360)
                    if angle_small <= 0:
                        angle_small_dup=angle_big
                        angle_big = angle_small + 360
                        angle_small = angle_small_dup
                    else:
                        angle_small_dup=angle_small
                        angle_small = angle_big - 360
                        angle_big = angle_small_dup
                ranger=(floor(angle_small),floor(angle_big)+1)
                draw_circle_range(pixel_object,x1,y1, r1/2, _range=ranger)
                
                
                angle_small=min(angle2,angle1)
                angle_big=max(angle2,angle1)
                
                if angle_small < angle1_2 < angle_big:
                    print(angle_small, angle1_2, angle_big, angle_small+360)
                    if angle_small <= 0:
                        angle_small_dup=angle_big
                        angle_big = angle_small + 360
                        angle_small = angle_small_dup
                    else:
                        angle_small_dup=angle_small
                        angle_small = angle_big - 360
                        angle_big = angle_small_dup
                ranger=(floor(angle_small),floor(angle_big)+1)
                draw_circle_range(pixel_object,x2,y2, r2/2, _range=ranger)
                
            angle1=angle2
        
        if not nested: 
            pixel_object.endDraw() 
            

    looparaound(d=tangents)
    
def calc_flow_matrix(w,h,rstep,nstep=0.06,min_val=0, max_val=360):
    xoff=random(10)
    arra=list()
    for ix in range(0,w,rstep):
        yoff=0
        cols=list()
        
        for jy in range(0,h,rstep):
            yoff+=nstep
            noise_val=noise(xoff,yoff)
            angle = map(noise_val, 0.0, 1.0, min_val, max_val)
            cols.append(angle)
            
        xoff+=nstep
        arra.append(cols)
    
    return arra       

def retrieve_cgo_val(pixel_object, coordinates):
    cval=get_rgba(pixel_object.pixels[coordinates[0]+coordinates[1]*width])
    return cval

def warping_executor(pixel_object,field,warp_dict,length_line=5, type=1):

    pixel_object.beginDraw()
    pixel_object.background(*background_col)   
    pixel_object.strokeWeight(1)
    
    start_time = time.time()
    
    try:
        loop_dict=warp_dict
        warp_dict=dict()

        for k,v in loop_dict.items():
            # Already contains only other pixels than background
            x,y,c=v[0],v[1],v[2]
            if (0 <= x < w) and (0 <= y < h):
                target=PVector().fromAngle(field[x][y]).mult(random(length_line-4,length_line+4))
                warp_dict[(x,y)]=(floor(x+target.x),floor(y+target.y), c)

    except AttributeError:
        print("Creating new dictionary")
        warp_dict=dict()
        for x in range(w):
            for y in range(h):
                c=retrieve_cgo_val(pixel_object,coordinates=(x,y))
                # print(c)
                if c[0:3] != background_col:
                    target=PVector().fromAngle(field[x][y]).mult(random(length_line))
                    warp_dict[(x,y)]=(floor(x+target.x),floor(y+target.y), c)
                    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time)  
           
    for k,v in warp_dict.items():
        pixel_object.stroke(color(*background_col)) 
        x1,y1=k[0],k[1]
        pixel_object.point(x1,y1)
        # print(k, v)
        x2,y2=int(v[0]),int(v[1])
        pixel_object.stroke(color(*v[2]))
        if type==1: 
            pixel_object.point(x2,y2)  
        elif type==2:
            pixel_object.line(x1,y1,x2,y2) 
        elif type==3:
            pixel_object.noStroke()
            pixel_object.fill(color(*v[2]))
            pixel_object.circle(x2,y2,resolution/4) 
    
    pixel_object.endDraw()
    
    print("Points warped: ", len(warp_dict))
    return warp_dict
    # pixel_object.updatePixels()
    # pixel_object.loadPixels()
    
def swoosh(pixel_object,x1,y1,r1,x2,y2,r2,c):
    distance = floor(dist(x2,y2,x1,y1))
    center=(floor((x2+x1)/2),floor((y2+y1)/2))
    atan_left = floor(degrees(atan2(x1-center[0],y1-center[1])))
    atan_right = floor(degrees(atan2(x2-center[0],y2-center[1])))
    smallest=min(atan_left,atan_right)
    largest=max(atan_left,atan_right)
    color_surplus=rd.sample(all_col,1)[0]
    
    for d in range(smallest,largest+1,1):
        xroute=center[0]+sin(radians(d))*distance/2
        yroute=center[1]+cos(radians(d))*distance/2
        inner_dist=floor(dist(x1,y1,xroute,yroute))
        ratio = float(inner_dist)/float(distance)
        rlerp = int(lerp(r1, r2+1, ratio));
        pixel_object.noStroke()
        pixel_object.noFill()
        # circ(x=xroute,y=yroute,r=rlerp)
        pixel_object.fill(color(*c))
        pixel_object.circle(xroute,yroute,rlerp)

    for d in range(smallest,largest+1,1):
        xroute=center[0]+sin(radians(d))*distance/2
        yroute=center[1]+cos(radians(d))*distance/2
        inner_dist=floor(dist(x1,y1,xroute,yroute))
        ratio = float(inner_dist)/float(distance)
        rlerp = int(lerp(r1, r2+1, ratio));
        pixel_object.noStroke()
        pixel_object.noFill()
        # circ(x=xroute,y=yroute,r=rlerp)
        pixel_object.fill(color(*color_surplus))
        pixel_object.circle(xroute,yroute,rlerp/2)
    
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################   
         
def draw():
    n_loops=int(random(5,12))
    n_swoosh=int(random(1,3))
    # n_swoosh=0
    # n_warps=int(random(3,5))
    n_warps=3
    n_partition=int(random(4,7))
    strokew=int(random(5,resolution))
    print(pick_color(k=2))
    col1,col2=pick_color(k=2)
    warp_dict=None
    
    print("Colors:", col1,col2)
    print("n_loops", n_loops)
    print("n_swoosh", n_swoosh)
    print("n_warps", n_warps)
    print("n_partition", n_partition)
    print("strokew", strokew)
    
    # Partition the canvas in random rectangles
    rectangles = partition_rectangle(ow*5, oh*5, w-ow*5, h-oh*5, n_partition) 
    print(rectangles)
    print(len(rectangles))
    
    # Printing the rectangles
    cg1.beginDraw()
    cg1.background(*background_col)       
    
    collect_circles = []
    
    for k,v in rectangles.items():
        # print(v)
        xr1,yr1 = v[0]
        xr2,yr2 = v[1]
        wid,hei=int(abs(xr2-xr1)), int(abs(yr2-yr1))
        r=min(wid/2,hei/2)
        if r > resolution:
            # cg1.fill(0) 
            cg1.noFill()  
            cg1.stroke(0)               
            # cg1.rect(xr1,yr1,wid,hei)
            center=(xr1+wid/2,yr1+hei/2)
            arc_meta=rotating_gap_seeker(cg1, x=center[0],y=center[1],r=r)
            draw_dict(cg1,arc_meta=arc_meta)
            
            collect_circles.append((center[0], center[1],r))
            # if rd.uniform(0,1) > 0.7:
            #     rectangle_overlay(x=xr1,y=yr1,rect_width=wid,rect_height=hei, block_size=int(r/20))
        # else:
        #     cg1.strokeWeight(resolution)
        #     cg1.fill(color(255,255,255))
        #     cg1.noFill()  
        #     cg1.rect(xr1-ow*5,yr1-ow*5,xr2-ow*5,yr2-ow*5)
            
     
    print("All Circles: ", collect_circles)         
    
    for i in range(n_loops):
        print("Executing Loop:", i)
        loopers=rd.sample(collect_circles,k=2)
        xloop1,yloop1,rloop1=loopers[0]
        xloop2,yloop2,rloop2=loopers[1]
        connect_circles(cg1,xloop1,yloop1,rloop1*2+strokew,xloop2,yloop2,rloop2*2+strokew,strokew=strokew, c=col1)     
    
    exclude_large_circles = [circ for circ in collect_circles if (circ[2]<resolution*3)]
    collect_circles=exclude_large_circles
    print("All Circles: ", collect_circles) 
    
    for i in range(n_swoosh):
        swooshers=rd.sample(collect_circles,k=2)
        xswoosh1,yswoosh1,rswoosh1=swooshers[0]
        xswoosh2,yswoosh2,rswoosh2=swooshers[1]
        swoosh(cg1,xswoosh1,yswoosh1,rswoosh1*2,xswoosh2,yswoosh2,rswoosh2*2,c=col2)        
                            
    cg1.endDraw()
    cg1.loadPixels()
    
    for i in range(n_warps):
        print("Executing Warp: "+ str(i+1)+"/"+str(n_warps))
        type=3
        warp_direction=int(random(360))
        min_val=0
        nstep=0.0001
        length_line=int(random(resolution,resolution*4))

        if i == n_warps-1:
            type=1
            min_val=0
            warp_direction=360
            length_line=10 
            warp_dict=None
            
        print(type, warp_direction, nstep, length_line)
        warper=calc_flow_matrix(w=w,h=h,rstep=1,nstep=nstep,min_val=min_val,max_val=warp_direction)
        warp_dict=warping_executor(pixel_object=cg1, field=warper,warp_dict=warp_dict, length_line=length_line,type=type) 
    
    
    pixels2pdf(cg1)
    # image(cg1,0,0)
    
    ezel_inv(w=w,ow=ow,h=h,oh=oh)
    ezel(top=oh,sides=ow)

    # filename= ''.join('rotfan'+timestamp+'.jpg')
    # save(filename)
    print("End of Program")
    exit()
    
    
    
