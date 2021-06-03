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

# cap = cv2.VideoCapture(0)
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# videoWriter = cv2.VideoWriter("MIDEAPIPE_SLEEPING_DETECTTION.mp4", fourcc, 20.0, (640, 480))
with mp_face_mesh.FaceMesh(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    # while cap.isOpened():
        image = cv2.imread('best-face-oil.png')
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
            print(ear)
            if ear < 0.225:
                score += 1
                cv2.putText(image, "BLINKED", (300, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                score = 0
            if score > 10:
                cv2.putText(image, "SLEEPING", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        end = time.time()
        totalTime = end - start

        fps = 1 / totalTime

        cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
        cv2.imwrite('MediaPIPE.png', image)
        # videoWriter.write(image)

#         if cv2.waitKey(5) & 0xFF == 27:
#             break
# cap.release()
# videoWriter.release()
# cv2.destroyAllWindows()
