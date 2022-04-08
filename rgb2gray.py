#!/usr/bin/env python3
# coding: utf-8
import cv2


def rgb2gray(img):
    # 转为灰度图像,不建议用,因为数组结构会发生变化
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


if __name__ == "__main__":
    img = cv2.imread('test.jpg')
    img=rgb2gray(img)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
