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
import cv2

def parse_args():
    """Parsing input command syntax"""
    parser = argparse.ArgumentParser()
    parser.add_argument('ann_dir', help='Annotations directory', type=str)
    parser.add_argument('img_dir', help='Images directory', type=str)

    args = parser.parse_args()
    return args
 
wait4AddLabels = [1,2]

def createData(ann_dir_src, img_dir_src, ann_dir_dst, img_dir_dst, labels):
    """Create training data by exiting labels"""

    size = [w,h]

    for obj in objs:
        #threes#
        object_new = doc.createElement("object")
        annotation.appendChild(object_new)
 
        name = doc.createElement('name')
        object_new.appendChild(name)
        name_txt = doc.createTextNode(obj[0])
        name.appendChild(name_txt)
 
        pose = doc.createElement('pose')
        object_new.appendChild(pose)
        pose_txt = doc.createTextNode("Unspecified")
        pose.appendChild(pose_txt)
 
        truncated = doc.createElement('truncated')
        object_new.appendChild(truncated)
        truncated_txt = doc.createTextNode("0")
        truncated.appendChild(truncated_txt)
 
        difficult = doc.createElement('Difficult')  # difficult = doc.createElement('difficult') in VOC2007
        object_new.appendChild(difficult)
        difficult_txt = doc.createTextNode("0")
        difficult.appendChild(difficult_txt)
        #threes-1#
        bndbox = doc.createElement('bndbox')
        object_new.appendChild(bndbox)

        box = convert(size,float(obj[1]),float(obj[2]),float(obj[3]),float(obj[4]))

        xmin = doc.createElement('xmin')
        bndbox.appendChild(xmin)
        xmin_txt = doc.createTextNode(str(box[0]))
        xmin.appendChild(xmin_txt)
 
        ymin = doc.createElement('ymin')
        bndbox.appendChild(ymin)
        ymin_txt = doc.createTextNode(str(box[1]))
        ymin.appendChild(ymin_txt)
 
        xmax = doc.createElement('xmax')
        bndbox.appendChild(xmax)
        xmax_txt = doc.createTextNode(str(box[2]))
        xmax.appendChild(xmax_txt)
 
        ymax = doc.createElement('ymax')
        bndbox.appendChild(ymax)
        ymax_txt = doc.createTextNode(str(box[3]))
        ymax.appendChild(ymax_txt)
        #threee-1#
        #threee#
        
    tempfile = tmp + "/" + "temp.xml"
    with open(tempfile, "w") as f:
        # print(doc.toprettyxml())
        f.write(doc.toprettyxml(indent = '\t'))
        
    rewrite = open(tempfile, "r")
    lines = rewrite.read().split('\n')
    newlines = lines[1:len(lines)-1]
    
    fw = open(wxml, "w")
    for i in range(0, len(newlines)):
        fw.write(newlines[i] + '\n')
    
    fw.close()
    rewrite.close()
    os.remove(tempfile)
    return
 

if __name__ == '__main__':
    args = parse_args()
    ann_dir_src = args.ann_dir_src
    img_dir_src = args.img_dir_src
    if not os.path.exists(ann_dir_src):
        print("Error !!! %s is not exists, please check the parameter"%ann_dir_src)
        sys.exit(0)
    if not os.path.exists(img_dir_src):
        print("Error !!! %s is not exists, please check the parameter"%img_dir_src)
        sys.exit(0)

    ## Output folders
    ann_dir_dst = "./new_labels"
    img_dir_dst = "./new_img"
    if not os.path.exists(ann_dir_dst):
        os.mkdir(ann_dir_dst)
    if not os.path.exists(img_dir_dst):
        os.mkdir(img_dir_dst)
    ## Check
    if ann_dir_dst[-1] == "/":
        ann_dir_dst = ann_dir_dst[:-1]
    if img_dir_dst[-1] == "/":
        img_dir_dst = img_dir_dst[:-1]
    

    for files in os.walk(ann_dir): # os.walk return (root,dirs,files)
        temp = "./temp"
        # print(files)
        if not os.path.exists(temp):
            os.mkdir(temp)
        for file in files[2]:
            print(file + "-->start!")
            fileInfor = os.path.splitext(file)
            img_name = fileInfor[0] + '.jpg'
            imgpath = img_dir + "/" + img_name
            if not os.path.exists(imgpath):
            	img_name = fileInfor[0] + '.png'
            	imgpath = img_dir + "/" + img_name
            if not os.path.exists(imgpath):
            	continue
           
            
            filelabel = open(ann_dir + "/" + file, "r")
            lines = filelabel.read().split('\n')[:-1]
            objs = []
            for line in lines:
                obj = line.split(" ")
                objs.append(obj)

            filelabel.close()
            filename = xml_dir + "/" + fileInfor[0] + '.xml'
            writeXml(temp, imgpath, width, height, objs, filename)
        os.rmdir(temp)
    print("Done!")
    print("Path of .xml = ", os.path.abspath(xml_dir))
