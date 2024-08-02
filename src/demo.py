import asyncio
import subprocess
import joblib
import numpy as np
from feature_extraction import GestureFeature

from ble.govee_h6004 import Govee_H6004
from ble.known_devices import GOVEE_BULB_ADDRESS


# Configuration
SAMPLING_RATE = 100
MIN_GESTURE_TIME = 25
MAX_GESTURE_TIME = 200
GYRO_THRESHOLD = 500
GYRO_CHANGE_THRESHOLD = 70
GESTURES = {1: "Snap", 2: "Clockwise", 3: "Counterclockwise", 4: "Up", 5: "Down"}

# Load the pre-trained machine learning model
clf = joblib.load("./model/rf_73.pkl")

# 6 value RGB colour wheel
RGB_WHEEL = ["#FF0000", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#FF00FF"]


class Lightbulb:
    def __init__(self, mac):
        self.led = Govee_H6004(mac)
        self.power = True
        self.colour = "#FF0000"
        self.colour_index = 0
        self.brightness = 100

    async def connect(self):
        await self.led.connect()
        await self.reset()

    async def disconnect(self):
        await self.led.disconnect()

    async def set_colour(self, colour):
        if colour in RGB_WHEEL:
            await self.led.set_colour(colour)
            self.colour = colour
            self.colour_index = RGB_WHEEL.index(colour)
        else:
            raise ValueError("Colour not in RGB wheel")

    async def set_brightness(self, brightness):
        if 1 <= brightness <= 100:
            await self.led.set_brightness(brightness)
            self.brightness = brightness
        else:
            raise ValueError("Brightness must be between 1 and 100")

    async def set_power(self, state):
        await self.led.set_state(state)
        self.power = state

    async def reset(self):
        await self.set_power(True)
        await self.set_colour(RGB_WHEEL[0])
        await self.set_brightness(100)

    async def toggle_power(self):
        new_state = not self.power
        await self.led.set_state(new_state)
        self.power = new_state

    async def next_colour(self):
        current_index = RGB_WHEEL.index(self.colour) if self.colour in RGB_WHEEL else 0
        next_index = (current_index + 1) % len(RGB_WHEEL)
        new_colour = RGB_WHEEL[next_index]
        await self.led.set_colour(new_colour)
        self.colour = new_colour
        self.colour_index = next_index

    async def previous_colour(self):
        current_index = RGB_WHEEL.index(self.colour) if self.colour in RGB_WHEEL else 0
        prev_index = (current_index - 1) % len(RGB_WHEEL)
        new_colour = RGB_WHEEL[prev_index]
        await self.led.set_colour(new_colour)
        self.colour = new_colour
        self.colour_index = prev_index

    async def increase_brightness(self):
        new_brightness = min(self.brightness + 20, 100)
        await self.led.set_brightness(new_brightness)
        self.brightness = new_brightness

    async def decrease_brightness(self):
        new_brightness = max(self.brightness - 20, 0)
        await self.led.set_brightness(new_brightness)
        self.brightness = new_brightness


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


async def gesture_to_control(gesture_id, lightbulb):
    if gesture_id == 1:
        await lightbulb.toggle_power()
    elif gesture_id == 2:
        await lightbulb.next_colour()
    elif gesture_id == 3:
        await lightbulb.previous_colour()
    elif gesture_id == 4:
        await lightbulb.increase_brightness()
    elif gesture_id == 5:
        await lightbulb.decrease_brightness()
    else:
        print(f"Unknown gesture_id: {gesture_id}")


async def main():
    """
    Runs the MicroPython script on the Arduino and process the output data.
    """
    print("Beginning demo...")
    try:
        # Run the MicroPython script using ampy
        port = "/dev/cu.usbmodem0000000000001"  # USB Port of the Arduino
        filepath = "src/demo_arduino.py"  # Path to MicroPython script
        process = subprocess.Popen(
            ["ampy", "--port", port, "run", filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        print("Script running on Arduino")

        gesture_data = []
        gesture_in_progress = False

        # Initialise the lightbulb
        led = Lightbulb(GOVEE_BULB_ADDRESS)
        await led.connect()
        print("Lightbulb initialised")

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
                                await gesture_to_control(predicted_gesture_id, led)

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
    except KeyboardInterrupt:
        print("Interrupted by user, stopping...")
        process.terminate()  # Terminate the subprocess
        process.wait()  # Wait for subprocess to terminate

    except Exception as e:
        print(f"Error: {e}")


asyncio.run(main())
