add_library('pdf')
import datetime
import time
import random as rd
# from collections import Counter

resolution=50
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

def line_gauss_path(x,y,destination,r, dest_init,spread, depth=300,form_shape=2):

    destx,desty=destination
    
    distance=int(dist(x,y,destx,desty))
    distance_covered=distance/dest_init*100

    if 10<distance_covered<100:
        ratio=random(0.10,.90)
    else:
        ratio=0.10

    if distance<r:
        r=max(distance,1)
        
    dx,dy=destx-x,desty-y
    destination_angle=int(degrees(atan2(dy,dx)))
    direction_angle=rd.gauss(mu=destination_angle,sigma=spread*ratio)
    target=PVector().fromAngle(radians(direction_angle)).mult(r)
    newx,newy=int(x+target.x),int(y+target.y)

    if (x != destx or y != desty) and depth>0:
        if form_shape==1:
            noStroke()
            vertex(newx,newy)
        elif form_shape==2:
            line(x,y,newx,newy)
        elif form_shape==3:
            point(newx,newy)
        depth-=1
        line_gauss_path(newx,newy,destination,r,dest_init,spread,depth=depth)
    # else:
    #     print("reached endpoint: ", x, y)
        

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################   
         
def draw():
    
    n_partition=int(random(2,6))
    # n_partition=1
    rectangles = partition_rectangle(0, 0, w, h, n_partition) 
    
    for k,v in rectangles.items():
        x1_partition,y1_partition = v[0]
        x2_partition,y2_partition = v[1]
        
        scaler=random(2,20)
        hei,wid=y2_partition-y1_partition,x2_partition-x1_partition
        min(hei,wid)
        distance=int(min(hei,wid)/scaler/2)
        # distance=3
        print(distance)
        for i in range(distance):
            sq1x,sq1y=int(x1_partition+scaler*i),int(y1_partition+scaler*i)
            sq2x,sq2y=int(x2_partition-scaler*i),int(y2_partition-scaler*i)
            noise_val=noise(i*1)
            fill_noise = int(map(noise_val, 0.0, 1.0, 0, 2))
            noise_val=noise(i*0.5)
            spread_noise = int(map(noise_val, 0.0, 1.0, 0, 10))
            # vertex(sq1x,sq1y)
            r=resolution/3
            c=rd.choice(all_col)
            # c=rd.choice(all_col)
            stroke(color(*rd.choice([c,(0,0,0)])))
            fill(color(*rd.choice([c,background_col])))
            for l in range(3):
                beginShape()
                strokeWeight(int(random(0,3)))
                line_gauss_path(x=sq1x,y=sq1y,destination=(sq2x,sq1y),r=r
                                ,dest_init=dist(sq1x,sq1y,sq2x,sq1y)
                                ,spread=spread_noise)
                
                line_gauss_path(x=sq2x,y=sq1y,destination=(sq2x,sq2y),r=r
                                ,dest_init=dist(sq2x,sq1y,sq2x,sq2y)
                                ,spread=spread_noise)
                
                line_gauss_path(x=sq2x,y=sq2y,destination=(sq1x,sq2y),r=r
                                ,dest_init=dist(sq2x,sq2y,sq1x,sq2y)
                                ,spread=spread_noise)
                
                line_gauss_path(x=sq1x,y=sq2y,destination=(sq1x,sq1y),r=r
                                ,dest_init=dist(sq1x,sq2y,sq1x,sq1y)
                                ,spread=spread_noise)
                endShape()
            
    
    # ezel_inv(w=w,ow=ow,h=h,oh=oh)
    # ezel(top=oh,sides=ow)

    filename= ''.join('line_gauss_path'+timestamp+'.jpg')
    save(filename)
    print("End of Program")
    exit()
    
    
    
