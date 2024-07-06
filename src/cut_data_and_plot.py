import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

n = 'tb_01_001'

# Load the CSV file
file_path = './data/'+ n +'.csv'
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
for i in range(len(col1)):
    if gyo[i] < 150:
        if flag == True and 40 <len(data1) < 200:
            res.append(data1)
        flag = False
        data1 = []
    else:
        flag = True
        data1.append(i)


print(len(res))

# Plot the data
plt.figure(figsize=(15, 8))

# Plot for the first column
plt.subplot(2, 1, 1)
plt.plot(col1, label='Column 1', color='r')
plt.plot(col2, label='Column 2', color='g')
plt.plot(col3, label='Column 3', color='b')

for i in range(len(res)):
    plt.axvline(x=res[i][0], color='r', linestyle='--')
    plt.axvline(x=res[i][-1], color='g', linestyle='--')
plt.title('Line Plot for Column x')
plt.xlabel('Index')
plt.ylabel('Value')
plt.ylim(-5, 5)
plt.legend()

# Plot for the second column
plt.subplot(2, 1, 2)
plt.plot(col4, label='Column 1', color='r')
plt.plot(col5, label='Column 2', color='g')
plt.plot(col6, label='Column 3', color='b')

for i in range(len(res)):
    plt.axvline(x=res[i][0], color='r', linestyle='--')
    plt.axvline(x=res[i][-1], color='g', linestyle='--')
plt.title('Line Plot for Column y')
plt.xlabel('Index')
plt.ylabel('Value')
plt.ylim(-2000, 2000)
plt.legend()


# Show the plots
plt.tight_layout()
plt.savefig('./img/'+ n +'_cut.png')
plt.show()