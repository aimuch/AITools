### Author : zyy
### Modify by: Andy
### Last modified : 2018-10-30

### This tool is used to draw bbox labels 
### -----------EXAMPLE-------------------
### python drawbdd.py \
###        /home/data/Annotations \
###        /home/data/JPEGImages \
###        /home/data/output_draw

import os 
# import xml
import  xml.dom.minidom
import sys
import argparse
import cv2
import random
from tqdm import tqdm

classes = ["wheel", "car_front", "car_back", "car_side"]

cls_clr = [(0,0,255),
           (0,255,0),
           (255,0,0),
           (0,255,255)] 

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('xml_dir', help='xml directory', type=str)
    parser.add_argument('img_dir', help='Image directory', type=str)
    parser.add_argument('output_dir', help='Output directory', type=str)
    args = parser.parse_args()
    return args


def draw(img, points, clr, attr):
  x0,y0, x1,y1, x2,y2, x3,y3 = map(int, points)
  cv2.line(img, (x0,y0), (x1,y1), clr)
  cv2.line(img, (x1,y1), (x2,y2), clr)
  cv2.line(img, (x2,y2), (x3,y3), clr)
  cv2.line(img, (x3,y3), (x0,y0), clr)
  cv2.putText(img, attr, (x1+5,y1), cv2.FONT_HERSHEY_SIMPLEX, 1, clr, 1)
  return img

def draw_labelling(xml_dir, img_dir, output_dir):
    count = 0
    filelist = os.listdir(xml_dir)
    for xml_file in tqdm(filelist):
        count += 1
        #print("folder:%s,count:%d",folder,count)
        xml_file_path = os.path.join(xml_dir, xml_file)
        dom = xml.dom.minidom.parse(xml_file_path)
        image_path = os.path.join(img_dir, xml_file.replace("xml", "jpg"))
        img = cv2.imread(image_path)

        objs = dom.getElementsByTagName('object')
        
        for obj in objs:
            name = obj.getElementsByTagName('name')[0].childNodes[0].data
            truncated = obj.getElementsByTagName('truncated')[0].childNodes[0].data
            difficult = obj.getElementsByTagName('difficult')[0].childNodes[0].data
            x0 = float(obj.getElementsByTagName('bndbox')[0].childNodes[1].childNodes[0].data)
            y0 = float(obj.getElementsByTagName('bndbox')[0].childNodes[3].childNodes[0].data)
            x1 = float(obj.getElementsByTagName('bndbox')[0].childNodes[5].childNodes[0].data)
            y1 = float(obj.getElementsByTagName('bndbox')[0].childNodes[7].childNodes[0].data)
            x2 = float(obj.getElementsByTagName('bndbox')[0].childNodes[9].childNodes[0].data)
            y2 = float(obj.getElementsByTagName('bndbox')[0].childNodes[11].childNodes[0].data)
            x3 = float(obj.getElementsByTagName('bndbox')[0].childNodes[13].childNodes[0].data)
            y3 = float(obj.getElementsByTagName('bndbox')[0].childNodes[15].childNodes[0].data)

            img_draw = draw(img, [x0, y0, x1, y1, x2, y2, x3, y3], cls_clr[classes.index(name)], name)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, xml_file.replace("xml", "jpg"))
            #print("output_path:%s"%output_path)
            cv2.imwrite(output_path, img)


if __name__ == '__main__':
    args = parse_args()
    xml_dir = args.xml_dir
    img_dir = args.img_dir
    output_dir = args.output_dir

    if not os.path.exists(xml_dir):
        print("Error !!! %s is not exists, please check the parameter"%xml_dir)
        sys.exit(0)

    if not os.path.exists(img_dir):
        print("Error !!! %s is not exists, please check the parameter"%img_dir)
        sys.exit(0)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print("Output folder = ", os.path.abspath(output_dir))

    # xml_dir = "./labelxml"
    # img_dir = "./images"
    # output_dir = "./output"
    draw_labelling(xml_dir, img_dir, output_dir)
