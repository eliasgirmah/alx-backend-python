import asyncio
from bleak import BleakScanner

async def scan():
    print("🔍 Scanning for Bluetooth devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"{device.name or 'Unknown'} - {device.address}")

asyncio.run(scan())
