import asyncio
from govee_h6004 import Govee_H6004

from known_devices import GOVEE_BULB_ADDRESS

async def main():
    async with Govee_H6004(GOVEE_BULB_ADDRESS) as led:
        await led.set_state(True)
        print("LED turned on.")
        print("Enter a colour HEX code (e.g. #FF0000) or CTRL+C to exit:")

        while True:
            try:
                colour = input('Colour value: ')
                await led.set_colour(colour)
            except KeyboardInterrupt:
                print('\nExiting...')
                break
            except ValueError:
                print('Invalid input. Please enter a valid colour.')
asyncio.run(main())
