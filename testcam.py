import cv2, glob

for camera in glob.glob("/dev/video?"):
    c = cv2.VideoCapture(camera)
for i in range(1000):
	ret,frame=c.read()
	cv2.imshow(frame)

c.release()
cv2.destroyWindows()
	
	
