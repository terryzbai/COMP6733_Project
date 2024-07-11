import asyncio
from govee_h6004 import Govee_H6004

from known_devices import GOVEE_BULB_ADDRESS


# Example usage
async def main():
    async with Govee_H6004(GOVEE_BULB_ADDRESS) as led:
        print('Switching on LED')
        await led.set_state(True)
        await asyncio.sleep(.5)

        print('Changing colours in RGB')
        colours = [
            '#FF0000',   # Red
            '#FF7F00',   # Orange
            '#FFFF00',   # Yellow
            '#7FFF00',   # Lime
            '#00FF00',   # Green
            '#00FF7F',   # Spring Green
            '#00FFFF',   # Cyan
            '#007FFF',   # Azure
            '#0000FF',   # Blue
            '#7F00FF',   # Violet
            '#FF00FF',   # Magenta
            '#FF007F'    # Rose
        ]
        for colour in colours:
            print(f'[*] {colour}')
            await led.set_colour(colour)
            await asyncio.sleep(1)

        print('Changing brightness')
        for brightness in [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
            print(f'[*] {brightness}%')
            await led.set_brightness(brightness)
            await asyncio.sleep(1)

        # TODO: Complete white temperature functionality
        # print('Changing temperature in white-mode')
        # for i in range(18, 90):
        #     val = i*100
        #     print(f'[*] white-temperature: {val}')
        #     await led.set_white_temperature(val)
        #     await asyncio.sleep(.2)

        print('Switching off LED')
        await led.set_state(False)

asyncio.run(main())
