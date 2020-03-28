#coding=utf-8
import  xml.dom.minidom
import sys
import os


def toTxt( xmlName ):

	dom = xml.dom.minidom.parse(sys.argv[1]+'/'+xmlName)
	vedioName = xmlName[:-4]

	images = dom.getElementsByTagName('image')
	os.mkdir('txt/'+vedioName)

	for image in images:
		id=image.getAttribute("id")
		file = open('txt/'+vedioName+'/'+vedioName+'_'+id+'.txt','w+')
		file2 = open('txt_all/'+vedioName+'_'+id+'.txt','w+')
		file.write('imagesource:frontCamera\ngsd:0.2\n')
		file2.write('imagesource:frontCamera\ngsd:0.2\n')
		polygons = image.getElementsByTagName('polygon')
		for polygon in polygons:
			points = polygon.getAttribute("points")
			points = points.replace(',',' ').replace(';',' ')
			if len(points.split()) > 8:
				print(vedioName, "file error!")
				break
			label = polygon.getAttribute("label")
			attributes = polygon.getElementsByTagName("attribute")
			for attribute in attributes:
				if attribute.getAttribute("name") == 'difficult':
					if attribute.firstChild.data == 'no':
						difficult = '0'
					else:
						difficult = '1'

			file.write(points+' '+label+' '+ difficult + '\n')
			file2.write(points+' '+label+' '+ difficult + '\n')

		file.close()
		file2.close()

	return

if __name__ == '__main__':
	xmlPath = sys.argv[1]
	xmlNames = os.listdir(xmlPath)
	for xmlName in xmlNames:
		toTxt(xmlName)
