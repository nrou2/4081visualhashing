import os
from PIL import Image
import numpy as np
import math
debug = True
n = 32
print("What image folder within the same directory would you like to scan?")
foldername = input()
filenum = 0
rawimages = []
#Here the initial extraction of the image data happens before we begin the grouping, shortening to greyscale to deal with image shape for now
for filename in os.listdir(foldername):
    filepath = os.path.join(foldername, filename)
    if debug:
        print("scanning file " + str(filenum))
    try:
        #greyscale conversion, so we deal with shapes of objects rather than too much focus on the color details
        image = Image.open(filepath).convert("L")
        #resize to a standardized grid, even if the image is long
        image = image.resize((n, n), Image.Resampling.LANCZOS)
        rawimages.append(image)
    except:
        continue
    if debug:
        filenum+=1
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
        #Calculating once per x value to not repeat it multiple times, since this needs to be executed millions of times on a large folder
        xval = 0

        xval = math.pi*u*((2*x)+1)
        xval = xval / (2*n)
        xval = math.cos(xval)
        
        
        while y < n:
            yval = 0
            yval = math.pi*v*((2*y)+1)
            yval = yval / (2*n)
            yval = math.cos(yval)
            total+=xval*yval*imagematrix[x][y]

            y+= 1
        x += 1
        y = 0
    return total*part1


if debug:
    #Making sure things mathematically make sense and I didn't botch the formula, seems to match on the first image I tested
    print(coefficient(0,0,pixeldata[0]))
    print(np.mean(pixeldata[0]) * n)

#In case editing pixeldata directly corrupts something later
frequencydata = pixeldata.copy()
k = 0
i = 0
j = 0
while k < len(pixeldata):
    if debug:
        print("k =" + str(k))
    while i < n:
        if debug:
            print("I =" + str(i))
        while j < n:
            if debug:
                print("J = " + str(j))
            frequencydata[k][i][j] = coefficient(i,j,pixeldata[k])
            j+=1
        i+=1
    k+=1

print("done")
