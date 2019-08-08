# Photo Database Generator for Neural Networks
### Author: Jacob Crouse
### Date Created: August 6th, 2019
The purpose of this program is to minimize repetitive work necessary when creating large, randomized photo databases which are generally used for training neural networks. Normally when doing this sort of work, it involves superimposing some image over a background in random locations and orientations in order to increase the material the neural network has to train with. But, this can be time-consuming and tedious, so I wanted to create this program to speed that process up.

## Install Dependencies
This python script requires the numpy and Pillow modules. If you don't have Python or these modules installed, you can run:
`sh install_dependencies.sh`
to install all the dependencies (this script only works in Ubuntu Linux at the moment). This script should be run before the python script is used for the first time.

After the dependencies are downloaded, the file can be run using:
`python3 photo_generator.py`
This script only works in Python 3 at the moment.


## Future Changes
In the future, I would like to improve this program by adding the following functionality:
1. ~~Implement ability to print many random copies, instead of just one random copy per fore/background combination.~~
2. ~~Better organize generated photos (put them all in a folder).~~
3. Take folder inputs for fore and background images instead of explicitly stating them. 
4. Improve user-friendliness by making the executable prompt the user for folder locations.
5. Add a simple GUI to improve user-friendliness.
6. Improve extensibility?
