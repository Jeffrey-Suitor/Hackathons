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
    edges = cv2.Canny(img,0,53)
    im2, contours, = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    cv2.drawContours(img, contours, 1, (0,255,0), 3)
    plt.subplot(121),plt.imshow(img,cmap='gray')
    plt.title("PLACEHOLDER"), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges, cmap = 'gray')
    plt.title("Edge Image"), plt.xticks([]), plt.yticks([])
    plt.draw()
    input()
    prevCount=0

    plt.imshow(edges)
    plt.show()
    input()
