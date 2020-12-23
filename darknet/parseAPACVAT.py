# -*- coding: utf-8 -*-
# Reference VOC scrips
# Author : Andy Liu
# last modify : 2020-09-27

# This tool is used to convert VOC xml format to YOLO V3 format
# And pick 80% for train, left for val
# Files Tree: NOTE: One xml file corresponds to one image folder
# .
# ├── img
# │   ├── 1
# │   │   ├── img_1.jpg
# │   │   └── img_2.jpg
# │   └── 2
# │       ├── img_1.jpg
# │       └── img_2.jpg
# └──  label
#     ├── 1.xml
#     └── 2.xml

# input : python parseAPACVAT.py "./label"   "./img"
# output :
#       ./txt
#		./train.txt
#		./val.txt
#       ./trainAll.txt

import xml.dom.minidom
import random
import pickle
import os
import sys
import cv2
import argparse
import shutil
from os import listdir, getcwd
from os.path import join
from tqdm import tqdm

WITH_IMAGE = True
REWRITE = True
DRAW_LABEL = True
COPY_TXT_TO_IMG_FOLDER = True
TRAIN_RATE = 0.8
CONER_ROI_SIZE = 31

classes = ["ps_box", "ps_point"]

error_log = "./log.txt"
draw_folder = "draw_img"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('xml_dir', help='xml directory', type=str)
    if WITH_IMAGE:
        parser.add_argument('img_dir', help='image directory', type=str)

    args = parser.parse_args()
    return args

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = abs(box[1] - box[0]) #box[1] - box[0]
    h = abs(box[3] - box[2]) #box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x, y, w, h)

