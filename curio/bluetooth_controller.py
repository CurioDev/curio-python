from threading import Thread
import asyncio
from bleak import BleakClient, BleakScanner
import nest_asyncio


nest_asyncio.apply()


class BluetoothController:
    UUID_NORDIC_TX = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
    UUID_NORDIC_RX = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

    def __init__(self, mac_address, stream_stop_event):
        self.mac_address = mac_address
        self.stream_stop_event = stream_stop_event
        self.client = None
        self.loop = asyncio.new_event_loop()
        self.ble_thread = Thread(target=self.run_loop, args=(self.loop,))
        self.ble_thread.start()

    def run_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run_client())

    async def run_client(self):
        async with BleakClient(self.mac_address) as client:
            self.client = client
            print("Connected")
            await client.start_notify(self.UUID_NORDIC_RX, self.uart_data_received)

            while not self.stream_stop_event.is_set():
                await asyncio.sleep(1)

            await client.stop_notify(self.UUID_NORDIC_RX)
            print("Disconnected")

    async def write_command(self, command):
        if self.client:
            await self.client.write_gatt_char(self.UUID_NORDIC_TX, command, True)

    def send_command(self, command):
        future = asyncio.run_coroutine_threadsafe(
            self.write_command(command), self.loop)
        future.result()

    def uart_data_received(self, sender, data):
        # print(f"Curio> {data}")
        pass

    def stop(self):
        self.stream_stop_event.set()
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.ble_thread.join()

    @staticmethod
    async def scan_for_devices():
        devices = await BleakScanner.discover()
        for d in devices:
            print(d)
