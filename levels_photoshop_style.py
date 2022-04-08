#!/usr/bin/env python3
# coding: utf-8
import numpy as np
import cv2

"""
用于图像预处理，模拟ps的色阶调整
img：传入的图片
Highlight：白场(Shadow-255)
Shadow：黑场(0-Highlight)
0 <= Shadow < Highlight <= 255
返回一张图片
"""


def level_filter(img, inB, inW, inG=1.0, outB=0, outW=255):
    inBlack = np.array([inB, inB, inB], dtype=np.float32)
    inWhite = np.array([inW, inW, inW], dtype=np.float32)
    inGamma = np.array([inG, inG, inG], dtype=np.float32)
    outBlack = np.array([outB, outB, outB], dtype=np.float32)
    outWhite = np.array([outW, outW, outW], dtype=np.float32)

    img = np.clip((img - inBlack) / (inWhite - inBlack), 0, 255)
    img = (img ** (1 / inGamma)) * (outWhite - outBlack) + outBlack
    img = np.clip(img, 0, 255).astype(np.uint8)
    return img


if __name__ == "__main__":
    img = cv2.imread("test.jpg")
    img = level_filter(img, 81, 161)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
