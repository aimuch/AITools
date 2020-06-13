# -*- coding: utf-8 -*-
# Reference VOC scrips
# Author : Andy Liu
# last modify : 2020-06-13

# This tool is used to convert VOC xml format to YOLO V3 format
# NOTE: All processing by annotations xml files, one video create one xml files,
#       and video pictures are merged into one fold
# And pick 80% for train, left for val
# input : python xml2txt.py "/home/andy/data/xml_dirs"   "/home/andy/data/img_dirs"

# |-xml_dirs
# |--xml_dir1==img_dir1
# |---xml_file1

# |-img_dirs
# |--img_dir1==xml_dir1
# |---img_file1

import xml
import xml.dom.minidom
import random
import pickle
import os
import sys
import cv2
import argparse
import shutil
from tqdm import tqdm

WITH_GROUP_ID = False
TRAIN_RATIO = 0.8
classes = ["Car","Van","Bus","Truck"]
sub_classes = ["brakelight", "headlight"]

error_log = "./log.txt"
draw_path = "./draw_img"
output_txt_path = "./output_txt"
output_img_path = "./output_img"
txt_train_path = "./train.txt"
txt_val_path = "./val.txt"

if not os.path.exists(output_txt_path):
    os.makedirs(output_txt_path)
if not os.path.exists(output_img_path):
    os.makedirs(output_img_path)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('xml_dirs', help='xml directories', type=str)
    parser.add_argument('img_dirs', help='image directories', type=str)
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
    return (x,y,w,h)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

    

def convert_annotations(xml_dirs, img_dirs):
    xml_dirs = os.path.abspath(xml_dirs)
    if xml_dirs[-1] == "/":
        xml_dirs = xml_dirs[:-1]
    
    img_dirs = os.path.abspath(img_dirs)
    if img_dirs[-1] == "/":
        img_dirs = img_dirs[:-1]

    xml_dir_list = os.listdir(xml_dirs)

    log_file = open(error_log, 'w')

    for xml_dir in xml_dir_list:
        print("|-", xml_dir + " ----> start!")
        xml_dir_path = os.path.join(xml_dirs, xml_dir)
        xml_list = os.listdir(xml_dir_path)
        for xml_file in xml_list:
            print("|--", xml_file, " ----> start!")
            xml_file_ = xml_file
            # while xml_file_[0].isdigit() or xml_file_[0] == "_":
            while is_number(xml_file_[0]) or xml_file_[0] == "_":
                xml_file_ = xml_file_[1:]

            xml_path = os.path.join(xml_dir_path, xml_file)

            if not os.path.exists(xml_path):
                print(xml_path, "is not exists!")
                log_file.write(xml_path + "\n")
                continue

            DOMTree = xml.dom.minidom.parse(xml_path)
            annotations = DOMTree.documentElement
            meta = annotations.getElementsByTagName('meta')[0]
            task = meta.getElementsByTagName('task')[0]
            name = task.getElementsByTagName('name')[0].childNodes[0].data
            step = task.getElementsByTagName('frame_filter')[0].childNodes[0].data.split("=")[-1]
            images = annotations.getElementsByTagName('image')
            for image in images:
                frame_id = image.getAttribute('id')
                width = int(image.getAttribute('width'))
                height = int(image.getAttribute('height'))
                boxes = image.getElementsByTagName('box')
                img_src_path = os.path.join(img_dirs, xml_dir)
                img_src_path = os.path.join(img_src_path, name+"_"+frame_id+".jpg")
                if not os.path.exists(img_src_path):
                    img_src_path = os.path.join(img_src_path, name+"_"+frame_id+".png")
                if not os.path.exists(img_src_path):
                    print(img_src_path, " is not exists!")
                    log_file.write(os.path.basename(img_src_path) + "\n")
                    continue
                # Check whether the image is complete
                img = cv2.imread(img_src_path)
                if img is None:
                    print("%s can't read!"%img_src_path)
                    continue
                
                txt_file_path = os.path.join(output_txt_path, name+"_"+frame_id+".txt")
                img_dst_path = os.path.join(output_img_path, os.path.basename(img_src_path))
                txt_file = open(txt_file_path, 'w')
                for box in boxes:
                    if box.hasAttribute('group_id'):
                        group_id = int(box.getAttribute('group_id'))
                    else:
                        group_id = None
                    
                    if not group_id and WITH_GROUP_ID:
                        continue
                    
                    label = box.getAttribute('label')

                    if label not in classes:
                        continue

                    xtl = float(box.getAttribute('xtl'))
                    ytl = float(box.getAttribute('ytl'))
                    xbr = float(box.getAttribute('xbr'))
                    ybr = float(box.getAttribute('ybr'))
                    xtl = xtl if xtl > 0 else 0
                    ytl = ytl if ytl > 0 else 0
                    xbr = xbr if xbr < width else width
                    ybr = ybr if ybr < height else height
                    bb = convert((width, height), (xtl, xbr, ytl, ybr))

                    if label == 'light':
                        for box_attr in box.getElementsByTagName('attribute'):
                            if box_attr.getAttribute('name') == 'type':
                                light_type = box_attr.childNodes[0].data
                                label = light_type

                    txt_file.write(label + " " + " ".join([str(a) for a in bb]) + '\n')

                txt_file.close()
                shutil.copyfile(img_src_path, img_dst_path)
    
    log_file.close()


    img_list = os.listdir(output_img_path)
    trainnum = int(len(img_list)*TRAIN_RATIO)
    trainset = random.sample(img_list, trainnum)
    txt_train_list = open(txt_train_path, 'w')
    txt_val_list = open(txt_val_path, 'w')
    for img in img_list:
        if img in trainset:
            txt_train_list.write(os.path.abspath(img) + '\n')
        else:
            txt_val_list.write(os.path.abspath(img) + '\n')


## TODO
            cv2.rectangle(img, (int(xbr), int(ybr)), (int(xtl), int(ytl)), (0, 0, 255))
            # print(label, xtl, ytl, xbr, ybr)
            label_id = classes.index(label)
            b = (float(xtl), float(xbr), float(ytl), float(ybr))
            bb = convert((w, h), b)
            out_file.write(str(label_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            # out_file.flush()
            cv2.rectangle(img, (xtl, ytl), (xbr, ybr), (255, 0, 0))

        cv2.imwrite(new_img, img)
    
    print("Path of txt folder = ", os.path.abspath(output_txt_path))
    print("Path of train text = ", os.path.abspath(txt_train_path))
    print("Path of valid text = ", os.path.abspath(txt_val_path))

if __name__ == '__main__':
    # args = parse_args()
    # xml_dirs = args.xml_dirs
    # if not os.path.exists(xml_dirs):
    #     print("Error !!! %s is not exists, please check the parameter"%xml_dirs)
    #     sys.exit(0)
    
    # img_dirs = args.img_dirs
    # if not os.path.exists(img_dirs):
    #     print("Error !!! %s is not exists, please check the parameter"%img_dirs)
    #     sys.exit(0)

    xml_dirs = "./xml"
    img_dirs = "./img"
    convert_annotations(xml_dirs, img_dirs)
    print("Done!")
    os.system("cat train.txt val.txt > trainAll.txt")
    print("Path of all train text =", os.path.abspath("./trainAll.txt"))
