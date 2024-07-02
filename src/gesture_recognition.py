import os
import re
import numpy as np
import pandas as pd
import feature_extraction

sampling_rate = 100

def getFeatures(data):
    ACEnergy = feature_extraction.ACEnergy(data)
    ACLowEnergy = feature_extraction.ACLowEnergy(data, sampling_rate)
    DCMean = feature_extraction.DCMean(data)
    DCTotalMean = feature_extraction.DCTotalMean(data)
    DCArea = feature_extraction.DCArea(data, sampling_rate)
    DCPostureDist = feature_extraction.DCPostureDist(data)
    ACAbsMean = feature_extraction.ACAbsMean(data)
    ACAbsArea = feature_extraction.ACAbsArea(data, sampling_rate)
    ACTotalAbsArea = feature_extraction.ACTotalAbsArea(data)
    ACVar = feature_extraction.ACVar(data)
    ACAbsCV = feature_extraction.ACAbsCV(data)
    ACIQR = feature_extraction.ACIQR(data)
    ACRange_per_axis = feature_extraction.ACRange(data)

    features = np.concatenate((ACEnergy, ACLowEnergy, DCMean, DCTotalMean, DCArea, DCPostureDist,
                               ACAbsMean, ACAbsArea, ACTotalAbsArea, ACVar, ACAbsCV, ACIQR,
                               ACRange_per_axis))
    return features

# Load the CSV file
data_dir = './data'
file_names = os.listdir('./data/')

for file_name in file_names:
    file_path = os.path.join(data_dir, file_name)

    pattern = r"(?P<experimenter_id>\w+)_(?P<gesture_id>\w+)_(?P<sample_id>\w+)\.csv"
    match = re.match(pattern, file_name)
    if match:
        # Extract the parameters using named groups
        experimenter_id = match.group("experimenter_id")
        gesture_id = match.group("gesture_id")
        sample_id = match.group("sample_id")
        params = {
            "experimenter_id": experimenter_id,
            "gesture_id": int(gesture_id),
            "sample_id": int(sample_id)
        }
        print(params)
    else:
        continue

    data = pd.read_csv(file_path, header=None).to_numpy()
    features = getFeatures(data)
    print(f"{file_path}-{gesture_id}: {features}")
