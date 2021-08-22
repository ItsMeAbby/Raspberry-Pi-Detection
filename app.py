import os
from flask import Response
from flask import Flask, request, redirect
from flask import render_template, url_for
import time
import numpy as np
import time
from scipy.spatial import distance as dist
import cv2
import mediapipe as mp
import threading
import json
import base64
import datetime

app = Flask(__name__)


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


@app.route("/read")
def read():
    # return the rendered template
    return render_template("changable_variables.json")


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        data = request.form
        print(data)
        updateJson(data)
        return redirect('/')
        # return render_template("index.html")
    if request.method == "GET":
        print("accessed via get")
        return render_template("index.html")


# @app.route("/sleeping")
# def read_sleep():
#     # return the rendered template
#     return render_template("sleeping.json")


# @app.route("/blinking")
# def read_blink():
#     # return the rendered template
#     return render_template("blinking.json")


def updateJson(data):
    with open("templates/changable_variables.json", "r") as json_file:
        changable_variables_list = json.load(json_file)
        # print(changable_variables_list)
        # print(changable_variables_list["range"]["thresholdVal"]["value"])
        changable_variables_list["range"]["thresholdVal"]["value"] = float(
            data["thresholdVal"])
        changable_variables_list["range"]["timeOfAlarm"]["value"] = float(
            data["timeOfAlarm"])

        changable_variables_list["select"]["alarmOnEdgeCases"]["selected"] = True if data["alarmOnEdgeCases"] == "true" else False

        changable_variables_list["select"]["displayFPS"]["selected"] = True if data["displayFPS"] == "true" else False
        changable_variables_list["select"]["anotateEyes"]["selected"] = True if data["anotateEyes"] == "true" else False
        changable_variables_list["number"]["cameraPort"]["value"] = changable_variables_list[
            "number"]["cameraPort"]["value"] if data["cameraPort"] == "" else int(data["cameraPort"])

        changable_variables_list["number"]["port"]["value"] = changable_variables_list[
            "number"]["port"]["value"] if data["port"] == "" else int(data["port"])
        changable_variables_list["string"]["hostip"]["value"] = changable_variables_list[
            "string"]["hostip"]["value"] if data["hostip"] == "" else data["hostip"]
    # json_file = os.remove("templates/changable_variables.json")
    with open("templates/changable_variables.json", "w") as json_file:
        json.dump(changable_variables_list, json_file, indent=4)
    assignVariables()


def readFromJSON():
    print("reading configured variables")
    global variables_dict
    json_file = open("templates/changable_variables.json", "r")
    variables_dict = json.load(json_file)
    json_file.close()
    return variables_dict


