import cv2
import numpy as np

img = cv2.imread('laser2.png')
cv2.imshow('Image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
imgHLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
cv2.imshow('Image',imgHLS)
cv2.waitKey(0)
cv2.destroyAllWindows()

Lchannel = imgHLS[:,:,1]
mask = cv2.inRange(Lchannel, 250, 255)
res = cv2.bitwise_and(img,img, mask= mask)
cv2.imshow('Image',res)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(imgHLS[200][0:300])
print(imgHLS[200][300:520])
'''
img([y][x])

count = cv2.countNonZero(img)
print(count)
'''
