from tokenize import Hexnumber
from PIL import Image, ImageDraw
import math
import random

size_x = 1280
size_y = 720

cRange = 6 # color range (smaller = less color variation)
setting = 'scale' #scale or random
colorStr = "55aaef" #color (without hashtag)

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
    elif setting == 'scale':
        for i in hexNumbers:
            scale = random.randrange(-range_,range_)

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


for i in range(math.floor(size_x/20)):
    for j in range(math.floor(size_y/20)):
        
        square_center = (i*20,j*20)
        square_length = 120

        square_vertices = (
            (square_center[0] + square_length / 2, square_center[1] + square_length / 2),
            (square_center[0] + square_length / 2, square_center[1] - square_length / 2),
            (square_center[0] - square_length / 2, square_center[1] - square_length / 2),
            (square_center[0] - square_length / 2, square_center[1] + square_length / 2)
        )

        square_vertices = [rotated_about(x,y, square_center[0], square_center[1], math.radians(random.randrange(5,175))) for x,y in square_vertices]
        
        img.polygon(square_vertices, fill=f"#{hexCloseTo(colorStr,cRange)}")


img_.save('image.png')