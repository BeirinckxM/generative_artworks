add_library('pdf')
import datetime
import random as rd

w=500
h=600
ow=oh=50

color_list=[[255,142,106,255],
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
            [133,175,154,255]]


timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def setup():
    size(w,h,PDF, ''.join('linepack'+timestamp+'.pdf'))
    #size(w,h)
    background(250,250,250)
    noLoop()

def draw():
    noFill()
    rect(ow,oh,w-ow*2,h-oh*2)
    
    def return_color(pxval):
        r=int(red(pxval))
        g=int(green(pxval))
        b=int(blue(pxval))
        return (r,g,b)
    
    #image(cg,0,0)
    
    def split_rect(splitx,splity):
        # ignore edges or points that are already black
        if (splitx in (ow,w-ow)) or (splity in (oh,h-oh)) or (cg.get(splitx,splity) != -1):
            pass
        else:
            cg.stroke(0)
            # xrange
            xr, yr = splitx, splity
            while cg.get(xr,yr) == -1:
                cg.point(xr,yr)
                xr+=1
            else:
                outer_right=xr

            xl, yl = splitx-1, splity
            while cg.get(xl,yl) == -1:
                cg.point(xl,yl)
                xl-=1
            else:
                outer_left=xl
                
            # yrange
            xd, yd = splitx, splity+1
            while cg.get(xd,yd) == -1:
                cg.point(xd,yd)
                yd+=1
            else:
                outer_down=yd

            xu, yu = splitx, splity-1
            while cg.get(xu,yu) == -1:
                cg.point(xu,yu)
                yu-=1
            else:
                outer_up=yu
                
            # retrieve coordinates
            coord_dict=dict()
            if (None in [outer_left,outer_up,splitx,splity]) == False:
                coord_dict["UL"]=((outer_left,outer_up),
                                (splitx,outer_up),
                                (splitx,splity),
                                (outer_left,splity))
                
            if (None in [outer_right,outer_up,splitx,splity]) == False:
                coord_dict["UR"]=((splitx,outer_up),
                                (outer_right,outer_up),
                                (outer_right,splity),
                                (splitx,splity))
                
            if (None in [outer_right,outer_down,splitx,splity]) == False:
                coord_dict["LR"]=((splitx,splity),
                                (outer_right,splity),
                                (outer_right,outer_down),
                                (splitx,outer_down))
                
            if (None in [outer_left,outer_down,splitx,splity]) == False:
                coord_dict["LL"]=((outer_left,splity),
                                (splitx,splity),
                                (splitx,outer_down),
                                (outer_left,outer_down))
            return coord_dict
    
    cg=createGraphics(w,h)
    cg.beginDraw()
    cg.background(255)
    cg.colorMode(RGB, 255)
    cg.blendMode(REPLACE)
    cg.noFill()
    cg.rect(ow,oh,w-ow*2,h-oh*2)
    #cg.stroke(0)
    combi_dict=dict()
    for i in range(50):
        it_dict=split_rect(splitx=int(random(ow,w-ow)),splity=int(random(oh,h-oh)))
        combi_dict[str(i)]=it_dict
    cg.endDraw() 
    
    print(len(combi_dict))
    blendMode(REPLACE)
    
    #image(cg,0,0)
    
    def draw_rectangles(_key):
        stroke(0)
        beginShape()
        if rd.uniform(0,1) > .8:
            #fill(color(*rd.choice(color_list)))
            vertex(combi_dict[kit][_key][int(random(0,4))])
        else:
            noFill()
        vertex(combi_dict[kit][_key][0])
        #vertex(combi_dict[kit][_key][1])
        #vertex(combi_dict[kit][_key][2])
        vertex(combi_dict[kit][_key][int(random(4))])
        endShape(CLOSE)
    
    def draw_gaussian(_key,amountp=100,sig=30):
        stroke(0)
        strokeWeight(random(1))
        point_list_r1=[point(p,combi_dict[kit][_key][0][1]) for p in [int(rd.gauss(mu=combi_dict[kit][_key][0][0],sigma=sig)) for n in range(amountp)] if (p > combi_dict[kit][_key][0][0] and p < combi_dict[kit][_key][1][0])]
        point_list_r2=[point(p,combi_dict[kit][_key][3][1]) for p in [int(rd.gauss(mu=combi_dict[kit][_key][3][0],sigma=sig)) for n in range(amountp)] if (p > combi_dict[kit][_key][3][0] and p < combi_dict[kit][_key][2][0])]
        point_list_l1=[point(p,combi_dict[kit][_key][1][1]) for p in [int(rd.gauss(mu=combi_dict[kit][_key][1][0],sigma=sig)) for n in range(amountp)] if (p < combi_dict[kit][_key][1][0] and p > combi_dict[kit][_key][0][0])]
        point_list_l2=[point(p,combi_dict[kit][_key][2][1]) for p in [int(rd.gauss(mu=combi_dict[kit][_key][2][0],sigma=sig)) for n in range(amountp)] if (p < combi_dict[kit][_key][2][0] and p > combi_dict[kit][_key][3][0])]
        point_list_d1=[point(combi_dict[kit][_key][0][0],p) for p in [int(rd.gauss(mu=combi_dict[kit][_key][0][1],sigma=sig)) for n in range(amountp)] if (p > combi_dict[kit][_key][0][1] and p < combi_dict[kit][_key][3][1])]
        point_list_d2=[point(combi_dict[kit][_key][1][0],p) for p in [int(rd.gauss(mu=combi_dict[kit][_key][1][1],sigma=sig)) for n in range(amountp)] if (p > combi_dict[kit][_key][1][1] and p < combi_dict[kit][_key][2][1])]
        point_list_u1=[point(combi_dict[kit][_key][2][0],p) for p in [int(rd.gauss(mu=combi_dict[kit][_key][2][1],sigma=sig)) for n in range(amountp)] if (p < combi_dict[kit][_key][2][1] and p > combi_dict[kit][_key][1][1])]
        point_list_u2=[point(combi_dict[kit][_key][3][0],p) for p in [int(rd.gauss(mu=combi_dict[kit][_key][3][1],sigma=sig)) for n in range(amountp)] if (p < combi_dict[kit][_key][3][1] and p > combi_dict[kit][_key][0][1])]
    # coo=combi_dict
    
    def fill_lines(_key,amountp=100,sig=30,yspacing=3):
        stroke(color(*rd.choice(color_list)))
        strokeWeight(0)
        get_width=combi_dict[kit][_key][1][0]-combi_dict[kit][_key][0][0]
        get_height=combi_dict[kit][_key][3][1]-combi_dict[kit][_key][0][1]
        xstart=combi_dict[kit][_key][0][0]
        ystart=combi_dict[kit][_key][0][1]
        for line in range(ystart,ystart+get_height,1):
            point_list_r=[point(p,line) for p in [int(rd.gauss(mu=combi_dict[kit][_key][0][0],sigma=sig)) for n in range(amountp)] if (p > combi_dict[kit][_key][0][0] and p < combi_dict[kit][_key][1][0])]
            point_list_l=[point(p,line) for p in [int(rd.gauss(mu=combi_dict[kit][_key][1][0],sigma=sig)) for n in range(amountp)] if (p < combi_dict[kit][_key][1][0] and p > combi_dict[kit][_key][0][0])]
        # def lerp_line(x1,y1,x2,y2,spacing=2):
        #     distance=sqrt((x2-x1)**2+(y2-y1)**2)
        #     lerps=int(distance/spacing)
        #     for i in range(lerps+1):
        #         step=i/float(lerps)
        #         x = lerp(x1, x2, step)
        #         y = int(lerp(y1, y2, step))
        #         if x >= xstart+get_width:
        #             x=xstart+get_width
        #         if y >= ystart+get_height:
        #             y=ystart+get_height
        #         point(x,y)
                
        # for sp in range(ystart, ystart+get_height,yspacing):
        #     lerp_line(x1=xstart, y1=sp, x2=xstart+get_width, y2=sp,spacing=2)
    
    def draw_arc(_key,spacing=int(random(10))):
        stroke(0)
        strokeWeight(random(2))
        get_width=combi_dict[kit][_key][1][0]-combi_dict[kit][_key][0][0]
        get_height=combi_dict[kit][_key][3][1]-combi_dict[kit][_key][0][1]
        xstart=combi_dict[kit][_key][0][0]
        ystart=combi_dict[kit][_key][0][1]
        arcx=xstart+int(get_width/2)
        arcy=ystart+int(get_height/2)
        
        cf=rd.uniform(0,1)
        if cf < .5:
            arc(arcx,arcy,get_width,int(random(5,10)),0,PI)
        elif cf < .9:
            arc(arcx,arcy,get_width,int(random(5,10)),PI,TWO_PI)
        else:
            for arcs in range(ystart,ystart+get_height,spacing):
                arc(arcx,arcs,get_width,int(random(5,10)),0,PI)
    
    def corner_circle(_key,r=5):
        fill(0)
        stroke(0)
        strokeWeight(0)
        loc=rd.choice([0,1,2,3])
        ccx=combi_dict[kit][_key][loc][0]
        ccy=combi_dict[kit][_key][loc][1]
        circle(ccx,ccy,3)
        # while r > 1:
        #     for angle in range(0,360):
        #         px=ccx+sin(radians(angle))*r
        #         py=ccy+cos(radians(angle))*r
        #         if rd.uniform(0,1) > .8 :
        #             point(px,py)
        #     r-=1
        
                    
    for kit in combi_dict:
        for k, v in combi_dict[kit].items():
            if rd.uniform(0,1) >.8:
                draw_rectangles(_key=k)
            # print(combi_dict[kit][k])
            draw_gaussian(_key=k)
            if rd.uniform(0,1) > .9:
                fill_lines(_key=k)
            if rd.uniform(0,1) > .8:
                draw_arc(_key=k)
            elif rd.uniform(0,1) > .8:
                corner_circle(_key=k)
            

    bep=None
    bep2=123
    
    li=[bep,bep2]
    print(li)
    print(None in li)
    
    # filename= ''.join('boxes'+timestamp+'.jpg')
    #save(filename)
    print("End of Program")
    exit()
