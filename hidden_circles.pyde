add_library('pdf')
import datetime
import random as rd
import itertools

scaler=1
resolution=10
ow=oh=resolution*3*scaler
w=resolution*50*scaler
h=resolution*80*scaler

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
    # size(w,h,PDF, ''.join('fuzzy_circle'+timestamp+'.pdf'))
    size(w,h)
    background(*background_col)
    noLoop()
    blendMode(REPLACE)

def draw():
    
    print("Starting")
        
    def palette(n, all_col):
        _color_list = [rd.choice(all_col) for i in range(n)]
        return _color_list
    
    color_list=palette(int(random(5,15)), all_col=all_col)
    
    def calc_flow_matrix(w,h,rstep=1,nstep=0.06,max_val=1):
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
        
    def retrieve_cgo_val(pixel_object, coordinates):
        cval=get_rgba(pixel_object.pixels[coordinates[0]+coordinates[1]*width])
        
        return cval
    
    def get_average_field(field):
        all_values=sum(field, [])
        _mean=sum(all_values)/len(all_values)
        
        return _mean
    
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

    def create_hidden_circle(x,y,object, field):
        object.beginDraw()
        object.pushMatrix()
        object.background(255)
        
        object.circle(x,y,int(random(w/4,w)))
            
        object.popMatrix()
        object.endDraw()   
        
    # def retrieve_surroundings(x,y, kernel=9):
    #     sideval = int(sqrt(kernel)-round((sqrt(kernel)-sqrt(kernel)/2)))
    #     yarray = [i for i in range(-(sideval),(sideval)+1)]
    #     xarray = [i for i in range(-(sideval),(sideval)+1)]
    #     checks = [(xval,yval) for yval in [(y+j) for j in yarray] for xval in [(x+i) for i in xarray]]
    #     pixvals=[get_rgba(value=get(int(p[0]),int(p[1]))) for p in checks]  
    #     # print(pixvals)
    #     background_count=pixvals.count((245.0, 240.0, 219.0, 255.0)) 
    #     return background_count
    
    # def retrieve_surroundings(x,y, r=30):
    #     sideval = int(sqrt(r)-round((sqrt(r)-sqrt(r)/2)))
    #     # yarray = [i for i in range(-(sideval),(sideval)+1)]
    #     # xarray = [i for i in range(-(sideval),(sideval)+1)]
    #     # checksy = [(x,y+j) for j in yarray]
    #     # checksx = [(x+j,y) for j in xarray]
    #     checks=list()
    #     for angle in range(360):
    #         xcheck=x+cos(radians(angle))*r
    #         ycheck=y+sin(radians(angle))*r
    #         checks.append((xcheck, ycheck))
    #         # point(xcheck,ycheck)   
    #     pixvals=[get_rgba(value=get(int(p[0]),int(p[1]))) for p in set(checks)]  
    #     # print(pixvals)
    #     background_count=len(pixvals)-pixvals.count((245.0, 240.0, 219.0, 255.0)) 
    #     # if background_count != 0:
    #     #     print("stop")
    #     return background_count
                
    def retrieve_surroundings(x,y, r=10):
        field_angle=radians(field1[x][y]*360)
        #print(degrees(field_angle))
        target = PVector().fromAngle(field_angle).mult(r)
        stroke(color(255,0,0))
        #line(x,y,x+target.x,y+target.y)
        sideval = int(sqrt(r)-round((sqrt(r)-sqrt(r)/2)))
        # yarray = [i for i in range(-(sideval),(sideval)+1)]
        # xarray = [i for i in range(-(sideval),(sideval)+1)]
        # checksy = [(x,y+j) for j in yarray]
        # checksx = [(x+j,y) for j in xarray]
        checks=list()
        for angle in range(int(degrees(field_angle))-90, int(degrees(field_angle)+90)):
            xcheck=x+cos(radians(angle))*r
            ycheck=y+sin(radians(angle))*r
            checks.append((xcheck, ycheck))
            # point(xcheck,ycheck)   
        pixvals=[get_rgba(value=get(int(p[0]),int(p[1]))) for p in set(checks)]  
        # print(pixvals)
        background_count=len(pixvals)-pixvals.count((245.0, 240.0, 219.0, 255.0)) 
        # if background_count != 0:
        #     print("stop")
        return background_count                
                
    def follow_path(field,field_bis,x,y, kernel=81):
        # store_values=list()
        bgc=0
        stroke(color(*rd.choice(color_list)))
        noFill()
        # stroke(0)
        while (ow<x<w-ow) and (oh<y<h-oh) and (bgc <= 40):
            # print(bgc)
            stroker=field_bis[int(x)][int(y)]*2
            strokeWeight(1)
            r=1
            angle=field[int(x)][int(y)]*360
            x+=cos(radians(angle))*r
            y+=sin(radians(angle))*r
            bgc=retrieve_surroundings(x=int(x),y=int(y))
            stroke(0)
            point(int(x),int(y))
                                        
    field1 = calc_flow_matrix(w,h,rstep=1,nstep=0.004,max_val=1)
    field2 = calc_flow_matrix(w,h,rstep=1,nstep=0.008,max_val=1)
    field3 = calc_flow_matrix(w,h,rstep=1,nstep=0.004,max_val=1)
    # field4 = calc_flow_matrix(w,h,rstep=1,nstep=0.007,max_val=1)
    # for i in range(8):
    #     noFill()
    #     circle(random(w),random(h),random(w))
    
    # def wiggle_stripe(field=field4,linlen=50, xs=int(random(ow,w-ow)), ys=int(random(oh,h-oh)), mu=100, n=int(random(5,20))):
    #     stroke(color(*rd.choice(color_list)))
    #     strokeWeight(random(2,20))
    #     xoff=random(100)
    #     for i in range(n):
    #         xd=int(xs+abs(randomGaussian())*mu)
    #         # print(xd,ys, target.y)
    #         line(xd,ys,int(xd+noise(xoff)*20),int(ys+random(150)))
    #         xoff+=0.01
    
    # def gaussian_stripes(n=50, mu=10, yspread=1000):
    #     xs=int(random(ow,w-ow))
    #     for y in range(yspread):
    #         if rd.uniform(0,1) > 0.5:
    #             r=int(random(20))
    #             x=xs+randomGaussian()*mu
    #             bcg=retrieve_surroundings(x,y)
    #             fill(0)
    #             if rd.uniform(0,1) > 0.95:
    #                 wiggle_stripe(field=field4,linlen=random(100),
    #                                xs=int(random(ow,w-ow)),
    #                                 ys=int(random(oh,h-oh)),
    #                                  mu=100, n=int(random(1,10)))
                    
    # def gaussian_circles(n=50, mu=100, yspread=200):
    #     xs=int(random(ow,w-ow))
    #     for y in range(yspread):
    #         if rd.uniform(0,1) > 0.5:
    #             r=int(random(400))
    #             x=xs+randomGaussian()*mu
    #             bcg=retrieve_surroundings(x,y)
    #             fill(0)
    #             if rd.uniform(0,1) > 0.95:
    #                 noStroke()
    #                 circle(x,y,r)                    
                    
    # gaussian_stripes(n=50, mu=80, yspread=100)
    
    # gaussian_circles(n=50, mu=80, yspread=100)

    for i in range(100):
        # updatePixels()
        # field1 = calc_flow_matrix(w,h,rstep=1,nstep=0.005,max_val=1)
        if 0 < rd.uniform(0,1) < 0.5:
            l = follow_path(field=field1,field_bis=field2, x=int(random(ow,w-ow)),y=int(random(oh,h-oh)))
        else:
            l = follow_path(field=field3,field_bis=field1, x=int(random(ow,w-ow)),y=int(random(oh,h-oh)))
        # else:
        #     l = follow_path(field=field3,field_bis=field4, x=int(random(ow,w-ow)),y=int(random(oh,h-oh)))            
        
        # print(l)
        
    # field5 = calc_flow_matrix(w,h,rstep=1,nstep=0.003,max_val=1)      
    
    # pg1=createGraphics(w,h)
    # pg1.beginDraw()
    # pg1.background(*background_col)
    # pg1.endDraw()
    pg2=createGraphics(w,h)
    loadPixels()
    # pg1.pixels=pixels 
    
    # def transform_image(field, objectout): 
    #     pg2.beginDraw()
    #     for x in range(0,w):
    #         for y in range(0,h):
    #             print(x,y)
    #             # redraw
    #             target = PVector().fromAngle(field[x][y]).mult(50)
    #             # print(target)
    #             trace_col=pixels[x+y*width]
    #             objectout.stroke(color(*get_rgba(trace_col)))
    #             objectout.point(x+target.x,y+target.y)
    #     pg2.endDraw()
                
    # transform_image(field=field5, objectout=pg2)  
    # background(*background_col)
        
    # image(pg2,0,0)
        
    # ezel_inv(w=w,ow=ow,h=h,oh=oh)
    
    # ezel(top=oh,sides=ow)
    
    filename= ''.join('twomblyesk'+timestamp+'.jpg')
    # save(filename)
    print("End of Program")
    # exit()
    
    
