import asyncio
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from known_devices import GOVEE_BULB_ADDRESS


def print_details(device: BLEDevice, advertisement: AdvertisementData = None):
    if advertisement:
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
        print(f"{device.address}: {device.name}")


async def search(device_address: str) -> None:
    found_device = asyncio.Event()

    def on_detected(device: BLEDevice, advertisement: AdvertisementData):
        nonlocal found_device
        if device.address.lower() == device_address.lower():
            print_details(device, advertisement)
            found_device.set()

    scanner = BleakScanner(detection_callback=on_detected)
    await scanner.start()
    try:
        await found_device.wait()
    finally:
        await scanner.stop()


async def discover(verbose: bool = False):
    devices = await BleakScanner.discover(timeout=5.0, return_adv=True)
    if verbose:
        for device, advertisement in devices.values():
            print_details(device, advertisement)
    else:
        for device, advertisement in devices.values():
            print_details(device)


# asyncio.run(discover())
asyncio.run(search(GOVEE_BULB_ADDRESS))
