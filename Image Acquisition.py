import cv2
import numpy as np
import matplotlib.pyplot as plt
import picamera
import os
from imutils import contours, grab_contours

#------------------------------Camera Class-----------------------------------

# Consists of setters and getters for camera settings
# Capture takes a picture and saves it to a directory 

class Camera():
    def __init__(self):
        self.cam = picamera.PiCamera()
        self.cam.resolution = (1920, 1080)
        self.cam.exposure_mode = 'off'
        self.cam.framerate = 10
        self.cam.start_preview()
    
    def get_framerate(self):
        return self.cam.framerate
    
    def get_analog_gain(self):
        return self.cam.analog_gain
        
    def get_digital_gain(self):
        return self.cam.digital_gain
        
    def get_shutter_speed(self):
        return self.cam.shutter_speed
    
    def get_camera_iso(self):
        return self.cam.iso
        
    
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
        
    def capture(self, directory):
        self.cam.capture(directory)
        self.cam.stop_preview()
        self.cam.close()
        
        
        
        
#----------------------Initialize Variables------------------------------------
    
# global variables
angles = []
intensities = []

# initialize cam object
cam = Camera()


#------------------------Main Functions----------------------------------------
'''

Capture() - Captures an image and returns light intensity if image is not saturated
    *OVERWRITES PREVIOUS SAVED IMAGE OF NAME "IMG" WITH EACH FUNCTION CALL*

Capture(angle, boolean=False) - Captures an image and saves it with angle as name,
    if boolean == True: shows the plot of intensity Vs Angle
    if boolean == False: returns calculated intensity at angle

    *if second argument is not passed, it is automatically set to false*

Reset() - Clears all data points on the scatter plot in order to plot new angle range

plot_folder_images(folder) - Calculates  and plots the intensity of images in a folder

'''


#--------------------Saturation Calculations-----------------------------------


# Determines percentage of saturated pixels
# If the number of saturated pixels makes up 10% of the image, 
# not including the background, then the image is saturated   
# Returns a boolean, True, if image is saturated. Otherwise, return False
def is_saturated1(img_bgr):
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1];
    saturated_pixels = np.count_nonzero(saturation == 255)
    zeros = np.count_nonzero(saturation == 0)
    total_pixels = saturation.size
    
    # Can change 0.1 (10%) threshold 
    return saturated_pixels != 0 and saturated_pixels / (total_pixels - zeros) > 0.1



# Counts the number of saturated pixel clusters in the a grayscale image.
# Converts all values less than 255 to 0 by thresholding.
# Performs a series of dilation and erosion to remove small noise on the image.
# Draw a contour around the cluster of saturated pixels from the threshold image.
# Returns a tuple of the number of circles (groups of saturated pixels) and the radius of each circle.
def group_saturated(img_gray):
    ret, thresh = cv2.threshold(img_gray.copy(), 254, 255, cv2.THRESH_TOZERO)
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)
    

    # Draw contour  
    # RETR_EXTERNAL: return only extreme outer flags and leave child contours behind 
    #   Outer contours only
    # CHAIN_APPROX_SIMPLE: compresses horizontal, vertical, and diagonal segments
    #   Leaves only their end points
    contour = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = grab_contours(contour)
 
    count = 0
    rad = []
   
    for (i, c) in enumerate(contour):
        (x, y, w, h) = cv2.boundingRect(c)
        
        ((cX, cY), radius) = cv2.minEnclosingCircle(c)
        cv2.circle(img_gray, (int(cX), int(cY)), int(radius),
    		(0, 0, 255), 3)
        cv2.putText(img_gray, "#{}".format(i + 1), (x, y - 15),
    		cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        
        count = i+1
        rad.append(radius)

    return count, rad

# Determines saturated image by counting the clusters of saturated pixels and its radius
# If there is a group of 255 pixels detected and the radius of that is greater than 20
# then it is a saturated image
# Returns a boolean, True, if image is saturated. Otherwise, return False
def is_saturated2(img_gray):
    count, radius = group_saturated(img_gray)
    return count > 0 and max(radius) > 20



#------------------------------Intensity Calculations--------------------------

# Calculates intensity by summing all pixel values in grayscale
def sum_intensity(img_bgr):
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY).sum()


#Calculate light intensity using HLS image format
def light_HLS(img):
    light= img[:,:,1]
    total_light = np.sum(light)
    pixels=img.shape[0]*img.shape[1]
    black_p=np.count_nonzero(light == 0)
    Avg_light=total_light/(pixels-black_p)

    return Avg_light


#--------------------------------Plotting--------------------------------------

# Shows a scatter plot of x (list of angles) and y (list of intensities)
def plot_scatter(x, y):
    plt.title("Intensity vs Angle")
    plt.xlabel("Angle (°)")
    plt.ylabel("Intensity")
    plt.scatter(x, y)
    plt.show()


        
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
        gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
       
        # convert image to HLS
        bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        hls = cv2.cvtColor(bgr, cv2.COLOR_BGR2HLS)
        intensity_list.append(light_HLS(hls))
        
        # get angle (assuming only double digit)
        angle = int(img[:2])
        angle_list.append(angle)
        
    
    # plot the function
    plot_scatter(angle_list, intensity_list)
    
    
#Clear matplotlib graph in order to plot new angle range
def reset():
    # reinitialize global variables
    del angles[:]
    del intensities[:]
    
    
#--------------------------------Capture--------------------------------------

#Captures FHD image and returns light intensity
#OVERWRITES PREVIOUS SAVED IMAGE OF NAME "IMG"!
def capture():
   
    cam.capture("/home/pi/Desktop/Image_Acquisition/test_img/img.png")
    gray = cv2.imread('/home/pi/Desktop/Image_Acquisition/test_img/img.png',0)

    #Checks if image is saturated
    if is_saturated2(gray):
        print("ERROR: Image is Saturated")
        return 0;

    bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    #Can adjust threshold cut off value
    th, dst = cv2.threshold(bgr,0,255,cv2.THRESH_TOZERO)
    #BGR -> HLS
    imgHLS = cv2.cvtColor(dst, cv2.COLOR_BGR2HLS)
    
    return light_HLS(imgHLS)




# Captures image (with angle as name)
# If boolean == True: shows the plot of image
# If second argument is not passed, it is automatically set to False
# If boolean == False: returns calculated intensity at angle
def capture(angle,boolean=False):

    #Changed pi dir: saved images test_img folder
    cam.capture('/home/pi/Desktop/Image_Acquisition/test_img/'+angle+'.png')
    gray = cv2.imread('/home/pi/Desktop/Image_Acquisition/test_img/'+angle+'.png',0)

    if is_saturated2(gray):
        print("ERROR: Image is Saturated")
        return 0;
    
    bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    #Can adjust threshold cut off value
    th, dst = cv2.threshold(bgr,0,255,cv2.THRESH_TOZERO)
    imgHLS = cv2.cvtColor(dst, cv2.COLOR_BGR2HLS)

    # calculate the intensity
    intensity = light_HLS(imgHLS)
    
    # append calculated values to list
    intensities.append(intensity)
    angles.append(angle)
    
    # Plot points
    if boolean:
        plot_scatter(angles, intensities)
    
    return intensity

    
    


