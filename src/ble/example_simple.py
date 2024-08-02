import asyncio
from govee_h6004 import Govee_H6004

from known_devices import GOVEE_BULB_ADDRESS


# Example usage
async def main():
    led = Govee_H6004(GOVEE_BULB_ADDRESS)
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


asyncio.run(main())
