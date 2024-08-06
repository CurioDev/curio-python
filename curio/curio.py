from threading import Event
from curio.bluetooth_controller import BluetoothController
from curio.video_stream import VideoStreamer


class Curio():
    def __init__(self, mac_address, camera_ip, camera_port):
        self.stream_stop_event = Event()
        self.bluetooth_controller = BluetoothController(
            mac_address, self.stream_stop_event)
        self.video_streamer = VideoStreamer(
            camera_ip, camera_port, self.stream_stop_event)

    def send_command(self, command):
        self.bluetooth_controller.send_command(command)

    def get_frame(self):
        return self.video_streamer.get_frame()

    def stop(self):
        self.stream_stop_event.set()
        self.bluetooth_controller.stop()
        self.video_streamer.stop()

    @staticmethod
    async def scan_for_devices():
        await BluetoothController.scan_for_devices()
