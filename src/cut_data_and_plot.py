import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

n = 'tb_woquan'

min_gus_time = 25
max_gus_time = 200
thredhold = 500
mang_change = 70

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