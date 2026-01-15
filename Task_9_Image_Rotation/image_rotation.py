import cv2 as cv
import math
import numpy as np
import matplotlib.pyplot as plt

def image_rotation(path):

    img = cv.imread(img_path)

    # converting image to RGB
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    # converting image to GRAY SCALE
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Edge detection of an image through Canny
    edges = cv.Canny(img_gry, 250, 250, apertureSize=3)

    # Detect Lines of an image through Houghlines
    lines = cv.HoughLines(edges, 2, np.pi / 90, 280)

    angles = []
    for r_theta in lines:
        # storing theta values of lines
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr

        # store theta values in a and b
        a = np.cos(theta)
        b = np.sin(theta)

        # stores value of rcos and rsin
        X0 = a * r
        Y0 = b * r

        # stores the round off values high coordinates
        X1 = int(X0 + 1000 * (-b))
        Y1 = int(Y0 + 1000 * (a))

        # store the the round off values - low coordinates
        X2 = int(X0 - 1000 * (-b))
        Y2 = int(Y0 - 1000 * (a))

        # Returning the angle in radians between the positive x-axis and the point (x, y)
        angle_rad = math.atan2(Y2 - Y1, X2 - X1)

        # converting radian to degrees
        angle_deg = math.degrees(angle_rad)

        angles.append(angle_deg)
        # cv.line(img, (X1, Y1), (X2, Y2), (0, 0, 255), 2)

    angle_deg = max(angles)

    # print(angle_deg)

    # image height width shaping
    (h, w) = img.shape[:2]

    # Find the center of the image
    center = (w // 2, h // 2)

    # Creating image transformation matrics with the perticular angle with respect to the center
    M = cv.getRotationMatrix2D(center, angle_deg, 1.0)
    # apply the rotation that use matrics
    rotated = cv.warpAffine(
        img_rgb, M, (w, h), flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE
    )

    # ploting the images - ORIGNAL and ROTATED
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(img_rgb)
    axes[0].set_title("Original Image")
    axes[1].imshow(rotated)
    axes[1].set_title("Corrected Image")
    plt.show()



img_path = input("Enter Image Path >> ")


if __name__ == '__main__':
    image_rotation(img_path)