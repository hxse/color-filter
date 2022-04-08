#!/usr/bin/env python3
# coding: utf-8
from httpx import main
import numpy as np
import cv2


def posterization(img, level):
    '''
    https://stackoverflow.com/questions/11064454/adobe-photoshop-style-posterization-and-opencv
    level  # Number of levels of quantization
    '''

    indices = np.arange(0, 256)  # List of all colors

    divider = np.linspace(0, 255, level + 1)[1]  # we get a divider

    quantiz = np.int0(np.linspace(0, 255, level))  # we get quantization colors

    color_levels = np.clip(
        np.int0(indices / divider), 0, level - 1
    )  # color levels 0,1,2..

    palette = quantiz[color_levels]  # Creating the palette

    img2 = palette[img]  # Applying palette on image

    img2 = cv2.convertScaleAbs(img2)  # Converting image back to uint8
    return img2
if __name__ == "__main__":
    img = cv2.imread("test.jpg")
    img=posterization(img, 4)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

