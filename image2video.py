# -*- coding: utf-8 -*-

import os
import sys
import glob
from tqdm import tqdm
import argparse
import numpy as np
import cv2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_dir', help='image directory', type=str)
    parser.add_argument('output_dir', help='output vedeo directory ', type=str)
    parser.add_argument('--fps', help='frames per second', default=10, type=int)
    args = parser.parse_args()
    return args



def img2video(image_dir, output_dir, fps):
    img_list = os.listdir(image_dir)
    img_shape = cv2.imread(os.path.join(image_dir, img_list[0])).shape[:2]
    print(img_shape)

    # Define the codec and create VideoWriter object

    #fourcc = cv2.VideoWriter_fourcc(*'XVID') # .avi
    # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    videoWriter = cv2.VideoWriter(os.path.join(output_dir, 'output.avi'), fourcc, fps, (img_shape[1], img_shape[0]))

    for i in tqdm(img_list):
        filename = os.path.join(image_dir, i)
        # print(filename)
        img = cv2.imread(filename)
        if img is None:
            continue
        # print(img.shape)
        videoWriter.write(img)

    # Release everything if job is finished
    videoWriter.release()



if __name__ == '__main__':
    args = parse_args()

    image_dir = args.image_dir
    image_dir = os.path.abspath(image_dir)
    output_dir = args.output_dir
    output_dir = os.path.abspath(output_dir)
    fps = args.fps

    if not os.path.exists(image_dir):
        print("Error !!! %s is not exists, please check the parameter"%image_dir)
        sys.exit(0)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img2video(image_dir, output_dir, fps)
    print("Done !")
