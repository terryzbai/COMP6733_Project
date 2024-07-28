import subprocess
import joblib
import numpy as np
from feature_extraction import GestureFeature

sampling_rate = 100
min_gus_time = 25
max_gus_time = 200
thredhold = 500
mang_change = 70

# 假设 X_test 已经定义
# 加载模型
clf = joblib.load('./model/vf.pkl')

# 进行预测
# y_pred = clf.predict(X_test)

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

def gyo(data):
    return data[3]**2 + data[4]**2 + data[5]**2

def run_micropython_script(port, filepath):
    try:
        print("run script...")
        # Run the MicroPython script using ampy
        process = subprocess.Popen(
            ["ampy", "--port", port, "run", filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        guesture_cut = []
        flag = False
        # Capture and process the output in real-time
        with process.stdout as pipe:
            for line in pipe:
                # print(line.strip())
                data = line.strip().split(',')
                data = [float(x) for x in data]
                # print(data)
                if guesture_cut == []:
                    guesture_cut.append(data)
                else:
                    current_gyo = gyo(data)
                    
                    if current_gyo < thredhold and np.abs(gyo(guesture_cut[-1]) - current_gyo) < mang_change:
                        if flag == True and min_gus_time <len(guesture_cut) < max_gus_time :
                            guesture_cut = np.array(guesture_cut)
                            features = getFeatures(guesture_cut)
                            
                            y_pred = clf.predict([features])
                            print('guesture number is:',y_pred)
                        flag = False
                        guesture_cut = []
                    else:
                        flag = True
                        guesture_cut.append(data)


        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, process.args, output=process.stdout, stderr=process.stderr)

    except Exception as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    port = '/dev/cu.usbmodem0000000000001'  # Replace with the correct port for your system
    filepath = 'src/record_data.py'  # Path to your Python script

    run_micropython_script(port, filepath)
