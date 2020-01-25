
import time
import cv2
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join

matplotlib.use('Qt5Agg')
plt.ion()
mypath="newTarget/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for fileName in range(len(onlyfiles)):
    img = cv2.imread(str(mypath)+str(onlyfiles[fileName]))
    img=cv2.imread("Target 1/image_11.png")
    img = img[200:500, 200:500]
    tempImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] < 10:
                img[i][j]=255
            if img[i][j]>170:
                img[i][j]=255
    dimensions=img.shape
    img=cv2.rectangle(img,(0,0),(dimensions[1],dimensions[0]),(0,255,0),10)
    thresh = cv2.Canny(img,2,60)
    edges = cv2.Canny(img,2,60)
    contours,hierarchy1 = cv2.findContours(thresh,cv2.RETR_TREE, 3)

    cnt = contours[0]
    count=0
    newContours=[]
    newAreas=[]
    for idx, cnt in enumerate(contours):
        #if cv2.contourArea(cnt)>4 or cv2.arcLength(cnt,True)>10:
        if cv2.contourArea(cnt)>2:
            count+=1
            newContours.append(cnt)
            newAreas.append(cv2.contourArea(cnt))
    print(len(newAreas))
    print(np.average(newAreas))
    finalAreas = [area for area in newAreas if area > 8 ]
    print(len(finalAreas))
    print(finalAreas)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    cv2.drawContours(img, newContours, -1, (0,255,0),3,)
    plt.subplot(121),plt.imshow(img,cmap='gray')
    plt.title("PLACEHOLDER"), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(tempImage, cmap = 'gray')
    plt.title("Edge Image"), plt.xticks([]), plt.yticks([])
    plt.draw()
    input()
