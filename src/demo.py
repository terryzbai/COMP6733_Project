import subprocess
import joblib
import numpy as np
from feature_extraction import GestureFeature

# Configuration
SAMPLING_RATE = 100
MIN_GESTURE_TIME = 25
MAX_GESTURE_TIME = 200
GYRO_THRESHOLD = 500
GYRO_CHANGE_THRESHOLD = 70
GESTURES = {1: "Snap", 2: "Clockwise", 3: "Counterclockwise", 4: "Up", 5: "Down"}

# Load the pre-trained machine learning model
clf = joblib.load("./model/rf.pkl")


def extract_features(data):
    """
    Extracts features from the input data
    """
    gf = GestureFeature(data, SAMPLING_RATE)
    features = np.concatenate(
        [
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
            np.array([len(data)]),
        ]
    )
    return features


def calculate_gyroscope_magnitude(data):
    """
    Calculates the sum of the squared magnitudes of the gyroscope data
    """
    return data[3] ** 2 + data[4] ** 2 + data[5] ** 2


def main():
    """
    Runs the MicroPython script on the Arduino and process the output data.
    """
    try:
        print("Running script...")
        # Run the MicroPython script using ampy
        port = "/dev/cu.usbmodem0000000000001"  # USB Port of the Arduino
        filepath = "src/record_data.py"  # Path to MicroPython script
        process = subprocess.Popen(
            ["ampy", "--port", port, "run", filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        gesture_data = []
        gesture_in_progress = False

        with process.stdout as pipe:
            for line in pipe:
                try:
                    # Parse the incoming data
                    data = list(map(float, line.strip().split(",")))

                    if not gesture_data:
                        gesture_data.append(data)
                    else:
                        current_gyro_magnitude = calculate_gyroscope_magnitude(data)
                        last_gyro_magnitude = calculate_gyroscope_magnitude(
                            gesture_data[-1]
                        )

                        if (
                            current_gyro_magnitude < GYRO_THRESHOLD
                            and abs(last_gyro_magnitude - current_gyro_magnitude)
                            < GYRO_CHANGE_THRESHOLD
                        ):

                            if (
                                gesture_in_progress
                                and MIN_GESTURE_TIME
                                < len(gesture_data)
                                < MAX_GESTURE_TIME
                            ):
                                features = extract_features(np.array(gesture_data))
                                predicted_gesture_id = int(clf.predict([features])[0])
                                predicted_gesture = GESTURES[predicted_gesture_id]
                                print(
                                    f"Detected {predicted_gesture} ({predicted_gesture_id})"
                                )

                            gesture_in_progress = False
                            gesture_data = []
                        else:
                            gesture_in_progress = True
                            gesture_data.append(data)
                except ValueError:
                    print("Warning: Received malformed data:", line.strip())

        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode,
                process.args,
                output=process.stdout,
                stderr=process.stderr,
            )

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
