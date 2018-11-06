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
import json
import sys
import argparse
import cv2
import random
from tqdm import tqdm

classes = ["person", "vehicle", "trafficsign", "trafficlight"]

cls_clr = [(0,0,255),
           (0,255,0),
           (255,0,0),
           (0,255,255)] 

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('json_dir', help='Json directory', type=str)
    parser.add_argument('img_dir', help='Image directory', type=str)
    parser.add_argument('output_dir', help='Output directory', type=str)
    args = parser.parse_args()
    return args


def draw_img(img, box, clr, attr):
  x1, y1, x2, y2 = map(int, box)
  cv2.rectangle(img, (x1,y1),(x2,y2), clr, 2) 
  cv2.putText(img, attr, (x1,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 1, clr, 2)
  return img

def draw_attrs_box(img, cls, object_list):
    clr_id = classes.index(cls) 
    img_out = img

    dict_attrs = ""
    box = []
    for id_dict in object_list:
        #print("id_dict:%s"%id_dict)
        if "attrs" in id_dict:
            #print("attrs:%s\n"%id_dict["attrs"])
            dict_attrs = id_dict["attrs"]["ignore"][0] # dict_attrs = ignore_type_occlusion_led_color_direction
            
            if id_dict["attrs"].has_key("type") and id_dict["attrs"]["type"] :
               dict_attrs += "_" + id_dict["attrs"]["type"]
            if id_dict["attrs"].has_key("occlusion") and id_dict["attrs"]["occlusion"] :
               dict_attrs += "_" + id_dict["attrs"]["occlusion"][0] 
            if id_dict["attrs"].has_key("led") and id_dict["attrs"]["led"]:
                dict_attrs += "_" + id_dict["attrs"]["led"][0] 
            if id_dict["attrs"].has_key("color") and id_dict["attrs"]["color"] :
                dict_attrs += "_" + id_dict["attrs"]["color"][0] 
            if id_dict["attrs"].has_key("direction") and id_dict["attrs"]["direction"]:
                dict_attrs += "_" + id_dict["attrs"]["direction"][0] 


        #print("attrs:%s"%dict_attrs)
        if "data" in id_dict:
            box = id_dict["data"]

        img_out = draw_img(img_out, box, cls_clr[clr_id], dict_attrs)

    return img_out

def draw_labelling(json_dir, img_dir, output_dir):
    count = 0
    for folder in os.listdir(json_dir):
        folder_path = os.path.join(json_dir, folder)
        filelist = os.listdir(folder_path)
        for json_file in filelist:
            count += 1
            #print("folder:%s,count:%d",folder,count)
            json_file_path = os.path.join(folder_path, json_file)
            with open(json_file_path, "r") as json_f:
                lines = json_f.readlines()
                for line in lines:
                    json_dict = json.loads(line)
                    if "image_key" not in json_dict:
                        continue
                    image_name = json_dict["image_key"]

                    image_folder = folder.split("_")[0]
                    image_path = os.path.join(img_dir, image_folder + "/" + image_name)
                    print("image_path:%s"%image_path)
                    img = cv2.imread(image_path)

                    #if ("person" in json_dict) and (json_dict["person"]):
                    #   img = draw_attrs_box(img, "person", json_dict["person"]) 
                    # if ("vehicle" in json_dict) and (json_dict["vehicle"]):
                    #    img = draw_attrs_box(img, "vehicle", json_dict["vehicle"]) 
                    if ("trafficsign" in json_dict) and ( json_dict["trafficsign"]):
                       #print(json_dict["trafficsign"])
                       #a = input("a")
                       img = draw_attrs_box(img, "trafficsign", json_dict["trafficsign"]) 
                    if ("trafficlight" in json_dict) and (json_dict["trafficlight"]):
                       img = draw_attrs_box(img, "trafficlight", json_dict["trafficlight"]) 

                    output_folder = os.path.join(output_dir, image_folder)
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                    output_path = os.path.join(output_folder, image_name)
                    #print("output_path:%s"%output_path)
                    cv2.imwrite(output_path, img)

        print("%s done"%folder_path)

if __name__ == '__main__':
  args = parse_args()
  json_dir = args.json_dir
  img_dir = args.img_dir
  output_dir = args.output_dir

  if not os.path.exists(json_dir):
    print("Error !!! %s is not exists, please check the parameter"%json_dir)
    sys.exit(0)

  if not os.path.exists(img_dir):
    print("Error !!! %s is not exists, please check the parameter"%img_dir)
    sys.exit(0)

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print("Output folder = ", os.path.abspath(output_dir))

  draw_labelling(json_dir, img_dir, output_dir)
