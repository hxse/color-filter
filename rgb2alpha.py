#!/usr/bin/env python3
# coding: utf-8
import cv2
import numpy as np


def isWhite(img):
    # https://stackoverflow.com/questions/19770361/find-index-positions-where-3d-array-meets-multiple-conditions
    cond1 = np.logical_and(
        img[:, :, 0] == 255, img[:, :, 1] == 255, img[:, :, 2] == 255
    )
    cond2 = (img[:, :, 0] == 255) & (img[:, :, 1] == 255) & (img[:, :, 2] == 255)
    cond3 = [img[:, :, 0] == 255, img[:, :, 1] == 255, img[:, :, 2] == 255]
    return cond1


def notWhite(img):
    return ~isWhite(img)


def isWhite2(img, h, v):
    return img[h, v, 0] == 255 & img[h, v, 1] == 255 & img[h, v, 2] == 255


def notWhite2(img, h, v):
    return not isWhite2(img, h, v)


def rgb2alpha(img, trans_mask):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    cw = np.where(trans_mask(img))
    hArr, vArr = cw
    for h, v in zip(hArr, vArr):
        # 这里实在没能力把for循环删掉,where返回的是新对象,速度过得去,建议别尝试了
        img[h][v][3] = 0
    return img


def rgb2alpha2(img, callback):
    # 太慢了
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
    """
    模式1,程序运行时间:2079.610586166382 毫秒
    模式2,程序运行时间:31401.586532592773 毫秒
    """
    testPath = "out/test/test_out.jpg"
    import time

    T1 = time.time()
    img = cv2.imread(testPath)
    img = rgb2alpha(img, isWhite)
    # jpg不支持不透明,png支持
    cv2.imwrite(
        "out/test/isWhite_alpha.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0]
    )
    img = cv2.imread(testPath)
    img = rgb2alpha(img, notWhite)
    # jpg不支持不透明,png支持
    cv2.imwrite(
        "out/test/notWhite_alpha.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0]
    )
    T2 = time.time()
    print(f"模式1,程序运行时间:{(T2 - T1)*1000} 毫秒")

    T1 = time.time()
    img = cv2.imread(testPath)
    img = rgb2alpha2(img, isWhite2)
    # jpg不支持不透明,png支持
    cv2.imwrite(
        "out/test/isWhite_alpha2.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0]
    )
    img = cv2.imread(testPath)
    img = rgb2alpha2(img, notWhite2)
    # jpg不支持不透明,png支持
    cv2.imwrite(
        "out/test/notWhite_alpha2.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0]
    )
    T2 = time.time()
    print(f"模式2,程序运行时间:{(T2 - T1)*1000} 毫秒")
