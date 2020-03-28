#coding=utf-8
import numpy as np
import cv2
import os
import sys


def drawBox(txt,txtPath,imagePath,destDir):
	
	imageName = txt[:-3]+'jpg'
	if not os.path.exists(destDir):
		os.mkdir(destDir)
	if os.path.exists(destDir+'/'+imageName):
		return

	file = open(txtPath+'/'+txt,'r')
	srcImg=cv2.imread(imagePath+'/'+imageName)
	lines = file.readlines()[2:]
	img = srcImg.copy()

	for line in lines:
		points = line.split()[:-2]
		pts = np.array([[points[0], points[1]], [points[2], points[3]], [points[4], points[5]], [points[6], points[7]]],dtype = np.float)
		cv2.polylines(img, np.int32([pts]), True, (255, 255, 0), 2)

	cv2.imwrite(destDir+'/'+imageName, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
	
	file.close()
	return


if __name__ == '__main__':
	txtPath = sys.argv[1]
	imagePath = sys.argv[2]
	destDir = sys.argv[3]

	if not os.path.exists(txtPath) or not os.path.exists(imagePath) or not os.path.exists(destDir):
		print('lack of argv : txtPath, imagePath, destDir')

	txtNames = os.listdir(txtPath)
	for txtName in txtNames:
		drawBox(txtName,txtPath,imagePath,destDir)
