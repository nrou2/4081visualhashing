import os
from PIL import Image
import numpy as np
import math
debug = False
superdebug = False
n = 16
print("What image folder within the same directory would you like to scan?")
foldername = input()
filenum = 0
rawimages = []
print("Scanning images....")
      
#Here the initial extraction of the image data happens before we begin the grouping, shortening to greyscale to deal with image shape for now
for filename in os.listdir(foldername):
    filepath = os.path.join(foldername, filename)
    if superdebug:
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
print("Preprocessing reused variables....")
#Now to convert them to pixel arrays so they can be easily worked with

pixeldata = []

for image in rawimages:
    data = np.array(image, dtype=np.float64)
    pixeldata.append(data)

#Precalculate cosines so they arent redone millions of times
cosines = []
u = 0
while u < n:
    row = []
    x = 0
    while x < n:
        row.append(math.cos(math.pi*u*(2*x+1)/(2*n)))
        x+=1
    cosines.append(row)
    u+=1


    

#The phash algorithm uses a discrete cosine transform, the following are pieces that form it.
#This is ultimately done to measure the shape of things rather than raw pixel data, such that minor compression or brightness changes dont count as
#the entire image being different p , and as just a minor change in form..
def normal(k):
    sqrt2 = 1 / math.sqrt(2)
    if k == 0:
        return sqrt2
    else:
        return 1


#Precompute the normals as well
#This part is the same for every single X,Y, so it's better to pre calculate it rather than do so hundreds of times later.
#part1 = 2/n * normal(u) * normal(v)
part1s = [[0 for thing in range(n)] for thing in range(n)]
u = 0
v = 0
while u < n:
    v=0
    while v < n:    
        part1s[u][v] = 2/n * normal(u) * normal(v)
        v+=1
        
    u+=1
def coefficient(u,v,imagematrix,n=32):

    
    
    x = 0
    y = 0
    total = 0
    while x < n:
        #Calculating once per x value to not repeat it multiple times, since this needs to be executed millions of times on a large folder
        xval = 0

        xval = cosines[u][x]
        
        
        while y < n:
            yval=cosines[v][y]
            total+=xval*yval*imagematrix[x][y]

            y+= 1
        x += 1
        y = 0
    return total*part1s[u][v]


if debug:
    #Making sure things mathematically make sense and I didn't botch the formula, seems to match on the first image I tested
    print(coefficient(0,0,pixeldata[0],n))
    print(np.mean(pixeldata[0]) * n)


#In case editing pixeldata directly corrupts something later
frequencydata = [image.copy() for image in pixeldata]
k = 0
i = 0
j = 0
half = False
halfway = len(pixeldata) / 2
print("Calculating frequencies of each image....")
while k < len(pixeldata):
    i = 0
    j = 0
    if not half and k > halfway:
        print("Halfway through processing image frequency...")
        half = True
    if debug:
        print("k =" + str(k))
    while i < n:
        if superdebug:
            print("I =" + str(i))
        while j < n:
            if superdebug:
                print("J = " + str(j))
            frequencydata[k][i][j] = coefficient(i,j,pixeldata[k],n)
            j+=1
        j = 0
        i+=1
    k+=1

print("done")
