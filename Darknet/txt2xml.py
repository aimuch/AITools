# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-8-14
# This tool is used to covert YOLO v3 txt format label to VOC2007 format label
# input : python txt2xml.py "/home/andy/data/ann_dir" "/home/andy/data/img_dir"
# output:
#	./xml


from xml.dom.minidom import Document
import os
import os.path
import shutil
import sys
import argparse
from PIL import Image

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ann_dir', help='Annotations directory', type=str)
    parser.add_argument('img_dir', help='Images directory', type=str)

    args = parser.parse_args()
    return args
 

def convert(size, x,y,w,h):
    box = []
    box.append(int(x*size[0] + 1.0 - 0.5*w*size[0])) #xmin
    box.append(int(y*size[1] + 1.0 - 0.5*h*size[1])) #ymin
    box.append(int(x*size[0] + 1.0 + 0.5*w*size[0])) #xmax
    box.append(int(y*size[1] + 1.0 + 0.5*h*size[1])) #ymax
    return box

 
def writeXml(tmp, imgname, w, h, objs, wxml):
    doc = Document()
    #owner
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)
    #owner
    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    foldename = os.path.dirname(imgname).split("/")[-1]
    folder_txt = doc.createTextNode(foldename)
    folder.appendChild(folder_txt)
 
    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    imgInfor = os.path.basename(imgname).split(".")
    filename_txt = doc.createTextNode(imgInfor[0])
    filename.appendChild(filename_txt)

    pathname = doc.createElement('path')
    annotation.appendChild(pathname)
    pathname_txt = doc.createTextNode(imgname)
    pathname.appendChild(pathname_txt)

    #ones#
    source = doc.createElement('source')
    annotation.appendChild(source)
 
    database = doc.createElement('database')
    source.appendChild(database)
    database_txt = doc.createTextNode("VOC2007 Database")
    database.appendChild(database_txt)
 
    # annotation_new = doc.createElement('annotation')
    # source.appendChild(annotation_new)
    # annotation_new_txt = doc.createTextNode("PASCAL VOC2007")
    # annotation_new.appendChild(annotation_new_txt)
 
    image = doc.createElement('image')
    source.appendChild(image)
    image_txt = doc.createTextNode(os.path.basename(imgname).split(".")[0])
    image.appendChild(image_txt)
    #onee#
    #twos#
    size = doc.createElement('size')
    annotation.appendChild(size)
 
    width = doc.createElement('width')
    size.appendChild(width)
    width_txt = doc.createTextNode(str(w))
    width.appendChild(width_txt)
 
    height = doc.createElement('height')
    size.appendChild(height)
    height_txt = doc.createTextNode(str(h))
    height.appendChild(height_txt)
 
    depth = doc.createElement('depth')
    size.appendChild(depth)
    depth_txt = doc.createTextNode("3")
    depth.appendChild(depth_txt)
    #twoe#
    segmented = doc.createElement('segmented')
    annotation.appendChild(segmented)
    segmented_txt = doc.createTextNode("0")
    segmented.appendChild(segmented_txt)

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
    newlines = lines[1:len(lines)-1] # ['<?xml version="1.0" ?>', '<annotation>', '</annotation>', '']

    
    fw = open(wxml, "w")
    for i in range(0, len(newlines)):
        fw.write(newlines[i] + '\n')
    
    fw.close()
    rewrite.close()
    os.remove(tempfile)
    return
 

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

    xml_dir = "./xml"
    if not os.path.exists(xml_dir):
        os.makedirs(xml_dir)

    if ann_dir[-1] == "/":
        ann_dir = ann_dir[:-1]
    if img_dir[-1] == "/":
        img_dir = img_dir[:-1]
    

    for files in os.walk(ann_dir): # os.walk return (root,dirs,files)
        temp = "./temp"
        # print(files)
        if not os.path.exists(temp):
            os.makedirs(temp)
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
            im=Image.open(imgpath)  
            width= int(im.size[0])
            height= int(im.size[1])
            im.close()
            
            filelabel = open(ann_dir + "/" + file, "r")
            lines = filelabel.read().split('\n')[:-1] # # ['0 0.6 0.7 0.04 0.06', '3 0.5 0.6 0.01 0.01', ''] -> ['0 0.6 0.7 0.04 0.06', '3 0.5 0.6 0.01 0.01']
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
