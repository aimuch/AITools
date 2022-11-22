# -*- coding: utf-8 -*-

import os
import cv2

def drowBox(imgPath,txtPath, destPath):
	point_color = (0, 255, 0) # BGR
	thickness = 1 
	lineType = 4
	for name in os.listdir(imgPath):
		name = name.rstrip('.jpg')
		print(name)

		img = os.path.join(imgPath, name) + '.jpg'		
		txt = os.path.join(txtPath, name) + '.txt'
		dest = os.path.join(destPath, name) + '.jpg'

		fimg = cv2.imread(img)
		h,w = fimg.shape[:2]

		ftxt = open(txt, "r") 
		
		for line in ftxt.readlines():
			c1,c2,d1,d2 = [float(i) for i in line.split()[1:]]
			x1,y1,x2,y2 = yolo2Box(c1,c2,d1,d2,w,h)
			cv2.rectangle(fimg, (x1,y1), (x2,y2), point_color, thickness, lineType)

		ftxt.close()

		cv2.imshow(img,fimg)
		cv2.imwrite(dest, fimg)
		cv2.destroyAllWindows()


def yolo2Box(c1,c2,d1,d2,w,h):
	x1 = int(c1 * w - (d1/2) * w)
	y1 = int(c2 * h - (d2/2) * h)
	x2 = int(c1 * w + (d1/2) * w)
	y2 = int(c2 * h + (d2/2) * h)

	return (x1,y1,x2,y2)

if __name__ == '__main__':

	imgPath = r'./img'
	txtPath = r'./txt'
	destPath = r'./draw_box'

	drowBox(imgPath,txtPath,destPath)
	print("-------------------------\nDone\n")
