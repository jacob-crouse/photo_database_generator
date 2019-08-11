# Photo Database Generator for Neural Networks
### Author: Jacob Crouse
### Date Created: August 6th, 2019
The purpose of this program is to minimize repetitive work necessary when creating large, randomized photo databases which are generally used for training neural networks. Normally when doing this sort of work, it involves superimposing some image over a background in random locations and orientations in order to increase the material the neural network has to train with. But, this can be time-consuming and tedious, so I wanted to create this program to speed that process up.  

At the moment, the script scales the foreground to be a certain size within the background in order to make the image look as if the background image was taken at 25 meters above the ground, with the foregrounds being a certain specified size as per the IMAV ruleset. In the future, I hope to extend this functionality to make it more general.

## Install Dependencies
This python script requires the numpy and Pillow modules. If you don't have Python or these modules installed, you can run:  

`sh install_dependencies.sh`  

to install all the dependencies (this script only works in Ubuntu Linux at the moment). This script should be run before the python script is used for the first time.  

## Setup
Befor running the script, please create 2 folders: "backgrounds" and "foregrounds" in the working directory of the script. As you would expect, place all the photos you would like to use as backgrounds in the "backgrounds" folder and all the photos you would like to use as foregrounds (photos to superimpose over the backgrounds) in the "foregrounds" folder.  

After the dependencies are downloaded, the script can be run using: 

`python3 photo_generator.py`  

At this point, the program will prompt you for a number of randomly-generated composite photos you would like per background image. Input this number and sit back as it generates all these photos and puts them in a script-generated folder called "generated_photos".  

In order to properly train a NN, you will need ground truth information, describing exactly where the foreground was superimposed. This information is provided in `ground_truth.txt` which is formatted in the following way:  

`superimposed_image_name.png,top_left_xval,top_left_yval,bottom_right_xval,bottom_right_yval`  

These two (x,y) values describe a box which surrounds the superimposed image. The coordinate system for these coordinates starts at the top-left corner of the background image and +x moves toward the top-right of the image, and +y moves toward the bottom of the image. The bounding box is slightly larger than the superimposed images in an effort to reduce false-negatives.

This script only works in Python 3 at the moment.


## Future Changes
In the future, I would like to improve this program by adding the following functionality:
1. ~~Implement ability to print many random copies, instead of just one random copy per fore/background combination.~~
2. ~~Better organize generated photos (put them all in a folder).~~
3. ~~Take folder inputs for fore and background images instead of explicitly stating them.~~
4. Improve user-friendliness by making the executable prompt the user for folder locations.
5. Add a simple GUI to improve user-friendliness.
6. Improve extensibility?
