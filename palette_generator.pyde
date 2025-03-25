add_library('pdf')
import datetime
import random as rd
import itertools

scaler=1.3
resolution=10
ow=oh=resolution*3*scaler
w=int(resolution*50*scaler)
h=int(resolution*50*scaler)

color_list=[
            
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
    
    def square_up():
        for i,x in enumerate(range(10,w,50)):
            for j,y in enumerate(range(10,h,50)):
                col=[int(random(0,255)) for t in range(3)]
                print(i, j, col)
                fill(color(*col))
                square(x,y,30)
                fill(0)
                text(str(i)+","+str(j),x,y)
    
    square_up()
    
    # filename= ''.join('boxes'+timestamp+'.jpg')
    # save(filename)
    print("End of Program")
    # exit()
    
    
