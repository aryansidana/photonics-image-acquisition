import cv2
import numpy as np
import matplotlib.pyplot as plt
import picamera


#Calculate light intensity using HLS image formate
def light_HLS(img):
    light= img[:,:,1]
    total_light = np.sum(light)
    pixels=img.shape[0]*img.shape[1]
    black_p=np.count_nonzero(light == 0)
    Avg_light=total_light/(pixels-black_p)

    return Avg_light

#Captures FHD image and returns light intensity
def capture():
    cam = picamera.PiCamera
    cam.resolution = (1920, 1080)
    cam.exposure_mode('off')
    cam.start_preview()
    
    #Might have to change file directory name (Did't check Pi yet)
    cam.capture("Desktop/Image_Acquisition/img.png")
    
    img = cv2.imread('Desktop/Image_Acquisition/img.png')

    #Can adjust threshold cut off value
    th, dst = cv2.threshold(img,0,255,cv2.THRESH_TOZERO)
    
    imgBRG = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    imgHLS = cv2.cvtColor(imgBRG, cv2.COLOR_BGR2HLS)
    
    cam.close()
    return light_HLS(imgHLS)

#Captures and saves FHD image (with angle as name) and returns light intensity
def capture(angle):
 `  cam = picamera.PiCamera
    cam.resolution = (1920, 1080)
    cam.exposure_mode('off')
    cam.start_preview()

    #Might have to change file directory name (Did't check Pi yet)
    cam.capture('Desktop/Image_Acquisition/'+angle+'.png')
    
    img = cv2.imread('Desktop/Image_Acquisition/'+angle+'.png')

    #Can adjust threshold cut off value
    th, dst = cv2.threshold(img,0,255,cv2.THRESH_TOZERO)
    
    imgBRG = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    imgHLS = cv2.cvtColor(imgBRG, cv2.COLOR_BGR2HLS)

    cam.close()
    return light_HLS(imgHLS)


def capture(angle,boolean)




