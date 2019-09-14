##################################################################:
# Photo Database Generator                                       #
# Author: Jacob Crouse                                           #
# Date Created: August 6th, 2019                                 #
# Date Modified: September 14th, 2019                            #
# Purpose: This program is for randomly creating superimposed    #
#          images that will be used to train neural networks     #
#          for target recognition and object detection.          #
##################################################################
from PIL import Image
import numpy as np
import os

#calculate cropped sizes for each foreground image
def calcSizes(box_physical_dims, bg_physical_dims, bg_images, numBackgrounds, numForegrounds): #[rows][columns]
    crop_sizes = []

    for bg in range(numBackgrounds): #for each background
        crop_sizes += [[]]
        for fore in range(numForegrounds): #and for each foreground, calculate the cropped image dimensions
                xdim = np.floor(box_physical_dims[fore][0] / bg_physical_dims[bg][0] * bg_images[bg][0].size[0])
                ydim = np.floor(box_physical_dims[fore][1] / bg_physical_dims[bg][1] * bg_images[bg][0].size[1])
                crop_sizes[bg].append([xdim, ydim])

    return crop_sizes

#generate cropped images for all foregrounds for each background
def genCroppedImages(numBackgrounds, numForegrounds, fore_references,crop_sizes): #rows = bg, cols = fore
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
def superimpose(bg_copies, numBackgrounds, cropped_fores, numForegrounds, totalPhotosToGenerate):
    overflowCounter = 0

    #change the working directory to a pre-generated folder (for organization)
    try:
        foldername = "generated_photos1"
        os.mkdir(foldername)
    except:
        base = "generated_photos"
        i = 2
        error = True
        while error == True:
            print("%s already exists. Trying %s..." % (foldername, base+str(i)))
            foldername = base + str(i)
            try:
                os.mkdir(foldername)
                error = False
            except:
                i += 1
                continue

    #create the file which will contain the true locations of all the foregrounds
    allnames = os.listdir(".")
    alreadyExists = True
    i = 1
    base = "ground_truth"

    while alreadyExists == True:#checking to make sure I'm not overwriting a previous ground_truth.txt
        counter = 1
        filename = "ground_truth" + str(i) + ".txt"

        for name in allnames:#checking the currently proposed filename against everything in the current directory
            if name == filename:
                print("%s already exists. Trying %s..." % (filename, base+str(i+1)+".txt"))
                break
            elif name != filename and counter == len(allnames):
                alreadyExists = False
                break

            counter += 1

        i += 1

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
            print("photo %d generated." % var.photosGenerated)
            var.photosGenerated += 1

    #close the file and folder
    f.close()
    os.close(fd)
    os.chdir("..")



#define the class to instantiate a static variable
class var:
    photosGenerated = 1


#define the main script of the function
def main():
    #define constant variables
    numPhotosToGeneratePerBackground = int(input("How many photos would you like per background?: "))

    #read in the input file parameters
    f = open("input.txt", "r")
    row = f.readlines()

    bg_physical_dims = [] 
    box_physical_dims = [] 
    i = 0
    sec = 0
    ontext = False

    while i < len(row):
        #logic for determining what sort of value the current line contains
        if row[i] == "ar\n":
            ontext = True
        if row[i] == "bg\n":
            sec += 1
            ontext = True
        elif row[i] == "fg\n":
            sec += 1
            ontext = True

        if sec == 0 and ontext == False:#current line is an aspect ratio value
            tmp = row[i].split(",")
            originalPhotoAspectRatio = [int(tmp[0]), int(tmp[1])]
            #print(originalPhotoAspectRatio)
        elif sec == 1 and ontext == False:#current line is a background physical dimension
            tmp = row[i].split(",")
            bg_physical_dims.append((float(tmp[0]), float(tmp[1])))
            #print(bg_physical_dims)
        elif sec == 2 and ontext == False:#current line is a foreground physical dimension
            tmp = row[i].split(",")
            box_physical_dims.append((float(tmp[0]), float(tmp[1])))
            #print(box_physical_dims)

        ontext = False
        i += 1

    f.close()

    #convert the lists to tuples (immutable)
    bg_physical_dims = tuple(bg_physical_dims)
    box_physical_dims = tuple(box_physical_dims)

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

    print("Total photos to be generated: %d" % (numPhotosToGeneratePerBackground*numBackgrounds))

    totalPhotosToGenerate = numPhotosToGeneratePerBackground * numBackgrounds #number of photos to be generated

    #generate the right amount of copies of the background images
    bg_copies = genBackgroundCopies(numBackgrounds, numForegrounds, bg_references, totalPhotosToGenerate, originalPhotoAspectRatio)

    #calculate the different sizes for the fore images
    crop_sizes = calcSizes(box_physical_dims, bg_physical_dims, bg_copies, numBackgrounds, numForegrounds)

    #generate the cropped images
    cropped_fores = genCroppedImages(numBackgrounds, numForegrounds, fore_references, crop_sizes)

    #superimpose each foreground onto each background, save the images
    superimpose(bg_copies, numBackgrounds, cropped_fores, numForegrounds, totalPhotosToGenerate)

if __name__ == "__main__":
    main()
