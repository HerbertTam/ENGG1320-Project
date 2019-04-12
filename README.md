# ENGG1320-Project

The unorganisedFunction.py contains all the codes you guys did on colab. Please read the following and work on the main.py and make sure each part is able to work together.

Planned Structure of Code:

Please add (done) after the entry if the item is FULLY TESTED AND WORKS.

PART 1: BASIC IMAGEBASE HANDLING

1. a list used to handle the image (imageBase).

2. a function that recognizes a face in a photo taken from the entrance, and checks if the new face matches any of the old faces to prevent duplication. If it doesn't, the function assigns a name and notes down the time in the imageBase (see 5.), and puts the photo in known_image.

3. a function that recognizes all the faces in a photo taken from the exit, checks if the faces matches any of the faces in imageBase. If it does, the function notes down the time the photo is taken, compares the difference in time (see 4.), and outputs the entry time (time when the photo was taken from the entrance) and the time difference (time elapsed since entry until exit) into a log file (see 7.). Also deletes the faces in known_images, and the entry in imageBase if a match is found (see 6.). Ignores all unknown faces.

4. a function that calculates the difference in time.

5. a function that adds a photo to imageBase.

6. a function that removes a photo from imageBase.

7. a function that can write the entry time and time difference into a log file in a uniform manner (so the data can be used for poasibly part 3.

PART 2: VIDEO/PHOTOS HANDLING

We need to find a way to either:

a. Take images from the entrance and exit camera live

(might have to use arduino) the main function(s) should be able to collect the images from the cameras and analyzes them instantly (see 2. and 3.). Might have to use two separate python files for each camera.
 
b. Take videos from the entrance and exit camera live

same as a., but need to implement a function that can analyze each video (or every x amount of frames).
 
c. Just use prerecorded videos

need to implement a function that can analyze each video (or every x amount of frames), as well as calulate the time. the main function should be able to analyze the videos, calculate the time, and perform the analysis (see 2. and 3.).
 
d. Just use pretaken images

easiest of the four, need to make folders entrance_images and exit_images, containing the images used for analysis. the main function should be be able to extract the photos from these folders. The images should also be named a specific way that shows time.

PART 3: DATA ANALYSIS

If all the above things are done, we can work on using the data for actually predicting the time the queue would take. Since we would have a log file containing entry time and time elapsed, we would have to find some way to extrapolate the data, possibly with somw machine learning.
  
EXTRA THINGS THAT MIGHT BE NESSESARY

1. a way to handle time.

2. uniform documentation.
