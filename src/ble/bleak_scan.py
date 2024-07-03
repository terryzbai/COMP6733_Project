import asyncio
from bleak import BleakScanner


async def discover():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device)


asyncio.run(discover())
