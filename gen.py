from PIL import Image, ImageDraw, ImageFont
import math
import numpy
import random

size_x = 1920
size_y = 1080

cRange = 6 # color range (smaller = less color variation)
setting = 'shade' #shade or random
colorStr = "222222" #color (without hashtag)
mode = "grid" #grid or random
square_length = 120

def hexCloseTo(str_,range_):
    hexNumbers = [str_[i:i+2] for i in range(0, len(str_), 2)]
    outputNumbers = []
    if setting == 'random':
        for i in hexNumbers:
            number = int(i,16)
            number += random.randrange(-range_,range_)
            if number > 255: number = 255
            if number < 0: number = 0

            number = ("0"+str(hex(number))[2:])[-2:]
            outputNumbers.append(number)
    elif setting == 'shade':
        scale = random.randrange(-range_,range_)
        for i in hexNumbers:
            number = int(i,16)
            number += scale
            if number > 255: number = 255
            if number < 0: number = 0

            number = ("0"+str(hex(number))[2:])[-2:]
            outputNumbers.append(number)
        
    return "".join(outputNumbers)


def distance(ax, ay, bx, by):
    return math.sqrt((by - ay)**2 + (bx - ax)**2)

#rotates point `A` about point `B` by `angle` radians clockwise.
def rotated_about(ax, ay, bx, by, angle):
    radius = distance(ax,ay,bx,by)
    angle += math.atan2(ay-by, ax-bx)
    return (
        round(bx + radius * math.cos(angle)),
        round(by + radius * math.sin(angle))
    )

img_ = Image.new("RGB",(size_x,size_y))
img = ImageDraw.Draw(img_)

if mode == "random":
    for i in range(math.floor(size_x/20*(120/square_length))):
        for j in range(math.floor(size_y/20*(120/square_length))):
            square_center = (i*(square_length/6),j*(square_length/6))
            
            square_vertices = (
                (square_center[0] + square_length / 2, square_center[1] + square_length / 2),
                (square_center[0] + square_length / 2, square_center[1] - square_length / 2),
                (square_center[0] - square_length / 2, square_center[1] - square_length / 2),
                (square_center[0] - square_length / 2, square_center[1] + square_length / 2)
            )

            square_vertices = [rotated_about(x,y, square_center[0], square_center[1], math.radians(random.randrange(5,175))) for x,y in square_vertices]
            
            img.polygon(square_vertices, fill=f"#{hexCloseTo(colorStr,cRange)}")
elif mode == "grid":
    slope = random.random()
    perpSlope = -1/slope
    angle = math.atan(slope)

    for i in range(int(math.floor(size_x/120+30*(120/square_length)))):
        for j in range(int(math.floor(size_y/120+30*(120/square_length)))):
            d = square_length*i / 1.5 #distance
            #print(d)
            jd = square_length*j

            #help: https://math.stackexchange.com/questions/175896/finding-a-point-along-a-line-a-certain-distance-away-from-another-point
            p0 = [0,0]
            p1 = [4,4*slope]

            v = [x-y for x,y in list(zip(p0,p1))]
            u = [float(k/numpy.abs(k)) * d for k in v]

            #result = u (i hope)
            #print(u)

            #help: https://www.mathworks.com/matlabcentral/answers/484422-how-to-find-the-coordinates-of-a-point-perpendicular-to-a-line-knowing-the-distance

            perpYint = u[1] - perpSlope*u[0]
            centerX = u[0]+(jd*math.sqrt(1/(1+perpSlope**2)))*-1
            centerY = u[1]+(perpSlope*jd*math.sqrt(1/(1+perpSlope**2)))*-1

            square_center = (centerX+3000,centerY+1000)

            square_vertices = (
                (square_center[0] + square_length / 2, square_center[1] + square_length / 2),
                (square_center[0] + square_length / 2, square_center[1] - square_length / 2),
                (square_center[0] - square_length / 2, square_center[1] - square_length / 2),
                (square_center[0] - square_length / 2, square_center[1] + square_length / 2)
            )

            square_vertices = [rotated_about(x,y, square_center[0], square_center[1], angle) for x,y in square_vertices]
            
            img.polygon(square_vertices, fill=f"#{hexCloseTo(colorStr,cRange)}")

img_.save('image.png')