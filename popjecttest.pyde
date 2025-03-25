add_library('pdf')

import datetime
import random as rd

w = 3300
h = 3800
ow = 150
oh = 200
alpha_ = 200
color_list = [[209, 6, 20], [252, 255, 199]]
color_list2 = [[44, 103, 147, alpha_]]

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename = ''.join('lineswitch' + timestamp + '.pdf')

cback = color(245,245,245)

def setup():
    size(w, h, PDF, filename)
    #size(w, h)
    background(cback)
    noLoop()

def draw():

    def calc_flow_matrix(wee, haa, rstep, nstep=0.0005, angles=(0, 360)):
        xoff = 0
        arra = list()
        for ix in range(0, wee, rstep):
            yoff = 0
            xoff += nstep
            cols = list()
            for jy in range(0, haa, rstep):
                yoff += nstep
                noise_val = noise(xoff, yoff)
                angle = map(noise_val, 0.0, 1.0, angles[0], angles[1])
                cols.append(angle)
            arra.append(cols)

        return arra

    flow_angles1 = calc_flow_matrix(
        wee=w, haa=h, rstep=1, nstep=0.0005, angles=(110, 120))

    pg = createGraphics(w, h)
    pg.beginDraw()
    pg.background(255)
    pg.noStroke()
    obdict = dict()
    nobs = 28
    colob = zip(*[rd.sample(range(255), nobs) for i in range(3)])
    for ob in range(nobs):
        obx = int(random(ow,w-ow))
        oby = int(random(oh,h-oh))
        col = colob[ob]
        obdict[col] = {}
        obdict[col].update({"Coordinates": (obx, oby)})
        pg.fill(*colob[ob])
        chance = rd.uniform(0, 1)
        if chance > .8:
            print("circle")
            pg.circle(obx, oby, random(w / 3))
            obdict[col].update({"Shape": "circle"})
            obdict[col].update({"mid": (obx, oby)})
        elif chance > .2:
            print("rect")
            rectw = int(random(200, w / 4))
            recth = int(random(200, h / 4))
            obdict[col].update({"Shape": "rect"})
            obdict[col].update({"mid": (obx + rectw / 2, oby + recth / 2)})
            pg.rect(obx, oby, rectw, recth)
        else:
            print("beam")
            obx = 0
            obdict[col].update({"Shape": "beam"})
            rectw = int(random(1000,w))
            recth = int(random(200, h / 5))
            pg.rect(0, oby, rectw, recth)
            obdict[col].update({"Coordinates": (obx, oby)})
            obdict[col].update({"mid": (obx + rectw / 2, oby + recth / 2)})

    pg.endDraw()
    pg.loadPixels()

    #image(pg, 0, 0)

    # Draw lines from the edge toward the object, increment r until pixel is

    small_line = 100
    max_length = w * 2
    strokeWeight(1)
    for i in range(50000):
        if i % 2500 == 0:
            print(i)
        x = int(random(w))
        y = int(random(h))
        angle = random(360)
        length_line = 0
        if color(pg.pixels[x + y * width]) == -1:
            while True:
                target = PVector().fromAngle(angle).mult(length_line)
                if (0 <= (x + target.x) <= w - 1) and (0 <= (y + target.y) <= h - 1):
                    length_line += 20
                    colorget=color(pg.pixels[(x + int(target.x)) + (y + int(target.y)) * width])
                    if colorget != -1:
                        a = (colorget >> 24) & 0xFF
                        re = (colorget >> 16) & 0xFF 
                        gr = (colorget >> 8) & 0xFF   
                        bl = colorget & 0xFF   
                        #print(obdict[(re,gr,bl)]["mid"])
                        stroke(color(*rd.choice(color_list2)))
                        line(x, y, x + int(target.x), y + int(target.y))
                        #circle(x+int(target.x), y+int(target.y),5)
                        #headingangle
                        stat_angle = flow_angles1[
                            x + int(target.x)][y + int(target.y)]
                        stat_target = PVector().fromAngle(
                            stat_angle).mult(small_line)
                        # print(degrees(stat_target.heading()))
                        stat_targetx=(x + int(target.x)+int(stat_target.x))
                        stat_targety=(y + int(target.y)+int(stat_target.y))
                        if (0 <= stat_targetx <= w - 1) and (0 <= stat_targety <= h - 1):
                            colorget2=color(pg.pixels[stat_targetx + stat_targety * width])
                            if colorget2 != -1:
                                stroke(color(*rd.choice(color_list)))
                                
                                line(x + int(target.x), y + int(target.y),
                                    stat_targetx,
                                    stat_targety)
                            else:
                                stat_targetx=(x + int(target.x)+int(stat_target.x))
                                stat_targety=(y + int(target.y)-int(stat_target.y))
                                if (0 <= stat_targetx <= w - 1) and (0 <= stat_targety <= h - 1):
                                    colorget2=color(pg.pixels[stat_targetx + stat_targety * width])
                                    if colorget2 != -1:
                                        stroke(color(*rd.choice(color_list)))
                                        
                                        line(x + int(target.x), y + int(target.y),
                                            stat_targetx,
                                            stat_targety)
                                    else:
                                        stat_targetx=(x + int(target.x)-int(stat_target.x))
                                        stat_targety=(y + int(target.y)+int(stat_target.y))
                                        if (0 <= stat_targetx <= w - 1) and (0 <= stat_targety <= h - 1):
                                            colorget3=color(pg.pixels[stat_targetx + stat_targety * width])
                                            if colorget3 != -1:
                                                stroke(color(*rd.choice(color_list)))
                                                
                                                line(x + int(target.x), y + int(target.y),
                                                    stat_targetx,
                                                    stat_targety)
                        break
                    elif 0 == (x + target.x) or w == (x + target.x) or h == (y + target.y) or 0 == (y + target.y) or length_line == max_length:
                        stroke(color(*rd.choice(color_list2)))
                        line(x, y, x + int(target.x), y + int(target.y))
                        break
                else:
                    break

    def ezel_inv(w, ow, h, oh):
        noStroke()
        fill(cback)
        rect(0, 0, w, oh)
        rect(0, 0, ow, h)
        rect(0, h - oh, w, oh)
        rect(w - ow, 0, ow, h)

    def ezel(top, sides, c=cback):
        stroke(0)
        strokeWeight(5)
        line(sides, top, w - sides, top)
        line(w - sides, top, w - sides, h - top)
        line(w - sides, h - top, sides, h - top)
        line(sides, h - top, sides, top)

    ezel_inv(w=w, ow=ow, h=h, oh=oh)

    ezel(top=oh, sides=ow)

    print("End of Program")
    exit()
