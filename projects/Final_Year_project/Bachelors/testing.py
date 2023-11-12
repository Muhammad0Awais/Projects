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

# Get the path of the training set

# Load the List for storing the LBP Histograms, address of images, and the corresponding label 
X_name, X_test, y_test = joblib.load("lbp.pkl")

# Opening camera and uploading images
# cap = cv2.VideoCapture(0)
# while(1):
#     ret, frame = cap.read()
#     if 0xFF == ord('r'):
#         break;
# cap.release()

# Store the path of testing images in test_images
test_images_path = "data/lbp/test/"
test_images = cvutils.imlist(test_images_path)

# Dictionary containing image paths as keys and corresponding label as value
test_dic = {}
with open('data/lbp/class_test.txt', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        test_dic[row[0]] = int(row[1])

# Dict containing scores
results_all = {}

for test_image in test_images:
    print("\nCalculating Normalized LBP Histogram for {}".format(test_image))
    # Read the image
    im = cv2.imread(test_image)
    # Convert to grayscale as LBP works on grayscale image
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(im_gray, (5, 5), 0)
    ret, thresh1 = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    radius = 3
    # Number of points to be considered as neighbors 
    no_points = 8 * radius
    # Uniform LBP is used
    lbp = local_binary_pattern(thresh1, no_points, radius, method='uniform')
    # Calculate the histogram
    x = itemfreq(lbp.ravel())
    # Normalize the histogram
    hist = x[:, 1] / sum(x[:, 1])
    # Display the query image
    results = []
    # For each image in the training dataset
    # Calculate the chi-squared distance and then sort the values
    for index, x_hist in enumerate(X_test):
        score = cv2.compareHist(np.array(x_hist, dtype=np.float32), np.array(hist, dtype=np.float32), cv2.cv.CV_COMP_CHISQR)
        results.append((X_name[index], round(score, 3)))
    results = min(results, key=lambda score: score[1])
    results_all[test_image] = results
    print("Displaying scores for {} ** \n".format(test_image))
    name = results[0][15:]
    print(name)
    # for image, score in results:
    #     print "{} has score {}".format(image, score)
    # print(results)
    # for test_image, results in results_all.items():
    #     # Read the image
    #     im = cv2.imread(test_image)
    #     # Display the results
    #     nrows = 2
    #     ncols = 3
    #     fig, axes = plt.subplots(nrows,ncols)
    #     fig.suptitle("** Scores for -> {}**".format(test_image))
    #     for row in range(nrows):
    #         for col in range(ncols):
    #             axes[row][col].imshow(cv2.imread(results[row*ncols+col][0]))
    #             axes[row][col].axis('off')
    #             axes[row][col].set_title("Score {}".format(results[row*ncols+col][1]))
    #     fig.canvas.draw()
    #     im_ts = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    #     im_ts = im_ts.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    #     cv2.imshow("** Query Image -> {}**".format(test_image), im)
    #     cv2.imshow("** Scores for -> {}**".format(test_image), im_ts)
    #     cv2.waitKey()
    #     cv2.destroyAllWindows() 
