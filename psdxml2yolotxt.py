# -*- coding: utf-8 -*-
# Reference VOC scrips
# Author : Andy Liu
# last modify : 2020-09-27

# This tool is used to convert VOC xml format to YOLO V3 format
# And pick 80% for train, left for val
# input : python xml2txt.py "/home/andy/data/xml"   "/home/andy/data/img"
# output :
#       ./txt
#	./train.txt
#	./val.txt
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
CONER_ROI_SIZE = 21

classes = ["01_key_point", "02_key_point", "03_key_point", "04_key_point", "05_key_point", "06_key_point", "07_key_point"]
# classes = ["01_key_point", "02_key_point", "03_key_point", "04_key_point",
#             "01 key_point", "02 key_point", "03 key_point", "04 key_point"]

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
    xml_dir = os.path.abspath(xml_dir)
    if xml_dir[-1] == "/":
        xml_dir = xml_dir[:-1]

    if WITH_IMAGE:
        img_dir = os.path.abspath(img_dir)
        if img_dir[-1] == "/":
            img_dir = img_dir[:-1]

    filelist = os.listdir(xml_dir)
    print("images num = ", len(filelist))

    trainnum = int(len(filelist)*TRAIN_RATE)
    trainset = random.sample(filelist, trainnum)

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

    for f in filelist:
        print(f + "-->start!")
        fileInfor = f.split(".")
        # xmlfile = fileInfor[0][:fileInfor[0].rfind("_")] + ".xml"
        xml_path = os.path.join(xml_dir, f)

        if not os.path.exists(xml_path):
            print(f, "is not exists!")
            log_file.write(f + "\n")
            continue

        imgfile = img_dir + "/" + fileInfor[0] + ".jpg"
        if not os.path.exists(imgfile):
            imgfile = img_dir + "/" + fileInfor[0] + ".png"
        if not os.path.exists(imgfile):
            print(imgfile, " is not exists!")
            log_file.write(imgfile + "\n")
            continue

        # Check whether the image is good
        img = cv2.imread(imgfile)
        height, width, _ = img.shape
        if img is None:
            print("%s can't read!"%imgfile)
            continue

        if f in trainset:
            txt_train_list.write(imgfile + '\n')
        else:
            txt_val_list.write(imgfile + '\n')

        txt_path = txt_dir + "/" + fileInfor[0] + ".txt"
        out_file = open(txt_path, 'w')

        dom = xml.dom.minidom.parse(xml_path)
        annotation = dom.documentElement
        xml_img = annotation.getElementsByTagName('filename')[0].childNodes[0].data
        if xml_img != os.path.basename(imgfile):
            print("image file name {} is exit in image folders!!".format(xml_img))
            continue
        img_size = annotation.getElementsByTagName('imagesize')[0]
        w = float(img_size.getElementsByTagName("ncols")[0].childNodes[0].data)
        h = float(img_size.getElementsByTagName("nrows")[0].childNodes[0].data)
        w_rate =  width / w
        h_rate =  height / h
        for obj in annotation.getElementsByTagName('object'):
            label = obj.getElementsByTagName('name')[0].childNodes[0].data
            labelInfo = label.split(" ")
            if len(labelInfo) > 1:
                label = "_".join(labelInfo)
            if label not in classes:
                print("{} is not in classes!!".format(label))
                continue
            polygon = obj.getElementsByTagName('polygon')[0]
            pt = polygon.getElementsByTagName('pt')[0]
            x = int(float(pt.getElementsByTagName('x')[0].childNodes[0].data) * w_rate)
            y = int(float(pt.getElementsByTagName('y')[0].childNodes[0].data) * h_rate)
            xtl = int(x - (CONER_ROI_SIZE)/2)
            ytl = int(y - (CONER_ROI_SIZE)/2)
            xbr = int(x + (CONER_ROI_SIZE)/2)
            ybr = int(y + (CONER_ROI_SIZE)/2)
            xtl = xtl if xtl > 0 else 0
            ytl = ytl if ytl > 0 else 0
            xbr = xbr if xbr < w else w
            ybr = ybr if ybr < h else h
            cv2.rectangle(img, (int(xbr), int(ybr)), (int(xtl), int(ytl)), (0, 0, 255))
            # print(label, xtl, ytl, xbr, ybr)

            # label_id = classes.index(label)
            label_id = 0    #! TODO
            b = (float(xtl), float(xbr), float(ytl), float(ybr))
            bb = convert((w, h), b)
            out_file.write(str(label_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            # out_file.flush()
            cv2.circle(img, (x, y), 4, (0, 0, 255), -1)
            cv2.rectangle(img, (xtl, ytl), (xbr, ybr), (255, 0, 0))

        out_file.close()
        if COPY_TXT_TO_IMG_FOLDER:
            dst_txt = os.path.join(img_dir, os.path.basename(txt_path))
            shutil.copyfile(txt_path, dst_txt)
        if DRAW_LABEL:
            draw_path =  xml_dir + "_" + draw_folder
            if not os.path.exists(draw_path):
                os.makedirs(draw_path)
            new_img = os.path.join(draw_path, os.path.basename(imgfile))
            #print("new_img", new_img)
            cv2.imwrite(new_img, img)

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
    xml_dir = ["/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Brick/parking_key_point1013_zd_L_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Curve/parking_key_point1023_xld_L_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Curve/parking_key_point1023_xld_R_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Grass/parking_key_point0828_cd_L_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Grass/parking_key_point0828_cd_R_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Oblique/parking_key_point0903_L_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Oblique/parking_key_point0903_R_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Open/parking_key_point0828_L_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Open/parking_key_point0828_R_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Open/parking_key_point1012_tf_L_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Open/parking_key_point1012_tf_R_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1012_bq_L_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1012_bq_R_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1023_ck_L_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1023_ck_R_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1102_rk_L_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1102_rk_R_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1116_yq_L_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1116_yq_R_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1119_yq_L_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1119_yq_R_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Trapezoidal/parking_key_point1019_guan_L_xml",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Trapezoidal/parking_key_point1019_guan_R_xml"]
    img_dir = ["/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Brick/parking_key_point1013_zd_L",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Curve/parking_key_point1023_xld_L",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Curve/parking_key_point1023_xld_R",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Grass/parking_key_point0828_cd_L",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Grass/parking_key_point0828_cd_R",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Oblique/parking_key_point0903_L",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Oblique/parking_key_point0903_R",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Open/parking_key_point0828_L",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Open/parking_key_point0828_R",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Open/parking_key_point1012_tf_L",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Open/parking_key_point1012_tf_R",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1012_bq_L",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1012_bq_R",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1023_ck_L",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1023_ck_R",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1102_rk_L",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1102_rk_R",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1116_yq_L",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1116_yq_R",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1119_yq_L",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Rectangular/parking_key_point1119_yq_R",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Trapezoidal/parking_key_point1019_guan_L",
                "/home/andy/WorkSpace/PSD/dataset/Parking-slot-dataset/Trapezoidal/parking_key_point1019_guan_R"]
    for x, i in zip(xml_dir, img_dir):
        convert_annotation(x, i)
    print("Done!")
    os.system("cat train.txt val.txt > trainAll.txt")
    print("Path of all train text =", os.path.abspath("./trainAll.txt"))
