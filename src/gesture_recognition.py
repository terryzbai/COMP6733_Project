import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from feature_extraction import GestureFeature
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestCentroid
from sklearn.metrics import classification_report, accuracy_score

sampling_rate = 100

def getFeatures(data):
    gf = GestureFeature(data, sampling_rate)

    features = np.concatenate((
        gf.ACEnergy(),
        gf.ACLowEnergy(),
        gf.DCMean(),
        gf.DCTotalMean(),
        gf.DCArea(),
        gf.DCPostureDist(),
        gf.ACAbsMean(),
        gf.ACAbsArea(),
        gf.ACTotalAbsArea(),
        gf.ACVar(),
        gf.ACAbsCV(),
        gf.ACIQR(),
        gf.ACRange_per_axis()
    ))
    return features

def getDataset(dataset_path):
    # Load the CSV file
    file_names = os.listdir(dataset_path)
    x = []
    y = []

    for file_name in file_names:
        file_path = os.path.join(dataset_path, file_name)

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
        x.append(features)
        y.append(int(gesture_id))

    return np.array(x), np.array(y)

X, y = getDataset('./noise_data')
print(X)
print(X.shape)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create and train the Nearest Centroid classifier
clf = NearestCentroid()
clf.fit(X_train, y_train)

# Predict the labels for the test set
y_pred = clf.predict(X_test)
print(y_pred)
print(y_test)

# Evaluate the classifier
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

