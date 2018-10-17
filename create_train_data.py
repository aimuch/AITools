# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-10-16
# This tool is used to create data when the training samples are not balanced
# input : python3 create_train_data.py "/home/andy/data/ann_dir" "/home/andy/data/img_dir"
# output:
#	     ./new_img
#        ./new_labels

import os
import os.path
import shutil
import sys
import argparse
import random
import cv2
from tqdm import tqdm

wait4AddLabels = [0]
scales = [0.6, 1.8]


def parse_args():
    """Parsing input command syntax"""
    parser = argparse.ArgumentParser()
    parser.add_argument('ann_dir_src', help='Annotations directory', type=str)
    parser.add_argument('img_dir_src', help='Images directory', type=str)
    parser.add_argument('ROIs_dir', help='ROI images directory', type=str)
    parser.add_argument('-n','--num', help='image display wait time', default=100, type=int)

    args = parser.parse_args()
    return args


def rotate(image, angle, center=None, scale=1.0): 
    (h, w) = image.shape[:2]
    if center is None:
        center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, scale) 
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated


def convert(imgsize, box):
    dw = 1./(imgsize[0])
    dh = 1./(imgsize[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


def createData(ann_dir_src, img_dir_src, ROIs_dir, wait4AddLabels, num, scales):
    """Create training data by exiting labels"""
    ann_dir_dst = "./new_labels"
    img_dir_dst = "./new_img"
    if os.path.exists(ann_dir_dst):
        shutil.rmtree(ann_dir_dst)  
    os.makedirs(ann_dir_dst)
    if os.path.exists(img_dir_dst):
        shutil.rmtree(img_dir_dst)  
    os.makedirs(img_dir_dst)
   
    ## change to abs path
    ann_dir_src = os.path.abspath(ann_dir_src)
    img_dir_src = os.path.abspath(img_dir_src)
    ann_dir_dst = os.path.abspath(ann_dir_dst)
    img_dir_dst = os.path.abspath(img_dir_dst)
    ROIs_dir = os.path.abspath(ROIs_dir)
    ## Remove "/" from the last path
    if ann_dir_src[-1] == "/":
        ann_dir_src = ann_dir_src[:-1]
    if img_dir_src[-1] == "/":
        img_dir_src = img_dir_src[:-1]
    if ann_dir_dst[-1] == "/":
        ann_dir_dst = ann_dir_dst[:-1]
    if img_dir_dst[-1] == "/":
        img_dir_dst = img_dir_dst[:-1]
    if ROIs_dir[-1] == "/":
        ROIs_dir = ROIs_dir[:-1]
    
    img_list = os.listdir(img_dir_src)

    for label in wait4AddLabels:
        roi_folder = ROIs_dir + "/" + str(label)
        roi_list = os.listdir(roi_folder)

        ann_folder_dst = ann_dir_dst + "/" + str(label)
        img_folder_dst = img_dir_dst + "/" + str(label)
        os.makedirs(ann_folder_dst)
        os.makedirs(img_folder_dst)
        
        for i in tqdm(range(num)):
            roi_name = random.choice(roi_list)
            roi_path = roi_folder + "/" + roi_name
            roi_img = cv2.imread(roi_path)
            roi_height, roi_width, roi_channel = roi_img.shape

            ## Data Augment
            scale_w = random.uniform(scales[0], scales[1])
            scale_h = random.uniform(scales[0], scales[1])
            newSize = (int(roi_height*scale_h), int(roi_width*scale_w)) 
            roi_img_new = cv2.resize(roi_img, newSize)
            #cv2.imwrite("./roi.jpg", roi_img_new)
            
            roi_height_new, roi_width_new, roi_channel = roi_img_new.shape
            img_name = random.choice(img_list)
            img_path = img_dir_src + "/" + img_name
            img = cv2.imread(img_path)
            height, width, channel = img.shape
            top = random.randint(int(height*0.1), int(height*0.9)-roi_height_new)
            left = random.randint(int(width*0.1), int(width*0.9)-roi_width_new)
            ## Check ROI
            #cv2.rectangle(img, (left, top), (left+roi_width_new, top+roi_height_new), (0,255,0), 2)
            img[top:top+roi_height_new, left:left+roi_width_new] = roi_img_new
            img_path_dst = img_folder_dst + "/" + img_name.split(".")[-2] + "_" + str(i) + ".jpg"
            cv2.imwrite(img_path_dst, img)
            cv2.waitKey(5)
            
            ## labels
            label_src_path = ann_dir_src + "/" + img_name.split(".")[-2] + ".txt"
            label_src = open(label_src_path, "r")
            lines_src = label_src.read().split('\n')[:-1]
            box = (float(left), float(left+roi_width_new), float(top), float(top+roi_height_new))
            bb = convert((width, height), box)
            objs = [str(label) + ' ' + ' '.join([str(i) for i in bb])]
            for line in lines_src:
                objs.append(line)
            label_src.close()

            label_dst_path = ann_folder_dst + "/" + img_name.split(".")[-2] + "_" + str(i) + ".txt"
            label_dst = open(label_dst_path, 'w')
            for obj in objs:
            	label_dst.write(obj + '\n')

if __name__ == '__main__':
    args = parse_args()
    ann_dir_src = args.ann_dir_src
    img_dir_src = args.img_dir_src
    ROIs_dir = args.ROIs_dir
    num = args.num
    if not os.path.exists(ann_dir_src):
        print("Error !!! %s is not exists, please check the parameter"%ann_dir_src)
        sys.exit(0)
    if not os.path.exists(img_dir_src):
        print("Error !!! %s is not exists, please check the parameter"%img_dir_src)
        sys.exit(0)
    if not os.path.exists(ROIs_dir):
        print("Error !!! %s is not exists, please check the parameter"%ROIs_dir)
        sys.exit(0)
    if not num:
        print("Error !!! %s is not exists, please check the parameter"%num)
        sys.exit(0)
    
    createData(ann_dir_src, img_dir_src, ROIs_dir, wait4AddLabels, num, scales)