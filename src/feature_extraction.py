import numpy as np


class GestureFeature:
    def __init__(self, data, sampling_rate):
        self.data = data
        self.sampling_rate = sampling_rate
        self.window_length = len(self.data)

        # FFT coefficients
        self.fft_coefficients = np.fft.fft(self.data)

    def ACEnergy(self):
        # Calculate magnitudes with the half of FFT (due to symmetry)
        half_fft = self.fft_coefficients[:self.window_length // 2]
        magnitudes = np.abs(half_fft)

        # Calculate ACEnergy
        result = (1 / (self.window_length / 2)) * np.sum(magnitudes ** 2)
        return np.array([result])

    def ACLowEnergy(self):
        # Frequencies
        frequencies = np.linspace(0, self.sampling_rate, len(self.data))

        # Filter low frequencies
        low_freq_indices = np.where((frequencies >= 0) & (frequencies <= 1))

        # Calculate ACLowEnergy
        fft_low_freq = self.fft_coefficients[low_freq_indices]
        result = np.sum(np.abs(fft_low_freq) ** 2)
        return np.array([result])

    def DCMean(self):
        DCMean_per_axis = np.mean(self.data, axis=0)
        return DCMean_per_axis

    def DCTotalMean(self):
        result = np.sum(self.data) / len(self.data)
        return np.array([result])

    def DCArea(self):
        time_data = np.linspace(0, len(self.data) / self.sampling_rate, len(self.data))

        result =  []
        for i in range(self.data.shape[1]):
            result.append(np.trapz(self.data[:, i], time_data))

        return result

    def DCPostureDist(self):
        result = np.sqrt(np.mean(self.data**2))
        return np.array([result])

    def ACAbsMean(self):
        result = np.mean(np.abs(self.data))
        return np.array([result])

    def ACAbsArea(self):
        time_data = np.linspace(0, len(self.data) / self.sampling_rate, len(self.data))

        result =  []
        for i in range(self.data.shape[1]):
            result = np.trapz(np.abs(self.data[:, i]), time_data)

            return np.array([result])

    def ACTotalAbsArea(self):
        result = np.sum(np.abs(self.data))
        return np.array([result])

    def ACVar(self):
        ACVar_per_axis = np.var(self.data, axis=0)
        return ACVar_per_axis

    def ACAbsCV(self):
        abs_mean = np.mean(np.abs(self.data))
        abs_std = np.std(np.abs(self.data))
        result = np.divide(abs_std, abs_mean, out=np.zeros_like(abs_mean), where=abs_mean != 0)
        return np.array([result])

    def ACIQR(self):
        Q1 = np.percentile(self.data, 25)
        Q3 = np.percentile(self.data, 75)
        result = Q3 - Q1
        return np.array([result])

    def ACRange_per_axis(self):
        result = np.max(self.data) - np.min(self.data)
        return np.array([result])
