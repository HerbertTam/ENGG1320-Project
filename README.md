# ENGG1320-Project

Planned Structure of Code:
Please add (done) after the entry if the item is FULLY TESTED AND WORKS.

PART 1: BASIC IMAGEBASE HANDLING
1. a list used to handle the image (imageBase)

2. a function that can recognize a face in a photo taken from the entrance, and check if the new face matches any of the old faces to prevent duplication. If it doesn't, assign a name to and notes down the time in the imageBase, and put the photo in known_image, .

3. a function that can recognize all face in a photo taken from the exit, checks if the faces matches any of the faces in imageBase. If it does, note down the time of the photo, compare the difference in time (see 4.), and output the difference in the log file. Also delete the the faces in known_images and entry in imageBase if a match is found. Ignore all unknown faces.

4. a function that can calculate the difference in time.

5. a function that can add a photo to imageBase

6. a function that can remove a photo from imageBase

PART 2: VIDEO/PHOTOS HANDLING
We need to find a way to either:

a. Take images from the entrance and exit camera live 
    (might have to use arduino) the main function(s) should be able to collect the images from the cameras and analyzes them instantly (see and 3.). Might have to use two separate python files for each camera.
 
b. Take videos from the entrance and exit camera live
    same as a., but need to implement a function that can analyze each video (or every x amount of frames)
 
c. Just use prerecorded videos
    need to implement a function that can analyze each video (or every x amount of frames), as well as calulate the time. the main function should be able to analyze the videos, calculate the time, and perform the analysis (see 2. and 3.)
 
d. Just use pretaken images
    easiest of the four, need to make folders entrance_images and exit_images, containing the images used for analysis. the main function should be be able to extract the photos from these folders. The images should also be named a specific way that shows time.
  
EXTRA THINGS THAT MIGHT BE NESSESARY
1. a way to handle time

2. uniform documentation