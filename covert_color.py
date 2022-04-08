#!/usr/bin/env python3
# coding: utf-8
import cv2
from posterization_photoshop_style import posterization
from levels_photoshop_style import level_filter
from change_hsv import change_hsv
from rgb2alpha import rgb2alpha, isWhite, notWhite
import numpy as np
import pathlib

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


def mkdir(path):
    return pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def main():
    path = "out/test/stack" + str(num)
    mkdir(path)
    img = get_stack(imgArr, numh)
    cv2.imwrite(f"{path}/test_out.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

    img_isWhite_alpha = rgb2alpha(img, isWhite)
    img_notWhite_alpha = rgb2alpha(img, notWhite)
    cv2.imwrite(
        f"{path}/isWhite_alpha.png",
        img_isWhite_alpha,
        [int(cv2.IMWRITE_PNG_COMPRESSION), 0],
    )
    cv2.imwrite(
        f"{path}/notWhite_alpha.png",
        img_notWhite_alpha,
        [int(cv2.IMWRITE_PNG_COMPRESSION), 0],
    )

    # cv2.imshow("image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def main2():
    path = "out/test/single"
    mkdir(path)
    for index, img in enumerate(imgArr):
        cv2.imwrite(
            f"{path}/test_out_{index}.png", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0]
        )

        img_isWhite_alpha = rgb2alpha(img, isWhite)
        img_notWhite_alpha = rgb2alpha(img, notWhite)
        cv2.imwrite(
            f"{path}/isWhite_alpha_{index}.png",
            img_isWhite_alpha,
            [int(cv2.IMWRITE_PNG_COMPRESSION), 0],
        )
        cv2.imwrite(
            f"{path}/notWhite_alpha_{index}.png",
            img_notWhite_alpha,
            [int(cv2.IMWRITE_PNG_COMPRESSION), 0],
        )


if __name__ == "__main__":
    '''
    拼接存放,程序运行时间:1163.0017757415771 毫秒
    单独存放,程序运行时间:1143.8803672790527 毫秒
    '''
    import time
    T1 = time.time()
    main()
    T2 = time.time()
    print(f"拼接存放,程序运行时间:{(T2 - T1)*1000} 毫秒")

    T1 = time.time()
    main2()
    T2 = time.time()
    print(f"单独存放,程序运行时间:{(T2 - T1)*1000} 毫秒")

