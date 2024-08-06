from curio.video_stream import VideoStream
import ipywidgets as widgets
from IPython.display import display, Image, clear_output
import asyncio
import cv2


def create_control_buttons(curio, commands):
    forward_button = widgets.Button(description="Forward")
    back_button = widgets.Button(description="Back")
    left_button = widgets.Button(description="Left")
    right_button = widgets.Button(description="Right")
    stop_button = widgets.Button(description="Stop")

    forward_button.on_click(lambda x: asyncio.create_task(
        curio.send_command(commands['forward'])))
    back_button.on_click(lambda x: asyncio.create_task(
        curio.send_command(commands['back'])))
    left_button.on_click(lambda x: asyncio.create_task(
        curio.send_command(commands['left'])))
    right_button.on_click(lambda x: asyncio.create_task(
        curio.send_command(commands['right'])))
    stop_button.on_click(lambda x: asyncio.create_task(
        curio.send_command(commands['stop'])))

    control_box = widgets.HBox(
        [forward_button, back_button, left_button, right_button, stop_button])
    return control_box


async def display_stream(video_stream, video_output):
    try:
        image_widget = widgets.Image(format='jpg')
        video_output.clear_output(wait=True)
        with video_output:
            display(image_widget)

        while not video_stream.stop_event.is_set():
            frame = video_stream.get_frame()
            if frame is not None:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                _, jpeg = cv2.imencode('.jpg', frame)
                image_widget.value = jpeg.tobytes()
            await asyncio.sleep(0.01)
    except KeyboardInterrupt:
        print("Stream stopped")
    finally:
        video_stream.stop()


def create_video_output():
    return widgets.Output()
