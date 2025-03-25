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
            [158, 37, 38],
            [207, 83, 27],
            [194, 27, 20],
            [34, 84, 63],
            [41, 64, 90],
            [33, 51, 44],
            [10, 56, 113],
            [3, 98, 127],
            [255, 255, 255],
            [255, 255, 255],
            [255, 255, 255],
            [255, 255, 255],
            [255, 255, 255],
            [255, 255, 255],
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

background_col=(239,234,212)

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

square_size=resolution*20

print(square_size*square_size)

def setup():
    # size(w,h,PDF, ''.join('collage'+timestamp+'.pdf'))
    size(w,h)
    background(*background_col)
    noLoop()
    noSmooth()
 
    # blendMode(REPLACE)
    
    global cg1
    global cg2
    
    cg1=createGraphics(square_size,square_size)
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

# def retrieve_cgo_val(pixel_object, coordinates):
#     cval=get_rgba(pixel_object.pixels[coordinates[0]+coordinates[1]*width])
#     return cval

def pixels2pdf(pixel_object):
    # pixel_object.updatePixels()
    for x in range(0,w):
        for y in range(0,h):
            c=retrieve_cgo_val(pixel_object=pixel_object, coordinates=(x,y),pobw=width)
            stroke(color(*c))
            point(x,y)
    
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


def retrieve_cgo_val(pixel_object, coordinates, pobw):
    cval=get_rgba(pixel_object.pixels[coordinates[0]+coordinates[1]*pobw])
    return cval

def split_length(total_length, min_length, max_length):
    # Initialize list to store the sub-lengths
    sub_lengths = []

    # Ensure there is enough total length to create sections with the given minimum length
    if total_length <= min_length:
        sub_lengths.append(total_length)
        
        # raise ValueError("Total length is smaller than the minimum section length.")
    else:
        remaining_length = total_length
        
        while remaining_length > min_length:
            # print("2")
            # Ensure the remaining length is enough to create at least one more section
            max_possible_length = min(remaining_length, max_length)
            section_length = rd.randint(min_length, max_possible_length)
            # print("section_length", section_length)
            # Add the section length to the list
            sub_lengths.append(section_length)
            
            # Subtract the section length from the remaining length
            remaining_length -= section_length
        
        # If the remaining length is smaller than min_length, adjust last section
        # else:
            # print("3")
        if (sub_lengths[-1] + remaining_length) > max_length:
            sub_lengths.append(remaining_length)
        else:
            sub_lengths[-1] += remaining_length
    
    # print(sum(sub_lengths))
    return sub_lengths

def accumu(lis):
    total = 0
    for x in lis:
        total += x
        yield total
        
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

def line_gauss_path(pixel_object,x,y,destination,r,spread,lookback,dest_init=False,depth=40,form_shape=2):
    destx,desty=destination
    distance=round(dist(x,y,destx,desty))
    dx,dy=destx-x,desty-y
    destination_angle=round(degrees(atan2(dy,dx)))
    
    if dest_init==False:
        dest_init=(distance,destination_angle)
        
    try:
        distance_covered=100-distance/dest_init[0]*100
    
        on_track = (dest_init[1]-90 <= destination_angle <= dest_init[1]+90)
        if distance_covered < 3 and on_track:
            ratio=1
            mu=(destination_angle)
            # print(distance,distance_covered,dest_init)
        elif 3<distance_covered<97 and on_track:
            ratio=random(0.05,.95)
            mu=(destination_angle+lookback)/2
        else:
            ratio=0.1
            mu=destination_angle
    
        if distance<r:
            r=distance
            
        direction_angle=rd.gauss(mu=mu,sigma=spread*ratio)
        target=PVector().fromAngle(radians(direction_angle)).mult(r)
        lookback=direction_angle
        newx,newy=min(round(x+target.x),w),min(round(y+target.y),h)
        if (x != destx or y != desty):
            if form_shape==1:
                pixel_object.noStroke()
                pixel_object.vertex(newx,newy)
            elif form_shape==2:
                pixel_object.line(x,y,newx,newy)
            elif form_shape==3:
                pixel_object.point(newx,newy)
            elif form_shape==4:
                pixel_object.noStroke()
                pixel_object.square(newx,newy,10)
            depth-=1
            line_gauss_path(pixel_object,newx,newy,destination,r,spread,lookback,dest_init,depth=depth,form_shape=form_shape)
        # else:
        #     print("reached endpoint: ", x, y)
    except ZeroDivisionError:
        print("Did not draw anything")
        pass

