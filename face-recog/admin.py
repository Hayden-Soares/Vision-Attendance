import cv2 as cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector
from time import time



if __name__ == '__main__':
    id = 1001 #Change to make it Command Line Argument...


    output_folder_path = 'images'
    confidence_val = 70
    save = True
    offsetP_width = 20 #as a percentage, how much increase size!
    offsetP_height = 15
    cap_width, cap_height = 640, 480
    
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, cap_width)#3 means width
    cap.set(4, cap_height)

    detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img_out = img.copy()

        img, bboxs = detector.findFaces(img, draw=False)

        # Check if any face is detected
        if bboxs:
            # Loop through each bounding box
            for bbox in bboxs:
                # ---- Get Data  ---- #
                x, y, w, h = bbox['bbox']
                score = int(bbox['score'][0] * 100)#score is apparently a list

                # ---- Check Quality ---- #
                if score > confidence_val:
                    
                    # ---- Calc Bigger BB ---- #
                    offsetW = (offsetP_width/100) * w
                    offsetH = (offsetP_height/100) * h

                    x = int(x - offsetW)
                    w = int(w + offsetW * 2)
                    y = int(y - offsetH * 3)
                    h = int(h + offsetH * 3.5)

                    # ---- Avoid below 0 crash! ---- #
                    if x < 0: x = 0
                    if y < 0: y = 0
                    if w < 0: w = 0
                    if h < 0: h = 0

                    # ---- Blurriness Determining ---- #
                    faceImg = img[y:y+h, x:x+w]
                    blur_value = cv2.Laplacian(faceImg, cv2.CV_64F).var()

                    # ---- Draw Data  ---- #
                    cv2.imshow("Face Focus", faceImg)
                    cvzone.putTextRect(img_out, f'Score: {score}% Blur:{int(blur_value)}', (x, y - 10), scale=2, thickness=2)
                    cvzone.cornerRect(img_out, (x, y, w, h))
                
        # Display the image in a window named 'Image'
        cv2.imshow("Image", img_out)
        # Wait for 1 millisecond, and keep the window open, unless input q
        key = 0xFF & cv2.waitKey(1)
        if key == ord('c') and save:
            # ---- Save Image ---- #
            cv2.imwrite(f'{output_folder_path}/{id}.jpg', faceImg)
            save = False

        if key == ord('q'):
            break
