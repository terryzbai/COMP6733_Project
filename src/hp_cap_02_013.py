import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

n = 'hp_02_013'

min_gus_time = 25
max_gus_time = 200
threshold = 500
mang_change = 70

file_path = './data/' + n + '.csv'
data = pd.read_csv(file_path)

col1 = data.iloc[:, 0]
col2 = data.iloc[:, 1]
col3 = data.iloc[:, 2]
col4 = data.iloc[:, 3]
col5 = data.iloc[:, 4]
col6 = data.iloc[:, 5]

def plot_with_highlighted_segments(data, segments):
    col1 = data.iloc[:, 0]
    col2 = data.iloc[:, 1]
    col3 = data.iloc[:, 2]
    col4 = data.iloc[:, 3]
    col5 = data.iloc[:, 4]
    col6 = data.iloc[:, 5]

    plt.figure(figsize=(15, 8))

    plt.subplot(2, 1, 1)
    plt.plot(range(0, len(col1)*10, 10), col1, color='r', label='col1')
    plt.plot(range(0, len(col1)*10, 10), col2, color='g', label='col2')
    plt.plot(range(0, len(col1)*10, 10), col3, color='b', label='col3')

    for start_time, end_time in segments:
        plt.axvline(x=start_time, color='r', linestyle='--')
        plt.axvline(x=end_time, color='g', linestyle='--')
    plt.title('Accelerometer', fontsize=24)
    plt.xlabel('Time(ms)', fontsize=24)
    plt.ylabel('Value(g)', fontsize=24)
    plt.ylim(-5, 5)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(range(0, len(col1)*10, 10), col4, color='r', label='col4')
    plt.plot(range(0, len(col1)*10, 10), col5, color='g', label='col5')
    plt.plot(range(0, len(col1)*10, 10), col6, color='b', label='col6')

    for start_time, end_time in segments:
        plt.axvline(x=start_time, color='r', linestyle='--')
        plt.axvline(x=end_time, color='g', linestyle='--')
    plt.title('Gyroscope', fontsize=24)
    plt.xlabel('Time(ms)', fontsize=24)
    plt.ylabel('Value(dps)', fontsize=24)
    plt.ylim(-2000, 2000)
    plt.legend()

    plt.tight_layout()
    plt.savefig('./img/' + n + '_highlighted_segments.png')
    plt.show()

segments = [(300, 1100), (1200, 2000), (2300, 3100), (3500, 4300), (4540, 5450), (5900, 6700), (7100, 7950), (8050, 9000)]

plot_with_highlighted_segments(data, segments)