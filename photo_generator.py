##################################################################:
# Photo Database Generator                                       #
# Author: Jacob Crouse                                           #
# Date Created: August 6th, 2019                                 #
# Date Modified: August 12th, 2019                               #
# Purpose: This program is for randomly creating superimposed    #
#          images that will be used to train neural networks     #
#          for target recognition and object detection.          #
##################################################################
from PIL import Image
import numpy as np
import os

#calculate cropped sizes for each foreground image
def calcSizes(box_physical_dims, fore_dims, bg_images, numBackgrounds, numForegrounds): #[rows][columns]
    crop_sizes = []

    for bg in range(numBackgrounds): #for each background
        crop_sizes += [[]]
        for fore in range(numForegrounds): #and for each foreground, calculate the cropped image dimensions
                xdim = np.floor(box_physical_dims[fore][0] / bg_physical_dims[0] * bg_images[bg][0].size[0])
                ydim = np.floor(box_physical_dims[fore][1] / bg_physical_dims[1] * bg_images[bg][0].size[1])
                crop_sizes[bg].append([xdim, ydim])

    return crop_sizes

#generate cropped images for all foregrounds for each background
def genCroppedImages(numBackgrounds, numForegrounds, fore_references): #rows = bg, cols = fore
    cropped_fores = []

    for bg in range(numBackgrounds):
        cropped_fores += [[]]
        for fore in range(numForegrounds):
            cropped_fores[bg].append(fore_references[fore].copy()) #add the copy to the array
            cropped_fores[bg][fore] = cropped_fores[bg][fore].resize([int(crop_sizes[bg][fore][0]), int(crop_sizes[bg][fore][1])])

    return cropped_fores

#for each background, create one copy per foreground
def genBackgroundCopies(numBackgrounds, numForegrounds, bg_references, totalPhotosToGenerate, originalPhotoAspectRatio): #rows = bg, cols = fore
    bg_copies = []

    for bg in range(numBackgrounds):
        bg_copies += [[]]
        for fore in range(int(np.floor(totalPhotosToGenerate/numBackgrounds))):
            AR = [bg_references[bg].size[0], bg_references[bg].size[0]*(originalPhotoAspectRatio[1]/originalPhotoAspectRatio[0])]
            
            bg_copies[bg].append(bg_references[bg].copy().crop([0,0,AR[0],AR[1]]))

    return bg_copies

#superimpose each foreground image onto each background image
def superimpose(bg_copies, cropped_fores,totalPhotosToGenerate):
    overflowCounter = 0

    #change the working directory to a pre-generated folder (for organization)
    try:
        foldername = "generated_photos"
        os.mkdir(foldername)
    except:
        print("I would move the generated_photos folder out of the current directory...\n")
        foldername = "generated_photos1"
        os.mkdir(foldername)

    #create the file which will contain the true locations of all the foregrounds
    try:
        filename = "ground_truth.txt"
        f = open(filename, "w+")
    except:
        print("I would move the ground_truth.txt file out of the current directory...\n")
        filename = "ground_truth1.txt"
        f = open(filename, "w+")

    fd = os.open(foldername, os.O_RDONLY)
    os.fchdir(fd)

    for bg in range(numBackgrounds):
        overflowCounter = 0
        for fore in range(int(np.floor(totalPhotosToGenerate/numBackgrounds))):
            #find a random location in the background to paste the foreground
            bg_dim = bg_copies[bg][fore].size
            random_x = np.random.randint(0,bg_dim[0],1) #pixels
            random_y = np.random.randint(0,bg_dim[1],1) #pixels

            #find a random angle by which to rotate the foreground
            random_ang = np.random.randint(0,360,1) #degrees

            #in the event that totalPhotosToGenerate/numBackgrounds>numForegrounds, start with the first fg again
            if (fore >= numForegrounds) and (overflowCounter >= numForegrounds):
                overflowCounter = 0

            #superimpose the image
            bg_copies[bg][fore].paste(cropped_fores[bg][overflowCounter].rotate(random_ang), [random_x, random_y])

            #generate the name, format: bgX_fgX.png
            image_name = "bg" + str(bg) + "_" + "fg" + str(fore) + ".png"

            #save the ground truth info to a text file
            largest_fore_dim = max(cropped_fores[bg][overflowCounter].size)
            to_file = image_name + "," + str(random_x[0]) + "," + str(random_y[0]) + "," + str(random_x[0] + largest_fore_dim)  + "," + str(random_y[0] + largest_fore_dim) + ","
            f.write(to_file)

            #save the image
            bg_copies[bg][fore].save(image_name)
            overflowCounter += 1

    #close the file and folder
    f.close()
    os.close(fd)
    os.chdir("..")



#define constant variables
numPhotosToGeneratePerBackground = int(input("How many photos would you like per background?: "))
originalPhotoAspectRatio = [4,3] #the original aspect ratio of the camera for the background images
bg_physical_dims = (80.56, 60.5) #m, ground dimensions of the image from 25m above the ground
boxDims_red = (0.75, 0.65) #m, dimensions of the post box
boxDims_blue = (1.2, 1.2) #m, dimensions of the post box
boxDims_yellow = (1.5, 1.5) #m, dimensions of the post box
box_physical_dims = (boxDims_red, boxDims_blue, boxDims_yellow)

#import all the foregrounds
os.chdir("foregrounds")
foreground_files = os.listdir(".")
numForegrounds = len(foreground_files)
fore_references = []
fore_dims = []
counter = 0
for file in foreground_files:
    fore_references += [Image.open(file)]
    fore_dims += [fore_references[counter].size]
    counter += 1

#import all the backgrounds
os.chdir("../backgrounds")
background_files = os.listdir(".")
numBackgrounds = len(background_files)
bg_references = []
counter = 0
for file in background_files:
    bg_references += [Image.open(file)]
    counter += 1

os.chdir("..")

totalPhotosToGenerate = numPhotosToGeneratePerBackground * numBackgrounds #number of photos to be generated

#generate the right amount of copies of the background images
bg_copies = genBackgroundCopies(numBackgrounds, numForegrounds, bg_references, totalPhotosToGenerate, originalPhotoAspectRatio)

#calculate the different sizes for the fore images
crop_sizes = calcSizes(box_physical_dims, fore_dims, bg_copies, numBackgrounds, numForegrounds)

#generate the cropped images
cropped_fores = genCroppedImages(numBackgrounds, numForegrounds, fore_references)

#superimpose each foreground onto each background, save the images
superimpose(bg_copies, cropped_fores, totalPhotosToGenerate)
