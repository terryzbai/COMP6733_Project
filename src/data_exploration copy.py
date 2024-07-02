import pandas as pd
import matplotlib.pyplot as plt

n = 'yc_01_001'

# Load the CSV file
file_path = './data/'+ n +'.csv'
data = pd.read_csv(file_path)

# Display the dataframe to understand its structure
data.head()

# Extract columns
col1 = data.iloc[:, 0]
col2 = data.iloc[:, 1]
col3 = data.iloc[:, 2]

# Plot the data
plt.figure(figsize=(15, 10))

# Plot for the first column
plt.subplot(3, 1, 1)
plt.plot(col1, label='Column 1', color='b')
plt.title('Line Plot for Column x')
plt.xlabel('Index')
plt.ylabel('Value')
plt.ylim(-5, 5)
plt.legend()

# Plot for the second column
plt.subplot(3, 1, 2)
plt.plot(col2, label='Column 2', color='g')
plt.title('Line Plot for Column y')
plt.xlabel('Index')
plt.ylabel('Value')
plt.ylim(-5, 5)
plt.legend()

# Plot for the third column
plt.subplot(3, 1, 3)
plt.plot(col3, label='Column 3', color='r')
plt.title('Line Plot for Column z')
plt.xlabel('Index')
plt.ylabel('Value')
plt.ylim(-5, 5)
plt.legend()

# Show the plots
plt.tight_layout()
plt.savefig('./img/'+ n +'.png')
plt.show()