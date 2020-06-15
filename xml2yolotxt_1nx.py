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
WITH_SUB_CLASSES = True
WITH_PROCESS_SUB_CLASSES = True
DRAW_VEHICLE = False
DRAW_LIGHT = False
TRAIN_RATIO = 0.8
classes = ["car","van","bus","truck"]
sub_classes = ["brakelight", "headlight"]

error_log = "./log.txt"
draw_path1 = "./draw_img1"
draw_path2 = "./draw_img2"
output_txt_path = "./output_txt"
output_img_path = "./output_img"
output_txt_path_subclass = "./output_txt_subclass"
output_img_path_subclass = "./output_img_subclass"
txt_train_path = "./train.txt"
txt_val_path = "./val.txt"

if not os.path.exists(output_txt_path):
    os.makedirs(output_txt_path)
if not os.path.exists(output_img_path):
    os.makedirs(output_img_path)
if WITH_PROCESS_SUB_CLASSES:
    if not os.path.exists(output_txt_path_subclass):
        os.makedirs(output_txt_path_subclass)
    if not os.path.exists(output_img_path_subclass):
        os.makedirs(output_img_path_subclass)

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
                # Check whether the image is completename+"_"+frame_id+".jpg"
                img = cv2.imread(img_src_path)
                if img is None:
                    print("%s can't read!"%img_src_path)
                    continue
                
                txt_file_path = os.path.join(output_txt_path, name+"_"+frame_id+".txt")
                img_dst_path = os.path.join(output_img_path, os.path.basename(img_src_path))
                txt_file = open(txt_file_path, 'w')

                # {'group_id': {'car': [xtl, ytl, xbr, ybr], 'brakelight': [[xtl1, ytl1, xbr1, ybr1], [xtl2, ytl2, xbr2, ybr2]]}}
                obj_groups = {}
                for box in boxes:
                    if box.hasAttribute('group_id'):
                        group_id = box.getAttribute('group_id')
                    else:
                        group_id = None
                    
                    if WITH_GROUP_ID and not group_id:
                        continue
                    
                    label = box.getAttribute('label')

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

                    if WITH_SUB_CLASSES:
                        if label not in classes and label not in sub_classes:
                            continue
                    else:
                        if label not in classes:
                            continue
                    
                    txt_file.write(label + " " + " ".join([str(a) for a in bb]) + '\n')

                    if WITH_PROCESS_SUB_CLASSES and group_id:
                        # print("---", group_id, ", ", label)
                        if label in classes:
                            if group_id not in obj_groups:
                                obj_groups[group_id] = {"vehicle":[xtl, ytl, xbr, ybr]} # 固定住key便于后面便利
                            else:
                                obj_groups[group_id]["vehicle"] = [xtl, ytl, xbr, ybr]
                        if label in sub_classes:
                            if group_id not in obj_groups:
                                obj_groups[group_id] = {label:[[xtl, ytl, xbr, ybr]]}
                            else:
                                if label not in obj_groups[group_id]:
                                    obj_groups[group_id][label] = [[xtl, ytl, xbr, ybr]]
                                else:
                                    obj_groups[group_id][label].append([xtl, ytl, xbr, ybr])
                    
                    if DRAW_VEHICLE:
                        cv2.rectangle(img, (int(xtl), int(ytl)), (int(xbr), int(ybr)), (0,0,255))          
                txt_file.close()
                shutil.copyfile(img_src_path, img_dst_path)

                # draw box in image
                if DRAW_VEHICLE:
                        img_draw1 = os.path.join(draw_path1, name+"_"+frame_id+".jpg")
                        cv2.imwrite(img_draw1, img)
    
                # Process sub class
                for group_id, objs in obj_groups.items(): # group
                    if "vehicle" not in  list(objs.keys()):
                        print("---- Warning: image=%s, group_id=%s only contains lights!" %(img_src_path, group_id))
                        continue
                    for label, coordinate in objs.items(): # classes
                        if label in sub_classes:
                            xtl1 = objs["vehicle"][0]
                            ytl1 = objs["vehicle"][1]
                            xbr1 = objs["vehicle"][2]
                            ybr1 = objs["vehicle"][3]
                            name_subclass = os.path.basename(img_src_path).split(".")[0]+"_"+group_id
                            txt_file_path_subclass = os.path.join(output_txt_path_subclass, name_subclass+".txt")
                            txt_file_subclass = open(txt_file_path_subclass, 'w')
                            img_dst_sub_name = name_subclass + ".jpg"
                            img_dst_path_subclass = os.path.join(output_img_path_subclass, img_dst_sub_name)
                            cv2.imwrite(img_dst_path_subclass, img[int(ytl1):int(ybr1), int(xtl1):int(xbr1)])
                            for coor in coordinate: # sub classes
                                xtl2 = coor[0] - xtl1
                                ytl2 = coor[1] - ytl1
                                xbr2 = coor[2] - xtl1
                                ybr2 = coor[3] - ytl1
                                
                                bb = convert((xbr1-xtl1, ybr1-ytl1), (xtl2, xbr2, ytl2, ybr2))
                                txt_file_subclass.write(label + " " + " ".join([str(a) for a in bb]) + '\n')

                            txt_file_subclass.close()

    log_file.close()
    
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
    # os.system("cat train.txt val.txt > trainAll.txt")
    # print("Path of all train text =", os.path.abspath("./trainAll.txt"))
