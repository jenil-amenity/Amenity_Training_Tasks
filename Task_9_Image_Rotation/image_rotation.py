import cv2 as cv
import math
import numpy as np
import matplotlib.pyplot as plt


def image_rotation(path):

    img = cv.imread(path)

    # converting image to RGB : parameters - image and formate of the image like in RGB
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    # converting image to GRAY SCALE : parameters - image and formate of the image like grayscale
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Edge detection of an image through Canny: parameters
    # - passed gray scale img for better edge detection, lower threshhold : edge detection ni minimum limit set karva
    # - upper threshhold : max limit of edge detection set krva it will not detect edge after this value

    edges = cv.Canny(img_gry, 250, 250)

    # Detect Lines of an image through Houghlines
    # to find the edge lines in the image for roatation : edges of img, line ni width set karva 2, calculating angle of the lines,
    # 280 - threshhold value 6e ke jenathi a line max aa value sudhi j detect krse enathi highest value thi a return kri dese detect nahi kre
    lines = cv.HoughLines(edges, 2, np.pi / 90, 280)

    # for loop to convert lines values to angles
    angles = []
    for r_theta in lines:
        # storing theta values of lines
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr  # theta value and radians value arr mathi extract krse

        # store theta values in a and b
        a = np.cos(theta)  # a coordinate[theta] value ne cosec ma convert krse
        b = np.sin(theta)  # b coordinate[theta] value ne sin ma convert krse

        # stores value of rcos and rsin
        X0 = a * r  # theta * radian [angle curve of the line]
        Y0 = b * r  # theta * radian [angle curve of the line]

        # stores the round off values high coordinates
        X1 = int(
            X0 + 1000 * (-b)
        )  # theta values X1 ne coordinates ma convert krse that is showing in chart
        Y1 = int(Y0 + 1000 * (a))  # same as above for Y1

        # store the the round off values - low coordinates
        X2 = int(X0 - 1000 * (-b))
        Y2 = int(Y0 - 1000 * (a))

        # Returning the angle in radians between the positive x-axis and the point (x, y)
        # atan2 funtion thi line na bne coordinates thi center find krse jeti radius no center point madi jai
        angle_rad = math.atan2(Y2 - Y1, X2 - X1)

        # converting radian to degrees
        # and_rad thi line ne ketla degree roatation ni jrur 6e a find krse
        angle_deg = math.degrees(angle_rad)

        angles.append(angle_deg)
        # appending all angles in list
        # cv.line(img, (X1, Y1), (X2, Y2), (0, 0, 255), 2)

    # ghani lines na coordinate negative ma jata hase jethi degrees loop ma negative ma avi sake
    # Etle max angle find krisu angles ni list mathi
    angle_deg = max(angles)

    # print(angle_deg)

    # image height width shaping
    # height and width deifin krsu same as image
    (h, w) = img.shape[:2]

    # Find the center of the image
    # rotation krva mate image nu center find karisu
    center = (w // 2, h // 2)

    # Creating image transformation matrics with the perticular angle with respect to the center
    # aa function thi image roatation complete thast with the imagecenter, rotation_angle, scale =1.0 ketli image zoom in krvi 6e
    M = cv.getRotationMatrix2D(center, angle_deg, 1.0)

    # apply the rotation that use matrics
    # aa function thi rotation nu calculation image ma apply krva mate use thase
    # colored image, rotation calculation, image upscaling krva flag inter cubic use thase
    # and after roatation image ni borders blank na rahi jai te mate border_replicate image complete krva mate
    rotated = cv.warpAffine(
        img_rgb, M, (w, h), flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE
    )

    # ploting the images - ORIGNAL and ROTATED
    fig, axes = plt.subplots(
        1, 2, figsize=(10, 5)
    )  # subplotting of two graph in one image
    axes[0].imshow(img_rgb)  # 0 index par original image show krva
    axes[0].set_title("Original Image")
    axes[1].imshow(rotated)  # 1 index par toated image
    axes[1].set_title("Corrected Image")
    plt.show()


if __name__ == "__main__":
    img_path = input("Enter Image Path >> ")
    image_rotation(img_path)
