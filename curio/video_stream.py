from threading import Thread
import cv2


class VideoStreamer:
    def __init__(self, camera_ip, camera_port, stream_stop_event):
        self.camera_url = f'http://{camera_ip}:{camera_port}/video'
        self.frame_buffer = None
        self.stream_stop_event = stream_stop_event
        self.capture_thread = Thread(target=self.capture_stream)
        self.capture_thread.start()

    def capture_stream(self):
        cap = cv2.VideoCapture(self.camera_url)
        try:
            while not self.stream_stop_event.is_set():
                ret, frame = cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                self.frame_buffer = frame
        except Exception as e:
            print(f"Stream error: {e}")
        finally:
            cap.release()
            self.stream_stop_event.set()

    def get_frame(self):
        return self.frame_buffer

    def stop(self):
        self.stream_stop_event.set()
        self.capture_thread.join()
