import platform

GOVEE_BULB_ADDRESS = (
    # MAC address on Linux/Windows
    "60:74:F4:EC:C8:A9"
    if platform.system() != "Darwin"
    else "EFA9751B-E8BE-FCAA-24CA-75130F3DD64E"
    # Bluetooth address on macOS
)
