import time
import cv2
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join

def mousecallback(event,x,y,flags,param):
    global plt
    global infoArray
    if event == cv2.EVENT_LBUTTONCLK: 
        for i in range(len(contours)):
            r=cv.pointPolygonTest(contour[i],Point(y,x),False)
            if r>0:
                plt.text((30,30),(90,30),"This contour is number "+ str(i))
                if infoArray[i][1]==255:
                    plt.text((30,60),(90,60),"This contour is white")
                else:
                    plt.text((30,90),(90,90),"This contour is black")
                plt.text((30,90),(90,90),"The area of this contour is "+str(infoArray[i][2]))
                plt.show()

matplotlib.use('Qt5Agg')
plt.ion()
mypath="newTarget/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for fileName in range(len(onlyfiles)):
    img = cv2.imread(str(mypath)+str(onlyfiles[fileName]))
    img=cv2.imread("Target 1/image_11.png")
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
    thresh = cv2.Canny(img,0,1)
    edges = cv2.Canny(img,0,1)
    contours,hierarchy1 = cv2.findContours(thresh,cv2.RETR_TREE, 4)

    cnt = contours[0]
    count=0
    newContours=[]
    newAreas=[]
    newAreas2=[]
    newContours2=[]
    for idx, cnt in enumerate(contours):
        if cv2.contourArea(cnt)>0 or cv2.arcLength(cnt,True)>10:
            count+=1
            newContours.append(cnt)
            newAreas.append(cv2.contourArea(cnt))
    for i in range(len(newAreas)):
        if newAreas[i] > 2:
            newAreas2.append(newAreas[i])
            newContours2.append(newContours[i])
    print(len(newContours2), len(newAreas2))
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    cv2.drawContours(img, newContours2, -1, (0,255,0),3,)
    plt.subplot(121),plt.imshow(img,cmap='gray')
    plt.title("PLACEHOLDER"), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(tempImage, cmap = 'gray')
    plt.title("Edge Image"), plt.xticks([]), plt.yticks([])
    plt.show()
    input()
    
    # [contour, (0=black, 255=white), area]
    infoArray=np.zeros((len(newContours2),3))
    for i in range(len(img)):
        print(i)
        for j in range(len(img[0])):
            for k in range(len(newContours2)):
                r=cv2.pointPolygonTest(newContours2[k],(i,j),False)
                if r>0:
                    if infoArray[k][0]==0:
                        infoArray[k][0]=k
                    if infoArray[k][1]==0:
                        if tempImage[i][j] > 150:
                            infoArray[k][1]=255
                        else:
                            infoArray[k][1]=0
                    if infoArray[k][2]==0:
                        infoArray[k][2]=newAreas2[k]
    
    for i in range(len(infoArray)):
        print(infoArray[i][0],infoArray[i][1],infoArray[i][2])
    input
    # cv2.namedWindow('image')
    # cv2.setMouseCallback('image',mousecallback)
