import pandas as pd
import matplotlib.pyplot as plt

n = 'tb_woquan'

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

plt.figure(figsize=(15, 8))

# Plot for the first column
plt.subplot(2, 1, 1)
plt.plot(range(0,len(col1)*10,10), col1, color='r')
plt.plot(range(0,len(col1)*10,10), col2, color='g')
plt.plot(range(0,len(col1)*10,10), col3, color='b')


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


plt.title(' Gyroscope ', fontsize=24)
plt.xlabel('Time(ms)', fontsize=24)
plt.ylabel('Value(dps)', fontsize=24)
plt.ylim(-2000, 2000)
plt.legend()

# Show the plots
plt.tight_layout()
plt.savefig('./img/'+ n +'.png')
plt.show()
