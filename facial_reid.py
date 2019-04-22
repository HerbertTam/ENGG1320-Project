import face_recognition
import cv2
import sys,os

# find faces in a video
def findFacesInVideo(nameOfVideo, known, knownPeople):
    file = open("data.csv","a")
    video_capture = cv2.VideoCapture(nameOfVideo)
    if known:
        print("processing entrance video...")
    else:
        print("processing exit video...")
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
        frame = convertColours(frame)
        frame_count += 1
        face_locations = face_recognition.face_locations(frame, number_of_times_to_upsample=0)
        number_of_faces_in_frame = len(face_locations)
        # print("I found {} face(s) in frame #{}.".format(number_of_faces_in_frame, frame_count))
        count = 1
        for face_location in face_locations:
            # Print the location of each face in this frame
            top, right, bottom, left = face_location
            time = frame_count/fps
            croppedImage = cropImage(convertColours(frame),top, left, bottom, right)
            cv2.imwrite('croppedImage.jpg', croppedImage)
            print("found a face at pixel location Top: {}, Left: {}, Bottom: {}, Right: {} at time {}".format(top, left, bottom, right, round(time,2)))
            if known:
                try:
                    image = face_recognition.load_image_file('croppedImage.jpg')
                    encoding = face_recognition.face_encodings(image, num_jitters=100)[0]
                except:
                    print("image not encodable (probably not a face)")
                    continue
                print("image encodable! ", end='')
                for knownPerson in knownPeople:
                    result = compareEncodings(knownPerson[0],encoding)[0]
                    if result:
                        print("person known! ", end='')
                        knownPerson[0].append(encoding) # adds the encoding into the array of known encodings
                        break
                    else:
                        continue
                else:
                    print("person not known!\nadding person to known people. ", end='')
                    knownPeople.append([[encoding],time]) # adds the first encoding in an array and time of first encoding to knownPeople
            else:
                try:
                    image = face_recognition.load_image_file('croppedImage.jpg')
                    encoding = face_recognition.face_encodings(image, num_jitters=100)[0]
                except:
                    print("image not encodable (probably not a face)")
                    continue
                print("image encodable! ", end='')
                for knownPerson in knownPeople:
                    if compareEncodings(knownPerson[0],encoding)[0]:
                        print("person known! updating data.txt and removing person from known people. ", end='')
                        # append the the time of first encoding and difference in time between the time of first encoding and time of reidentification 
                        # in the exit video into data.txt
                        file.write(str(knownPerson[1]) + "," + str(time-knownPerson[1]))
                        file.write("\n")
                        knownPeople.remove(knownPerson)
                        break
                else:
                    print("person not known! ", end='')
            count += 1
            os.remove("croppedImage.jpg") # removes croppedImage.jpg after usage
            print("number of known people =",len(knownPeople))
        if not known:
            if len(knownPeople) == 0:
                print("there are no more known people to be reidentified.")
                break
    if not known:
        print("data appended to data.csv!")
    file.close()
    return knownPeople

# convert colours to allow opencv/face_recognition to process the image
def convertColours(image):
    return image[:, :, ::-1]

# crops an image (tested and works)
def cropImage(image, top, left, bottom, right):
    return image[top:bottom,left:right]

def compareEncodings(arrayOfEncodings,newEncoding):
    return face_recognition.compare_faces(arrayOfEncodings, newEncoding, tolerance=0.5)
  
# main function (tested and works!)
def main():
    knownPeople = [] # arrays of encodings of each person and time of first encoding
    entrance_video = "in4.mp4" # change this
    exit_video = "out4.mp4" # and this
    knownPeople = findFacesInVideo(entrance_video, True, knownPeople)
    knownPeople = findFacesInVideo(exit_video, False, knownPeople)

main()
