import os
import datetime
import cv2 as cv
import filetype
def check_file(path):
    kind = filetype.guess(path)
    if kind is None:
        #print('Cannot guess file type!')
        return -1
    mime=kind.mime
    return mime.find("video")
dirName=input("Enter the address of the directory\n")
listOfFiles = list()
duration=0
for (dirpath, dirnames, filenames) in os.walk(dirName):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]
for li in listOfFiles:
    #if os.path.isfile(li) and (check_file(li)!=-1):
    if os.path.isfile(li) and (li.endswith('.mp4')):
        data=cv.VideoCapture(li)
        frames=data.get(cv.CAP_PROP_FRAME_COUNT)
        fps=int(data.get(cv.CAP_PROP_FPS))
        seconds = int(frames / fps)
        duration=duration+seconds
video_time = str(datetime.timedelta(seconds=duration))
print(video_time)
