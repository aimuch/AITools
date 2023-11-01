#!/bin/bash

# 获取命令行传入的目录路径
target_directory="$1"

# 检查目录是否存在
if [ ! -d "$target_directory" ]; then
  echo "指定的目录不存在：$target_directory"
  exit 1
fi

# 切换到目标目录
cd "$target_directory"

# 计算 .tar 文件的数量
total_files=$(ls *.tar 2> /dev/null | wc -l)

# 初始化计数器
count=0

# 遍历并解压 .tar 文件
for tarfile in *.tar; do
  # 更新计数器
  ((count++))

  # 创建以 .tar 文件名为名称的目录
  directory_name="${tarfile%.tar}"
  mkdir "$directory_name"

  # 将 .tar 文件解压到该目录
  tar -xf "$tarfile" -C "$directory_name"

  # 检查解压是否成功
  if [ $? -eq 0 ]; then
    
    # 尝试删除文件，最多重试3次
    retry_count=0
    max_retries=3

    while [ $retry_count -lt $max_retries ]; do
      rm -f "$tarfile" 2>/dev/null
      if [ $? -eq 0 ]; then
        break
      else
        echo "删除文件 $tarfile 出错：资源可能正忙，等待1秒后重试..."
        sleep 1
        ((retry_count++))
      fi
    done

    if [ $retry_count -eq $max_retries ]; then
      echo "重试达到最大次数，仍然无法删除 $tarfile"
    fi
    
    # 移动所有解压出的内容到目标文件夹
    mv "$directory_name"/*/* "$directory_name/" 2>/dev/null
    mv "$directory_name"/* "$directory_name/" 2>/dev/null

    # 删除空的子目录
    find "$directory_name" -type d -empty -delete
  else
    echo "解压文件 $tarfile 出错"
  fi

  # 打印进度条
  progress=$(( (count * 100) / total_files ))
  printf "进度：%3d%% (%d/%d)\r" $progress $count $total_files
done

# 打印完成信息
echo -e "\n解压完成。"
