import cv2
import sys
import numpy as np
import sys
import time
import os
import glob

import RPi.GPIO as GPIO

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from threading import  Thread\


subjects = ["", "Sanjeev Ranjan", "Vijay Singh"]

### Musical Note for buzzer

Buzzer = 11

CL = [0, 131, 147, 165, 175, 196, 211, 248]		# Frequency of Low C notes

CM = [0, 262, 294, 330, 350, 393, 441, 495]		# Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]		# Frequency of High C notes

song_1 = [	CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6], # Notes of song1
			CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3], 
			CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
			CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	]

beat_1 = [	1, 1, 3, 1, 1, 3, 1, 1, 			# Beats of song 1, 1 means 1/8 beats
			1, 1, 1, 1, 1, 1, 3, 1, 
			1, 3, 1, 1, 1, 1, 1, 1, 
			1, 2, 1, 1, 1, 1, 1, 1, 
			1, 1, 3	]

### musical Note ends Here

### Musical Function Starts

def setup():
	GPIO.setmode(GPIO.BOARD)		# Numbers GPIOs by physical location
	GPIO.setup(Buzzer, GPIO.OUT)	        # Set pins' mode is output
	global Buzz			        # Assign a global variable to replace GPIO.PWM 
	Buzz = GPIO.PWM(Buzzer, 440)	        # 440 is initial frequency.
	Buzz.start(50)				# Start Buzzer pin with 50% duty ration

def loop():
	print ('\n    Playing song 1...')
	for i in range(1, len(song_1)):		        # Play song 1
		Buzz.ChangeFrequency(song_1[i])	        # Change the frequency along the song note
		time.sleep(beat_1[i] * 0.1)		# delay a note for beat * 0.5s
	time.sleep(1)                                   # Wait a second for next song.
	destory()

def destory():
	Buzz.stop()					# Stop the buzzer
	GPIO.output(Buzzer, 1)		                # Set Buzzer pin to High
	GPIO.cleanup()


### Musical Function Ends
### ---------------------------------------------------------------------------------------------
###----------------------------------------------------------------------------------------------

### Email Function Starts

def sendmail(new_file):
    try:
        fromaddr = "vijay.vijaysingh.singh121@gmail.com"
        toaddr = "vijay.vijaysingh.singh121@gmail.com"
 
        msg = MIMEMultipart()
 
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Pi Security System"
 
        body = "Automated photo Send ..."
 
        msg.attach(MIMEText(body, 'plain'))
 
        filename = "npm_error.png"
        #attachment = open("/home/king/Pictures/npm_error.png", "rb")
        attachment = open(new_file, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
        msg.attach(part)
 
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "Mayasingh")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print("Sending mail Done :)")
    except:
        print("!! Proxy Error ! OR ! Port Not open !!")


### E-Mail Function Ends..
### ---------------------------------------------------------------------------------------------
### ---------------------------------------------------------------------------------------------


### Face Detection and Recognition Function Starts...

###Function To Get New File Name
def new_name():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    naming = "test-data/"+timestr+ ".jpg"
    #print (naming)
    return naming


###function to detect face using OpenCV
def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')   --- Detect Faces using LBPCascade Algoritm . Fast but less Accuracy
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')        #-- Detect Faces using HaarCascade Algoritm . Slow but Good Accuracy
    #faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5);
    faces = faceCascade.detectMultiScale(gray, 1.1, 5)
    if (len(faces) == 0):
        return None, None    
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]


### Fucntion to Train Faces From Images
def prepare_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    for dir_name in dirs:
        if not dir_name.startswith("s"):
            continue;
        label = int(dir_name.replace("s", ""))
        subject_dir_path = data_folder_path + "/" + dir_name
        subject_images_names = os.listdir(subject_dir_path)
        for image_name in subject_images_names:
            if image_name.startswith("."):
                continue;
            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            face, rect = detect_face(image)
            if face is not None:
                faces.append(face)
                labels.append(label)
            
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    
    return faces, labels


### Function To Draw Rectangle And Write Text Around Faces
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)


###  Function To Predict Images
def predict(test_img):
    print("Predicting images...")
    img = test_img.copy()
    face, rect = detect_face(img)
    try:
        label, fault = face_recognizer.predict(face)
        print("fault : "+str(fault))
        label_text = subjects[label]
        draw_rectangle(img, rect)
        draw_text(img, label_text, rect[0], rect[1]-5)
        if fault <=60:                     
            print(subjects[label]+"is a known face")
            return img                          
        else:
            print("Unknown face found")                 #----- coded by sanjeev
            t = Thread(target = sendmail(new_file))                                                                                                           
            t.start()
            t1 = Thread(target = setup())
            t2 = Thread(target = loop())
            t1.start()
            t2.start()
    except:
        print("No face Found")



### Function to Get the name of latest File in the Test-data Directory
def file_name_return():
    list_of_files = glob.glob('test-data/*.*') 
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

### Face Detection and Recognition Function Ends...
### ---------------------------------------------------------------------------------------------
### ---------------------------------------------------------------------------------------------


### Main Program On
 
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)


print("Training Faces From DataSet")
faces, labels = prepare_training_data("training-data")
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, np.array(labels))
print("Training Data Complete")


while True:
    ret,image = video_capture.read()
    if ret is True:
        #Convert to grayscale
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    else:
        continue

    # Face Detection Code .......................
    #Look for faces in the image using the loaded cascade file
    faces = faceCascade.detectMultiScale(gray, 1.1, 5)

    no_of_faces = (len(faces))
    print ("Found "+str(len(faces))+" face(s)")
    if (no_of_faces > 0):
        naming = new_name()
        cv2.imwrite(naming,image)
        #print (naming)
        # Face Detection Code Ends.......................
        
        #Face_Recognition Code ........................
        #load test images
        new_file = file_name_return()
        test_img1 = cv2.imread(new_file)

        #perform a prediction
        predicted_img1 = predict(test_img1)
        #predicted_img2 = predict(test_img2)
        print("Prediction complete")

    time.sleep(1.5)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

### Main Program OFF
### ---------------------------------------------------------------------------------------------
### ---------------------------------------------------------------------------------------------


### Release Resources ..........................

video_capture.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.destroyAllWindows()

