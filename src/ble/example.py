import asyncio
from bluetooth_led import BluetoothLED

from known_devices import GOVEE_BULB_ADDRESS


# Example usage
# NOTE: Not all functionalities are properly fully working
async def main():
    async with BluetoothLED(GOVEE_BULB_ADDRESS) as led:
        print('Switching on LED')
        await led.set_state(True)
        await asyncio.sleep(.5)

        print('Changing colors in RGB')
        for color in ['red', 'green', 'blue', 'purple', 'yellow', 'cyan', 'orange', 'white']:
            print(f'[*] {color}')
            await led.set_color(color)
            await asyncio.sleep(.5)

        print('Changing brightness')
        for i in range(5+1):
            val = i/5
            print(f'[*] {int(val*100):03d}%')
            await led.set_brightness(val)
            await asyncio.sleep(.5)

        print('Changing colors in white-mode')
        for i in range(-20, 20+1):
            val = i/20
            print(f'[*] {abs(int(val*100)):03d}% {"warm" if val <= 0 else "cold"} white')
            await led.set_color_white(val)
            await asyncio.sleep(.2)

        print('Switching off LED')
        await led.set_state(False)

asyncio.run(main())
