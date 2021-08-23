import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
from PIL import Image
# from scipy.stats import norm

# To do (in no particular order)
# Fill out methods
# Change aesthetics of add_text 
# To consider using > 8 bits
# rename some parameters for clarity (img --> bgr_img)
# Might change this  module to a class, but doesnt matter rn



# Probably dont need this...
# to close image just press any key in your keyboard
def show_img(img):
    cv2.imshow("img", img)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()


# Determine saturation by counting number of 255 pixels
# change threshold
def is_saturated1(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1];
    print("num of 255: ", np.count_nonzero(saturation == 255))
    return np.count_nonzero(saturation == 255) > 10

# Determine if image is saturated 
# Calculate the percentage of pixels with value of 255 and not include the black background
# img --> BGR
def is_saturated2(img):
    # hsv = [hue, saturation, value]
    # Extract saturation from hsv
    # Count number of saturated pixels (255)
    # Count number of zeros in the background
    # Count total number of pixels, including background

    # Check if number of saturated pixels is not zero (prevent ZERO DIVISION ERROR short circuiting) 
    # If number of saturated pixels is greater than zero, then
    # calculate the percentage of the pixels that is saturated, not including background value of 0 saturation
    # We can change this percentage
    
    ## print("max: ", saturation.max())
    ## print("saturation: ", saturation)
    ## print("saturated pixels: ", saturated_pixels)
    ## print("zeros: ", zeros)
    ## print("total pixels: ", total_pixels)
    ## print(saturated_pixels != 0 and saturated_pixels / (total_pixels - zeros))

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1];
    saturated_pixels = np.count_nonzero(saturation == 255)
    zeros = np.count_nonzero(saturation == 0)
    total_pixels = saturation.size
    
    return saturated_pixels != 0 and saturated_pixels / (total_pixels - zeros) > 0.1



# Before calling intensity functions, check if saturated and 8 bit image
# if not is_saturated2(img) and img.dtype == 'uint8':

# Calculate intensity by adding all pixels together
# Change BGR to gray scale and return sum
# img --> bgr
def calc_intensity1(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).sum()

# Calculates intensity by averaging all pixels together in gray scale
# img --> bgr
def calc_intensity2(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).mean()

# Calculates average intensity, not including background
# img --> BGR
def calc_intensity3(img):
    # Convert BGR to gray scale
    # Slice out all zeros from array
    # return average of non-zero values
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray[gray > 0].mean()


def calc_intensity4(img):
    pass

