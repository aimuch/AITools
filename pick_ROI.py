# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-10-16
# This tool is used to pick ROI by labels
# input : python3 pick_ROI.py "/home/andy/data/ann_dir" "/home/andy/data/img_dir"
# output:
#	     ./ROIs/

import os
import os.path
import shutil
import sys
import argparse
import cv2
from tqdm import tqdm

picklabels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]

picklabels = [ str(i) for i in picklabels ]
objdict = {}

def parse_args():
    """Parsing input command syntax"""
    parser = argparse.ArgumentParser()
    parser.add_argument('ann_dir', help='Annotations directory', type=str)
    parser.add_argument('img_dir', help='Images directory', type=str)

    args = parser.parse_args()
    return args

def convert(imsize, x,y,w,h):
    box = []
    box.append(int(x*imsize[0] + 1.0 - 0.5*w*imsize[0])) #xmin
    box.append(int(y*imsize[1] + 1.0 - 0.5*h*imsize[1])) #ymin
    box.append(int(x*imsize[0] + 1.0 + 0.5*w*imsize[0])) #xmax
    box.append(int(y*imsize[1] + 1.0 + 0.5*h*imsize[1])) #ymax
    return box

def createData(ann_dir, img_dir, picklabels):
    """Create training data by exiting labels"""
    
    ## Change to abs path
    ann_dir = os.path.abspath(ann_dir)
    img_dir = os.path.abspath(img_dir)

    ## Remove "/" from the last path
    if ann_dir[-1] == "/":
        ann_dir = ann_dir[:-1]
    if img_dir[-1] == "/":
        img_dir = img_dir[:-1]

    ## Output folders
    output_dir = "./ROIs"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)  
    os.makedirs(output_dir)

    ## Check path whether include "/"
    if output_dir[-1] == "/":
        output_dir = output_dir[:-1]
    

    annList = os.listdir(ann_dir)
    for txt in tqdm(annList):
        #print(txt + "-->start!")

        ## Pick the same name image frome image folders
        fileInfor = os.path.splitext(txt)
        img_name = fileInfor[0] + '.jpg'
        imgpath = img_dir + "/" + img_name
        if not os.path.exists(imgpath):
            img_name = fileInfor[0] + '.png'
            imgpath = img_dir + "/" + img_name
        if not os.path.exists(imgpath):
            continue

        img = cv2.imread(imgpath)
        if img is None:
            print("%s can't read!"%img_name)
            continue

        labelfile = open(ann_dir + "/" + txt, "r")
        lines = labelfile.read().split('\n')[:-1]    #['3 0.33 0.55 0.01 0.02', '3 0.82 0.51 0.05 0.08', '']
        for line in lines:
            objinfo = line.split(" ") # type(objinfo[0])=str
            obj = objinfo[0]
            if obj not in picklabels:
                continue
            else:
                imshape = img.shape
                imsize = [imshape[1], imshape[0]]
                roi_box = convert(imsize, float(objinfo[1]),float(objinfo[2]),float(objinfo[3]),float(objinfo[4]))
                roi_img = img[roi_box[1]:roi_box[3],roi_box[0]:roi_box[2]]

                if not obj in objdict:
                    objdict[obj] = 1
                    imgfolder = output_dir + "/" + obj
                    os.makedirs(imgfolder)
                else:
                    objdict[obj] += 1
                    imgfolder = output_dir + "/" + obj
                
                imgpath = imgfolder + "/" + str(objdict[obj]) + ".jpg"
                cv2.imwrite(imgpath, roi_img)

        labelfile.close()
        
    print("Done!")
    print("Path of ROI = ", os.path.abspath(output_dir))
 

if __name__ == '__main__':
    args = parse_args()
    ann_dir = args.ann_dir
    img_dir = args.img_dir
    if not os.path.exists(ann_dir):
        print("Error !!! %s is not exists, please check the parameter"%ann_dir)
        sys.exit(0)
    if not os.path.exists(img_dir):
        print("Error !!! %s is not exists, please check the parameter"%img_dir)
        sys.exit(0)

    createData(ann_dir, img_dir, picklabels)
