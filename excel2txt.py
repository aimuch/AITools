import pandas as pd

EXCEL_PATH = "/home/andy/DevWorkSpace/Data/label_proj_picture.xlsx"
TXT_PATH = "/home/andy/DevWorkSpace/Data/label_proj_picture.txt"

data = pd.read_excel(EXCEL_PATH)

image_list = data.iloc[2:994,0].values

with open(TXT_PATH, 'w') as f:
    for line in image_list:
        f.write(line + "\n")
