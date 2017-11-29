import cv2
import sys
import numpy
import sys
import time
import os
import glob



def new_name():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    naming = "test-data/"+timestr+ ".jpg"
    #print (naming)
    return naming
    
cascPath = "haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    ret,image = video_capture.read()
    if ret is True:
        #Convert to grayscale
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    else:
        continue

    #Look for faces in the image using the loaded cascade file
    faces = faceCascade.detectMultiScale(gray, 1.1, 5)

    #print ("Found "+str(len(faces))+" face(s)")
    no_of_faces = (len(faces))
    print("I Found "+str(no_of_faces)+" in this capture")

    #Draw a rectangle around every found face
    '''for (x,y,w,h) in faces:
        print("Cheese :)")
        #cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)'''

    if (no_of_faces > 0):
        #Save the result image
        naming = new_name()
        
        cv2.imwrite(naming,image)
        print (naming)
    time.sleep(2.0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
