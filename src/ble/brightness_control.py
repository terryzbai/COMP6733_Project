import asyncio
from bluetooth_led import BluetoothLED

from known_devices import GOVEE_BULB_ADDRESS

async def main():
    async with BluetoothLED(GOVEE_BULB_ADDRESS) as led:
        await led.set_state(True)
        print("LED turned on.")
        print("Enter brightness value (0-100) or CTRL+C to exit:")

        while True:
            try:
                brightness = float(input('Brightness (0-100): '))
                if 0 <= brightness <= 100:
                    await led.set_brightness(brightness / 100)
                else:
                    print('Invalid brightness. Please enter a number between 0 and 100.')
            except KeyboardInterrupt:
                print('\nExiting...')
                break
            except ValueError:
                print('Invalid input. Please enter a valid number.')
asyncio.run(main())
