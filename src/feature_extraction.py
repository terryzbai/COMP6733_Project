import numpy as np

'''
Input:
    @data           array with size of (window_length, num_dimension)
Output:
    @result         float
'''
def ACEnergy(data):
    # Window size
    window_length = len(data)

    # FFT coefficients
    fft_coefficients = np.fft.fft(data)

    # Calculate magnitudes with the half of FFT (due to symmetry)
    half_fft = fft_coefficients[:window_length // 2]
    magnitudes = np.abs(half_fft)

    # Calculate ACEnergy
    result = (1 / (window_length / 2)) * np.sum(magnitudes ** 2)
    return result

'''
Input:
    @data           array with size of (window_length, num_dimension)
    @sampling_rate  integer
Output:
    @result         float
'''
def ACLowEnergy(data, sampling_rate):
    # FFT
    fft_coefficients = np.fft.fft(data)

    # Frequencies
    frequencies = np.linspace(0, sampling_rate, len(data))

    # Filter low frequencies
    low_freq_indices = np.where((frequencies >= 0) & (frequencies <= 1))

    # Calculate ACLowEnergy
    fft_low_freq = fft_coefficients[low_freq_indices]
    result = np.sum(np.abs(fft_low_freq) ** 2)
    return result

'''
Input:
    @data           array with size of (window_length, num_dimension)
Output:
    @result         vector with length of num_dimension
'''
def DCMean(data):
    DCMean_per_axis = np.mean(data, axis=0)
    return DCMean_per_axis


'''
Input:
    @data           array with size of (window_length, num_dimension)
Output:
    @result         float
'''
def DCTotalMean(data):
    result = np.sum(data) / len(data)
    return result

'''
Input:
    @data           array with size of (window_length, num_dimension)
Output:
    @result         float
'''
def DCArea(data, time, sampling_rate): 
    time_data = np.linspace(0, time, sampling_rate * time)

    result =  []
    for i in range(data.shape[1]):
        result.append(np.trapz(data[:, i], time_data))

    return result

'''

'''
def DCPostureDist(data):
    result = np.sqrt(np.mean(data**2))
    return result

def ACAbsMean(data):
    result = np.mean(np.abs(data))
    return result

def ACAbsArea(data, time, sampling_rate):
    time_data = np.linspace(0, time, sampling_rate * time)
    
    result =  []
    for i in range(data.shape[1]):
        result = np.trapz(np.abs(data[:, i]), time_data)

    return result


def ACTotalAbsArea(data):
    result = np.sum(np.abs(data))
    return result

def ACVar(data):
    ACVar_per_axis = np.var(data, axis=0)
    return ACVar_per_axis

def ACAbsCV(data):
    abs_mean = np.mean(np.abs(data))
    abs_std = np.std(np.abs(data))
    result = np.divide(abs_std, abs_mean, out=np.zeros_like(abs_mean), where=abs_mean != 0)
    return result

def ACIQR(data):
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    result = Q3 - Q1
    return result

def ACRange(data):
    result = np.max(data) - np.min(data)
    return result