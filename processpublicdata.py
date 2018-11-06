# -*- coding: utf-8 -*-
# Author : Andy Liu
# Data: 2018-11-06

# This tool is used to process public data
# input: python processpublicdata.py /home/andy/data/txt /home/andy/data/img  /drawout /ROIs
# output:
#    ./drawout
#    ./ROIs

import os
import sys
import random
import argparse
import cv2
from tqdm import tqdm

classes = {}
colors = [(0,0,255),(0,255,0),(255,0,0),(0,255,255)]
img_error = []

def parse_args():
    '''Parsing command line arguments'''
    parse = argparse.ArgumentParser()
    parse.add_argument('txt_dir', help='Txt directory', type=str)
    parse.add_argument('img_dir', help='Image directory', type=str)
    parse.add_argument('drawout', help='Draw directory', type=str)
    parse.add_argument('ROIs' ,help='ROI directory', type=str)
    args = parse.parse_args()
    return args

def draw_img(img, box, clr, message):
    '''Draw bounding box on image'''
    x1, y1, x2, y2 = map(int, box) # map appley the first parameter function to the second parameter
    cv2.rectangle(img, (x1,y1), (x2,y2), clr, 1)
    cv2.putText(img, message, (x1-10,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, clr, 1)
    return img


def parse(txt_path):
    f = open(txt_path, "r")
    lines = f.read().split('\n') # ['0 0.6 0.7 0.04 0.06', '3 0.5 0.6 0.01 0.01', '']
    lines = lines[:-1] # ['0 0.6 0.7 0.04 0.06', '3 0.5 0.6 0.01 0.01']
    f.close()
    return lines
    # lines = parse(txt_dir)
    #     for line in lines:
    #         line = line.split(';') # split by ';'
    #         img_name = line[0] # with extend
    #         box = (line[1], line[2], line[3], line[4])
    #         label = line[-1]
    #         if label not in classes:
    #             classes[label] = 1
    #         else:
    #             classes[label] += 1
    #         imgname = img_name.split('.')[0]
    #         img = cv.imread(img_dir + '/' + img_name)
    #         roi = img[box[0]:box[2], box[1]:box[3]]
    #         cv2.imwrite(ROIs + '/' + imgname + '_' + random.randint(0,99)//random.randint(1,9) + '.png', roi)
    #         img_draw = draw_img(img, box, colors[0], label)
    #         cv2.imwrite(drawout + '/' + img_name, img_draw)
    # return 

def process(txt_dir, img_dir, drawout, ROIs):
    '''The main process images function'''
    if txt_dir[-1] == "/":
        txt_dir = txt_dir[:-1]
    if img_dir[-1] == "/":
        img_dir = img_dir[:-1]
    if drawout[-1] == "/":
        drawout = drawout[:-1]
    if ROIs[-1] == "/":
        ROIs = ROIs[:-1]

    if os.path.isfile(txt_dir):
        lines = parse(txt_dir)
        for line in tqdm(lines):
            line = line.split(';') # split by ';'
            img_name = line[0] # with extend
            box = (int(float(line[1])), int(float(line[2])), int(float(line[3])), int(float(line[4])))
            label = line[-1]
            if label not in classes:
                classes[label] = 1
            else:
                classes[label] += 1
            imgname = img_name.split('.')[0]
            img = cv2.imread(img_dir + '/' + img_name)
            if img is None:
                # print("%s can't read!"%(img_dir + '/' + img_name))
                img_error.append(img_dir + '/' + img_name)
                continue
            roi = img[box[1]:box[3], box[0]:box[2]]
            cv2.imwrite(ROIs + '/' + imgname + '_' + str(random.randint(0,99)//random.randint(1,9)) + '.png', roi)
            img_draw = draw_img(img, box, colors[0], label)
            cv2.imwrite(drawout + '/' + img_name, img_draw)
        
        return
    elif os.path.isdir(txt_dir):
        txt_list = os.listdir(txt_dir)
        for txt in tqdm(txt_list):
            lines = parse(txt_dir)
            for line in lines:
                line = line.split(';') # split by ';'
                img_name = line[0] # with extend
                box = (line[1], line[2], line[3], line[4])
                label = line[-1]
                if label not in classes:
                    classes[label] = 1
                else:
                    classes[label] += 1
                imgname = img_name.split('.')[0]
                img = cv.imread(img_dir + '/' + img_name)
                roi = img[box[1]:box[3], box[0]:box[2]]
                cv2.imwrite(ROIs + '/' + imgname + '_' + random.randint(0,99)//random.randint(1,9) + '.png', roi)
                img_draw = draw_img(img, box, colors[0], label)
                cv2.imwrite(drawout + '/' + img_name, img_draw)
            
        return




if __name__ == '__main__':
    args = parse_args()
    txt_dir = args.txt_dir
    img_dir = args.img_dir
    drawout = args.drawout
    ROIs = args.ROIs

    if not os.path.exists(txt_dir):
        print("Error !!! %s is not exists, please check the parameter"%txt_dir)
        sys.exit(0)

    if not os.path.exists(img_dir):
        print("Error !!! %s is not exists, please check the parameter"%img_dir)
        sys.exit(0)

    if not os.path.exists(drawout):
        os.makedirs(drawout)
        print("Output folder = ", os.path.abspath(drawout))

    if not os.path.exists(ROIs):
        os.makedirs(ROIs)
        print("Output folder = ", os.path.abspath(ROIs))

    process(txt_dir, img_dir, drawout, ROIs)
    print("The damaged images : %d"%len(img_error))
    for e in img_error:
        print(img_error)