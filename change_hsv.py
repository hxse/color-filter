#!/usr/bin/env python3
import numpy as np
import cv2


# coding: utf-8
def change_hsv(img, h=None, s=None, v=None, h2=None, s2=None, v2=None):
    """h,s,v,是绝对值0-255,h2,s2,v2,是相对值,正整数代表增加,负整数代表减少"""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = hsv.astype(np.int16)
    if h != None:
        hsv[:, :, 0] = h
    if s != None:
        hsv[:, :, 1] = s
    if v != None:
        hsv[:, :, 2] = v
    if h2 != None:
        hsv[:, :, 0] += h2
    if s2 != None:
        hsv[:, :, 1] += s2
    if v2 != None:
        hsv[:, :, 2] += v2
    hsv.clip(0, 255, out=hsv)
    hsv = hsv.astype(np.uint8)
    out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return out


if __name__ == "__main__":
    img = cv2.imread("test.jpg")
    img = change_hsv(img, None, 0, None, None, None, None)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
