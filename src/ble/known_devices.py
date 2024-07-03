import platform

GOVEE_BULB_ADDRESS = (
    # Bluetooth address on Linux/Windows
    "..."
    if platform.system() != "Darwin"
    else "EFA9751B-E8BE-FCAA-24CA-75130F3DD64E"
    # MAC address on macOS
)
