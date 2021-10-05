import cv2, numpy as np
import sys
from time import sleep
import math

def flick(x):
    pass

frame_rate = 30 # the rate of video
videoNames = ['shake.avi', # video path and name
              '4.mp4',
              '4.mp4',
              '4.mp4']
winNums = len(videoNames) # number of video to display -> it should not be greater than 4

if winNums > 4:
    print('Number of video should not be greater than 4.')
    sys.exit(1)

cv2.namedWindow('image', 0)
cv2.moveWindow('image', 250, 150)
cv2.namedWindow('controls')
cv2.moveWindow('controls',150, 50)

controls = np.zeros((50, 250), np.uint8)
cv2.putText(controls, "W/w: Play, S/s: Stay, Esc: Exit", (0,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155)


caps = []
totalFrames = []
for file in videoNames:
    video = cv2.VideoCapture(file)
    caps.append(video)
    totalFrames.append(video.get(cv2.CAP_PROP_FRAME_COUNT))
print(totalFrames)
frameIndex = [0 for i in range(winNums)]
winIndex = 0
preWinIndex = 0
images = []
trackBarNames = []

for i in range(winNums):
    trackBarName = str(i) + 'video'
    cv2.createTrackbar(trackBarName, 'image', 0, int(totalFrames[i]) - 1, flick)
    cv2.setTrackbarPos(trackBarName, 'image', 0)
    trackBarNames.append(trackBarName)

def process(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

status = 'stay'

while True:
    cv2.imshow("controls", controls)
    images.clear()

    try:
        maxWidth = 0
        maxHight = 0
        for i in range(len(frameIndex)):
            if (frameIndex[i] == (totalFrames[i] - 1)):
                frameIndex[i] = 0
            cap = caps[i]
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(frameIndex[i]))
            ret, image = cap.read()
            images.append(image)
            maxWidth = max(maxWidth, image.shape[1])
            maxHight = max(maxHight, image.shape[0])

        print('max:', maxWidth, maxHight)
        for i in range(len(images)):
            image = images[i]
            hight = int(image.shape[0])
            width = int(image.shape[1])
            print('info:', hight, width)
            insertColL = int(math.floor(abs(maxWidth - width) / 2))
            insertColR = maxWidth - width - insertColL
            #image = np.concatenate((np.zeros((hight, insertColL, 3), dtype=int), image), axis=1) # col left
            #image = np.concatenate((image, np.zeros((hight, insertColR, 3), dtype=int)), axis=1) # col right
            insertRowUp = int(math.floor((maxHight - hight) / 2))
            insertRowDown = maxHight - hight - insertRowUp
            #image = np.concatenate((np.zeros((insertRowUp, maxWidth, 3), dtype=int), image), axis=0) # row up
            #image = np.concatenate((image, np.zeros((insertRowDown, maxWidth), 3, dtype=int)), axis=0) # row down
            print(insertColL, ' ', insertColR, ' ', insertRowUp, ' ', insertRowDown, ' ')
            image = cv2.copyMakeBorder(image, top=insertRowUp, bottom=insertRowDown, left=insertColL, right=insertColR, borderType= cv2.BORDER_CONSTANT, value=[0,0,0] )
            print('shape', image.shape)

        for im in images:
            print('images:', im.shape)

        if 4 == winNums:
            imageUp = np.hstack(tuple(images[0 : 2]))
            imageDown = np.hstack(tuple(images[2 : 4]))
            imageFull = np.vstack((imageUp, imageDown))
        else:
            imageFull = np.hstack(tuple(images))

        #imageFull = temp #final image to display

        #r = 1200.0 / imageFull.shape[1]
        #dim = (1200, int(imageFull.shape[0] * r))
        #imageFull = cv2.resize(imageFull, dim, interpolation = cv2.INTER_AREA)
        #if imageFull.shape[0] > 600:
            #imageFull = cv2.resize(imageFull, (500,500))
            #controls = cv2.resize(controls, (imageFull.shape[1],25))

        height, width = imageFull.shape[0], imageFull.shape[1]
        widthNew = 1280
        heightNew = 720
        if width / height >= widthNew / heightNew:
            imageFull = cv2.resize(imageFull, (widthNew, int(height * widthNew / width)))
        else:
            imageFull = cv2.resize(imageFull, (int(width * heightNew / height), heightNew))

        #cv2.putText(im, status, )
        cv2.imshow('image', imageFull)

        status = {  ord('s'):'stay', ord('S'):'stay',
                    ord('w'):'play', ord('W'):'play',
                    -1: status, 
                    27: 'exit'}[cv2.waitKey(10)]

        if status == 'play':
            sleep((0.1 - frame_rate / 1000.0) ** 21021)
            for i in range(len(frameIndex)):
                frameIndex[i] += 1
                cv2.setTrackbarPos(trackBarNames[i],'image',frameIndex[i])
            continue
        if status == 'stay':
            for i in range(len(frameIndex)):
                frameIndex[i] = cv2.getTrackbarPos(trackBarNames[i],'image')

        if status == 'exit':
            break  
    

    except KeyError:
        print("Invalid Key was pressed")

for cap in caps:
    cap.release() # release resource

cv2.destroyWindow('image')