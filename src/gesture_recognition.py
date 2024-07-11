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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

sampling_rate = 100
min_gus_time = 30
max_gus_time = 200
thredhold = 500
mang_change = 70

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
        gf.ACRange_per_axis(),
        np.array([len(data)])
    ))
    return features

def extract_gesture_clip(filepath):
    res = []
    temp_data = []
    flag = False

    data = pd.read_csv(filepath).to_numpy()
    col4 = data[:, 3]
    col5 = data[:, 4]
    col6 = data[:, 5]
    gyo  = col4**2 + col5**2 + col6**2

    for i in range(1,len(data)):
        if gyo[i] < thredhold and np.abs(gyo[i] - gyo[i-1]) < mang_change:
            if flag == True and min_gus_time <len(temp_data) < max_gus_time :
                res.append(np.array(temp_data))
            flag = False
            temp_data = []
        else:
            flag = True
            temp_data.append(data[i])

    return res

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

            # Extract gesture clip
            gesture_clips = extract_gesture_clip(file_path)
            print(f"number of useful clips in {file_name}: {len(gesture_clips)}")

            for gesture_clip in gesture_clips:
                features = getFeatures(gesture_clip)
                x.append(features)
                y.append(int(gesture_id))

        else:
            continue

    return np.array(x), np.array(y)

X, y = getDataset('./tb_data')
print(f"X shape:, {X.shape}")

# Get unique values and their counts
labels, counts = np.unique(y, return_counts=True)

# Print unique values and their counts
for label, count in zip(labels, counts):
    print(f'Value: {label}, Count: {count}')
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#--------------------------------------------------
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

#--------------------------------------------------
neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X_train, y_train)
y_pred = neigh.predict(X_test)
print(y_pred)
print(y_test)
print(neigh.predict_proba(X_test))

# Evaluate the classifier
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

#--------------------------------------------------
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)
# Make predictions
y_pred = clf.predict(X_test)
print(y_pred)
print(y_test)

# Evaluate the classifier
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

#--------------------------------------------------
clf = LogisticRegression(random_state=0)
clf.fit(X_train, y_train)
# Make predictions
y_pred = clf.predict(X_test)
print(y_pred)
print(y_test)
print(clf.predict_proba(X_test))

# Evaluate the classifier
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))
