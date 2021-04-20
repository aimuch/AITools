# -*- coding: utf-8 -*-
# @Author: Andy Liu
# @Date:   2021-04-20
"""
Convert CVAT labels to PS2.0 JSON
"""
import os
import sys
import argparse
import cv2
import random
import shutil
import json
import xml.dom.minidom
from tqdm import tqdm

point_type = {"T":0, "L":1}
slot_type = {"vertical":1, "perpendicular":1}

def parse_args():
    parser = argparse.ArgumentParser(description='Convert CVAT labels to PS2.0 JSON')
    parser.add_argument('--srcLabelPath', type=str, default='') # all CVAT label folders
    parser.add_argument('--srcJpgPath', type=str, default='') # all input image folders
    parser.add_argument('--dstJsonPath', type=str, default='./dstJson')    # created voc folders
    parser.add_argument('--dstJpgPath', type=str, default='./dstIMG') # all input image folders
    parser.add_argument('--roiShape', type=tuple, default=(-1, -1)) # (width, height), (-1, -1) for no ROI

    args = parser.parse_args()
    return args

class cvat2jsons:
    def __init__(self, srcLabelPath, srcJpgPath, dstJsonPath, dstJpgPath, roiShape) -> None:
        self.srcLabelPath = srcLabelPath
        self.srcJpgPath = srcJpgPath
        self.dstJsonPath = dstJsonPath
        self.dstJpgPath = dstJpgPath
        if not os.path.exists(self.dstJsonPath):
            os.makedirs(self.dstJsonPath)
            print("%s is not exists, it has created!"% self.dstJsonPath)
        if not os.path.exists(self.dstJpgPath):
            os.makedirs(self.dstJpgPath)
            print("%s is not exists, it has created!"%self.dstJpgPath)
        self.roiShape = roiShape # (width, height)
        self.usingROI = False
        if self.roiShape[0] > 0 or self.roiShape[1] > 0:
            self.usingROI = True
        self.roiXbias = 0
        self.roiYbias = 0
        print("init done!")

    def run(self):
        cvatXmlList = os.listdir(self.srcLabelPath)
        for xml in cvatXmlList:
            xml_path = os.path.join(self.srcLabelPath, xml)
            self.cvat2json(xml_path)

    def write_json(self, name, data) -> None:
        """
        Write image and label with given name.
        """
        if "/" not in name:
            jsonPath = os.path.join(self.dstJsonPath, os.path.splitext(name)[0]+".json")
        else:
            jsonPath = os.path.splitext(name)[0] + ".json"
        with open(jsonPath, 'w') as file:
            json.dump(data, file)

    def cvat2json(self, xml_path) -> None:
        DOMTree = ''
        try:
            DOMTree = xml.dom.minidom.parse(xml_path)
        except Exception as e:
            print(e)
            return None
        annotation  = DOMTree.documentElement
        meta = annotation.getElementsByTagName('meta')[0]
        xmlName = meta.getElementsByTagName('name')[0].childNodes[0].data

        # ---- An  xml file in the cvat annotation file corresponds to a picture of a video ---- #
        img_list = annotation.getElementsByTagName('image')

        for img in img_list:
            imageID = img.getAttribute("id")
            imageName = img.getAttribute("name")

            # ------- filter xml ------- #
            if "LR" not in imageName:
                continue

            width_str = img.getAttribute("width")
            width_int = int(width_str)
            height_str = img.getAttribute("height")
            height_int = int(height_str)
            # points = img.getElementsByTagName('points')
            slots = img.getElementsByTagName('polygon')
            xmlname = imageName.split(".")[0]+".xml"
            picturepath = os.path.join(self.srcJpgPath, imageName)
            dstImgPath = os.path.join(self.dstJpgPath, imageName)
            if not os.path.exists(picturepath):
                print(picturepath, " is not exists!")
                continue
            imgSrc = cv2.imread(picturepath)
            roiLeft = 0
            roiRight = width_int
            roiTop = 0
            roiBottom = height_int
            if self.usingROI:
                width_roi = str(self.roiShape[0])
                height_roi = str(self.roiShape[1])
                self.roiXbias = int(width_int/2 - width_roi/2)
                self.roiYbias = int(height_int/2 - height_roi/2)
                roiLeft = int(width_int/2 -width_roi/2)
                roiRight = int(width_int/2 + width_roi/2)
                roiTop = int(height_int/2 - height_roi/2)
                roiBottom = int(height_int/2 + height_roi/2)
                imgROI = imgSrc[roiTop:roiBottom, roiLeft:roiRight]
                cv2.imwrite(dstImgPath, imgROI, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            else:
                cv2.imwrite(dstImgPath, imgSrc, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            jsonData = {}
            for slot in slots:
                with slot:
                    pnts = [[float(i.split(",")[0]), float(i.split(",")[1])] for i in slot.getAttribute('points').split(';')]
                    attributes = slot.getElementsByTagName('attribute')
                    pnt1Type = None
                    pnt2Type = None
                    slotType = None
                    for attr in attributes:
                        name = attr.getAttribute("name")
                        if name == "first_point_type":
                            pnt1Type = attr.childNodes[0].data
                        if name == "second_point_type":
                            pnt2Type = attr.childNodes[0].data
                        if name == "type":
                            slotType = attr.childNodes[0].data
                    side1 = [pnts[0][0], pnts[0][1], pnts[2][0], pnts[2][1], point_type[pnt1Type]]
                    side2 = [pnts[1][0], pnts[1][1], pnts[3][0], pnts[3][1], point_type[pnt2Type]]


                    if "marks" not in jsonData.keys():
                        jsonData["marks"] = [side1]
                    else:
                        if side1 not in jsonData["marks"]:
                            jsonData["marks"].append(side1)
                    if side2 not in jsonData["marks"]:
                        jsonData["marks"].append(side2)

                    if "slots" not in jsonData.keys():
                        jsonData["slots"] = [[jsonData["marks"].index(side1), jsonData["marks"].index(side2), slot_type[slotType], 90]]
                    else:
                        jsonData["slots"].append([jsonData["marks"].index(side1), jsonData["marks"].index(side2), slot_type[slotType], 90])

            dstJsonPath = os.path.join(self.dstJsonPath, os.path.splitext(imageName)[0] + ".json")
            self.write_json(dstJsonPath, jsonData)





if __name__ == '__main__':
    args = parse_args()
    srcLabelPath = args.srcLabelPath
    srcJpgPath = args.srcJpgPath
    dstJsonPath = args.dstJsonPath
    dstJpgPath = args.dstJpgPath
    roiShape = args.roiShape
    if not os.path.exists(srcLabelPath):
        print("Error !!! %s is not exists, please check the parameter"%srcLabelPath)
        sys.exit(0)
    if not os.path.exists(srcJpgPath):
        print("Error !!! %s is not exists, please check the parameter"%srcJpgPath)
        sys.exit(0)

    if not os.path.exists(dstJsonPath):
        os.makedirs(dstJsonPath)
        print("%s is not exists, it has created!"%dstJsonPath)
    if not os.path.exists(dstJpgPath):
        os.makedirs(dstJpgPath)
        print("%s is not exists, it has created!"%dstJpgPath)

    roiShape = (-1, -1)
    instance = cvat2jsons(srcLabelPath, srcJpgPath, dstJsonPath, dstJpgPath, roiShape)
    instance.run()
    print("Done!")