def convert_annotation(xml_dir, img_dir):
    '''
    One xml file corresponds to one image folder
    '''
    xml_dir = os.path.abspath(xml_dir)
    if xml_dir[-1] == "/":
        xml_dir = xml_dir[:-1]

    if WITH_IMAGE:
        img_dir = os.path.abspath(img_dir)
        if img_dir[-1] == "/":
            img_dir = img_dir[:-1]

    xmlList = os.listdir(xml_dir)
    imgFolderList = os.listdir(img_dir)
    # imgNum = None
    # for folder in imgFolderList:
    #     folderPath = os.path.join(img_dir, folder)
    #     imgList = os.listdir(folderPath)
    #     imgNum += len(imgList)

    # print("images num = ", imgNum)

    # trainnum = int(len(filelist)*TRAIN_RATE)
    # trainset = random.sample(filelist, trainnum)

    txt_dir = os.path.join(os.path.dirname(xml_dir), os.path.basename(xml_dir) + "_txt")
    if os.path.exists(txt_dir):
        shutil.rmtree(txt_dir)
    os.makedirs(txt_dir)
    # txt_train_path =  os.path.join(os.path.dirname(xml_dir), "train.txt")
    # txt_val_path =  os.path.join(os.path.dirname(xml_dir), "val.txt")

    if REWRITE:
        txt_train_path =  "./train.txt"
        txt_val_path =  "./val.txt"
        txt_train_list = open(txt_train_path, 'a+')
        txt_val_list = open(txt_val_path, 'a+')
        log_file = open(error_log, 'a+')
    else:
        txt_train_path =  os.path.join(os.path.dirname(xml_dir), "train.txt")
        txt_val_path =  os.path.join(os.path.dirname(xml_dir), "val.txt")
        txt_train_list = open(txt_train_path, 'w')
        txt_val_list = open(txt_val_path, 'w')
        log_file = open(error_log, 'w')

    for f in xmlList:
        print(f + "-->start!")
        xmlInfor = f.split(".")
        xmlPath = os.path.join(xml_dir, f)

        if not os.path.exists(xmlPath):
            print(xmlPath, "is not exists!")
            log_file.write(xmlPath + "\n")
            continue

        dom = xml.dom.minidom.parse(xmlPath)
        annotation = dom.documentElement
        meta = annotation.getElementsByTagName('meta')[0]
        task = meta.getElementsByTagName('task')[0]
        xmlName = task.getElementsByTagName('name')[0].childNodes[0].data
        imgNumInXml = task.getElementsByTagName('size')[0].childNodes[0].data
        images = annotation.getElementsByTagName('image')
        imgInXmlList = []
        txtList = []
        for image in images:
            imageID = image.getAttribute("id")
            imageName = image.getAttribute("name")
            width = image.getAttribute("width")
            height = image.getAttribute("height")
            if '/' in imageName:
                imagePath = os.path.join(img_dir, imageName)
                imgInXmlList.append(imagePath.split('/')[-1])
            else:
                imagePath = os.path.join(img_dir, xmlName, imageName)
                imgInXmlList.append(imagePath)

            # Check if image exists
            if not os.path.exists(imagePath):
                print(imagePath, " is not exists!")
                log_file.write(imagePath + "\n")
                continue

            # Check if image is good
            imgdata = cv2.imread(imagePath)
            height, width = imgdata.shape[:2]
            if imgdata is None:
                print("%s is broken!"%imagePath)
                continue
            polygons = image.getElementsByTagName('polygon')
            txtPath = os.path.join(txt_dir, os.path.basename(imagePath).split(".")[0] + ".txt")
            txtList.append(os.path.basename(txtPath))
            outFile = open(txtPath, 'w')
            for polygon in polygons:
                label = polygon.getAttribute("label")
                points = polygon.getAttribute('points').split(';')

                # Draw all points
                for point in points:
                    p = (int(float(point.split(',')[0])), int(float(point.split(',')[1])))
                    xtl = int(p[0] - (CONER_ROI_SIZE)/2)
                    ytl = int(p[1] - (CONER_ROI_SIZE)/2)
                    xbr = int(p[0] + (CONER_ROI_SIZE)/2)
                    ybr = int(p[1] + (CONER_ROI_SIZE)/2)
                    xtl = xtl if xtl > 0 else 0
                    ytl = ytl if ytl > 0 else 0
                    if xbr < 0 or ybr < 0:
                        continue
                    xbr = xbr if xbr < width else width
                    ybr = ybr if ybr < height else height
                    cv2.rectangle(imgdata, (int(xbr), int(ybr)), (int(xtl), int(ytl)), (0, 0, 255))
                    labelID = 0 #! TODO
                    b = (float(xtl), float(xbr), float(ytl), float(ybr))
                    bb = convert((width, height), b)
                    outFile.write(str(labelID) + " " + " ".join([str(a) for a in bb]) + '\n')
                    cv2.circle(imgdata, (p[0], p[1]), 4, (0, 0, 255), -1)
                    cv2.rectangle(imgdata, (xtl, ytl), (xbr, ybr), (255, 0, 0))

                # # Only draw entry points
                # enterPoint1 = (int(float(points[0].split(',')[0])), int(float(points[0].split(',')[1])))
                # xtl1 = int(enterPoint1[0] - (CONER_ROI_SIZE)/2)
                # ytl1 = int(enterPoint1[1] - (CONER_ROI_SIZE)/2)
                # xbr1 = int(enterPoint1[0] + (CONER_ROI_SIZE)/2)
                # ybr1 = int(enterPoint1[1] + (CONER_ROI_SIZE)/2)
                # xtl1 = xtl1 if xtl1 > 0 else 0
                # ytl1 = ytl1 if ytl1 > 0 else 0
                # xbr1 = xbr1 if xbr1 < width else width
                # ybr1 = ybr1 if ybr1 < height else height
                # cv2.rectangle(imgdata, (int(xbr1), int(ybr1)), (int(xtl1), int(ytl1)), (0, 0, 255))
                # labelID = 0 #! TODO
                # b = (float(xtl1), float(xbr1), float(ytl1), float(ybr1))
                # bb = convert((width, height), b)
                # outFile.write(str(labelID) + " " + " ".join([str(a) for a in bb]) + '\n')
                # cv2.circle(imgdata, (enterPoint1[0], enterPoint1[1]), 4, (0, 0, 255), -1)
                # cv2.rectangle(imgdata, (xtl1, ytl1), (xbr1, ybr1), (255, 0, 0))

                # # The second entry point
                # enterPoint2 = (int(float(points[1].split(',')[0])), int(float(points[1].split(',')[1])))
                # xtl2 = int(enterPoint2[0] - (CONER_ROI_SIZE)/2)
                # ytl2 = int(enterPoint2[1] - (CONER_ROI_SIZE)/2)
                # xbr2 = int(enterPoint2[0] + (CONER_ROI_SIZE)/2)
                # ybr2 = int(enterPoint2[1] + (CONER_ROI_SIZE)/2)
                # xtl2 = xtl2 if xtl2 > 0 else 0
                # ytl2 = ytl2 if ytl2 > 0 else 0
                # xbr2 = xbr2 if xbr2< width else width
                # ybr2 = ybr2 if ybr2 < height else height
                # cv2.rectangle(imgdata, (int(xbr2), int(ybr2)), (int(xtl2), int(ytl2)), (0, 0, 255))
                # labelID = 0 #! TODO
                # b = (float(xtl2), float(xbr2), float(ytl2), float(ybr2))
                # bb = convert((width, height), b)
                # outFile.write(str(labelID) + " " + " ".join([str(a) for a in bb]) + '\n')
                # cv2.circle(imgdata, (enterPoint2[0], enterPoint2[1]), 4, (0, 0, 255), -1)
                # cv2.rectangle(imgdata, (xtl2, ytl2), (xbr2, ybr2), (255, 0, 0))
            outFile.close()
            if COPY_TXT_TO_IMG_FOLDER:
                dst_txt = os.path.join(img_dir, os.path.basename(txtPath))
                shutil.copyfile(txtPath, dst_txt)
            if DRAW_LABEL:
                draw_path =  os.path.join(xml_dir + "_" + draw_folder, os.path.dirname(imagePath).split("/")[-1])
                if not os.path.exists(draw_path):
                    os.makedirs(draw_path)
                new_img = os.path.join(draw_path, os.path.basename(imagePath))
                #print("new_img", new_img)
                cv2.imwrite(new_img, imgdata)
        txtNum = len(txtList)
        trainnum = int(txtNum*TRAIN_RATE)
        trainset = random.sample(txtList, trainnum)
        for t in txtList:
            if t in trainset:
                txt_train_list.write(t + '\n')
            else:
                txt_val_list.write(t + '\n')


    print("Path of txt folder = ", os.path.abspath(txt_dir))
    print("Path of train text = ", os.path.abspath(txt_train_path))
    print("Path of valid text = ", os.path.abspath(txt_val_path))

if __name__ == '__main__':
    # args = parse_args()
    # xml_dir = args.xml_dir
    # if not os.path.exists(xml_dir):
    #     print("Error !!! %s is not exists, please check the parameter"%xml_dir)
    #     sys.exit(0)


    # if WITH_IMAGE:
    #     img_dir = args.img_dir
    #     if not os.path.exists(img_dir):
    #         print("Error !!! %s is not exists, please check the parameter"%img_dir)
    #         sys.exit(0)
    # else:
    #     img_dir = None

    # xml_dir = "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Curve/parking_key_point1023_xld_L_xml"
    # img_dir = "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Curve/parking_key_point1023_xld_L"
    xml_dir = ["./label/"]
    img_dir = ["./img"]
    for x, i in zip(xml_dir, img_dir):
        convert_annotation(x, i)
    print("Done!")
    os.system("cat train.txt val.txt > trainAll.txt")
    print("Path of all train text =", os.path.abspath("./trainAll.txt"))
