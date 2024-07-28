import numpy as np
import cv2
from PIL import Image
from cvzone.FaceDetectionModule import FaceDetector
from facenet_pytorch import MTCNN, InceptionResnetV1
import pickle
import os


#Import student images from no-sql db: images folder
def getImages(folder_path):
    folder_path_list = os.listdir(folder_path)
    img_list = []
    student_ids = []
    for path in folder_path_list:
        img_list.append(Image.open(os.path.join(folder_path, path)))
        id = os.path.splitext(path)[0]
        student_ids.append(id)
    return img_list, student_ids

#Generate the encodings
def genEncodings(image_list):
    face_localizer = MTCNN(margin=40)
    encoding_generator = InceptionResnetV1(pretrained='vggface2').eval()
    
    encoding_list = []


    for i, img in enumerate(image_list):
        print(f"{i}: {student_ids[i]}") #debug

        img_cropped = face_localizer(img)
        cv2_image = np.transpose(img_cropped.numpy(), (1, 2, 0))
        cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        img_embedding = encoding_generator(img_cropped.unsqueeze(0))
        #GENERATE ENCODINGS -> TODO: FIX HERE

        encoding_list.append(img_embedding)

        print(type(img_cropped), img_cropped.shape)
        cv2.imshow("Face Recognition", cv2_image)
        
        key = 0xFF & cv2.waitKey(0)
        if key == ord('q'):
            continue


    return encoding_list



if __name__ == '__main__':
    folder_path = 'images'
    
    img_list, student_ids = getImages(folder_path)
    
    print(student_ids)
    print(img_list)

    list_of_encodings = genEncodings(img_list)
    for encoding, id in zip(list_of_encodings, student_ids):
        print(f"{id}: \n {encoding.shape}")
    #print(list_of_encodings)
    store_list_encodings_ids = [list_of_encodings, student_ids]

    #pickle file to efficiently store encodings
    encode_file = open("Encodings.p", "wb") #write binary
    pickle.dump(store_list_encodings_ids, encode_file)
    encode_file.close()