def get_rgba(value):
    rgba=(red(value), green(value), blue(value), alpha(value))
    
    return rgba  

def retrieve_cgo_val(pixel_object, coordinates):
    cval=get_rgba(pixel_object.pixels[coordinates[0]+coordinates[1]*width])
    return cval

def line_fill(pixel_object,x,y,x2,y2,field,form_shape):
    print(x,y,x2,y2)
    for yl in range(y,y2,10):
        space_finder=0
        for xl in range(x,x2):
            c=retrieve_cgo_val(pixel_object, coordinates=(xl,yl))
            # print(c)
            if c[0:3] == background_col and xl < (x2-1):
                space_finder+=1
            else:
                if space_finder > 10:
                    a=field[xl][yl]
                    if form_shape == 2:
                        a=255
                    else:
                        a=field[xl][yl]
                    pixel_object.stroke(color(255,0,0,a))
                    pixel_object.fill(color(255,0,0,a))
                    # pixel_object.line(x,y,x-space_finder,y)
                    # for j in range(1):
                    pixel_object.strokeWeight(int(random(2)))
                    # pixel_object.strokeWeight(1)
                    line_gauss_path(pixel_object=pixel_object
                                    ,x=xl-space_finder,y=yl,destination=(xl-15,yl),r=10
                                    ,lookback=False
                                    ,dest_init=False
                                    ,spread=random(10)
                                    ,form_shape=form_shape)
                space_finder=0

def generate_points_by_noise(pixel_object, x, y, field, depth=1, r=10, l=False):
    print(x, y, depth)
    noise_angle = field[x][y]
    target=PVector().fromAngle(radians(noise_angle)).mult(r)
    newx,newy=min(max(0,int(x+target.x)),w-1),min(max(0,int(y+target.y)),h-1)

    if depth > 0:
        print(newx,newy)
        if l != False:
            l.append((newx,newy))
        else:
            l=[(x,y)]
            l.append((newx,newy))
        depth-=1
        # pixel_object.line(x,y,newx,newy)
        generate_points_by_noise(pixel_object=pixel_object
                                 ,x=newx, y=newy, field=field, depth=depth, r=5, l=l)
    
    return l
        

        
        
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################   
         
def draw():
    

    
    field1=calc_flow_matrix(w,h,rstep=1,nstep=1,min_val=0, max_val=360)
      
    cg2.beginDraw()
    cg2.background(*background_col)  
    cg2.loadPixels()        
    cg2.stroke(0)
    path_length = 300
    x,y = (int(round(random(w))),int(round(random(h)))) 
    pixel_object=cg2
    l1=generate_points_by_noise(pixel_object, x, y, field1, depth=path_length, r=20)
    
    field2=calc_flow_matrix(w,h,rstep=1,nstep=1,min_val=0, max_val=360)
    x,y = (int(round(random(w))),int(round(random(h))))
    l2=generate_points_by_noise(pixel_object, x, y, field2, depth=path_length, r=10)
    
    print(len(l1),len(l2))
    
    for p1,p2 in zip(l1,l2):
        # print(p1,p2)
        x,y=p1
        line_gauss_path(pixel_object=cg2
                        ,x=x,y=y,destination=p2,r=resolution/2
                        ,lookback=False
                        ,dest_init=False
                        ,spread=random(20))
        
    
    # npoints=100
    
    # points = [(round(random(w)),round(random(h))) for p in range(npoints)]
    
    # for i,p in enumerate(points[1:]):
    #     if i==1:
    #         x,y=(round(random(w)),round(random(h)))
    #     else:
    #         x,y=points[i-1]
    #     destination=p
    #     for i in range(int(random(1,int(npoints/4)))):
    #         strokeWeight(int(random(4)))
    #         collect_angles=line_gauss_path(pixel_object=cg2
    #                                     ,x=x,y=y,destination=p,r=resolution/2
    #                                     ,lookback=False
    #                                     ,dest_init=False
    #                                     ,spread=random(20))
        
    # line_fill(pixel_object=cg2,x=xs,y=ys,x2=xs+midx,y2=ys+midy,field=field,form_shape=4)
    
    cg2.endDraw() 
    
    image(cg2,0,0)
        
    
    # ezel_inv(w=w,ow=ow,h=h,oh=oh)
    # ezel(top=oh,sides=ow)

    filename= ''.join('line_gauss_path_core'+timestamp+'.jpg')
    # save(filename)
    print("End of Program")
    # exit()
    
    
    
