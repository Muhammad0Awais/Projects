# OpenCV bindings
import cv2
# To performing path manipulations 
import os
# Local Binary Pattern function
from skimage.feature import local_binary_pattern
# To calculate a normalized histogram 
from scipy.stats import itemfreq
from sklearn.preprocessing import normalize
# To read class from file
import csv
# For plotting
import matplotlib.pyplot as plt
# For array manipulations
import numpy as np
# For saving histogram values
from sklearn.externals import joblib
# For command line input
import argparse as ap
# Utility Package
import cvutils
from sklearn.svm import LinearSVC

# Get the path of the training set
# Store the path of training images in train_images
train_images_path = "data/lbp/train/"
train_images = cvutils.imlist(train_images_path)

# List for storing the Local Binary Pattern (LBP) histograms, image paths, and corresponding labels 
histograms = []
image_paths = []
labels = []

# For each image in the training set, calculate the LBP histogram
# and update histograms, image_paths, and labels
for i in range(len(train_images)):
    print(train_images[i])
    # Read the image
    image = cv2.imread(train_images[i])
    # Convert to grayscale as LBP works on grayscale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur and Otsu's thresholding
    blur = cv2.GaussianBlur(gray_image, (5, 5), 0)
    ret, thresh1 = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    radius = 3
    # Number of points to be considered as neighbours
    no_points = 8 * radius

    # Uniform LBP is used
    lbp = local_binary_pattern(thresh1, no_points, radius, method='uniform')
    
    # Calculate the histogram
    x = itemfreq(lbp.ravel())
    # Normalize the histogram
    hist = x[:, 1] / sum(x[:, 1])
    
    # Append image path in image_paths
    image_paths.append(train_images[i])
    # Append histogram to histograms
    histograms.append(hist)
    # Append class label in labels
    labels.append(train_images[i])

joblib.dump((image_paths, histograms, labels), "lbp.pkl", compress=3)

# Display the training images (commented out for now)
# nrows = 2
# ncols = 3
# fig, axes = plt.subplots(nrows, ncols)
# for row in range(nrows):
#     for col in range(ncols):
#         axes[row][col].imshow(cv2.cvtColor(cv2.imread(image_paths[row * ncols + col]), cv2.COLOR_BGR2RGB))
#         axes[row][col].axis('off')
#         axes[row][col].set_title("{}".format(os.path.split(image_paths[row * ncols + col])[1]))
#
# # Convert to numpy and display the image
# fig.canvas.draw()
# im_ts = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
# im_ts = im_ts.reshape(fig.canvas.get_width_height()[::-1] + (3,))
# cv2.imshow("Training Set", im_ts)
# cv2.waitKey()
