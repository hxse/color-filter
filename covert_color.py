#!/usr/bin/env python3
# coding: utf-8
import cv2
from posterization_photoshop_style import posterization
from levels_photoshop_style import level_filter
from change_hsv import change_hsv
from rgb2alpha import rgb2alpha, isWhite, notWhite
import numpy as np
import pathlib
from pathlib import Path


def getImgArr(path, num, numh):
    """
    num = 4  # 色阶分离个数,色调分离个数
    numh = 2  # imshow每行并列显示个数
    """
    assert (num % numh == 0, "要整除,imshow才能并排显示,除非用空画布补全")

    img = cv2.imread(str(path))

    img = change_hsv(img, None, 0)
    img = posterization(img, num)
    # img=level_filter(img, 0,100, 0)

    imgArr = []
    for i in range(num):
        colorNum = int(255 / num)
        imgArr.append(level_filter(img, colorNum * i, colorNum * i + colorNum, 0))
    return imgArr


def upgrade_nest(obj, step):
    return [obj[i : i + step] for i in range(0, len(obj), step)]


def get_stack(imgArr, numh):
    hstackArr = upgrade_nest(imgArr, numh)
    for index, value in enumerate(hstackArr):
        hstackArr[index] = np.hstack(value)
    return np.vstack(hstackArr)


def mkdir(path):
    return Path(path).mkdir(parents=True, exist_ok=True)


def write(img, path, outName, index=""):
    getIndex = lambda x: "" if x == "" else f"{x}_"
    # import pdb; pdb.set_trace()

    cv2.imwrite(
        Path(f"{path}/{outName.stem}_out_{getIndex(index)}.png").as_posix(),
        img,
        [int(cv2.IMWRITE_PNG_COMPRESSION), 0],
    )
    img_isWhite_alpha = rgb2alpha(img, isWhite)
    img_notWhite_alpha = rgb2alpha(img, notWhite)
    cv2.imwrite(
        Path(f"{path}/{outName.stem}_isWhite_alpha_{getIndex(index)}.png").as_posix(),
        img_isWhite_alpha,
        [int(cv2.IMWRITE_PNG_COMPRESSION), 0],
    )
    cv2.imwrite(
        Path(f"{path}/{outName.stem}_notWhite_alpha_{getIndex(index)}.png").as_posix(),
        img_notWhite_alpha,
        [int(cv2.IMWRITE_PNG_COMPRESSION), 0],
    )


def stack_img(inName, outName="", path="", num=4, numh=2):
    inName = Path(inName)
    path = Path(f"out/{inName.stem}_stack_{num}") if not path else Path(path)
    outName = inName if not outName else Path(outName)
    mkdir(path)

    imgArr = getImgArr(inName, num, numh)
    img = get_stack(imgArr, numh)
    write(img, path, outName)

    # cv2.imshow("image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def separate_img(inName, outName="", path="", num=4, numh=2):
    inName = Path(inName)
    path = Path(f"out/{inName.stem}_separate_{num}") if not path else Path(path)
    outName = inName if not outName else Path(outName)
    mkdir(path)

    imgArr = getImgArr(inName, num, numh)
    for index, img in enumerate(imgArr):
        write(img, path, outName, index)


# def separate_img(name="test_out.png", path="out/test/separate", num=4):
#     mkdir(f"{path}_{num}")
#     for index, img in enumerate(imgArr):
#         cv2.imwrite(f"{path}/{index}_name", img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

#         img_isWhite_alpha = rgb2alpha(img, isWhite)
#         img_notWhite_alpha = rgb2alpha(img, notWhite)
#         cv2.imwrite(
#             f"{path}/isWhite_alpha_{index}.png",
#             img_isWhite_alpha,
#             [int(cv2.IMWRITE_PNG_COMPRESSION), 0],
#         )
#         cv2.imwrite(
#             f"{path}/notWhite_alpha_{index}.png",
#             img_notWhite_alpha,
#             [int(cv2.IMWRITE_PNG_COMPRESSION), 0],
#         )


if __name__ == "__main__":
    """
    拼接存放,程序运行时间:1163.0017757415771 毫秒
    单独存放,程序运行时间:1143.8803672790527 毫秒
    """
    import time

    T1 = time.time()
    main()
    T2 = time.time()
    print(f"拼接存放,程序运行时间:{(T2 - T1)*1000} 毫秒")

    T1 = time.time()
    separate_img()
    T2 = time.time()
    print(f"单独存放,程序运行时间:{(T2 - T1)*1000} 毫秒")
