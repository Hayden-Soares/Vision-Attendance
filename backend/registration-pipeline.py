import cv2
import os
import pickle
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np
import cvzone
from PIL import Image
from torch.linalg import norm
import time

def capture_picture(id):
    '''
        Pipeline to save a focused crop of a face!

        \n
        :param id: Unique identification of the user, whose face needs to be saved

        \n
        :return: Location of cropped image saved in cache (Current: Relative, on local machine)
    '''

    cap = cv2.VideoCapture(0)
    #Constants
    IMG_W = 640
    IMG_H = 480
    cap.set(3, 640)
    cap.set(4, 480)
    del_width = 20 #as a percentage, how much size increase!
    del_height = 15
    temp_cache = 'temp_images'

    #Pipeline (TODO: Add spoofing detector!)
    face_localizer = MTCNN(keep_all=True, margin=40)
    embedding_generator = InceptionResnetV1(pretrained='vggface2').eval()

    
    while True:
        count = 0
        blur_value = 0
        #TODO: Wrap in try-except block 
        #(errors possible: success is false, image has no one => None type returned)
        success, img = cap.read()
        
        img = cv2.flip(img, 1)
        img_out = img.copy()
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        
        current_frame_bboxes, _ = face_localizer.detect(frame)
        if current_frame_bboxes is None: 
            continue

        #Not useful here!
        #current_frame_faces = face_localizer(frame)
        #print("Number of faces: ",  len(faces_current_frame))
        #embeddings_current_frame = embedding_generator(current_frame_faces)
        #print("Number of embeddings:", len(embeddings_current_frame))

    
        for face_loc in current_frame_bboxes:
            
            #print(face_loc)
            #x1, y1, x2, y2 -> order for INVERTED IMAGE!!!
            x1, y1, x2, y2 = face_loc 
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            #Adjust bbox slightly, for a better picture
            #Usable for embedding generation and profile picture!
            w, h = x2 - x1, y2 - y1
            dW = (del_width/100) * w
            dH = (del_height/100) * h

            #Final calculation
            X = int(x1 - dW)
            Y = int(y1 - dH * 2)
            W = int(w + dW * 2)
            H = int(h + dH * 2.5)
            bbox = X, Y, W, H

            count += 1

            # ---- Blurriness Determining ---- #
            #Check blurriness for face: only it moves.
            faceImg = img[Y:Y+H, X:X+W]
            blur_value = cv2.Laplacian(faceImg, cv2.CV_64F).var()

            # ---- Draw Data  ---- #
            #Image to save

            flag1 = count > 1 
            flag2 = blur_value < 100
            message = "Ready? Press S to save!"  

            cvzone.putTextRect(img_out, f'Blur:{int(blur_value)}', (X + 5, Y-10), scale=2, thickness=2)
            if flag1: cvzone.putTextRect(img_out, f'CAUTION: ensure single face', (IMG_W // 20, IMG_H-20), scale=1, thickness=2, colorR=(0, 0, 255))
            if flag2: cvzone.putTextRect(img_out, f'Increase Blur Value', (3*IMG_W //5, IMG_H-20), scale=1, thickness=2, colorR=(0, 0, 255))
            cvzone.cornerRect(img_out, bbox, rt=0)

            cv2.imshow("Face Focus", faceImg)
            cv2.imshow(message, img_out)


        #TODO: Avoid saving on local machine, find better way to cache!
        key = 0xFF & cv2.waitKey(1)
        if key == ord('s') and not (flag1 or flag2):
            path = f'{temp_cache}/{id}.jpg'
            try:
                os.remove(path)
            except OSError:
                pass

            cv2.imwrite(path, faceImg)
            temp_cache = path
            break

    return temp_cache


def generate_single_embedding(image_path):
    '''
        Function to generate embedding of a single face!

        \n
        :param image_path: Location of the image containing the single face

        \n
        :return <class 'torch.Tensor'>: 512-D Embedding (as a row vector)
    '''

    if not os.path.exists(image_path):
        print("WTF!")
        return OSError()
    
    face_localizer = MTCNN(margin=40)
    encoding_generator = InceptionResnetV1(pretrained='vggface2').eval()
    
    img = Image.open(image_path)

    img_cropped = face_localizer(img)
    cv2_image = np.transpose(img_cropped.numpy(), (1, 2, 0))
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    img_embedding = encoding_generator(img_cropped.unsqueeze(0))#Shape: [1, 512]

    print(img_embedding.shape)
    return np.squeeze(img_embedding.numpy())#pgvector has support for numpy array, but not torch tensor


def send_user_reg_to_remote():
    #TODO!
    pass




if __name__ == '__main__':

    cached_img_path = capture_picture(4884)

    try:
        generate_single_embedding(cached_img_path)
    except :
        print("Path error")
