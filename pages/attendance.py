import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone

#counter = 0


#Load the encodings
def loadEncodings(encode_path):
    encode_file = open(encode_path, "rb")
    list_encodings_ids = pickle.load(encode_file)
    encode_file.close()

    list_of_encodings, student_ids = list_encodings_ids #1-1 mapping between encodings and ids, in the list
    
    return list_of_encodings, student_ids

def detect_student():
    #Load in, and check!
    encode_path = "Encodings.p"
    list_of_encodings, student_ids = loadEncodings(encode_path)
    print(student_ids) #NOTE: ids are strings!!!
    print(len(list_of_encodings))

    #Initialize global variables
    id = -1
    ppl_marked = [] #NOTE: Used for next phase...
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    folder_path = 'images'

    while True:
        success, img = cap.read()
        #img = cv2.flip(img, 1)
        img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

        #Detect face in current frame, and encode it (current bottleneck on FPS)
        faces_current_frame = face_recognition.face_locations(img_small)
        encodings_current_frame = face_recognition.face_encodings(img_small, faces_current_frame) #2nd parameter is optional locations

        #Match with list_of_encodings
        for encoded_face, face_loc in zip(encodings_current_frame, faces_current_frame):
            #Do the comparison
            matches = face_recognition.compare_faces(list_of_encodings, encoded_face)
            face_distances = face_recognition.face_distance(list_of_encodings, encoded_face)
            print(f"Matches: {matches}")
            print(f"Distances: {face_distances}")

            #Find the lowest dist one
            match_index = np.argmin(face_distances)
            print("Match Index: ", match_index)
            #See if the lowest dist one is detected...
            if(matches[match_index]):
                y1, x2, y2, x1 = face_loc #it's a 4-tuple, turns out like this
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = x1, y1, x2 - x1, y2 - y1
                img = cvzone.cornerRect(img, bbox, rt=0)
                id = student_ids[match_index]


        if(id == -1): continue
        #If person was detected:
        pp_file = id + ".jpg"
        pp_loc = os.path.join(folder_path, pp_file)
        person = cv2.imread(pp_loc)
        #Show their stored pic, and bbox in live feed
        #cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
        #cv2.imshow("Last Recognized", person)
        cv2.imshow("Face Recognition", img)

        key = 0xFF & cv2.waitKey(1)
        if key == ord('q'):
            break

        return id

