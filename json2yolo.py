# -*- coding: utf-8 -*-
### Author : zyy
### Modified : Andy
### Last modified : 2018-09-21

### This tool is used to transform hryt.json to yolo txt formate 
### -----------EXAMPLE-------------------
### python3 json2yolo.py /home/andy/data/json_folders /home/andy/data/output_folder

### -----------------NOTE---------------------
### The tree of json_folders: json_folders/json_folder/json 
### Example:
###         json/072901/20180729_0001_500.json

import os 
import json
import sys
import numpy as np
from tqdm import tqdm
import argparse

classes = {"person":["pedestrain", "cyclist", "others"], 
           "vehicle":["car", "suv", "bus", "truck", "van", "forklift", "train", "motorbike", "bike", "tricycle", "other"], 
           "trafficsign":["max_5", "max_10", "max_15", "max_20", "max_30", "max_40", "max_50", "max_60", "max_70", "max_80", 
                          "max_90", "max_100", "max_110", "max_120", "max_130", "min_30","min_40","min_50", "min_60", "min_70", "min_80", "min_90", "min_100",
                          "end_20","end_30","end_40","end_50","end_60",
                          "warning", "prohibitory", "indicative", "informational", "tourist", "others"],
           "trafficlight":["red_circle", "red_ahead", "red_left", "red_right", "red_back", "red_others",
                           "green_circle", "green_ahead", "green_left", "green_right", "green_back", "green_others",
                           "yellow_circle", "yellow_ahead", "yellow_left", "yellow_right", "yellow_back", "yellow_others", 
                           "other_circle", "other_ahead", "other_left", "other_right", "other_back","other_others"]}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('json_dir', help='Json directory', type=str)
    parser.add_argument('output_dir', help='Output directory', type=str)

    args = parser.parse_args()
    return args

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def write2txt1(json_file_path, txt_f, cls, object_list, pic_size, type_list):
    if len(object_list) == 0:
       return type_list 

    clr_id = 0
    if cls == "person":
        clr_id = 0
    elif cls == "vehicle":
        clr_id = 3 
    elif cls == "trafficsign":
        clr_id = 14
    elif cls == "trafficlight":
    	clr_id = 48

    box = []

    for id_dict in object_list:
        type_id = clr_id
        #print("id_dict:%s"%id_dict)
        if "attrs" in id_dict:
            #print("attrs:%s"%id_dict["attrs"])
            attrs_ignore = id_dict["attrs"]["ignore"]
            #print("attrs_ignore:", attrs_ignore)
            if attrs_ignore == '':
                print("ignore null :%s"%json_file_path)
                continue
            if attrs_ignore == "yes":
                #print("ignore file :%s"%json_file_path)
                continue

            attrs_occlusion = id_dict["attrs"]["occlusion"]
            if attrs_occlusion == "invisible":
                continue

            #print("id_dict['attrs']:%s"%id_dict["attrs"])
            #if not id_dict["attrs"].has_key("type"): # python2
            if "type" not in id_dict["attrs"]:
                #print(json_file_path)
                continue
            
            # if id_dict["attrs"]["type"] == 'ignore region':
            #     print("ignore_region:",json_file_path) 
            #     continue


            # if id_dict["attrs"]["type"] == False:
            #     print("type False:",json_file_path) 
            #     continue

            #print("attrs_type:", id_dict["attrs"]["type"])
            attrs_type = id_dict["attrs"]["type"].lower()
            #if id_dict["attrs"].has_key("color"): # python2
            if "color" in id_dict["attrs"]:
            	attrs_type = id_dict["attrs"]["color"].lower() + "_"  + attrs_type 
            #print("attrs_type:",attrs_type)

            # if attrs_type == "end_30":
            #     print("ignore file :%s"%json_file_path)
            
            # WanHong
            if attrs_type == "max_0":
                continue
            # LongMao
            if attrs_type == "min_5":
                continue
            if attrs_type == "min_7":
                continue
             
            type_id = clr_id + classes[cls].index(attrs_type) 
            #print("type_id:", type_id)
            type_list[type_id] += 1

        if "data" in id_dict:
            box = id_dict["data"]
            b = (int(min(box[0], box[2])), int(max(box[0], box[2])), int(min(box[1], box[3])), int(max(box[1], box[3])))
            bb = convert(pic_size, b)

            txt_f.write(str(type_id) + " " + " ".join(str(a) for a in bb) + '\n') 

    return type_list

def hryt2txt(json_dir, output_dir):
    type_list = np.zeros(72)
    count = 0
    for folder in os.listdir(json_dir):
        folder_path = os.path.join(json_dir, folder)
       
        for json_file in tqdm(os.listdir(folder_path)):
            count += 1
            #print("folder:%s,count:%d",folder,count)
            json_file_path = os.path.join(folder_path, json_file)

            txt_folder_path = os.path.join(output_dir, folder)
            if not os.path.exists(txt_folder_path):
                os.makedirs(txt_folder_path)
            txt_file_path  = os.path.join(txt_folder_path, json_file[:-4] + "txt" )

            #print("json_file_path:%s"%json_file_path) 
            #print("txt_file_path:%s"%txt_file_path) 
            
            txt_f = open(txt_file_path, "w")

            with open(json_file_path, "r") as json_f:
                lines = json_f.readlines()
                for line in lines:
                    json_dict = json.loads(line, encoding='utf-8')
                    if "image_key" not in json_dict:
                        continue
                    pic_size = (json_dict["width"], json_dict["height"])

                    if ("person" in json_dict) and (json_dict["person"]):
                        # type_list = write2txt1(json_file_path, txt_f, "person", json_dict["person"], pic_size, type_list)
                        pass
                    if ("vehicle" in json_dict) and (json_dict["vehicle"]):
                        # type_list = write2txt1(json_file_path, txt_f, "vehicle", json_dict["vehicle"], pic_size, type_list)
                        pass
                    if ("trafficsign" in json_dict) and ( json_dict["trafficsign"]):
                        type_list = write2txt1(json_file_path, txt_f, "trafficsign", json_dict["trafficsign"], pic_size, type_list)
                    if ("trafficlight" in json_dict) and (json_dict["trafficlight"]):
                        type_list = write2txt1(json_file_path, txt_f, "trafficlight", json_dict["trafficlight"], pic_size, type_list)
                    #print(type_list)
        box_num_txt = open("box_num_txt.txt", "w")
        # for idx, itm in enumerate(classes["person"]):
        #     box_num_txt.write(itm + ": " + str(type_list[idx]) + "\n")

        # for idx, itm in enumerate(classes["vehicle"]):
        #     box_num_txt.write(itm + ": " + str(type_list[3 + idx]) + "\n")
        for idx, itm in enumerate(classes["trafficsign"]):
            box_num_txt.write(itm + ": " + str(type_list[idx + 14]) + "\n")

        for idx, itm in enumerate(classes["trafficlight"]):
            box_num_txt.write(itm + ": " + str(type_list[idx + 48]) + "\n")

    box_num_txt.close()

if __name__ == '__main__':
  # json_dir = "/media/andy/andy/外发标注数据/wanhong/json" 
  # output_dir = "/home/andy/Desktop/w"

  args = parse_args()
  json_dir = args.json_dir
  output_dir = args.output_dir

  if not os.path.exists(json_dir):
    print("Error !!! %s is not exists, please check the parameter")
    sys.exit(0)

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  hryt2txt(json_dir, output_dir)
