##################################################################
# Photo Database Generator                                       #
# Author: Jacob Crouse                                           #
# Date Created: August 6th, 2019                                 #
# Date Modified: August 6th, 2019                                #
# Purpose: This program is for randomly creating superimposed    #
#          images that will be used to train neural networks     #
#          for target recognition and object detection.          #
##################################################################
from PIL import Image

#define constant variables
numPhotos = 100 #number of photos to be generated
numBackgrounds = 4
numForegrounds = 3
background_dims = (60.50, 80.56) #m, grounddimensions of the image from 25m above the ground
boxDims_red = (0.75, 0.65) #m, dimensions of the post box
boxDims_blue = (1.2, 1.2) #m, dimensions of the post box
boxDims_yellow = (1.5, 1.5) #m, dimensions of the post box
box_physical_dims = (boxDims_red, boxDims_blue, boxDims_yellow)

#import the postbox images
RED = Image.open("red.png")
RED_dims = RED.size
BLUE = Image.open("blue.png")
BLUE_dims = BLUE.size
YELLOW = Image.open("yellow.png")
YELLOW_dims = YELLOW.size
fore_dims = (RED_dims, BLUE_dims, YELLOW_dims)
fore_references = (RED, BLUE, YELLOW)

#import the background images
BG1 = Image.open("background1.png")
BG1_dims = BG1.size
BG2 = Image.open("background2.png")
BG2_dims = BG2.size
BG3 = Image.open("background3.png")
BG3_dims = BG3.size
BG4 = Image.open("background4.png")
BG4_dims = BG4.size
bg_dims = (BG1_dims, BG2_dims, BG3_dims, BG4_dims)
bg_references = (BG1, BG2, BG3, BG4)

#calculate the different sizes for the fore images
crop_sizes = calcSizes(physical_dims, fore_dims, bg_dims)

#generate the cropped images
cropped_images = genCroppedImages(numBackgrounds, numForegrounds, fore_references)

#generate the right amount of copies of the background images
bg_copies = generateBackgroundCopies(numBackgrounds, numForegrounds)

#superimpose each foreground onto each background, save the images
superimpose(bg_references, fore_references)


#A single image test
""" 
RED_cropped = RED.copy()
print(np.floor(boxDims_red[0]/background_dims[0]*BG1_dims[0]))
print(np.floor(boxDims_red[1]/background_dims[1]*BG1_dims[1]))
RED_cropped = RED_cropped.crop((0,0,np.floor(boxDims_red[0]/background_dims[0]*BG1_dims[0]),np.floor(boxDims_red[1]/background_dims[1]*BG1_dims[1])))
RED_cropped.save("test_RED.png")
BG1_forsi = BG1.copy()
BG1_forsi.save("testBG.png")

#superimpose the images
BG1_forsi.paste(RED_cropped)
BG1_forsi.save("test1.png")
"""

#calculate cropped sizes for each foreground image
def calcSizes(physical_dims, fore_dims, bg_dims): #rows = bg, cols = fore
    crop_sizes = []

    for bg in bg_dims: #for each background
        for fore in fore_dims: #and for each foreground, calculate the cropped image dimensions
                xdim = box_physical_dims[fore][0] / background_dims[0] * bg_dims[bg][0]
                ydim = box_physical_dims[fore][1] / background_dims[1] * bg_dims[bg][1]
                crop_sizes[bg][fore] = (xdim, ydim)

    return crop_sizes

#generate cropped images for all foregrounds for each background
def genCroppedImages(numBackgrounds, numForegrounds, fore_references): #rows = bg, cols = fore
    cropped_fores = []

    for bg in range(numBackgrounds):
        for fore in range(numForegrounds):
            cropped_fores[bg][fore] = fore_references[fore].copy().crop(0,0,crop_sizes[bg][fore][0], crop_sizes[bg][fore][1])

    return cropped_fores

#for each background, create one copy per foreground
def genBackgroundCopies(numBackgrounds, numForegrounds): #rows = bg, cols = fore
    bg_copies = []

    for bg in range(numBackgrounds):
        for fore in range(numForegrounds):
            bg_copies[bg][fore] = bg_references[bg].copy()

    return bg_copies

#superimpose each foreground image onto each background image
def superimpose(bg_references, fore_references):

    for bg in bg_references:
        for fore in fore_references:
            #superimpose the image
            bg_copies[bg][fore].paste(cropped_fores[bg][fore])

            #generate the name, format: bgX_fgX.png
            filename = "bg" + str(bg) + "_" + "fg" + str(fore) + ".png"

            #save the image
            bg_copies[bg][fore].save(filename)