def assignVariables():
    global hostip, port, alarmOnEdgeCases, thresholdVal, timeOfAlarm, cameraPort, displayFPS, anotateEyes
    readFromJSON()
    thresholdVal = variables_dict["range"]["thresholdVal"]["value"]
    timeOfAlarm = variables_dict["range"]["timeOfAlarm"]["value"]
    alarmOnEdgeCases = variables_dict["select"]["alarmOnEdgeCases"]["selected"]
    displayFPS = variables_dict["select"]["displayFPS"]["selected"]
    anotateEyes = variables_dict["select"]["anotateEyes"]["selected"]
    cameraPort = variables_dict["number"]["cameraPort"]["value"]
    port = str(variables_dict["number"]["port"]["value"])
    hostip = variables_dict["string"]["hostip"]["value"]


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[2], eye[3])
    B = dist.euclidean(eye[4], eye[5])
    D = dist.euclidean(eye[6], eye[7])
    E = dist.euclidean(eye[8], eye[9])
    C = dist.euclidean(eye[0], eye[1])
    # compute the eye aspect ratio
    ear_ = (A + B + D + E) / (5.0 * C)
    # return the eye aspect ratio
    return ear_


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame
    global lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def write_json(new_data, filename, value):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[value].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def detection():
    global displayFPS
    global anotateEyes
    global thresholdVal
    global timeOfAlarm

    global cap, outputFrame, lock
    val = thresholdVal
    valU = 0.10
    valD = -0.13

    score = 0

    detectionDo = True
    mp_face_mesh = mp.solutions.face_mesh
    assignVariables()
    with mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
        while True:
            # print(val)
            # draw.rectangle((0,0,_width,_height), outline=0, fill=0)
            # draw.text((x, top),"    DETECTING ....   ",  font=font, fill=255)
            try:

                success, image = cap.read()
            except Exception as e:
                print(e)

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
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    a = [data_point for data_point in face_landmarks.landmark]
                right_eye = [263, 362, 249, 390, 373, 374, 380,
                             381, 382, 466, 388, 387, 386, 385, 384, 398]  #
                req_re = [263, 362, 384, 381, 385, 380, 387, 373, 388, 390]
                req_le = [133, 33, 161, 163, 160, 144, 157, 154, 158, 153]
                left = []
                right = []

                left_eye = [133, 33, 155, 154, 153, 145, 144,
                            163, 7, 173, 157, 158, 159, 160, 161, 246]  #
                for i in range(len(a)):
                    if i in right_eye or i in left_eye:
                        if i in req_le:
                            left.append((a[i].x, a[i].y))
                        if i in req_le:
                            right.append((a[i].x, a[i].y))
                        if anotateEyes:
                            size = np.array([w, h])
                            box = [a[i].x, a[i].y] * size
                            (X, Y) = box.astype(int)
                            cv2.circle(image, (X, Y), 2, (0, 255, 0), -1)

                    # cv2.putText(image, str(i), (X, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.1, (0, 255, 0), 1)
                distanceLeft = a[33].x-a[34].x
                distanceRight = a[264].x-a[359].x

                distanceUP = a[10].z - a[152].z
                if distanceLeft < 0.020:
                    val = 0.27
                    valU = 0.070

                elif distanceLeft < 0.027:
                    val = 0.23
                    if distanceUP < -0.05:
                        val = 0.25
                else:
                    val = 0.225
                    valU = 0.10
                    valD = -0.13

                if distanceLeft < 0.00:
                    cv2.putText(image, " watching left", (150, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    detectionDo = False
                    if alarmOnEdgeCases:
                        score += 1
                elif distanceRight < 0.00:
                    cv2.putText(image, " watching right", (150, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    detectionDo = False
                    if alarmOnEdgeCases:
                        score += 1
                elif distanceUP >= valU:
                    cv2.putText(image, " watching up", (150, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    detectionDo = False
                    if alarmOnEdgeCases:
                        score += 1
                elif distanceUP <= valD:
                    cv2.putText(image, " watching down", (150, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    detectionDo = False
                    if alarmOnEdgeCases:
                        score += 1
                else:
                    detectionDo = True
                if detectionDo:

                    leftEAR = eye_aspect_ratio(left)
                    rightEAR = eye_aspect_ratio(right)

                    ear = (leftEAR + rightEAR) / 2.0
                    # print(ear, val)
                    # cv2.putText(image, str(ear), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3)
                    # print(ear)
                    if ear < val:
                        # print("reached")
                        score += 1
                        #draw = ImageDraw.Draw(_image)
                        #draw.rectangle((0,0,_width,_height), outline=0, fill=0)
                        cv2.putText(image, "BLINKED", (300, 70),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        # draw.text((x, top+8),       "      BLINKED   ",  font=font, fill=255)
                        # disp.image(_image)
                        # disp.display()
                        # GPIO.output(buzzer,GPIO.HIGH)
                        # GPIO.output(led,GPIO.HIGH)
                        # IMAGE SAVE
                        # image_ = cv2.resize(image, (256, 256))
                        # # retval, buffer = cv2.imencode('.jpg', image_)
                        # if retval:

                        # x = datetime.datetime.now()
                        # y = {

                        #     "name": str(x),
                        #     "date": str(x.strftime("%x")),
                        #     "time": str(x.strftime("%X"))
                        # }
                        #     write_json(
                        #         y, "templates/blinking.json", "blinking")
                        # cv2.imwrite("test.jpg", image_)
                        # print(image_)
                    else:
                        #draw.rectangle((0,0,_width,_height), outline=0, fill=0)
                        # disp.clear()
                        # GPIO.output(buzzer,GPIO.LOW)
                        # GPIO.output(led,GPIO.LOW)
                        score = 0
                    if score > timeOfAlarm:

                        cv2.putText(image, "SLEEPING", (200, 400),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                        # disp.clear()
                        # draw.text((x, top+16),       "   SLEEPING   ",  font=font, fill=255)
                        # GPIO.output(buzzer,GPIO.HIGH)
                        # GPIO.output(led,GPIO.HIGH)
                        # sleep(1)
                        # IMAGE SAVE 2
                        # image_ = cv2.resize(image, (256, 256))
                        # # retval, buffer = cv2.imencode('.jpg', image_)
                        # if retval:

                        # x = datetime.datetime.now()
                        # y = {

                        #     "name": str(x),
                        #     "date": str(x.strftime("%x")),
                        #     "time": str(x.strftime("%X"))
                        # }
                        #     write_json(
                        #         y, "templates/blinking.json", "blinking")
                        # cv2.imwrite(str(x)+".jpg", image_)
                        # cv2.putText(image, str(i), (X, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.1, (0, 255, 0), 1)
                else:
                    if score > timeOfAlarm:
                        cv2.putText(image, "Watch Front", (200, 400),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                        # GPIO.output(buzzer,GPIO.HIGH)
                        # GPIO.output(led,GPIO.HIGH)
                        # sleep(1)

            end = time.time()
            totalTime = end - start
            if displayFPS:
                try:
                    fps = 1 / totalTime
                except:
                    pass

                cv2.putText(image, f'FPS: {int(fps)}', (20, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

            with lock:
                outputFrame = image.copy()


if __name__ == '__main__':
    print("starting")
    variables_dict = None
    try:
        assignVariables()
    except Exception as e:
        print(e)
        hostip = "0.0.0.0"
        port = "5000"
        alarmOnEdgeCases = False
        thresholdVal = 0.225
        timeOfAlarm = 15
        cameraPort = 0
        displayFPS = True
        anotateEyes = True
        print("choosing default")

    cap = cv2.VideoCapture(cameraPort)
    outputFrame = None
    lock = threading.Lock()
    t = threading.Thread(target=detection, args=())
    t.daemon = True

    t.start()
    # start the flask app
    app.run(host=hostip, port=port, debug=True,
            threaded=True, use_reloader=False)

    cap.release()
    cv2.destroyAllWindows()
