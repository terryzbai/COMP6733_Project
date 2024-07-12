import subprocess

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

        # Capture and process the output in real-time
        with process.stdout as pipe:
            for line in pipe:
                process_output(line.strip())

        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, process.args, output=process.stdout, stderr=process.stderr)

    except Exception as e:
        print(f"Error: {e}")

def process_output(output):
    # This function can be customized to process the output as needed
    print(f"Captured output: {output}")


if __name__ == "__main__":
    port = '/dev/cu.usbmodem0000000000001'  # Replace with the correct port for your system
    filepath = 'src/record_data.py'  # Path to your Python script

    run_micropython_script(port, filepath)
