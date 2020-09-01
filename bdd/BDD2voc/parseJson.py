#!/usr/bin/env python
# -*- coding: utf8 -*-
#parse json，input json filename,output info needed by voc

import json
#这里是我需要的类别
categorys = ['car', 'bus', 'person', 'bike', 'truck', 'motor', 'train', 'rider', 'traffic sign', 'traffic light']

def parseJson(jsonFile):
    objs = []
    obj = []
    f = open(jsonFile)
    info = json.load(f)
    for ele in info:
        for i in ele['labels']:
            if(i['category'] in categorys):
                obj.append(int(i['box2d']['x1']))
                obj.append(int(i['box2d']['y1']))
                obj.append(int(i['box2d']['x2']))
                obj.append(int(i['box2d']['y2']))
                obj.append(i['category'])
                objs.append(obj)
                obj = []
        #print("objs",objs)
    return objs

#test
#parseJson("/home/nextcar/桌面/0a0a0b1a-7c39d841.json")
#
# def parseJson(jsonFile):
#     objs = []
#     obj = []
#     f = open(jsonFile)
#     info = json.load(f)
#     objects = info['frames'][0]['objects']
#     for i in objects:
#         if(i['category'] in categorys):
#             obj.append(int(i['box2d']['x1']))
#             obj.append(int(i['box2d']['y1']))
#             obj.append(int(i['box2d']['x2']))
#             obj.append(int(i['box2d']['y2']))
#             obj.append(i['category'])
#             objs.append(obj)
#             obj = []
#     #print("objs",objs)
#     return objs