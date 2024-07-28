from bleak import BleakClient

UUID_CONTROL_CHARACTERISTIC = "00010203-0405-0607-0809-0A0B0C0D2B11"

# A command packet's type
COMMAND_POWER = 0x01
COMMAND_BRIGHTNESS = 0x04
COMMAND_COLOUR = 0x05

# The mode in which a colour change happens in.
MODE_COLOUR = 0x0D
MODE_WHITE = 0x66


def colour2rgb(colour):
    """
    Converts a hex colour string into a 3-tuple of 0-255 valued ints.
    """
    # Ensure the input is a string and starts with a '#'
    if isinstance(colour, str) and colour.startswith("#") and len(colour) == 7:
        # Convert the hex string to RGB components
        r = int(colour[1:3], 16)
        g = int(colour[3:5], 16)
        b = int(colour[5:7], 16)
        return (r, g, b)
    else:
        raise ValueError("Invalid input. Please use a hex colour string.")


class Govee_H6004:
    """
    Bluetooth client for Govee's RGB LED H6004.
    """

    def __init__(self, mac, bt_backend_cls=BleakClient):
        self.mac = mac
        self._bt = bt_backend_cls(self.mac)
        self._dev = None

    async def __aenter__(self):
        await self._bt.connect()
        self._dev = self._bt
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._bt.disconnect()
        self._dev = None

    async def _send(self, cmd, payload):
        """
        Sends a command and handles payload padding.
        """
        if not isinstance(cmd, int):
            raise ValueError("Invalid command")
        if not isinstance(payload, bytes) and not (
            isinstance(payload, list) and all(isinstance(x, int) for x in payload)
        ):
            raise ValueError("Invalid payload")
        if len(payload) > 17:
            raise ValueError("Payload too long")

        frame = bytes([0x33, cmd]) + bytes(payload)
        # pad frame data to 19 bytes (plus checksum)
        frame += bytes([0] * (19 - len(frame)))

        # The checksum is calculated by XORing all data bytes
        checksum = 0
        for b in frame:
            checksum ^= b

        frame += bytes([checksum & 0xFF])

        # TODO: Remove command being printed
        # hex_bytes = [f'{byte:02x}' for byte in frame]
        # frame_str = f"{hex_bytes[0]} {hex_bytes[1]} {hex_bytes[2]} {hex_bytes[3]}{hex_bytes[4]}{hex_bytes[5]} {hex_bytes[6]} {hex_bytes[7]}{hex_bytes[8]}{hex_bytes[9]} {' '.join(hex_bytes[10:19])} {hex_bytes[19]}"
        # print(f"Sending command: {frame_str}")

        await self._dev.write_gatt_char(UUID_CONTROL_CHARACTERISTIC, frame)

    async def set_state(self, onoff):
        """
        Controls the power state of the LED.
        """
        await self._send(COMMAND_POWER, [0x1 if onoff else 0x0])

    async def set_brightness(self, value):
        """
        Sets the LED's brightness.
        """
        if not 1 <= value <= 100:
            raise ValueError(f"Brightness out of range: {value}")
        await self._send(COMMAND_BRIGHTNESS, [value])

    async def set_colour(self, colour):
        """
        Sets the LED's colour.
        """
        await self._send(COMMAND_COLOUR, [MODE_COLOUR, *colour2rgb(colour), 0x0])

    # TODO: Complete white_temperature
    async def set_white_temperature(self, temperature):
        """
        Sets the LED's temperature in white-mode.
        """
