import pandas as pd
import feature_extraction

# Load the CSV file
file_path = './data/move_1s.csv'
data = pd.read_csv(file_path, header=None).to_numpy()

sampling_rate = 100

ACEnergy = feature_extraction.ACEnergy(data)
print(f"Calculated ACEnergy: {ACEnergy}")

ACLowEnergy = feature_extraction.ACLowEnergy(data, sampling_rate)
print(f"Calculated ACLowEnergy: {ACLowEnergy}")

DCMean = feature_extraction.DCMean(data)
print(f"Calculated DCMean: {DCMean}")

DCTotalMean = feature_extraction.DCTotalMean(data)
print(f"Calculated DCTotalMean: {DCTotalMean}")

DCArea = feature_extraction.DCArea(data, 1, sampling_rate)
print(f"Calculated DCArea: {DCArea}")

DCPostureDist = feature_extraction.DCPostureDist(data)
print(f"Calculated DCPostureDist (RMS of the accelerometer data): {DCPostureDist}")

ACAbsMean = feature_extraction.ACAbsMean(data)
print(f"Calculated ACAbsMean: {ACAbsMean}")

ACAbsArea = feature_extraction.ACAbsArea(data, 1, sampling_rate)
print(f"Calculated ACAbsArea: {ACAbsArea}")

ACTotalAbsArea = feature_extraction.ACTotalAbsArea(data)
print(f"Calculated ACTotalAbsArea: {ACTotalAbsArea}")

ACVar = feature_extraction.ACVar(data)
print(f"Calculated ACVar: {ACVar}")

ACAbsCV = feature_extraction.ACAbsCV(data)
print(f"Calculated ACAbsCV: {ACAbsCV}")

ACIQR = feature_extraction.ACIQR(data)
print(f"Calculated ACIQR: {ACIQR}")

ACRange_per_axis = feature_extraction.ACRange(data)
print(f"Calculated ACRange per axis: {ACRange_per_axis}")