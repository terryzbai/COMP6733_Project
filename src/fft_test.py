import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file
file_path = './data/dong.csv'
data = pd.read_csv(file_path)

# Extract columns
col1 = data.iloc[:, 0]
col2 = data.iloc[:, 1]
col3 = data.iloc[:, 2]

# Perform FFT
fft_col1 = np.fft.fft(col1)
fft_col2 = np.fft.fft(col2)
fft_col3 = np.fft.fft(col3)

# Compute frequencies
freq = np.fft.fftfreq(len(col1))

# Create a new figure for the FFT plots
plt.figure(figsize=(15, 10))

# Plot FFT for the first column
plt.subplot(3, 1, 1)
plt.plot(freq, np.abs(fft_col1), label='FFT of Column 1', color='b')
plt.title('FFT of Column 1')
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.legend()

# Plot FFT for the second column
plt.subplot(3, 1, 2)
plt.plot(freq, np.abs(fft_col2), label='FFT of Column 2', color='g')
plt.title('FFT of Column 2')
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.legend()

# Plot FFT for the third column
plt.subplot(3, 1, 3)
plt.plot(freq, np.abs(fft_col3), label='FFT of Column 3', color='r')
plt.title('FFT of Column 3')
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.legend()

# Adjust layout
plt.tight_layout()

# Save the figure
output_path = './img/fft_plots.png'
plt.savefig(output_path)

# Show the plot
plt.show()

# Print the file path
print(f'FFT plot saved to {output_path}')
