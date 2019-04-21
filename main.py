import face_recognition
import cv2
import sys,os
import time
imageBase = list()    #The data structure for handling the images, structure is (image, time)


## Video Stuff
#find faces in a video and saves all the faces it find in known_people (tested and works)
def findFacesInVideo(nameOfVideo, known):
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
            print("processing faces...(this takes a while)")
            batch_of_face_locations = face_recognition.batch_face_locations(frames, number_of_times_to_upsample=0)
            # Now let's list all the faces we found in all 128 frames
            for frame_number_in_batch, face_locations in enumerate(batch_of_face_locations):
                number_of_faces_in_frame = len(face_locations)
                frame_number = frame_count - 128 + frame_number_in_batch
                if (number_of_faces_in_frame != 0):
                    print("I found {} face(s) in frame #{}.".format(number_of_faces_in_frame, frame_number))
                count = 1
                for face_location in face_locations:
                    # Print the location of each face in this frame
                    top, right, bottom, left = face_location
                    print(" - A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
                    if known:
                        name = 'known_people/{}_{}.jpg'.format(frame_number/fps,count)
                    else:
                        name = 'unknown_pictures/{}_{}.jpg'.format(frame_number/fps,count)
                    #cropping the face and saving it in known_people
                    cv2.imwrite(name, cropImage(frames[frame_number_in_batch],top, left, bottom, right))
            # Clear the frames array to start the next batch
            frames = []

## Video Stuff
#find faces in a video and saves all the faces it find in known_people (tested and works)
def findFacesInVideoNoGPU(nameOfVideo, known):
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
        frame_count += 1
        face_locations = face_recognition.face_locations(frame, number_of_times_to_upsample=2)
        number_of_faces_in_frame = len(face_locations)
        print("I found {} face(s) in frame #{}.".format(number_of_faces_in_frame, frame_count))
        count = 1
        for face_location in face_locations:
            # Print the location of each face in this frame
            top, right, bottom, left = face_location
            print(" - A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
            if known:
                name = 'known_people/{}_{}.jpg'.format(frame_count/fps,count)
            else:
                name = 'unknown_pictures/{}_{}.jpg'.format(frame_count/fps,count)
            #cropping the face and saving it in known_people
            cv2.imwrite(name, cropImage(frame,top, left, bottom, right))          

# crops an image (tested and works)
def cropImage(image, top, left, bottom, right):
    return image[top:bottom,left:right]

# removes images which cannot be encoded (tested and works)
def removeNotEncodable(directory):
    listFiles = os.listdir(directory)
    for i in range(len(listFiles)):
        if (listFiles[i].endswith(".jpg")):
            face = face_recognition.load_image_file(directory+'/'+listFiles[i])
            try:
                face_encoding = face_recognition.face_encodings(face)[0]
            except:
                print("removing not encodable image " + directory+'/'+listFiles[i])
                os.remove(directory+'/'+listFiles[i])

# removes images with similar encodings (tested and works)
def removeDuplicates(directory):
    listFiles = os.listdir(directory)
    for i in range(len(listFiles)):
        for j in range(len(listFiles)):
            try:
                if (i != j and listFiles[i].endswith(".jpg") and listFiles[j].endswith(".jpg")):
                    picture1 = face_recognition.load_image_file(directory+'/'+listFiles[i])
                    picture2 = face_recognition.load_image_file(directory+'/'+listFiles[j])
                    encoding1 = face_recognition.face_encodings(picture1)
                    encoding2 = face_recognition.face_encodings(picture2)
                    if (encoding1 and encoding2):
                        if face_recognition.compare_faces([encoding1[0]], encoding2[0]):
                            print("Found duplicate: removing " + directory+'/'+listFiles[j])
                            os.remove(directory+'/'+listFiles[j])
            except:
                continue

# return true or false depending on similarily between two faces (tested and works)
def compareFaces(face_1,face_2):
    face1 =  face_recognition.load_image_file(face_1)
    face2 =  face_recognition.load_image_file(face_2)
    face1_encoding = face_recognition.face_encodings(face1)
    face2_encoding = face_recognition.face_encodings(face2)
    return face_recognition.compare_faces([face1_encoding[0]], face2_encoding[0])

# find matching faces in known_people and unknown_pictures, calculates the time between them, edits data.txt, and removes matching faces (tested and works)
def findMatchingFaces(known_people,unknown_pictures):
    file = open("data.txt","w")
    listKnownFaces = os.listdir(known_people)
    listUnknownFaces = os.listdir(unknown_pictures)
    for i in range(len(listUnknownFaces)):
        for j in range(len(listKnownFaces)):
            try:
                if (listUnknownFaces[i].endswith(".jpg") and listKnownFaces[j].endswith(".jpg")):
                    known_picture = known_people+'/'+listKnownFaces[j]
                    unknown_picture = unknown_pictures+'/'+listUnknownFaces[i]
                    if compareFaces(known_picture,unknown_picture):
                        known_time = float(listKnownFaces[j][:listKnownFaces[j].index('_')])
                        unknown_time = float(listUnknownFaces[i][:listUnknownFaces[i].index('_')])
                        file.write(str(known_time) + " " + str(unknown_time-known_time))
                        file.write("\n")
                        print("Found match: removing " + known_picture + " and " + unknown_picture)
                        os.remove(known_picture)
                        os.remove(unknown_picture)
            except:
                continue
    file.close()

# main function (tested and works!)
def main():
    entrance_video = "in1.mp4"
    exit_video = "in1.mp4"
    findFacesInVideo(entrance_video, True)
    findFacesInVideo(exit_video, False)
    removeNotEncodable("known_people")
    removeNotEncodable("unknown_pictures")
    removeDuplicates("known_people")
    removeDuplicates("unknown_pictures")
    findMatchingFaces('known_people','unknown_pictures')
    f = open("data.txt", "r")
    print(f.read())

main()
