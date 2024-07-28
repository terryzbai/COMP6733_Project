from ubluepy import Peripheral, Service, Characteristic, UUID
import uasyncio as asyncio

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
    if isinstance(colour, str) and colour.startswith("#") and len(colour) == 7:
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

    def __init__(self, mac):
        self.mac = mac
        self.device = None
        self.characteristic = None

    async def connect(self):
        p = Peripheral()
        p.connect(self.mac)
        control_svc = p.getServices()[2]
        control_wrt = control_svc.getCharacteristics()[1]

        self.device = p
        self.characteristic = control_wrt

    async def disconnect(self):
        self.device.disconnect()

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
        frame += bytes([0] * (19 - len(frame)))
        checksum = 0
        for b in frame:
            checksum ^= b
        frame += bytes([checksum & 0xFF])

        self.characteristic.write(frame)

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
        rgb = colour2rgb(colour)
        await self._send(COMMAND_COLOUR, [MODE_COLOUR, rgb[0], rgb[1], rgb[2], 0x0])

    # TODO: Complete white_temperature
    async def set_white_temperature(self, temperature):
        """
        Sets the LED's temperature in white-mode.
        """


async def test():
    mac = "60:74:F4:EC:C8:A9"
    blu = "EFA9751B-E8BE-FCAA-24CA-75130F3DD64E"
    led = Govee_H6004(mac)
    await led.connect()
    print("Switching on LED")
    await led.set_state(True)
    await asyncio.sleep(1)

    print("Changing colours in RGB")
    colours = [
        "#FF0000",  # Red
        "#00FF00",  # Green
        "#0000FF",  # Blue
    ]
    for colour in colours:
        print(f"[*] {colour}")
        await led.set_colour(colour)
        await asyncio.sleep(1)

    print("Changing brightness")
    for brightness in [100, 50, 1]:
        print(f"[*] {brightness}%")
        await led.set_brightness(brightness)
        await asyncio.sleep(1)

    print("Switching off LED")
    await led.set_state(False)
    await asyncio.sleep(1)

    await led.disconnect()


asyncio.run(test())
