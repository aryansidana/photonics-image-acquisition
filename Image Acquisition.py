import cv2
import numpy as np
import matplotlib.pyplot as plt
import picamera
import os


class Camera():
    def __init__(self):
        self.cam = picamera.PiCamera()
        self.cam.resolution = (1920, 1080)
        self.cam.exposure_mode = 'off'
        self.cam.start_preview()
        
    def capture(self, directory):
        self.cam.capture(directory)
        self.cam.close()
        
    def set_framerate(self, rate):
        self.cam.framerate = rate
    
    def set_analog_gain(self, value):
        self.cam.analog_gain = value
        
    def set_digital_gain(self, value):
        self.cam.digital_gain = value
        
    def set_shutter_speed(self, speed):
        self.cam.shutter_speed = speed
    
    def set_camera_iso(self, iso):
        self.cam.iso = iso
    
    
#-------------------Initialize Variables-------
    
# global variables
angles = []
intensities = []

# initialize cam object
cam = Camera()

#----------------------------------------------


# Check if image is saturated using HSV 
# img --> BGR
def is_saturated(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1];
    saturated_pixels = np.count_nonzero(saturation == 255)
    zeros = np.count_nonzero(saturation == 0)
    total_pixels = saturation.size
    
    # Can change 0.1 (10%) threshold 
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
# OVERWRITES PREVIOUS SAVED IMAGE OF NAME "IMG"!
def capture():
    #Might have to change file directory name (Did't check Pi yet)
    cam.capture("/home/pi/Desktop/Image_Acquisition/test_img/img.png")
    img = cv2.imread('/home/pi/Desktop/Image_Acquisition/test_img/img.png')

    if is_saturated(img):
        print("ERROR: Image is Saturated")
        return 0;
    
    #Can adjust threshold cut off value
    th, dst = cv2.threshold(img,0,255,cv2.THRESH_TOZERO)
    imgHLS = cv2.cvtColor(dst, cv2.COLOR_BGR2HLS)
    return light_HLS(imgHLS)


#Captures and saves FHD image (with angle as name) and returns light intensity
def capture(angle):
    #Changed pi dir: saved images test_img folder
    cam.capture('/home/pi/Desktop/Image_Acquisition/test_img/'+angle+'.png')
    img = cv2.imread('/home/pi/Desktop/Image_Acquisition/test_img/'+angle+'.png')

    if is_saturated(img):
        print("ERROR: Image is Saturated")
        return 0;
    
    #Can adjust threshold cut off value
    th, dst = cv2.threshold(img,0,255,cv2.THRESH_TOZERO)
    imgHLS = cv2.cvtColor(dst, cv2.COLOR_BGR2HLS)
    
    # calculate the intensity
    intensity = light_HLS(imgHLS)
    
    # append calculated values to list
    intensities.append(intensity)
    angles.append(angle)
    
    return intensity


def plot_scatter(x, y):
    plt.title("Intensity vs Angle")
    plt.xlabel("Angle (°)")
    plt.ylabel("Intensity")
    plt.scatter(angles, intensities)
    plt.show()


# captures image (with angle as name)
# if boolean == True: shows the plot of image
# if boolean == False: returns calculated intensity at angle
def capture(angle,boolean):

    #Changed pi dir: saved images test_img folder
    cam.capture('/home/pi/Desktop/Image_Acquisition/test_img/'+angle+'.png')
    img = cv2.imread('/home/pi/Desktop/Image_Acquisition/test_img/'+angle+'.png')

    if is_saturated(img)==True:
        print("ERROR: Image is Saturated")
        return 0;
    
    #Can adjust threshold cut off value
    th, dst = cv2.threshold(img,0,255,cv2.THRESH_TOZERO)
    imgHLS = cv2.cvtColor(dst, cv2.COLOR_BGR2HLS)

    # calculate the intensity
    intensity = light_HLS(imgHLS)
    
    # append calculated values to list
    intensities.append(intensity)
    angles.append(angle)
    
    # Plot points
    if boolean:
        plot_scatter(angles, intensities)
        
    else:
        return intensity
    
    
#Clear matplotlib graph in order to plot new angle range
def reset():
    # reinitialize global variables
    del angles[:]
    del intensities[:]
    
        
# Calculates the intensity of images in a folder
# folder location is in same directory as this code file
# Plots the calculated intensity
# check img types --> bgr/gray/hls
def plot_folder_images(folder):
    cur_path = os.path.dirname(os.path.realpath(__file__))
    # Change folder name
    img_path = os.path.join(cur_path, folder)
    
    intensity_list = []
    angle_list = []

    for i, img in enumerate(os.listdir(img_path)):
        path = os.path.join(img_path, img)
        
        #assuming camera takes gray images
        gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE) #--> This reads the image as gray
       
        # convert image to HLS
        bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        hls = cv2.cvtColor(bgr, cv2.COLOR_BGR2HLS)
        intensity_list.append(light_HLS(hls))
        
        # get angle (assuming only double digit)
        angle = int(img[:2])
        angle_list.append(angle)
        
    
    # plot the function
    plot_scatter(angle_list, intensity_list)




        
        
    
    



