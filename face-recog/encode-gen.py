import cv2
import face_recognition
import pickle
import os


#Import student images from no-sql db: images folder
def getImages(folder_path):
    folder_path_list = os.listdir(folder_path)
    img_list = []
    student_ids = []
    for path in folder_path_list:
        img_list.append(cv2.imread(os.path.join(folder_path, path)))
        id = os.path.splitext(path)[0]
        student_ids.append(id)
    return img_list, student_ids

#Generate the encodings
def genEncodings(image_list):
    encoding_list = []
    for i, img in enumerate(image_list):
        #print(f"{i}: {student_ids[i]}") #debug

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #opencv uses BGR 
        #GENERATE ENCODINGS
        encoding = face_recognition.face_encodings(img)[0] #face_recog returns list of all detected, we focus on first
        encoding_list.append(encoding)
    return encoding_list



if __name__ == '__main__':
    folder_path = 'images'
    
    img_list, student_ids = getImages(folder_path)
    
    print(student_ids)
    print(len(img_list))

    list_of_encodings = genEncodings(img_list)
    #print(list_of_encodings)
    store_list_encodings_ids = [list_of_encodings, student_ids]

    #pickle file to efficiently store encodings
    encode_file = open("Encodings.p", "wb") #write binary
    pickle.dump(store_list_encodings_ids, encode_file)
    encode_file.close()