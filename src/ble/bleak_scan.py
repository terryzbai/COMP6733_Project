import asyncio
from bleak import BleakScanner


async def discover(verbose):
    devices = await BleakScanner.discover(timeout=5.0, return_adv=True)
    if verbose:
        for device, advertisement in devices.values():
            print(f"Name: {device.name}")
            print(f"Address: {device.address}")
            print(f"RSSI: {advertisement.rssi}")
            print(f"Local Name: {advertisement.local_name}")
            print(f"Manufacturer Data: {advertisement.manufacturer_data}")
            print(f"Service Data: {advertisement.service_data}")
            print(f"Service UUIDs: {advertisement.service_uuids}")
            print(f"TX Power: {advertisement.tx_power}")
            print(f"Platform Data: {advertisement.platform_data}")
            print("-" * 50)
    else:
        for device, advertisement in devices.values():
            print(f"{device.address}: {device.name}")


asyncio.run(discover(True))
