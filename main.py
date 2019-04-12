import face_recognition
import cv2
import os
import time
imageBase = list()    #The data structure for handling the images, structure is (image, time)

## Video Stuff
#find faces in a video and saves all the faces it find in known_people (could be the same ppl) (not tested)
def findFacesInVideo(nameOfVideo):
    video_capture = cv2.VideoCapture(nameOfVideo)
    frames = []
    frame_count = 0
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    
    while video_capture.isOpened():
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Bail out when the video file ends
        if not ret:
            break

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        frame = frame[:, :, ::-1]

        # Save each frame of the video to a list
        frame_count += 1
        frames.append(frame)

        # Every 128 frames (the default batch size), batch process the list of frames to find faces
        if len(frames) == 128:
            batch_of_face_locations = face_recognition.batch_face_locations(frames, number_of_times_to_upsample=0)

            # Now let's list all the faces we found in all 128 frames
            for frame_number_in_batch, face_locations in enumerate(batch_of_face_locations):
                number_of_faces_in_frame = len(face_locations)


                frame_number = frame_count - 128 + frame_number_in_batch
                print("I found {} face(s) in frame #{}.".format(number_of_faces_in_frame, frame_number))

                count = 1
                for face_location in face_locations:
                    # Print the location of each face in this frame
                    top, right, bottom, left = face_location
                    print(" - A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

                    #cropping the face and saving it in known_people
                    crop_img = img[bottom:top, left:right]
                    name = 'known_people/{}_{}.jpg'.format(round(frame_number/fps),count)
                    cv2.imwrite(name, crop_img)
                    addData(name)        #add name to imageBase
                    count++

            # Clear the frames array to start the next batch
            frames = []

##face detection (Leon, Aero, Hei) (Depreciated, Video Stuff already includes the operations)
def detectionFace(image, folder):
    import face_recognition
    pic = face_recognition.load_image_file(image)
    face_locations = face_recognition.face_locations(pic)
    return face_locations

##face recognition (Herbert, Vanessa, Joe) (not tested)
#input: folder of known faces, image w/ ppl to be recognised
#output: when the image is taken in seconds (if someone is recognised), return 0 otherwise.
def recognitionFace(unknown_picture,known_people):
    for unknown_picture in face_locations: #check the faces in the image one by one
        for known_face in known_people: #check the faces in known_people one by one
            if face_recognition.compare_faces([face_recognition.face_encodings(known_face)[0]], face_recognition.face_encodings(unknown_picture)[0] == True:
                index = known_face.index('_')
                return known_face[:index]
    return 0


!ls known_people > known.txt
!ls unknown_pictures > unknown.txt
##Identify faces in pictures (Joe)not tested yet!
#input: path of known_people directory, path of a picture from unknown_pictures directory
#output: return match(True) / no match(False)
def identifyFace(path_known_dir, path_unknown_pic):
    unknown_image = face_recognition.load_image_file(path_unknown_pic + "path_unknown_pic") #edited as the pic is inside "unknown_pictures"
  
ry, path of a picture from unknown_pictures directory

##output: return match(True) / no match(False)
def identifyFace(path_known_dir, path_unknown_pic):
  
  unknown_image = face_recognition.load_image_file(path_unknown_pic + "path_unknown_pic") #edited as the pic is inside "unknown_pictures"
  
  jpgname = open(path_known_dir + "known.txt", "r")    #edited as the txt is inside "known_people"
  
    #compare unknown picture with each picture in known_people directory
    #output list of results
    i = 0
    for name in jpgname:
        known_image = face_recognition.load_image_file(path_known_dir + "\\" + name)

        biden_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        results[i] = face_recognition.compare_faces([biden_encoding], unknown_encoding)
        i += 1
  
    #check if True in results[][0] slot when face exists
    boo = False
    for result in results: 
        if result[0] == True:
            boo = True
    return boo

##Data structure (Aero)
def addData(image):
    global imageBase.append([image, time.time()])

#Output time (Aero)
def calcTime(second):
    return (time.time() - second)

#Display time (Aero)
def displayTime(duration):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(duration + "\n")

##main function
def main():
    nameOfVideo = input()
    image = input()
    flag = False
    imageIndex = 0
    duration = 0
    while True:
        known_people = findFacesInVideo(nameOfVideo)
        face_locations = detectionFace(image)
        flag, image = recognitionFace(face_locations,known_people)
        if (flag == True):
            duration = calcTime(imageBase[image][1])
            imageBase.pop(imageIndex)
            displayTime(duration)
            flag = False
