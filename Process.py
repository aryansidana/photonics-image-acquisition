import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
# from scipy.stats import norm

# To do (in no particular order)
# Fill out methods
# Change aesthetics of add_text 
# To consider using > 8 bits
# rename some parameters for clarity (img --> bgr_img)
# Might change this  module to a class, but doesnt matter rn


# Might be useful to be able to use os.join to 
# access the images in a for loop later when we
# integrate all the modules together and process the 
# images one by one from where it is stored
def load_images():
    # least of our priorities
    pass

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

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1];
    saturated_pixels = np.count_nonzero(saturation == 255)
    zeros = np.count_nonzero(saturation == 0)
    total_pixels = saturation.size
    
    ## print("max: ", saturation.max())
    ## print("saturation: ", saturation)
    ## print("saturated pixels: ", saturated_pixels)
    ## print("zeros: ", zeros)
    ## print("total pixels: ", total_pixels)
    ## print(saturated_pixels != 0 and saturated_pixels / (total_pixels - zeros))
    
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


# Hard one, but calculate intensity using Gaussian curve?
def calc_intensity4(img):
    pass
        

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

    fig, ax = plt.subplots(3,1)
    ax[0].plot(angles, intensities[0])
    ax[1].plot(angles, intensities[1])
    ax[2].plot(angles, intensities[2])

    ax[0].set_ylabel("Intensity1")
    ax[1].set_ylabel("Intensity2")
    ax[2].set_ylabel("Intensity3")
    
    plt.xlabel("Angle (°)")
    

    
    fig.suptitle("Angle vs Intensities")
    plt.show()

    '''
    for i, intensity_list in enumerate(intensities):
        plt.xlabel("Angle (degrees)")
        plt.ylabel("Intensity%d" %(i))
        plt.subplot(3,1,i+1)
        plt.plot(angles, intensity_list)
        
    plt.show()
    '''




def main():

    cur_path = os.path.dirname(os.path.realpath(__file__))
    img_path = os.path.join(cur_path, "..", "sample_laser")

    intensities = [[],[],[]]

    for i, img in enumerate(os.listdir(img_path)):
        path = os.path.join(img_path, img)
        img = cv2.imread(path) #--> This reads the image as BGR

        intensities[0].append(calc_intensity1(img))
        intensities[1].append(calc_intensity2(img))
        intensities[2].append(calc_intensity3(img))


        print("image%d" %(i+1))
        print("saturated1: ", is_saturated1(img))
        print("saturated2: ", is_saturated2(img))
        print("calc_intensity1: ", calc_intensity1(img)) #Sum of gray pixels
        print("calc_intensity2: ", calc_intensity2(img)) #Avg in gray scale
        print("calc_intensity3: ", calc_intensity3(img)) #Avg of gray pixels, without background
        print("\n")
        
    angles = [angle for angle in range(45,50)]
    plot(angles, intensities)


main()


#path = r"C:/Users/grace/Desktop/SEED NANOTECH/code/sample_laser/img1.jpg"
#path = r"C:/Users/grace/Desktop/SEED NANOTECH/code/saturated_img/green_laser.jpeg"

'''
# Test add_text
directory = 'saturated_img'
angle = '40'
saturated = 'saturated'
add_text(img, directory, 10, 30)
add_text(img, angle, 10, 60)
show_img(add_text(img, saturated, 10, 90))
'''
