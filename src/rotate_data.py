import os
import pandas as pd
import numpy as np

def rotate_vector(vector, R):
    return np.dot(R, vector)

def process_file(input_path, output_path, R_x):
    # 读取CSV文件
    data = pd.read_csv(input_path)
    print(data.shape)
    
    # 对每一组xyz数据应用旋转矩阵
    col_groups = [[0, 1, 2], [3, 4, 5]]
    rotated_data = pd.DataFrame()
    
    for col_group in col_groups:
        rotated_vectors = data.apply(lambda row: rotate_vector([row[col_group[0]], row[col_group[1]], row[col_group[2]]], R_x), axis=1)
        rotated_df = pd.DataFrame(rotated_vectors.tolist(), columns=[f'col_{i}_rot' for i in col_group])
        rotated_data = pd.concat([rotated_data, rotated_df], axis=1)
    
    # 保存旋转后的数据到新的CSV文件
    rotated_data.to_csv(output_path, index=False, header=False)

def process_folder(input_folder, output_folder):
    print(input_folder, output_folder)
    # 旋转角度（弧度）
    theta = np.deg2rad(10)  # 10度转换为弧度

    # 绕 x 轴的旋转矩阵
    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta), np.cos(theta)]
    ])

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有CSV文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, 'r'+filename)
            process_file(input_path, output_path, R_x)
            print(f"Processed {filename}")

# 输入文件夹和输出文件夹路径
input_folder = './data'
output_folder = './data_aug'

process_folder(input_folder, output_folder)
print("All files processed.")
