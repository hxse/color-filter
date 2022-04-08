#!/usr/bin/env python3
# coding: utf-8
import cv2
from posterization_photoshop_style import posterization
from levels_photoshop_style import level_filter
from change_hsv import change_hsv
from rgb2alpha import rgb2alpha, isWhite, notWhite
import numpy as np

num = 4  # 色阶分离个数,色调分离个数
numh = 2  # imshow每行并列显示个数
assert (num % numh == 0, "要整除,imshow才能并排显示,除非用空画布补全")

path = "test.jpg"
img = cv2.imread("test.jpg")

img = change_hsv(img, None, 0)
img = posterization(img, num)
# img=level_filter(img, 0,100, 0)

imgArr = []
for i in range(num):
    colorNum = int(255 / num)
    imgArr.append(level_filter(img, colorNum * i, colorNum * i + colorNum, 0))
img = imgArr[0]


def upgrade_nest(obj, step):
    return [obj[i : i + step] for i in range(0, len(obj), step)]


def get_stack(imgArr, numh):
    hstackArr = upgrade_nest(imgArr, numh)
    for index, value in enumerate(hstackArr):
        hstackArr[index] = np.hstack(value)
    return np.vstack(hstackArr)


img = get_stack(imgArr, numh)
cv2.imwrite("out/test/test_out.jpg", img)

img_isWhite_alpha = rgb2alpha(img, isWhite)
img_notWhite_alpha = rgb2alpha(img, notWhite)
cv2.imwrite("out/test/isWhite_alpha.png", img_isWhite_alpha, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
cv2.imwrite("out/test/notWhite_alpha.png", img_notWhite_alpha, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])


# cv2.imshow("image", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
