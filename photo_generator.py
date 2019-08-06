from PIL import Image

import numpy as np

#define constant variables
numPhotos = 100 #number of photos to be generated
numBackgrounds = 4
backgroundDims = (60.50, 80.56) #m, grounddimensions of the image from 25m above the ground
boxDims_red = (0.75, 0.65) #m, dimensions of the post box
boxDims_blue = (1.2, 1.2) #m, dimensions of the post box
boxDims_yellow = (1.5, 1.5) #m, dimensions of the post box

#import the postbox images
RED = Image.open("red.png")
RED_dims = RED.size
BLUE = Image.open("blue.png")
BLUE_dims = BLUE.size
YELLOW = Image.open("yellow.png")
YELLOW_dims = YELLOW.size

#import the background images
BG1 = Image.open("background1.png")
BG1_dims = BG1.size
BG2 = Image.open("background2.png")
BG2_dims = BG2.size
BG3 = Image.open("background3.png")
BG3_dims = BG3.size
BG4 = Image.open("background4.png")
BG4_dims = BG4.size

#calculate the different sizes for the fore images
#for i in range(numBackgrounds*3):
RED_cropped = RED.copy()
print(np.floor(boxDims_red[0]/backgroundDims[0]*BG1_dims[0]))
print(np.floor(boxDims_red[1]/backgroundDims[1]*BG1_dims[1]))
RED_cropped = RED_cropped.crop((0,0,np.floor(boxDims_red[0]/backgroundDims[0]*BG1_dims[0]),np.floor(boxDims_red[1]/backgroundDims[1]*BG1_dims[1])))
RED_cropped.save("test_RED.png")
BG1_forsi = BG1.copy()
BG1_forsi.save("testBG.png")

#superimpose the images
BG1_forsi.paste(RED_cropped)
BG1_forsi.save("test1.png")

#generate cropped postbox images for each of the backgrounds
#RED_B1 = RED_raw.crop()

#loop through to generate the specified number of images
#for img in range(numPhotos):
#cropped_FORE = []


#def generateCroppedImages(FORE_Raw, BG_dims, cropped_FORE):
#    numBackgrounds = BG_dims/2
#    
#    for back in range(back, numBackgrounds):
#        for fore in PB_Images: #generate copies for each background
#            FORE_cropped[fore] = FORE_Raw[fore].copy()





