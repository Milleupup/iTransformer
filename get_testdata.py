'''
Author : JiangJc
Descriptions:模拟轨迹数据格式，用于直接测试itransformer模块的正常运行
'''
# %% Core module
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
import random
import math
import copy

plt.rcParams['font.sans-serif'] = 'STKAITI'
workdir = os.getcwd()
def export_dict_to_csv_1(save_dict, save_path):
    # 曾用名：save_Dict
    # key1 val1[0] val1[1] val1[2]...
    # key2 val2[0] val2[1] val2[2]...
    # ...
    with open(save_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 写入CSV文件的表头
        # writer.writerow(column_names)
        # 逐行写入数据
        for key, values in save_dict.items():
            writer.writerow([key] + list(values))
    print(f"字典已成功导出至{save_path}")


def export_dict_to_csv_2(dictionary, filename):
    # key1 key2 key3 ...
    # val1[0] val2[0] val3[0]...
    # val1[1] val2[1] val3[1]...
    # ...
    # 获取所有键和列表的长度
    keys = list(dictionary.keys())
    length = len(dictionary[keys[0]])
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keys)
        # 写入每一行的值
        for i in range(length):
            row = [dictionary[key][i] for key in keys]
            writer.writerow(row)
    print(f"字典已成功导出至{filename}")


# %% Development module
import numpy as np
import os
def get_onebyone(num_rows = 200,num_cols = 20,num_samples = 1028,parent_folder="dataset",folder_path="demo_dataset"):
    subfolder_path = os.path.join(parent_folder, folder_path)
    os.makedirs(subfolder_path, exist_ok=True)
    # 生成并保存数据
    for i in range(num_samples):
        data = np.random.random((num_rows, num_cols))
        filename = f"data_{i}.npz"
        file_path = os.path.join(subfolder_path, filename)
        np.savez(file_path, data=data)
        if i %100==0:
            print(f"已生成{i}份数据")
def get_Mbyone(num_rows = 200,num_cols = 20,num_samples = 1028,parent_folder="dataset",folder_path="demo_dataset"):
    # todo
    '''
    尚未开发完成
    '''
    subfolder_path = os.path.join(parent_folder, folder_path)
    os.makedirs(subfolder_path, exist_ok=True)
    data_dict = {}
    for i in range(num_samples):
        # 生成完全随机的数据
        data = np.random.random((num_rows, num_cols))
        # 定义保存的键名（例如 "xx_1.npz"、"xx_2.npz"）
        key = f"xx_{i + 1}.npz"
        # 将数据添加到字典中
        data_dict[key] = data
    # 使用 np.savez 将字典中的数据保存为 npz 文件
    filename = f"file_{i}.npz"
    file_path = os.path.join(subfolder_path, filename)
    np.savez(filename, **data_dict)#

import random
ind=random.randint(0,50000)
parent_folder,folder_path="dataset","demo_dataset"
subfolder_path = os.path.join(parent_folder, folder_path)
data=np.load(os.path.join(os.getcwd(),subfolder_path,f"data_{ind}.npz"))
s=data['data']
# %% Testing Module
if __name__ == '__main__':
    print("hello,world!")
