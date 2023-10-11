# -*- coding: utf-8 -*-

import os
import sys
import glob
import re
import argparse
import numpy as np
import cv2
from tqdm import tqdm

def extract_number(filename):
    return int(re.search(r'\d+', filename).group())

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_dir', help='image directory', type=str)
    parser.add_argument('output_video', help='output vedeo path ', type=str)
    parser.add_argument('--fps', help='frames per second', default=30, type=int)
    args = parser.parse_args()
    return args



def img2video(image_dir, output_video, fps):
    # images = os.listdir(image_dir)
    images = [img for img in os.listdir(image_dir) if img.endswith(".png") or img.endswith(".jpg")]
    images.sort(key=extract_number)

    height, width, channels = cv2.imread(os.path.join(image_dir, images[0])).shape[:2]
    print(height, ", ", width)

    # Define the codec and create VideoWriter object

    fourcc = cv2.VideoWriter_fourcc(*'XVID') # .avi
    # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    # fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    videoWriter = cv2.VideoWriter(output_video, fourcc, fps, (width, height))                                                                                  cv2.Size=(width, height)


    for i in tqdm(images):
        filename = os.path.join(image_dir, i)
        # print(filename)
        img = cv2.imread(filename)
        if img is None:
            continue
        # print(img.shape)
        videoWriter.write(img)

    # Release everything if job is finished
    cv2.destroyAllWindows()
    videoWriter.release()



if __name__ == '__main__':
    args = parse_args()

    image_dir = args.image_dir
    image_dir = os.path.abspath(image_dir)
    output_video = args.output_video
    output_video = os.path.abspath(output_video)
    fps = args.fps

    if not os.path.exists(image_dir):
        print("Error !!! %s is not exists, please check the parameter"%image_dir)
        sys.exit(0)

    if not os.path.exists(os.path.basename(output_video)):
        print("Error !!! %s is not exists, please check the parameter"%os.path.basename(output_video))

    img2video(image_dir, output_video, fps)
    print("Done !")
