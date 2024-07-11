import asyncio
from govee_h6004 import Govee_H6004

from known_devices import GOVEE_BULB_ADDRESS

async def main():
    async with Govee_H6004(GOVEE_BULB_ADDRESS) as led:
        await led.set_state(True)
        print("LED turned on.")
        print("Enter brightness value (1-100) or CTRL+C to exit:")

        while True:
            try:
                brightness = int(input('Brightness (1-100): '))
                if 1 <= brightness <= 100:
                    await led.set_brightness(brightness)
                else:
                    print('Invalid brightness. Please enter a number between 1 and 100.')
            except KeyboardInterrupt:
                print('\nExiting...')
                break
            except ValueError:
                print('Invalid input. Please enter a valid number.')
asyncio.run(main())