# Find the sum of intensity of each row
# Return the maximum sum of intensity  
def max_intensity(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_trans = np.transpose(gray)
    return np.array([row.sum() for row in gray_trans]).max()
    

# Adds text on specified image at location (x,y) using openCV
def add_text(img, text, x, y):
    location = (x,y)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = .75
    fontColor = (255, 0, 0)
    lineType = 2
    cv2.putText(img, text, 
                location, 
                font,
                fontScale,
                fontColor,
                lineType)
    return img


# plot angle vs intensity (line graph)
# angles is a list of angles
# intensities is a nested list of intensities
def plot(angles, intensities):

    fig, ax = plt.subplots(len(intensities),1)
    
    for i in range(len(intensities)):
        ax[i].plot(angles, intensities[i])
        ax[i].set_ylabel("Intensity%d" %(i+1))
   
    plt.xlabel("Angle (°)")  
    fig.suptitle("Angle vs Intensities")
    plt.show()


# Plots the intensity (sum of the whole column at a specific row) against the row
# https://stackoverflow.com/questions/10101286/statistical-analysis-on-bell-shaped-gaussian-curve
def plot_row(img, row=540):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_trans = np.transpose(gray)
    sum_col = [row.sum() for row in gray_trans]
    row = [i for i in range(len(sum_col))]
    plt.title("Sum of Pixels (intensity) vs Row")
    plt.xlabel("Row")
    plt.ylabel("Intensity")
    plt.plot(row ,sum_col)
    
def calc_gauss():
    pass

  
    
# https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv/48367205#48367205
# https://realpython.com/python-opencv-color-spaces/
# threshold and mask the image
# get the sum of pixel intensity of that spot  
def crop(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low = np.array([0,0,1])
    high = np.array([0,0,255])
    mask = cv2.inRange(hsv, low, high)
    masked = cv2.bitwise_and(img, img, mask=mask)
       
    show_img(hsv)
    show_img(mask)
    

    
def threshold(img):
    # Find the contours of the image
    # gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # obtain threshold of the image
    thresh = 1
    ret, thresh_img = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    # find contours
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #create an empty image for contours
    img_contours = np.zeros(img.shape)
    # draw the contours on the empty image
    cv2.drawContours(img_contours, contours, -1, (0,255,0), 3)
    show_img(img_contours)
    




#https://publiclab.org/notes/MaggPi/08-09-2018/raspberry-pi-manual-camera-control
#loc: mean of te distribution
#scale: standard dev/ spread or width of distribution
#size: tuple 
def create_saturated(loc, scale, size):
    data = np.random.normal(loc, scale, size)
    
    return np.array(data ,dtype=np.uint8)
  
    

#img2 = create_saturated(255,0.1,(1920, 1080, 3))
#hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
#show_img(hsv)
#print(is_saturated2(img2))
#plot_row(img2)

def main():

    cur_path = os.path.dirname(os.path.realpath(__file__))
    img_path = os.path.join(cur_path, "..", "sample_laser")

    intensities = [[],[],[],[]]

    for i, img in enumerate(os.listdir(img_path)):
        path = os.path.join(img_path, img)
        img = cv2.imread(path) #--> This reads the image as BGR

        intensities[0].append(calc_intensity1(img))
        intensities[1].append(calc_intensity2(img))
        intensities[2].append(calc_intensity3(img))
        intensities[3].append(max_intensity(img))
        

    
        print("image%d" %(i+1))
        print("saturated1: ", is_saturated1(img))
        print("saturated2: ", is_saturated2(img))
        print("calc_intensity1: ", calc_intensity1(img)) #Sum of gray pixels
        print("calc_intensity2: ", calc_intensity2(img)) #Avg in gray scale, with background
        print("calc_intensity3: ", calc_intensity3(img)) #Avg of gray pixels, without background
        print("max_intensity: ", max_intensity(img)) 
        print("\n")
        
        
    angles = [angle for angle in range(45,50)]
    plot(angles, intensities)


#main()

#path = r"C:/Users/grace/Desktop/SEED NANOTECH/code/sample_laser/img1.jpg"
#img = cv2.imread(path)

#show_img(img)
#show_img(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))

#plot_row(img)


#print(max_intensity(img))
#path = r"C:/Users/grace/Desktop/SEED NANOTECH/code/saturated_img/green_laser.jpeg"

#crop(img)
#trans = cv2.imread("test.png")
#show_img(trans)
# turn background to transparent and not black
#https://stackoverflow.com/questions/53380318/problem-about-background-transparent-png-format-opencv-with-python



#plot_row(img)
#plot_3D(img)

#threshold(img)
'''
show_img(img)

# Find the contours of the image
# gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# obtain threshold of the image
thresh = 1
ret, thresh_img = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
# find contours
contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#create an empty image for contours
img_contours = np.zeros(img.shape)
# draw the contours on the empty image
cv2.drawContours(img_contours, contours, -1, (0,255,0), 3)
show_img(img_contours)


# crop image

#(thresh, bw) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
#show_img(bw)

#hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#lower = np.array([32,0,0])
#upper = np.array([255,0,0])
#mask = cv2.inRange(hsv, lower, upper)

'''


'''
# Test add_text
directory = 'saturated_img'
angle = '40'
saturated = 'saturated'
add_text(img, directory, 10, 30)
add_text(img, angle, 10, 60)
show_img(add_text(img, saturated, 10, 90))
'''

'''   
def plot_3D(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x = np.linspace(0,gray.shape[0], 50)
    y = np.linspace(0,gray.shape[1], 50)
    
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    def f(x, y):
        return gray[x][y]
    
    
    ax.scatter3D(x, y, f(x,y))
    plt.show()
'''
'''
    #Change black background to transparent
    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    _,alpha = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    b,g,r = cv2.split(masked)
    rgba = [b,g,r, alpha]
    masked_tr = cv2.merge(rgba, 4)
    cv2.imwrite("test.png", masked_tr)
    '''
    
# =============================================================================
#      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#      
#      height = gray.shape[1]
#      row = round(height/2)
#      # [row, col]
#      val = gray[row, :]
#      print(val)
#      count = [i for i in range(len(val))]
#      plt.plot(count, val)
#      plt.show()
# =============================================================================
     