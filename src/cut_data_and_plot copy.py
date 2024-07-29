import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

min_gus_time = 25
max_gus_time = 200
thredhold = 500
mang_change = 70

def kalman_filter_1d(measurements, A, H, Q, R, x0, P0):
    """
    一维卡尔曼滤波器实现

    参数:
    measurements: 一维测量数组
    A: 状态转移矩阵
    H: 测量矩阵
    Q: 过程噪声协方差矩阵
    R: 测量噪声协方差矩阵
    x0: 初始状态
    P0: 初始协方差矩阵

    返回:
    估计的状态数组
    """
    n = len(measurements)
    x = x0
    P = P0
    estimates = []

    for z in measurements:
        # 预测步骤
        x = np.dot(A, x)
        P = np.dot(np.dot(A, P), A.T) + Q

        # 计算卡尔曼增益
        S = np.dot(np.dot(H, P), H.T) + R
        K = np.dot(np.dot(P, H.T), np.linalg.inv(S))

        # 更新步骤
        y = z - np.dot(H, x)  # 测量残差
        x = x + np.dot(K, y)
        P = np.dot(np.eye(len(P)) - np.dot(K, H), P)

        # 保存估计结果
        estimates.append(x[0, 0])

    return estimates

dt = 1.0  # 时间步长
A = np.array([[1, dt], [0, 1]])  # 状态转移矩阵
H = np.array([[1, 0]])  # 测量矩阵
Q = np.array([[1, 0], [0, 1]])  # 过程噪声协方差矩阵
R = np.array([[10]])  # 测量噪声协方差矩阵
x0 = np.array([[0], [0]])  # 初始状态 (位置和速度)
P0 = np.eye(2)  # 初始协方差矩阵


# List all files in the current directory
file_list = os.listdir("./data")

for file in file_list:
    print(file)
    file_path = './data/'+ file
    data = pd.read_csv(file_path)

# Display the dataframe to understand its structure
    data.head()

    # Extract columns
    col1 = data.iloc[:, 0]
    col2 = data.iloc[:, 1]
    col3 = data.iloc[:, 2]
    col4 = data.iloc[:, 3]
    col5 = data.iloc[:, 4]
    col6 = data.iloc[:, 5]


    

    gyo  = col4**2 + col5**2 + col6**2

    # gyo = kalman_filter_1d(gyo, A, H, Q, R, x0, P0)


    res = []
    data1 = []
    flag = False
    for i in range(1,len(col1)):
        if gyo[i] < thredhold and np.abs(gyo[i] - gyo[i-1]) < mang_change:
            if flag == True and min_gus_time <len(data1) < max_gus_time :
                res.append(data1)
            flag = False
            data1 = []
        else:
            flag = True
            data1.append(i)


    print(len(res))
    print([len(x) for x in res])

    # Plot the data
    plt.figure(figsize=(15, 8))

    # Plot for the first column
    plt.subplot(2, 1, 1)
    plt.plot(range(0,len(col1)*10,10), col1, color='r')
    plt.plot(range(0,len(col1)*10,10), col2, color='g')
    plt.plot(range(0,len(col1)*10,10), col3, color='b')

    for i in range(len(res)):
        plt.axvline(x=res[i][0]*10, color='r', linestyle='--')
        plt.axvline(x=res[i][-1]*10, color='g', linestyle='--')
    plt.title('Accelerometer', fontsize=24)
    plt.xlabel('Time(ms)', fontsize=24)
    plt.ylabel('Value(g)', fontsize=24)
    plt.ylim(-5, 5)
    plt.legend()

    # Plot for the second column
    plt.subplot(2, 1, 2)
    plt.plot(range(0,len(col1)*10,10),col4, color='r')
    plt.plot(range(0,len(col1)*10,10),col5, color='g')
    plt.plot(range(0,len(col1)*10,10),col6, color='b')

    for i in range(len(res)):
        plt.axvline(x=res[i][0]*10, color='r', linestyle='--')
        plt.axvline(x=res[i][-1]*10, color='g', linestyle='--')
    plt.title(' Gyroscope ', fontsize=24)
    plt.xlabel('Time(ms)', fontsize=24)
    plt.ylabel('Value(dps)', fontsize=24)
    plt.ylim(-2000, 2000)
    plt.legend()


    # Show the plots
    plt.tight_layout()
    plt.savefig('./img/data_img/'+ file.split('.')[0] +'_cut.png')
    # plt.show()

exit()

# Load the CSV file
file_path = './exp/'+ n +'.csv'
data = pd.read_csv(file_path)

# Display the dataframe to understand its structure
data.head()

# Extract columns
col1 = data.iloc[:, 0]
col2 = data.iloc[:, 1]
col3 = data.iloc[:, 2]
col4 = data.iloc[:, 3]
col5 = data.iloc[:, 4]
col6 = data.iloc[:, 5]

gyo  = col4**2 + col5**2 + col6**2


res = []
data1 = []
flag = False
for i in range(1,len(col1)):
    if gyo[i] < thredhold and np.abs(gyo[i] - gyo[i-1]) < mang_change:
        if flag == True and min_gus_time <len(data1) < max_gus_time :
            res.append(data1)
        flag = False
        data1 = []
    else:
        flag = True
        data1.append(i)


print(len(res))
print([len(x) for x in res])

# Plot the data
plt.figure(figsize=(15, 8))

# Plot for the first column
plt.subplot(2, 1, 1)
plt.plot(range(0,len(col1)*10,10), col1, color='r')
plt.plot(range(0,len(col1)*10,10), col2, color='g')
plt.plot(range(0,len(col1)*10,10), col3, color='b')

for i in range(len(res)):
    plt.axvline(x=res[i][0]*10, color='r', linestyle='--')
    plt.axvline(x=res[i][-1]*10, color='g', linestyle='--')
plt.title('Accelerometer', fontsize=24)
plt.xlabel('Time(ms)', fontsize=24)
plt.ylabel('Value(g)', fontsize=24)
plt.ylim(-5, 5)
plt.legend()

# Plot for the second column
plt.subplot(2, 1, 2)
plt.plot(range(0,len(col1)*10,10),col4, color='r')
plt.plot(range(0,len(col1)*10,10),col5, color='g')
plt.plot(range(0,len(col1)*10,10),col6, color='b')

for i in range(len(res)):
    plt.axvline(x=res[i][0]*10, color='r', linestyle='--')
    plt.axvline(x=res[i][-1]*10, color='g', linestyle='--')
plt.title(' Gyroscope ', fontsize=24)
plt.xlabel('Time(ms)', fontsize=24)
plt.ylabel('Value(dps)', fontsize=24)
plt.ylim(-2000, 2000)
plt.legend()


# Show the plots
plt.tight_layout()
plt.savefig('./img/'+ n +'_cut.png')
plt.show()