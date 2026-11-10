import os
from PIL import Image
import numpy as np
import math

print("What image folder within the same directory would you like to scan?")
foldername = input()

rawimages = []
#Here the initial extraction of the image data happens before we begin the grouping, shortening to greyscale to deal with image shape for now
for filename in os.listdir(foldername):
    filepath = os.path.join(foldername, filename)

    try:#greyscale conversion
        image = Image.open(filepath).convert("L")
        #resize to a standardized grid, even if the image is long
        image = image.resize((32, 32), Image.Resampling.LANCZOS)
        rawimages.append(image)
    except:
        continue

#Now to convert them to pixel arrays so they can be easily worked with

pixeldata = []

for image in rawimages:
    data = np.array(image)
    pixeldata.append(data)


#The phash algorithm uses a discrete cosine transform, the following are pieces that form it.
#This is ultimately done to measure the shape of things rather than raw pixel data, such that minor compression or brightness changes dont count as
#the entire image being different p , and as just a minor change in form..
def normal(k):
    sqrt2 = 1 / math.sqrt(2)
    if k == 0:
        return sqrt2
    else:
        return 1

def coefficient(u,v,imagematrix,n=32):
    #This part is the same for every single X,Y, so it's better to pre calculate it rather than do so hundreds of times later.
    part1 = 2/n * normal(u) * normal(v)
    
    x = 0
    y = 0
    total = 0
    while x < n:
        xval = 0

        xval = math.pi*u*((2*x)+1)
        xval = xval / 2*n
        xval = math.cos(xval)
        
        
        while y < n:
            yval = 0
            yval = math.pi*v*((2*y)+1)
            yval = yval / 2*n
            yval = math.cos(yval)
            total+=xval*yval*imagematrix[x][y]

            y+= 1
        x += 1
        y = 0
    return total*part1


coefficient(0,0,pixeldata[0])

