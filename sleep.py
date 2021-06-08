
import time
import RPi.GPIO as GPIO

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
GPIO.setwarnings(False)
#Select GPIO mode
GPIO.setmode(GPIO.BCM)
#Set buzzer - pin 23 as output

buzzer=5
led=16
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(led,GPIO.OUT)
# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
_width = disp.width
_height = disp.height
_image = Image.new('1', (_width, _height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(_image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,_width,_height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = _height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

#font = ImageFont.truetype('fonts/Minecraftia-Regular.ttf',8 )
#draw.rectangle((0,0,_width,_height), outline=0, fill=0)


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[2], eye[3])
    B = dist.euclidean(eye[4], eye[5])
    D = dist.euclidean(eye[6], eye[7])
    E = dist.euclidean(eye[8], eye[9])
    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[1])
    # compute the eye aspect ratio
    ear_ = (A + B + D + E) / (5.0 * C)
    # return the eye aspect ratio
    return ear_


import numpy as np
import time
from scipy.spatial import distance as dist
import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

score = 0
import  glob

for camera in glob.glob("/dev/video?"):
	cap = cv2.VideoCapture(camera)
#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#videoWriter = cv2.VideoWriter("RESULT.mp4", fourcc, 10.0, (640, 480))
with mp_face_mesh.FaceMesh(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    while True:
        draw.rectangle((0,0,_width,_height), outline=0, fill=0)
        draw.text((x, top),"    DETECTING ....   ",  font=font, fill=255)

        success, image = cap.read()
        if not success:
          #  print('failed frame')
            break
        h, w = image.shape[:2]

        start = time.time()

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = face_mesh.process(image)

        image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if not results.multi_face_landmarks:
                GPIO.output(buzzer,GPIO.LOW)
                GPIO.output(led,GPIO.LOW)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                a = [data_point for data_point in face_landmarks.landmark]
            right_eye = [263, 362, 249, 390, 373, 374, 380, 381, 382, 466, 388, 387, 386, 385, 384, 398]  #
            req_re = [263, 362, 384, 381, 385, 380, 387, 373, 388, 390]
            req_le = [133, 33, 161, 163, 160, 144, 157, 154, 158, 153]
            left = []
            right = []

            left_eye = [133, 33, 155, 154, 153, 145, 144, 163, 7, 173, 157, 158, 159, 160, 161, 246]  #
            for i in range(len(a)):
                if i in right_eye or i in left_eye:
                    if i in req_le:
                        left.append((a[i].x, a[i].y))
                    if i in req_le:
                        right.append((a[i].x, a[i].y))
                    size = np.array([w, h])
                    box = [a[i].x, a[i].y] * size
                    (X, Y) = box.astype(int)
                    cv2.circle(image, (X, Y), 2, (0, 255, 0), -1)

                # cv2.putText(image, str(i), (X, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.1, (0, 255, 0), 1)
            leftEAR = eye_aspect_ratio(left)
            rightEAR = eye_aspect_ratio(right)
            ear = (leftEAR + rightEAR) / 2.0
            # cv2.putText(image, str(ear), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3)
#            print(ear)
            if ear < 0.225:
                score += 1
                #draw = ImageDraw.Draw(_image)
                #draw.rectangle((0,0,_width,_height), outline=0, fill=0)
                cv2.putText(image, "BLINKED", (300, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)
                draw.text((x, top+8),       "      BLINKED   ",  font=font, fill=255)
                #disp.image(_image)
                #disp.display()
#                GPIO.output(buzzer,GPIO.HIGH)
 #               GPIO.output(led,GPIO.HIGH)
            else:
                #draw.rectangle((0,0,_width,_height), outline=0, fill=0)
                disp.clear()
                GPIO.output(buzzer,GPIO.LOW)
                GPIO.output(led,GPIO.LOW)
                score = 0
            if score > 10:
                cv2.putText(image, "SLEEPING", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                disp.clear()
                draw.text((x, top+16),       "   SLEEPING   ",  font=font, fill=255)
                GPIO.output(buzzer,GPIO.HIGH)
                GPIO.output(led,GPIO.HIGH)
  #              sleep(1)

        end = time.time()
        totalTime = end - start

        fps = 1 / totalTime

        cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
#        cv2.imshow('MediaPIPE', image)
#        videoWriter.write(image)
        disp.image(_image)
        disp.display()

        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
videoWriter.release()

