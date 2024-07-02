import numpy as np
import pandas as pd
import feature_extraction

# Load the CSV file
file_path = '../data/move_1s.csv'
data = pd.read_csv(file_path, header=None).to_numpy()

sampling_rate = 100

ACEnergy = feature_extraction.ACEnergy(data)
ACLowEnergy = feature_extraction.ACLowEnergy(data, sampling_rate)
DCMean = feature_extraction.DCMean(data)
DCTotalMean = feature_extraction.DCTotalMean(data)
DCArea = feature_extraction.DCArea(data, 1, sampling_rate)
DCPostureDist = feature_extraction.DCPostureDist(data)
ACAbsMean = feature_extraction.ACAbsMean(data)
ACAbsArea = feature_extraction.ACAbsArea(data, 1, sampling_rate)
ACTotalAbsArea = feature_extraction.ACTotalAbsArea(data)
ACVar = feature_extraction.ACVar(data)
ACAbsCV = feature_extraction.ACAbsCV(data)
ACIQR = feature_extraction.ACIQR(data)
ACRange_per_axis = feature_extraction.ACRange(data)

features = np.concatenate((ACEnergy, ACLowEnergy, DCMean, DCTotalMean, DCArea, DCPostureDist,
                     ACAbsMean, ACAbsArea, ACTotalAbsArea, ACVar, ACAbsCV, ACIQR,
                     ACRange_per_axis))

print(f"Combined features: {features}")
