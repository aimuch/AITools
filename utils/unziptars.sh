#!/bin/bash

# 递归解压zip/tar文件

# 获取命令行传入的目录路径
target_directory="$1"

# 检查目录是否存在
if [ ! -d "$target_directory" ]; then
  echo "指定的目录不存在：$target_directory"
  exit 1
fi

# # 切换到目标目录
# cd "$target_directory"

# 计算 .zip 和 .tar 文件的总数量
total_files=$(find "$target_directory" -name "*.tar" -o -name "*.zip" 2> /dev/null | wc -l)


# 遍历并解压 .tar 和 .zip 文件
# find "$target_directory" -name "*.tar" -o -name "*.zip" -print0 | while IFS= read -r -d '' file; do
for file in $(find "$target_directory" -name "*.tar" -o -name "*.zip"); do
  directory_name=$(dirname "$file")
  file_name=$(basename "$file")
  extension="${file_name##*.}"

  # 创建以文件名（不包括扩展名）为名称的目录
  directory_name_extract="${file_name%.*}"
  mkdir -p "$directory_name/$directory_name_extract"

  # 根据文件扩展名决定使用哪个命令进行解压
  if [ "$extension" == "tar" ]; then
    tar -xf "$file" -C "$directory_name/$directory_name_extract"
  elif [ "$extension" == "zip" ]; then
    unzip -q "$file" -d "$directory_name/$directory_name_extract"
  fi

  # 检查解压是否成功
  if [ $? -eq 0 ]; then
    # 移动所有解压出的内容到目标文件夹
    mv "$directory_name/$directory_name_extract"/*/* "$directory_name/$directory_name_extract/" 2>/dev/null
    mv "$directory_name/$directory_name_extract"/* "$directory_name/$directory_name_extract/" 2>/dev/null

    # 删除空的子目录
    find "$directory_name/$directory_name_extract" -type d -empty -delete
  else
    echo "解压文件 $file 出错"
  fi

  echo "directory_name/directory_name_extract= $directory_name/$directory_name_extract"

  # 计算 .zip 和 .tar 文件的总数量
  sub_total_files=$(find "$directory_name/$directory_name_extract" -name "*.tar" -o -name "*.zip" 2> /dev/null | wc -l)
  echo "sub_total_files = $sub_total_files"

  # 初始化计数器
  count=0

  # 遍历并解压 .tar 和 .zip 文件
  #find "$directory_name/$directory_name_extract" -name "*.tar" -o -name "*.zip" -print0 | while IFS= read -r -d '' sub_file; do
  for sub_file in $(find "$directory_name/$directory_name_extract" -name "*.tar" -o -name "*.zip"); do
    # 更新计数器
    ((count++))

    sub_directory_name=$(dirname "$sub_file")
    sub_file_name=$(basename "$sub_file")
    sub_extension="${sub_file_name##*.}"

    # 创建以文件名（不包括扩展名）为名称的目录
    sub_directory_name_extract="${sub_file_name%.*}"
    mkdir -p "$directory_name/$directory_name_extract/$sub_directory_name_extract"

    # 根据文件扩展名决定使用哪个命令进行解压
    if [ "$sub_extension" == "tar" ]; then
      tar -xf "$sub_file" -C "$directory_name/$directory_name_extract/$sub_directory_name_extract"
    elif [ "$sub_extension" == "zip" ]; then
      unzip "$sub_file" -d "$directory_name/$directory_name_extract/$sub_directory_name_extract"
    fi

    # 检查解压是否成功
    if [ $? -eq 0 ]; then
      # 移动所有解压出的内容到目标文件夹
      mv "$directory_name/$directory_name_extract/$sub_directory_name_extract"/*/* "$directory_name/$directory_name_extract/$sub_directory_name_extract/" 2>/dev/null
      mv "$directory_name/$directory_name_extract/$sub_directory_name_extract"/* "$directory_name/$directory_name_extract/$sub_directory_name_extract/" 2>/dev/null

      # 删除空的子目录
      find "$directory_name/$directory_name_extract/$sub_directory_name_extract" -type d -empty -delete
    else
      echo "解压文件 $sub_file 出错"
    fi

    # 打印进度条
    progress=$(( (count * 100) / sub_total_files ))
    printf "进度：%3d%% (%d/%d)\r" $progress $count $sub_total_files
  done
done

# 打印完成信息
echo -e "\n解压完成。"
