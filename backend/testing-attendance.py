import cv2
import os
import pickle
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np
import cvzone
from PIL import Image
from torch.linalg import norm
import time

#counter = 0

#Load the encodings
def loadEncodings(encode_path):
    encode_file = open(encode_path, "rb")
    list_encodings_ids = pickle.load(encode_file)
    encode_file.close()

    list_of_encodings, student_ids = list_encodings_ids #1-1 mapping between encodings and ids, in the list
    
    return list_of_encodings, student_ids


if __name__ == '__main__':
    
    #Load in, and check!
    encode_path = "Encodings.p"
    list_of_embeddings, student_ids = loadEncodings(encode_path)
    print(student_ids) #NOTE: ids are strings!!!
    print(len(list_of_embeddings))

    #Initialize global variables
    id = -1
    ppl_marked = [] #NOTE: Used for next phase...
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    offsetP_width = 20 #as a percentage, how much increase size!
    offsetP_height = 15
    folder_path = 'images'
    face_localizer = MTCNN(keep_all=True, margin=40)
    embedding_generator = InceptionResnetV1(pretrained='vggface2').eval()

    count = 0
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)

        #TODO: Change with facenet_pytorch
        faces_current_frame_boxes, probs = face_localizer.detect(frame)
        if faces_current_frame_boxes is None: continue
        #faces_current_frame = face_recognition.face_locations(img)
        faces_current_frame = face_localizer(frame)
        #print("Number of faces: ",  len(faces_current_frame) if faces_current_frame is not None else 0)
        embeddings_current_frame = embedding_generator(faces_current_frame) if faces_current_frame is not None else None
        #print("Number of embeddings:", len(embeddings_current_frame) if embeddings_current_frame is not None else 0)

        #Match with list_of_encodings
        for encoded_face, face_loc in zip(embeddings_current_frame, faces_current_frame_boxes):
            #TODO: manual comparison
            face_distances = []
            for db_embedding in list_of_embeddings:
                face_distances.append(norm(encoded_face - db_embedding, ord='fro').item())
            #print(f"Distances: {face_distances}")

        #     #Find the lowest dist one
            match_index = np.argmin(np.array(face_distances))
            if(count == 19):
                print("Match Index: ", match_index)
                print("Student: ", student_ids[match_index])
                
                #x1, y1, x2, y2 -> order for INVERTED IMAGE!!!
                print(face_loc)
            x1, y1, x2, y2 = face_loc #it's a 4-tuple, turns out like this
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            offsetW = (offsetP_width/100) * w
            offsetH = (offsetP_height/100) * h

            bbox = int(x1 - offsetW), int(y1 - offsetH * 3), int(w + offsetW * 2), int(h + offsetH * 3.5)
            img = cvzone.cornerRect(img, bbox, rt=1)
            id = student_ids[match_index]


        if(id == -1): continue
        #If person was detected:
        pp_file = id + ".jpg"
        pp_loc = os.path.join(folder_path, pp_file)
        person = cv2.imread(pp_loc)
        #Show their stored pic, and bbox in live feed
        cv2.imshow("Last Recognized", person)
        cv2.imshow("Face Recognition", img)
        count = (count + 1) % 20

           
        key = 0xFF & cv2.waitKey(1)
        if key == ord('q'):
            break
