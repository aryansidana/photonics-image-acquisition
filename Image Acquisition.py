import cv2
import numpy as np
import matplotlib.pyplot as plt
import picamera

# img --> BGR
def is_saturated(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1];
    saturated_pixels = np.count_nonzero(saturation == 255)
    zeros = np.count_nonzero(saturation == 0)
    total_pixels = saturation.size
    
    return saturated_pixels != 0 and saturated_pixels / (total_pixels - zeros) > 0.1


#Calculate light intensity using HLS image format
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

    if is_saturated(img)==True:
        print("ERROR: Image is Saturated")
        return 0;
    
    #Can adjust threshold cut off value
    th, dst = cv2.threshold(img,0,255,cv2.THRESH_TOZERO)
    
    imgHLS = cv2.cvtColor(dst, cv2.COLOR_BGR2HLS)
    
    cam.close()
    return light_HLS(imgHLS)
#Captures and saves FHD image (with angle as name) and returns light intensity
def capture(angle):
    cam = picamera.PiCamera
    cam.resolution = (1920, 1080)
    cam.exposure_mode('off')
    cam.start_preview()

    #Might have to change file directory name (Did't check Pi yet)
    cam.capture('Desktop/Image_Acquisition/'+angle+'.png')
    
    img = cv2.imread('Desktop/Image_Acquisition/'+angle+'.png')

    if is_saturated(img)==True:
        print("ERROR: Image is Saturated")
        return 0;
    
    #Can adjust threshold cut off value
    th, dst = cv2.threshold(img,0,255,cv2.THRESH_TOZERO)
    
    imgHLS = cv2.cvtColor(dst, cv2.COLOR_BGR2HLS)

    cam.close()
    return light_HLS(imgHLS)


def capture(angle,boolean):
    pass



#Clear matplotlib graph in order to plot new angle range
def reset():
    pass




