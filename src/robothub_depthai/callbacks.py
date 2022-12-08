import json
import time
from functools import partial

from depthai_sdk.callback_context import CallbackContext
from robothub import StreamHandle

mock_metadata = {
    'platform': 'robothub',
    'frame_shape': [1080, 1920, 3],
    'config': {
        'img_scale': 1.0,
        'show_fps': True,
        'detection': {
            'thickness': 1,
            'fill_transparency': 0.15,
            'box_roundness': 0,
            'color': [255, 255, 255],
            'bbox_style': 0,
            'line_width': 0.5,
            'line_height': 0.5,
            'hide_label': False,
            'label_position': 0,
            'label_padding': 10,
        },
        'text': {
            'font_color': [255, 255, 0],
            'font_transparency': 0.5,
            'font_scale': 1.0,
            'font_thickness': 2,
            'font_position': 0,
            'bg_transparency': 0.5,
            'bg_color': [0, 0, 0],
        },
    },
    'objects': []
}


def default_encoded_callback(stream_handle: StreamHandle, ctx: CallbackContext):
    packet = ctx.packet

    timestamp = int(time.time() * 1_000)
    frame_bytes = bytes(packet.imgFrame.getData())
    stream_handle.publish_video_data(frame_bytes, timestamp, mock_metadata)  # TODO change metadata


def default_nn_callback(stream_handle: StreamHandle, ctx: CallbackContext):
    packet = ctx.packet
    visualizer = ctx.visualizer

    metadata = json.loads(visualizer.serialize())
    visualizer.reset()

    # temp fix to replace None value that causes errors on frontend
    if not metadata['config']['detection']['color']:
        metadata['config']['detection']['color'] = [255, 0, 0]

    timestamp = int(time.time() * 1_000)
    frame_bytes = bytes(packet.imgFrame.getData())
    stream_handle.publish_video_data(frame_bytes, timestamp, metadata)


def get_default_color_callback(stream_handle: StreamHandle):
    return partial(default_encoded_callback, stream_handle)


def get_default_nn_callback(stream_handle: StreamHandle):
    return partial(default_nn_callback, stream_handle)


def get_default_depth_callback(stream_handle: StreamHandle):
    return partial(default_encoded_callback, stream_handle)
