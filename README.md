# AI Tools
- [formula.md](./formula.md) : AI相关公式
- [grid.xlsx](./grid.xlsx) ：可打印的网络格子
- [copyfiles.py](./copyfiles.py) ： 文件/文件夹复制脚本
- [abspath2txt.py](./abspath2txt.py) : 将文件夹中文件的绝对路径保存到txt中
    ```python
    input: 
        python3 abspath2txt.py "/home/andy/Data/img"
    output: 
        ./imgPath.txt
    ```
- [img2train.py](./img2train.py) ： 将图像分为训练和验证集，保存为train.txt和val.txt
    ```python
    input: 
        python3 img2train.py "/home/andy/Data/img"
    output: 
        ./train.txt
        ./val.txt
    ```
- [pick_img_by_list.py](./pick_img_by_list.py) ： 根据txt中的图像列表将图像和标签提取出来
    ```python
    input: 
        python3 pick_img_by_list.py "/home/andy/data/val.txt" "/home/andy/data/labels" "/home/andy/data/img"
    output: 
        ./pickedLabel
        ./pickedImg

- [create_VOC_txt.py](./create_VOC_txt.py) ： 创建VOC-like的txt文件，其中Main文件夹下的只有文件名，当前文件夹下的是完整的目录
    ```python
    input: 
        python3 create_txt_list.py "/home/andy/Data/img"
    output: 
        ./VOC/ImageSets/Main/train.txt
        ./VOC/ImageSets/Main/val.txt
        ./train.txt
        ./val.txt
    ```
- [showprocessbar.py](./showprocessbar.py) ： 显示处理进度脚本
- [pick_xml_img_by_xml.py](./pick_xml_img_by_xml.py) ： 从同一个文件夹中挑选xml和image文件分别到相应文件夹中
    ```python
    input: 
        python3 pick_xml_img_by_xml.py "/home/andy/data/labels" "/home/andy/data/img" 
    output:    
        ./pickedLabel
        ./pickedImg
    ```
- [pick_xml_img_by_img.py](./pick_xml_img_by_img.py) ： 根据图片文件夹将图片和标注文件挑选出来
    ```python
    input: 
        python pick_all_xml_img.py "/home/andy/data/labels" "/home/andy/data/img"
    output:    
        ./pickedLabel
        ./pickedImg
    ```
- [pick_txt_img_by_label.py](./pick_txt_img_by_label.py) : 根据指定标签将txt和image文件挑出来
    ```python
    input : 
        python3 pick_txt_img_by_label.py  "/home/andy/data/label_dir/"  "/home/andy/data/img_dir/" 
    output : 
        ./pickedLabel
        ./pickedImg
    ```
- [txt2xml.py](./txt2xml.py) ： YOLO的txt标签转VOC的xml格式标签脚本
    ```python
    input : 
        python3 txt2xml.py "/home/andy/data/ann_dir" "/home/andy/data/img_dir"
    output:
        ./xml
    ```
- [xml2txt.py](./xml2txt.py)　：　VOC数据集xml标签转YOLO需要的txt格式的标签脚本
    ```python
    input : 
        python3 xml2txt.py "/home/andy/data/xml"  "/home/andy/data/img"
    output :
        ./txt
        ./train.txt
        ./val.txt
        ./trianAll.txt
    ```

- [pick_non_empty_txt.py](./pick_non_empty_txt.py) : 提取text文件夹中非空的text文件
    ```python
    input : 
        python3 rm_empty_txt.py "/home/andy/data/txt"  "/home/andy/data/img"
    output :
        ./dst_txt
        ./dst_img
    ```