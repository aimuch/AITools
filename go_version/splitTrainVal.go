package main

import (
	"flag"
	"fmt"
	"os"
)

var valRate = flag.Float64("valRate", 0.2, "Rate of validation set")
var trainImgPath = flag.String("trainImgPath", "./train_img", "The path of the training images")
var trainLabelPath = flag.String("trainLabelPath", "./train_label", "The path of the training labels")
var valImgPath = flag.String("valImgPath", "./val_img", "The path of the validation images")
var valLabelPath = flag.String("valLabelPath", "./val_label", "The path of the validation labels")

// 判断所给路径文件/文件夹是否存在
func Exits(path string) bool {
	_, err := os.Stat(path)
	if err != nil {
		if os.IsExist(err) {
			return true
		}
		return false
	}
	return true
}

// 判断所给路径是否为文件夹
func IsDir(path string) bool {
	s, err := os.Stat(path)
	if err != nil {
		return false
	}
	return s.IsDir()
}

// 判断所给路径是否为文件
func IsFile(path string) bool {
	return !IsDir(path)
}

func main() {
	// 解析命令行参数
	flag.Parse()
	// 输出命令行参数
	fmt.Println(*valRate)
	fmt.Println(*trainImgPath)
	fmt.Println(*trainLabelPath)
	fmt.Println(*valImgPath)
	fmt.Println(*valLabelPath)

	//! TODO
}
