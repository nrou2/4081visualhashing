import os
from PIL import Image
import numpy as np

print("What image folder within the same directory would you like to scan?")
foldername = input()

rawimages = []
#Here the initial extraction of the image data happens before we begin the grouping, shortening to RGB so we don't try to compare transparency against jpgs
for filename in os.listdir(foldername):
    filepath = os.path.join(foldername, filename)

    try:
        image = Image.open(filepath).convert("RGB")
        images.append(image)
    except:
        continue

#Now to convert them to pixel arrays so they can be easily worked with

pixeldata = []

for image in rawimages:
    data = np.array(image)
    pixeldata.append(data)


