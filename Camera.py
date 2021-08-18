from picamera import PiCamera
from time import sleep
import numpy as np 


# Never been tested before
# To change naming to angles as suggested
# Save images to a more appropriate file path
# Consider if preview should not be included within capture methods
class Camera:
    
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1920, 1080)
        self.camera.framerate = 15
        #self.camera.rotation(180)
        self.num_img = 0 #number of captures
        self.num_vid = 0
        
    def set_resolution(self, x, y):
        self.camera.resolution = (x,y)

    def set_framerate(self, rate):
        self.camera.framerate = rate
        
    def get_resolution(self):
        return self.camera.resolution
    
    def get_framerate(self):
        return self.camera.framerate
        
    # Capturing a jpg image
    def capture_img_jpg(self):
        self.camera.start_preview()
        sleep(2) # Warm up camera
        self.camera.capture("img%d.jpg" %self.num_img)
        self.camera.stop_preview()
        self.num_img+=1 # update number of captures
        
    # Capturing a png image
    def capture_img_png(self):
        self.camera.start_preview()
        sleep(2) # Warm up
        self.camera.capture("img%d.png" %self.num_img)
        self.camera.stop_preview()
        self.num_img+=1 # update number of captures
        
    # Capture to an OpenCV object 
    # Returns an array of indicated resolution, BGR
    def capture_img_bgr(self):
        x_res = self.camera.resolution[0]
        y_res = self.camera.resolution[1]
        img = np.empty((y_res * x_res * 3), dtype = np.uint8)
        self.camera.capture(img, 'bgr')
        return img.reshape((y_res, x_res, 3))
        
    # time: length of the video
    def capture_vid(self, time):
        self.camera.start_preview()
        self.camera.start_recording("vid%d.jpg" %self.num_vid)
        sleep(time)
        self.camera.stop_recording()
        self.camera.stop_preview()
        self.num_vid+=1
        

    


def run():
    #camera = Camera()
    print("running")
        
    #while True:
        #camera.capture_img()
        

run()








'''
    while(motor is running)
    
        if detected:
            capture the image 
            process the image
        
        pass
    
    
#Process the image
class Process:
    
    def __init__(self, filepath):
        self.img = cv2.imread(filepath)
        
        pass
    
    def decompose_rgb(self):
        b, g, r = cv2.split(self.img)
        rgb = cv2.merge([r,g,b])
        return rgb
    
    def show_img(self):
        # first argument is the name of the window that is displayed 
        cv2.imshow('image', self.img)
        
   
class Initialize:
    
    def __init__(self):
        self.camera = PiCamera()
        
#Decompose image to RGB
# img cv2. imread(address)
# b, g, r = cv2.split(img)
# rgb = cv2.merge([r,g,b])
# plt.imshow(rgb_img)

# Captures the imag/video

# full HD 1920 x 1080
# frame rate: 15 fps
# capture duration 10 seconds
        
        
'''      
        
    
    
        



