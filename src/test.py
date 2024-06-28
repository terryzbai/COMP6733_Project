import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import feature_extraction

# Load the CSV file
file_path = '../data/dong.csv'
data = pd.read_csv(file_path)

accel_data = data

window_length = len(accel_data)
sampling_rate = 100

fft_coefficients = np.fft.fft(accel_data)

half_fft = fft_coefficients[:window_length // 2]

magnitudes = np.abs(half_fft)

ACEnergy = feature_extraction.ACEnergy(window_length, magnitudes)

print(f"Calculated ACEnergy: {ACEnergy}")

frequencies = np.linspace(0, sampling_rate, window_length)
plt.plot(frequencies, np.abs(np.fft.fft(accel_data)))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('FFT Amplitude Spectrum')
plt.show()