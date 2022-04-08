#!/usr/bin/env python3
# coding: utf-8
import fire
from covert_color import stack_img,separate_img

if __name__ == '__main__':

    fire.Fire({'ti':stack_img,'pi':separate_img})
