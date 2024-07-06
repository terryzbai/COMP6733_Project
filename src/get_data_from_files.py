import pandas as pd
import numpy as np

min_gus_time = 30
max_gus_time = 200
thredhold = 250
mang_change = 50

def get_data_from_files(*files):
    res = []
    temp_data = []
    flag = False
    for file in files:
        data = pd.read_csv(file).to_numpy()
        col4 = data[:, 3]
        col5 = data[:, 4]
        col6 = data[:, 5]
        gyo  = col4**2 + col5**2 + col6**2
        for i in range(1,len(data)):
            if gyo[i] < thredhold and np.abs(gyo[i] - gyo[i-1]) < mang_change:
                if flag == True and min_gus_time <len(temp_data) < max_gus_time :
                    res.append(temp_data)
                flag = False
                temp_data = []
            else:
                flag = True
                temp_data.append(data[i])
    
    return res
    
print(get_data_from_files('./data/yc_01_011.csv'))
print(len(get_data_from_files('./data/yc_01_011.csv')))
