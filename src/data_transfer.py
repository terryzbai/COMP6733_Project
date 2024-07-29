import os
import pandas as pd
import numpy as np

min_gus_time = 25
max_gus_time = 200
thredhold = 500
mang_change = 70

# data = pd.read_csv('./tb_data/tb_01_013.csv')
# data = data.to_numpy()
# print(data)
# print(len(data))

# exit()

def rotate_vector(vector, R):
    return np.dot(R, vector)

def process_file(input_path, output_path):
    # 读取CSV文件

    guesture_order = input_path.split('/')[-1].split('_')[1]

    data = pd.read_csv(input_path)
    data = data.to_numpy()

    # exit()
    data = np.pad(data, ((0, 0), (0, 6)), 'constant', constant_values=0)
    
    # print(data.size())

    
    col4 = data[:, 3]
    col5 = data[:, 4]
    col6 = data[:, 5]
    
    gyo  = col4**2 + col5**2 + col6**2

    res = []
    data1 = []
    flag = False
    for i in range(1,len(data)):
        if gyo[i] < thredhold and np.abs(gyo[i] - gyo[i-1]) < mang_change:
            if flag == True and min_gus_time <len(data1) < max_gus_time :
                res.append(data1)
            flag = False
            data1 = []
        else:
            flag = True
            data1.append(i)
 
    for sae in res:
        len1 = len(sae)
        for i in sae:
            data[i,5+int(guesture_order)] = ((i-sae[0]) + 1)/len1
            data[i,-1] = 1


    data = pd.DataFrame(data)

    data.to_csv(output_path, index=False, header=False)

def process_folder(input_folder, output_folder):
    print(input_folder, output_folder)

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有CSV文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            process_file(input_path, output_path)
            print(f"Processed {filename}")

# 输入文件夹和输出文件夹路径
input_folder = './tb_data'
output_folder = './data_stml'

process_folder(input_folder, output_folder)
print("All files processed.")
