'''
Author : JiangJc
Descriptions:

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
# def split_seq(select_track,in_time=3,pred_time=5,fps=25,step=5):#fixme
#     window_size =fps * (in_time + pred_time)
#     framelb, frameub = select_track['frame'].min(), select_track['frame'].max()
#     if frameub - frameub <window_size :
#         print(f"File:{file},track:{i} time is not satisfied")
#         return False,False
#     else:
#         features = ['frame', 'x', 'y', 'xVelocity', 'yVelocity', 'preceding_x', 'preceding_y', 'following_x',
#                     'following_y', 'leftPreceding_x',
#                     'leftPreceding_y', 'leftAlongside_x', 'leftAlongside_y', 'leftFollowing_x', 'leftFollowing_y',
#                     'rightPreceding_x', 'rightPreceding_y', 'rightAlongside_x', 'rightAlongside_y',
#                     'rightFollowing_x', 'rightFollowing_y']
#         for i in range(0, len(select_track) - window_size + 1, step):
#             window_df = select_track.iloc[i:i + window_size][features].reset_index(drop=True)
#             result_df = pd.concat([result_df, window_df], ignore_index=True)
#         return False,False

def load_scene(file,in_time=3,pred_time=5,fps=25,parent_folder="dataset",folder_path="demo_HighD",conditions=True):
    subfolder_path = os.path.join(parent_folder, folder_path)
    os.makedirs(subfolder_path, exist_ok=True)
    if file in [1, 2, 3, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]:#四车道
        lowerlaneids=[5,6]
    elif file in [26, 58, 59,60]:#七车道
        lowerlaneids = [6,7,8,9]
    else:
        lowerlaneids = [6, 7, 8]
    # (f"lower laneids : {lowerlaneids}")
    record = pd.read_csv(
        os.path.join(workdir, 'dataset', 'HighD', str(file).zfill(2) + '_recordingMeta.csv'))
    track = pd.read_csv(
        os.path.join(workdir, 'dataset', 'HighD', str(file).zfill(2) + '_tracks.csv'))
    df = track[track['laneId'].isin(lowerlaneids)]
    '''
    1.运动信息匹配
    '''
    for ind in ['precedingId', 'followingId', 'leftPrecedingId', 'leftAlongsideId',
       'leftFollowingId', 'rightPrecedingId', 'rightAlongsideId',
       'rightFollowingId']:
        df[ind[:-2]+'_x'] = df.apply(lambda row: 0 if row[ind] == 0 else
        df.loc[(df['id'] == row[ind]) & (df['frame'] == row['frame']), 'x'].values[0], axis=1)
        df[ind[:-2]+'_y'] = df.apply(lambda row: 0 if row[ind] == 0 else
        df.loc[(df['id'] == row[ind]) & (df['frame'] == row['frame']), 'y'].values[0], axis=1)
        print(f"================{ind}运动信息匹配完成================")
        # df[ind[:-2]+'_vx'] = df.apply(lambda row: 0 if row[ind] == 0 else
        # df.loc[(df['id'] == row[ind]) & (df['frame'] == row['frame']), 'xVelocity'].values[0], axis=1)
        # df[ind[:-2]+'_vy'] = df.apply(lambda row: 0 if row[ind] == 0 else
        # df.loc[(df['id'] == row[ind]) & (df['frame'] == row['frame']), 'yVelocity'].values[0], axis=1)
    df.to_csv(f'output_{file}.csv', index=False)
    print("================运动信息匹配完成，开始切割================")
    '''
    2.滑动时间窗切割
    '''
    meta = pd.read_csv(
        os.path.join(workdir, 'dataset', 'HighD',str(file).zfill(2) + '_tracksMeta.csv'))
    select_id = meta.groupby(["numLaneChanges", "drivingDirection"]).get_group((1, 2))['id'].unique()
    features = ['frame', 'x', 'y', 'xVelocity', 'yVelocity', 'preceding_x', 'preceding_y', 'following_x', 'following_y',
                'leftPreceding_x',
                'leftPreceding_y', 'leftAlongside_x', 'leftAlongside_y', 'leftFollowing_x', 'leftFollowing_y',
                'rightPreceding_x', 'rightPreceding_y', 'rightAlongside_x', 'rightAlongside_y',
                'rightFollowing_x', 'rightFollowing_y']
    window_size, step,count = 200, 5,0
    # window_size, step,count = 150, 5,0
    for i in select_id:
        select_track = df[df['id'] == i].reset_index()
        framelb,frameub=select_track['frame'].min(),select_track['frame'].max()
        if frameub-framelb<fps*(in_time+pred_time):
            print(f"File:{file},track:{i} time is not satisfied：{frameub-framelb}")
            continue
        else:
            count = count + 1
            for j in range(0, len(select_track) - window_size + 1, step):
                window_df = df.iloc[i:i + window_size][features].reset_index(drop=True)
                filename=f"file{file}_track{i}_windowind_{j}.npz"
                file_path = os.path.join(subfolder_path, filename)
                np.savez(file_path, data=window_df.to_numpy())
        if count%10==0:
            print(f"已处理{count}辆车的片段数据")
                # result_df = pd.concat([result_df, window_df], ignore_index=True)

for file in range(2,31):
    load_scene(file)
    print(f"--------------------文件{file}处理完毕--------------------")

# import random
# parent_folder,folder_path="dataset","demo_HighD"
# subfolder_path = os.path.join(parent_folder, folder_path)
# fileslist=os.listdir(subfolder_path)
#
# # os.path.listdir(os.path.join(os.getcwd(),subfolder_path))
# data=np.load(os.path.join(os.getcwd(),subfolder_path,random.choice(fileslist)))
# s=data['data']
# %% Testing Module
if __name__ == '__main__':
    print("hello,world!")
