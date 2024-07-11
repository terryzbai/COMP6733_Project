# Adapted from: https://github.com/chvolkmann/govee_btled

from enum import IntEnum
from bleak import BleakClient
from colour import Color

TEMP_TO_COLOUR = {
    1800: '#ff8200',
    1900: '#ff8700',
    2000: '#ff8d0b',
    2100: '#ff921d',
    2200: '#ff9829',
    2300: '#ff9d33',
    2400: '#ffa23c',
    2500: '#ffa645',
    2600: '#ffaa4d',
    2700: '#ffae54',
    2800: '#ffb25b',
    2900: '#ffb662',
    3000: '#ffb969',
    3100: '#ffbd6f',
    3200: '#ffc076',
    3300: '#ffc37c',
    3400: '#ffc682',
    3500: '#ffc987',
    3600: '#ffcb8d',
    3700: '#ffce92',
    3800: '#ffd097',
    3900: '#ffd39c',
    4000: '#ffd5a1',
    4100: '#ffd7a6',
    4200: '#ffd9ab',
    4300: '#ffdbaf',
    4400: '#ffddb4',
    4500: '#ffdfb8',
    4600: '#ffe1bc',
    4700: '#ffe2c0',
    4800: '#ffe4c4',
    4900: '#ffe5c8',
    5000: '#ffe7cc',
    5100: '#ffe8d0',
    5200: '#ffead3',
    5300: '#ffebd7',
    5400: '#ffedda',
    5500: '#ffeede',
    5600: '#ffefe1',
    5700: '#fff0e4',
    5800: '#fff1e7',
    5900: '#fff3ea',
    6000: '#fff4ed',
    6100: '#fff5f0',
    6200: '#fff6f3',
    6300: '#fff7f7',
    6400: '#fff8f8',
    6500: '#fff9fb',
    6600: '#fff9fd',
    6700: '#fefaff',
    6800: '#fcf8ff',
    6900: '#faf7ff',
    7000: '#f7f5ff',
    7100: '#f5f4ff',
    7200: '#f3f3ff',
    7300: '#f1f1ff',
    7400: '#eff0ff',
    7500: '#eeefff',
    7600: '#eceeff',
    7700: '#eaedff',
    7800: '#e9ecff',
    7900: '#e7eaff',
    8000: '#e5e9ff',
    8100: '#e4e9ff',
    8200: '#e3e8ff',
    8300: '#e1e7ff',
    8400: '#e0e6ff',
    8500: '#dfe5ff',
    8600: '#dde4ff',
    8700: '#dce3ff',
    8800: '#dbe2ff',
    8900: '#dae2ff',
    9000: '#d9e1ff'
}

UUID_CONTROL_CHARACTERISTIC = '00010203-0405-0607-0809-0A0B0C0D2B11'

def colour2rgb(colour):
    """
    Converts a colour-convertible into 3-tuple of 0-255 valued ints.
    """
    col = Color(colour)
    rgb = col.red, col.green, col.blue
    rgb = [round(x * 255) for x in rgb]
    return tuple(rgb)

class LedCommand(IntEnum):
    """
    A control command packet's type.
    """
    POWER       = 0x01
    BRIGHTNESS  = 0x04
    COLOUR      = 0x05

class LedMode(IntEnum):
    """
    The mode in which a colour change happens in.
    """
    COLOUR      = 0x0d
    WHITE       = 0x66

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
        """ Sends a command and handles payload padding. """
        if not isinstance(cmd, int):
            raise ValueError('Invalid command')
        if not isinstance(payload, bytes) and not (isinstance(payload, list) and all(isinstance(x, int) for x in payload)):
            raise ValueError('Invalid payload')
        if len(payload) > 17:
            raise ValueError('Payload too long')

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
        """ Controls the power state of the LED. """
        await self._send(LedCommand.POWER, [0x1 if onoff else 0x0])
    
    async def set_brightness(self, value):
        """
        Sets the LED's brightness.
        """
        if not 1 <= value <= 100:
            raise ValueError(f'Brightness out of range: {value}')
        await self._send(LedCommand.BRIGHTNESS, [value])
        
    async def set_colour(self, colour):
        """
        Sets the LED's colour.
        """
        await self._send(LedCommand.COLOUR, [LedMode.COLOUR, *colour2rgb(colour), 0x0])
    
    async def set_white_temperature(self, value):
        """
        Sets the LED's temperature in white-mode.
        """
        if not 1800 <= value <= 9000:
            raise ValueError(f'White value out of range: {value}')
        colour = TEMP_TO_COLOUR[value]
        
        # Set the colour to white (although ignored) and the boolean flag to True
        await self._send(LedCommand.COLOUR, [LedMode.WHITE, 0xff, 0xff, 0xff, 0x01, *colour2rgb(colour)])