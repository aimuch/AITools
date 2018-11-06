### Author : Andy
### Last modified : 2018-11-02

### This tool is used to draw bbox labels 
### -----------EXAMPLE-------------------
### python img_resize.py \
###        /home/data/Annotations \
###        /home/data/JPEGImages \
###        /home/data/output_draw

import os 
import sys
import argparse
import cv2
from tqdm import tqdm

size_dst = (416, 416) # Output size

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('img_src', help='source images directory', type=str)
    parser.add_argument('img_dst', help='output images directory', type=str)
    args = parser.parse_args()
    return args


def reimg(img_src, img_dst):
    folderlist = os.listdir(img_src)
    for folder in folderlist:
        folder_path = os.path.join(img_src, folder)
        filelist = os.listdir(folder_path)
        for file in tqdm(filelist):
            img_path = os.path.join(folder_path, file)
            img = cv2.imread(img_path)
            if img is None:
              print("%s can't read!"%file)
              continue
            output_folder = os.path.join(img_dst, folder)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            output_path = os.path.join(output_folder, file)
            #print("output_path:%s"%output_path)
            imgresized = cv2.resize(img, size_dst)
            cv2.imwrite(output_path, imgresized)
        print("%s done"%folder_path)

if __name__ == '__main__':
    args = parse_args()
    img_src = args.img_src
    img_dst = args.img_dst

    if not os.path.exists(img_src):
        print("Error !!! %s is not exists, please check the parameter"%img_src)
        sys.exit(0)

    if not os.path.exists(img_dst):
        os.makedirs(img_dst)
        print("Output folder = ", os.path.abspath(img_dst))

    reimg(img_src, img_dst)
