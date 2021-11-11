import cv2
import os
#Read video
cam=cv2.VideoCapture("I&O//demo.mp4")
framecount=0
if not os.path.exists("I&O//frames"):
    os.makedirs("I&O//frames")
os.chdir("I&O//frames")
print(os.getcwd())
ret,frame=cam.read()
while ret:
    name=str(framecount)+".jpg"
    cv2.imwrite(name,frame)
    framecount=framecount+1
    ret,frame=cam.read()
print("Extracted number of frames were"+framecount)
cam.release()
cv2.destroyAllWindows()
