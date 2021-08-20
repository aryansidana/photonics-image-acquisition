import cv2
import numpy as np
from numpy.linalg import norm
import numpy.ma as ma

def lightness(img):
    total_light = np.sum(img[:,:,1])
    pixels=img.shape[0]*img.shape[1]
    Avg_light=total_light/pixels

    return Avg_light

def lightness_No_Black(img):
    light= img[:,:,1]
    total_light = np.sum(light)
    pixels=img.shape[0]*img.shape[1]
    black_p=np.count_nonzero(light == 0)
    Avg_light=total_light/(pixels-black_p)

    return Avg_light

def show_img(img):
    cv2.imshow('Image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
img = cv2.imread('laser.png',0)

show_img(img)

th, dst = cv2.threshold(img,0,255,cv2.THRESH_TOZERO)

show_img(dst)

imgBRG = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
imgHLS = cv2.cvtColor(imgBRG, cv2.COLOR_BGR2HLS)

show_img(imgHLS)


AvgLight=lightness(imgHLS)
Avglight_NOB=lightness_No_Black(imgHLS)
percentLight=Avglight_NOB/255*100
print("Avg Pixel Light Intensity: " + str(Avglight_NOB))
print("Percent Light Intensity: " + str(percentLight))
size=imgHLS.shape[0]*imgHLS.shape[1]
print("# of Pixels: " + str(size))





