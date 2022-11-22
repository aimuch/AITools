# AI 相关的公式

## CNN
1. 计算卷积后输出尺寸
```python
new_height = (input_height - filter_height + 2 * P)/S + 1
new_width = (input_width - filter_width + 2 * P)/S + 1
```
- P: Padding
- S: Strides

2. 计算maxPool输出尺寸
```python
new_height = (input_height - filter_height)/S + 1
new_width = (input_width - filter_width)/S + 1
```
