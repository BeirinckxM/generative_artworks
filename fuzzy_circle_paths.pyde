add_library('pdf')
import datetime
import random as rd
import itertools

scaler=1
resolution=10
ow=oh=resolution*3*scaler
w=resolution*200*scaler
h=resolution*135*scaler

all_col    =[[198,26,26],
            [24,134,168],
            [141,175,155],
            [238,223,96],
            [238,119,0],
            [171,169,153],
            [244,92,86],
            [203,226,201],
            [253,235,131],
            [255,200,200],
            [41, 121, 222],
            [254, 242, 169],
            [170, 215, 211],
            [225, 60, 15],
            [207, 42, 41],
            [79, 145, 223],
            [226, 238, 225],
            [40, 133, 147],
            [136, 180, 168],
            [254, 252, 247],
            [14, 105, 109],
            [251, 60, 13],
            [235, 244, 188],
            [91, 191, 84],
            [182, 44, 53],
            [246, 172, 135],
            [231, 232, 224],
            [56, 165, 197],
            [250, 128, 13],
            [250, 89, 74],
            [250, 247, 125],
            [253, 234, 79],
            [230, 247, 248],
            [234, 221, 30],
            [218, 134, 115],
            [245, 242, 231],
            [137, 200, 122],
            [0,0, 0]        
]  

background_col=(245,240,219)

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def setup():
    size(w,h,PDF, ''.join('fuzzy_circle'+timestamp+'.pdf'))
    # size(w,h)
    background(*background_col)
    noLoop()
    #blendMode(DIFFERENCE)

def draw():
    
    print("Starting")
    
    def create_palette(n=10):
        picture=loadImage("Ficus_leaf.jpg")
        pw, ph = picture.width, picture.height
        samples=[(int(random(pw)), int(random(ph))) for i in range(n)]
        colors=[picture.pixels[p[0]+p[1]*picture.width] for p in samples]
        rgbs=[[red(value), green(value), blue(value), alpha(value)] for value in colors]
    
        return rgbs
    
    def palette(n, all_col):
        _color_list = [rd.choice(all_col) for i in range(n)]
        return _color_list
    
    color_list=palette(int(random(1,len(all_col))), all_col=all_col)
    
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
    
    def get_rgba(value):
        rgba=(red(value), green(value), blue(value), alpha(value))
        return rgba
    
    def create_pathlike(object,spacing, n_paths=1):
        object.beginDraw()
        object.pushMatrix()
        object.background(255)
        
        for p in range(n_paths):
            randx,randy=random(ow,w-ow), random(oh,h-oh)
            xoff,yoff,zoff=random(1),random(1),random(1)
            length_of_path=int(random(10000,30000))
            spreader=20
            object_space=int(random(10,30))
            obj_size=0
            r=1
            for p in range(0,length_of_path,object_space):
                while (ow < (randx) < (w-ow) and oh < (randy) < (h-oh)):
                    # Determining the coordinates for the drawn objects
                    nval=noise(xoff/spreader,yoff/spreader,zoff/spreader)
                    # print(randx, randy)
                    angle=map(nval,0,1,0,360)
                    randx+=cos(angle)*r
                    randy+=sin(angle)*r
                    zoff+=0.004
                    xoff+=0.002
                    yoff+=0.005
                    
                    # Drawing on the cgo
                    stroke_color=color(*rd.choice(color_list))
                    obj_size=map(noise(xoff),0,1,0,random(5,700)*scaler)
                    #print(get_rgba(stroke_color))
                    #object.stroke(0)
                    object.noStroke()
                    object.fill(stroke_color)
                    if angle > 180:
                        object.circle(randx,randy,obj_size*2)
                    else:
                        object.square(randx,randy,obj_size)
            
        object.popMatrix()
        object.endDraw()
        
    def retrieve_cgo_val(pixel_object, coordinates):
        cval=get_rgba(pixel_object.pixels[coordinates[0]+coordinates[1]*width])
        
        return cval
    
    def split_overlay(widths, field, factor=4, col=background_col):
        for yl in range(oh, h-oh, widths):
            for xl in range(0,w):
                target = PVector().fromAngle(radians(field[xl][yl])).mult(widths/factor)
                stroke(*col)
                line(xl,yl,xl,yl+target.y)
    
    def get_average_field(field):
        all_values=sum(field, [])
        _mean=sum(all_values)/len(all_values)
        
        return _mean

    def wear_overlay(widths, field1,field2, cgo, _mean, factor=4, col=background_col):
        for x in range(ow, w-ow):
            for y in range(oh,h-oh):
                erode_val=field1[x][y]
                if erode_val > (_mean*1.2):
                    pass
                else:
                    chance_of_print=int(map(erode_val,0,1,0,10))
                    sample_list1=[1 for s in range(chance_of_print)]
                    sample_list0=[0 for s in range((10-chance_of_print)*3)]
                    sample_list=sample_list1+sample_list0
                    print_bool=rd.choice(sample_list) 
                    if print_bool:
                        angle=map(erode_val,0,1,0,360)
                        target = PVector().fromAngle(angle).mult(int(random(10)))
                        _alpha=field2[x][y]
                        if rd.uniform(0,1) < 0.3:
                            ccc=[random(240, 255),random(240,255),random(240, 255),_alpha]
                        else: 
                            ccc=list(background_col)+[_alpha]
                        stroke(color(*ccc)) 
                        line(x,y,x+target.x,y+target.y)
            
    fluffy_field=calc_flow_matrix(w,h,rstep=1,nstep=0.01)
    erode_field=calc_flow_matrix(w,h,rstep=1,nstep=0.006, max_val=1)
    alpha_field=calc_flow_matrix(w,h,rstep=1,nstep=0.6, max_val=255)
    pg1=createGraphics(w,h)
    n_paths=int(random(3,10))
    create_pathlike(object=pg1, spacing=int(random(10,30)), n_paths=n_paths)

    # Loop over cgo object and draw lines with color of circles in buffer
    for px in range(ow,w-ow):
        for py in range(oh,h-oh):
            curcol=retrieve_cgo_val(pixel_object=pg1, coordinates=(px,py))
            if curcol == (255.0, 255.0, 255.0, 255.0):
                if rd.uniform(0,1)>0.8:
                    noStroke()
                    fill(0)
                    circle(px,py,2)
            elif rd.uniform(0,1) > 0.8:
                length_line=int(random(20))
                target = PVector().fromAngle(radians(fluffy_field[px][py])).mult(length_line)
                xto,yto=int(random(-6,6)), int(random(-6,6))
                stroke(*curcol)
                strokeWeight(1)
                line(px,py,px+target.x,py+target.y)
    
    wear_mean = get_average_field(field=erode_field)
    wear_overlay(widths=100, cgo=pg1, factor=1, field1=erode_field, field2=alpha_field, _mean=wear_mean)
    
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

    ezel_inv(w=w,ow=ow,h=h,oh=oh)
    
    ezel(top=oh,sides=ow)
    
    # filename= ''.join('boxes'+timestamp+'.jpg')
    # save(filename)
    print("End of Program")
    exit()
    
    
