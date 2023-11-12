import cv2
import numpy as np
from matplotlib import pyplot as plt

def get_pixel(img, center, x, y):
    """
    Get the pixel value based on the center and specified coordinates.
    """
    new_value = 0
    try:
        if img[x][y] >= center:
            new_value = 1
    except:
        pass
    return new_value

def calculate_lbp_pixel(img, x, y):

    '''
    Calculate the Local Binary Pattern (LBP) value for a pixel in the image.

     64 | 128 |   1
    ----------------
     32 |   0 |   2
    ----------------
     16 |   8 |   4    

    '''    
    center = img[x][y]
    val_ar = [
        get_pixel(img, center, x-1, y+1),     # top_right
        get_pixel(img, center, x, y+1),       # right
        get_pixel(img, center, x+1, y+1),     # bottom_right
        get_pixel(img, center, x+1, y),       # bottom
        get_pixel(img, center, x+1, y-1),     # bottom_left
        get_pixel(img, center, x, y-1),       # left
        get_pixel(img, center, x-1, y-1),     # top_left
        get_pixel(img, center, x-1, y)        # top
    ]
    power_val = [1, 2, 4, 8, 16, 32, 64, 128]
    val =     val = sum(val_ar[i] * power_val[i] for i in range(len(val_ar)))

    #print(val)
    return val

def show_output(output_list):
    """
    Display images and histograms based on the provided output list.
    """

    figure = plt.figure()

    for i, current_dict in enumerate(output_list):
        current_plot = figure.add_subplot(1, len(output_list), i + 1)

        if current_dict["type"] == "gray":
            current_plot.imshow(current_dict["img"], cmap=plt.get_cmap('gray'))
            current_plot.set_title(current_dict["title"])
            current_plot.set_xticks(current_dict["xtick"])
            current_plot.set_yticks(current_dict["ytick"])
            current_plot.set_xlabel(current_dict["xlabel"])
            current_plot.set_ylabel(current_dict["ylabel"])
        elif current_dict["type"] == "histogram":
            current_plot.plot(current_dict["img"], color="black")
            current_plot.set_xlim([0, 260])
            current_plot.set_title(current_dict["title"])
            current_plot.set_xlabel(current_dict["xlabel"])
            current_plot.set_ylabel(current_dict["ylabel"])
            ytick_list = [int(i) for i in current_plot.get_yticks()]
            current_plot.set_yticklabels(ytick_list, rotation=90)

    plt.show()
    
def main():
    image_file = 'GP/TTay.jpg'
    img_load = cv2.imread(image_file)
    img_bgr = cv2.resize(img_load, (400, 400))

    # Getting the height, width, and channel of the image
    height, width, _ = img_bgr.shape

    # Convert to gray image
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # Calculate LBP of the image
    img_lbp = np.zeros((height, width), np.uint8)


    for i in range(height):
        for j in range(width):
            img_lbp[i, j] = calculate_lbp_pixel(img_gray, i, j)

    # Process LBP image
    imgoned = np.zeros((16, 16), np.uint8)

    for rc in range(0, height, 16):
        for cc in range(0, width, 16):
            trc = rc
            for i in range(15):
                tcc = cc
                for j in range(15):
                    imgoned[i][j] = img_lbp[trc][tcc]
                    tcc += 1
                trc += 1

            hist_lbp1 = cv2.calcHist([imgoned], [0], None, [256], [0, 256])
            with open("_1test.txt", "a") as myfile:
                np.savetxt(myfile, np.array(hist_lbp1), fmt='%.2f')

    hist_lbp = cv2.calcHist([img_lbp], [0], None, [256], [0, 256])
    np.savetxt('GH/TTay.txt', np.array(hist_lbp), fmt='%.2f')

    # Prepare output for display
    output_list = [
        {"img": img_bgr, "title": "Image", "type": "gray"},
        {"img": img_gray, "title": "Gray Image", "type": "gray"},
        {"img": img_lbp, "title": "LBP Image", "type": "gray"},
        {
            "img": hist_lbp,
            "xlabel": "Bins",
            "ylabel": "Number of pixels",
            "title": "Histogram(LBP)",
            "type": "histogram",
        },
    ]

    # Display output
    show_output(output_list)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("LBP Program is finished")

if __name__ == '__main__':
    main()