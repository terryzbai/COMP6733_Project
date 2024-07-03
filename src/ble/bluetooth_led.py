# Adapted from: https://github.com/chvolkmann/govee_btled

from enum import IntEnum
from bleak import BleakClient
from colour import Color

SHADES_OF_WHITE = [
    '#ff8d0b',
    '#ff8912',
    '#ff921d',
    '#ff8e21',
    '#ff9829',
    '#ff932c',
    '#ff9d33',
    '#ff9836',
    '#ffa23c',
    '#ff9d3f',
    '#ffa645',
    '#ffa148',
    '#ffaa4d',
    '#ffa54f',
    '#ffae54',
    '#ffa957',
    '#ffb25b',
    '#ffad5e',
    '#ffb662',
    '#ffb165',
    '#ffb969',
    '#ffb46b',
    '#ffbd6f',
    '#ffb872',
    '#ffc076',
    '#ffbb78',
    '#ffc37c',
    '#ffbe7e',
    '#ffc682',
    '#ffc184',
    '#ffc987',
    '#ffc489',
    '#ffcb8d',
    '#ffc78f',
    '#ffce92',
    '#ffc994',
    '#ffd097',
    '#ffcc99',
    '#ffd39c',
    '#ffce9f',
    '#ffd5a1',
    '#ffd1a3',
    '#ffd7a6',
    '#ffd3a8',
    '#ffd9ab',
    '#ffd5ad',
    '#ffdbaf',
    '#ffd7b1',
    '#ffddb4',
    '#ffd9b6',
    '#ffdfb8',
    '#ffdbba',
    '#ffe1bc',
    '#ffddbe',
    '#ffe2c0',
    '#ffdfc2',
    '#ffe4c4',
    '#ffe1c6',
    '#ffe5c8',
    '#ffe3ca',
    '#ffe7cc',
    '#ffe4ce',
    '#ffe8d0',
    '#ffe6d2',
    '#ffead3',
    '#ffe8d5',
    '#ffebd7',
    '#ffe9d9',
    '#ffedda',
    '#ffebdc',
    '#ffeede',
    '#ffece0',
    '#ffefe1',
    '#ffeee3',
    '#fff0e4',
    '#ffefe6',
    '#fff1e7',
    '#fff0e9',
    '#fff3ea',
    '#fff2ec',
    '#fff4ed',
    '#fff3ef',
    '#fff5f0',
    '#fff4f2',
    '#fff6f3',
    '#fff5f5',
    '#fff7f7',
    '#fff6f8',
    '#fff8f8',
    '#fff8fb',
    '#fff9fb',
    '#fff9fd',
    '#fff9fd',
    '#fef9ff',
    '#fefaff',
    '#fcf7ff',
    '#fcf8ff',
    '#f9f6ff',
    '#faf7ff',
    '#f7f5ff',
    '#f7f5ff',
    '#f5f3ff',
    '#f5f4ff',
    '#f3f2ff',
    '#f3f3ff',
    '#f0f1ff',
    '#f1f1ff',
    '#eff0ff',
    '#eff0ff',
    '#edefff',
    '#eeefff',
    '#ebeeff',
    '#eceeff',
    '#e9edff',
    '#eaedff',
    '#e7ecff',
    '#e9ecff',
    '#e6ebff',
    '#e7eaff',
    '#e4eaff',
    '#e5e9ff',
    '#e3e9ff',
    '#e4e9ff',
    '#e1e8ff',
    '#e3e8ff',
    '#e0e7ff',
    '#e1e7ff',
    '#dee6ff',
    '#e0e6ff',
    '#dde6ff',
    '#dfe5ff',
    '#dce5ff',
    '#dde4ff',
    '#dae4ff',
    '#dce3ff',
    '#d9e3ff',
    '#dbe2ff',
    '#d8e3ff',
    '#dae2ff',
    '#d7e2ff',
    '#d9e1ff',
    '#d6e1ff'
]

UUID_CONTROL_CHARACTERISTIC = '00010203-0405-0607-0809-0A0B0C0D2B11'

def color2rgb(color):
    """ Converts a color-convertible into 3-tuple of 0-255 valued ints. """
    col = Color(color)
    rgb = col.red, col.green, col.blue
    rgb = [round(x * 255) for x in rgb]
    return tuple(rgb)

class LedCommand(IntEnum):
    """ A control command packet's type. """
    POWER      = 0x01
    BRIGHTNESS = 0x04
    COLOR      = 0x05

class LedMode(IntEnum):
    """
    The mode in which a color change happens in.
    
    Currently only manual is supported.
    """
    MANUAL     = 0x02
    MICROPHONE = 0x06
    SCENES     = 0x05

class BluetoothLED:
    """ Bluetooth client for Govee's RGB LED H6001. """
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

        cmd = cmd & 0xFF
        payload = bytes(payload)

        frame = bytes([0x33, cmd]) + bytes(payload)
        # pad frame data to 19 bytes (plus checksum)
        frame += bytes([0] * (19 - len(frame)))
        
        # The checksum is calculated by XORing all data bytes
        checksum = 0
        for b in frame:
            checksum ^= b
        
        frame += bytes([checksum & 0xFF])
        await self._dev.write_gatt_char(UUID_CONTROL_CHARACTERISTIC, frame)
    
    async def set_state(self, onoff):
        """ Controls the power state of the LED. """
        await self._send(LedCommand.POWER, [0x1 if onoff else 0x0])
    
    async def set_brightness(self, value):
        """
        Sets the LED's brightness.
        
        `value` must be a value between 0.0 and 1.0
        """
        if not 0 <= float(value) <= 1:
            raise ValueError(f'Brightness out of range: {value}')
        value = round(value * 0xFF)
        await self._send(LedCommand.BRIGHTNESS, [value])
        
    async def set_color(self, color):
        """
        Sets the LED's color.
        
        `color` must be a color-convertible (see the `colour` library),
        e.g. 'red', '#ff0000', etc.
        """
        await self._send(LedCommand.COLOR, [LedMode.MANUAL, *color2rgb(color)])
    
    async def set_color_white(self, value):
        """
        Sets the LED's color in white-mode.

        `value` must be a value between -1.0 and 1.0
        White mode seems to enable a different set of LEDs within the bulb.
        This method uses the hardcoded RGB values of whites, directly taken from
        the mechanism used in Govee's app.
        """
        if not -1 <= value <= 1:
            raise ValueError(f'White value out of range: {value}')
        value = (value+1) / 2 # in [0.0, 1.0]
        index = round(value * (len(SHADES_OF_WHITE)-1))
        white = Color(SHADES_OF_WHITE[index])
        
        # Set the color to white (although ignored) and the boolean flag to True
        await self._send(LedCommand.COLOR, [LedMode.MANUAL, 0xff, 0xff, 0xff, 0x01, *color2rgb(white)])