#!/usr/bin/env python3
# coding: utf-8
import cv2
import numpy as np


def isWhite(img, h, v):
    return img[h, v, 0] == 255 and img[h, v, 1] == 255 and img[h, v, 2] == 255

def notWhite(img, h, v):
    return not isWhite(img, h, v)


def rgb2alpha(img, callback):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    for h in range(0, img.shape[0]):  # 访问所有行
        for v in range(0, img.shape[1]):  # 访问所有列
            if callback(img, h, v):
                img[h, v, 3] = 0
    return img
    B, G, R, A = cv2.split(img)
    rgbImg = cv2.merge([B, G, R])
    cv2.imshow("RGB", rgbImg)
    cv2.imshow("A", A)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    img = cv2.imread("out/test/test_out.jpg")
    img = rgb2alpha(img, isWhite)
    # jpg不支持不透明,png支持
    cv2.imwrite("out/test/isWhite_alpha.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

    img = cv2.imread("out/test/test_out.jpg")
    img = rgb2alpha(img, notWhite)
    # jpg不支持不透明,png支持
    cv2.imwrite("out/test/notWhite_alpha.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
