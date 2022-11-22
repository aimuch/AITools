# The Cityscapes 数据集 
**[[英文](./README.md) | [中文](./README_zh.md)]**

该github库包含用于检查，准备和评估Cityscapes数据集的脚本。 该大型数据集包含来自50个不同城市的街道场景中记录的多种立体视频序列，除了20000个弱注释帧以外，还包含5000帧高质量像素级注释。

详细信息和下载链接请登录：www.cityscapes-dataset.net

## 数据集结构
Cityscapes dataset 的文件夹结构如下:
```vim
{root}/{type}{video}/{split}/{city}/{city}_{seq:0>6}_{frame:0>6}_{type}{ext}
```
其中独立元素的含义是:    
- **root** Cityscapes数据集的根文件夹。 我们的许多脚本检查指向该文件夹的环境变量“CITYSCAPES_DATASET”是否存在，并将其作为默认目录。
- **type** 数据类型或形态，比如 gtFine 代表精细的GroundTruth， leftImg8bit 代表左侧相机的八位图像。
- **split** 分割，即train， val， test， train_extra或demoVideo。 请注意，并非所有分组都存在所有类型的数据。 因此，偶尔找到空文件夹不要感到惊讶。
- **city** 这部分数据集的所属城市。
- **seq** 序列号，使用6位数字。
- **frame** 帧号，使用6位数字。 请注意，在一些城市中，虽然记录了非常长的序列，但在一些城市记录了许多短序列，其中仅记录了第19帧.
- **ext** 该文件的扩展名和可选的后缀，例如， _polygons.json为GroundTruth文件

**type**可能的值:    
- **gtFine** 精细注释，2975张训练图，500张验证图和1525张测试图。 这种类型的注释用于验证，测试和可选的训练。 注解使用包含单个多边形的“json”文件进行编码。 另外，我们提供png图像，其中像素值对标签进行编码。 有关详细信息，请参阅helpers / labels.py和prepare中的脚本。
- **gtCoarse** 粗略注释，可用于所有训练和验证图像以及另一组19998张训练图像（train_extra）。 这些注释可以用于训练，也可以与gtFine一起使用，也可以在弱监督的环境中单独使用。
- **gtBboxCityPersons** 行人边界框注释，可用于所有训练和验证图像。 有关更多详细信息，请参阅`helpers / labels_cityPersons.py`以及CityPersons出版物（Zhang等，CVPR’17）。
- **leftImg8bit** 左侧图像，采用8位LDR格式。这些图像都有标准的注释.
- **leftImg16bit** 左侧图像，采用16位HDR格式。这些图像提供每像素16位色彩深度并包含更多信息，特别是在场景的非常黑暗或明亮的部分。 警告：图像存储为16位PNG，这是非标准的，并且不是所有库都支持。
- **rightImg8bit** 右侧图像，采用8位LDR格式。
- **rightImg16bit** 右侧图像，采用16位HDR格式。
- **timestamp** 记录时间，单位是ns。 每个序列的第一帧总是有一个0的时间戳。
- **disparity** 预先计算的视差深度图。 为了获得视差值，对于p> 0的每个像素p计算：`d =（float（p）-1）/ 256`，而值p = 0是无效测量。 警告：图像存储为16位PNG，这是非标准的，并且不是所有库都支持。
- **camera** 内部和外部相机校准。 有关详情，请参阅 csCalibration.pdf
- **vehicle** 车辆测距，GPS坐标和室外温度。 详情请参阅csCalibration.pdf
随着时间的推移可能会增加更多类型，并且并非所有类型都是最初可用的，如果您需要其他元数据来运行您的方法，请告诉我们。

**split**可能出现的值:    
- **train** 通常用于训练, 包含 2975 张带有粗糙或精细标注的图像
- **val** 应该用于验证hyper-parameters，包含500个具有精细和粗糙注释的图像。 也可以用于训练.
- **test** 用于在我们的评估服务器上测试。 注释不公开，但为方便起见，我们包含自我车辆和整改边界的注释。
- **train_extra** 可以选择性地用于训练，包含带有粗略注释的19998张图像
- **demoVideo** 可用于定性评估的视频序列，这些视频不提供注释

## 脚本
在名为 `scripts` 的文件夹中有数据集包含几个脚本:    
- **helpers** 被其他脚本文件调用的帮助文件
- **viewer** 用于查看图像和标注的脚本
- **preparation** 用于将GroundTruth注释转换为适合您的方法的格式的脚本
- **evaluation** 评价你的方法的脚本
- **annotation** 被用来标注数据集的标注工具

请注意，所有文件顶部都有一个小型documentation。 非常重要

- `helpers/labels.py` 定义所有语义类ID的中心文件，并提供各种类属性之间的映射。
- `helpers/labels_cityPersons.py` 文件定义所有CityPersons行人类的ID并提供各种类属性之间的映射。
- `viewer/cityscapesViewer.py` 查看图像并覆盖注释。
- `preparation/createTrainIdLabelImgs.py` 将多边形格式的注释转换为带有标签ID的png图像，其中像素编码可以在“labels.py”中定义的“训练ID”。
- `preparation/createTrainIdInstanceImgs.py` 将多边形格式的注释转换为带有实例ID的png图像，其中像素编码由“train ID”组成的实例ID。
- `evaluation/evalPixelLevelSemanticLabeling.py` 该脚本来评估验证集上的像素级语义标签结果。该脚本还用于评估测试集的结果。
- `evaluation/evalInstanceLevelSemanticLabeling.py` 该脚本来评估验证集上的实例级语义标签结果。该脚本还用于评估测试集的结果。
- `setup.py` 运行 setup.py build_ext --inplace 启用cython插件以进行更快速的评估。仅针对Ubuntu进行了测试。


脚本可以通过 pip安装，如下： 
```shell
sudo pip install . 
```
这将脚本安装为名为cityscapesscripts的python模块并公开以下工具，请参阅上面的说明：    
- csViewer
- csLabelTool
- csEvalPixelLevelSemanticLabeling
- csEvalInstanceLevelSemanticLabeling
- csCreateTrainIdLabelImgs
- csCreateTrainIdInstanceImgs

请注意，对于您需要安装的图形工具:    
```shell
sudo apt install python-tk python-qt4
```

## 测评
一旦你想在测试集上测试你的方法，请在你提供的测试图像上运行你的方法并提交你的结果： 
www.cityscapes-dataset.net/submit/ 
对于语义标注，我们要求结果格式与我们的名为labelIDs的标签图像的格式相匹配。 
因此，您的代码应该生成图像，其中每个像素的值与labels.py中定义的类ID相对应。 
请注意，我们的评估脚本包含在脚本文件夹中，可用于在验证集上测试您的方法。 
有关提交过程的更多详细信息，请咨询我们的网站。

## 联系我们
如有任何问题，建议或意见，请随时与我们联系：

Marius Cordts, Mohamed Omran
mail@cityscapes-dataset.net
www.cityscapes-dataset.net