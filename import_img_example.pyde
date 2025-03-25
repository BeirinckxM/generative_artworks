add_library('pdf')
import datetime
import random as rd

scaler=1
resolution=10
ow=oh=0
w=924
h=862

color_list=[[198,26,26],
            [24,134,168],
            [141,175,155],
            [238,223,96],
            [238,119,0],
            [171,169,153],
            [244,92,86],
            [203,226,201],
            [253,235,131],
            [255,200,200],
            
]

background_col=(245,240,219)

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def setup():
    # size(w,h,PDF, ''.join('fuzzy_circle'+timestamp+'.pdf'))
    size(w,h)
    background(*background_col)
    noLoop()
    #blendMode(DIFFERENCE)

def draw():
    
    print("Starting")
    
    def calc_flow_matrix(w,h,rstep=1,nstep=0.06):
        xoff=random(1)
        arra=list()
        for ix in range(0,w,rstep):
            yoff=0
            cols=list()
            
            for jy in range(0,h,rstep):
                yoff+=nstep
                noise_val=noise(xoff,yoff)
                angle = map(noise_val, 0.0, 1.0, 0, 1)
                cols.append(angle)
                
            xoff+=nstep
            arra.append(cols)
        
        return arra
    
    def get_rgba(value):
        rgba=(red(value), green(value), blue(value), alpha(value))
        return rgba
    
    # pg1 = createGraphics(w,h)
    ficus_img = loadImage("city20231028_161044.jpg")
    
    test=ficus_img.pixels[175199]
    
    ficus_img.loadPixels()
    
    flow_values=calc_flow_matrix(w,h,nstep=0.01)
    
    for i,x in enumerate(range(ow, ow+ficus_img.width)):
        for j,y in enumerate(range(oh,oh+ficus_img.height)):
            flow_val=flow_values[x][y]
            rgba = get_rgba(ficus_img.pixels[(x-ow)+(y-oh)*(ficus_img.width)])
            if flow_val > 0.8:
                chance_of_print=int(map(flow_val,0,0.8,0,10))
                sample_list1=[0 for s in range(chance_of_print)]
                sample_list0=[1 for s in range(10-chance_of_print)]
                sample_list=sample_list1+sample_list0
                print_bool=rd.choice(sample_list) 
                if print_bool:
                    # print(x,y)
                    #rgba = get_rgba(ficus_img.pixels[(x+1)+(y)*(ficus_img.width)])
                    stroke(color(*rgba))
                    square(x,y,1)
            else:
                angle=map(flow_val,0,1,-360,360)
                target = PVector().fromAngle(radians(angle)).mult(int(random(200)))
                # stroke(color(*background_col))
                ccc=map(flow_val,0,1,0,255)
                stroke(color(*rgba))
                line(x,y,x+target.x,y+target.y)
    
    # image(img,ow,oh)
    
    #print(img.pixels)
    
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

    # ezel_inv(w=w,ow=ow,h=h,oh=oh)
    
    # ezel(top=oh,sides=ow)
    
    filename= ''.join('boxes'+timestamp+'.jpg')
    save(filename)
    print("End of Program")
    # exit()
    
    
