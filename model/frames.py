import json

_active_frame = 1
next_id = 2
frames = [
    {
        'id': 1,
        'length': 50
    }
]
is_loop = False


def get_as_json():
    return json.dumps(
        {
            'next_id': next_id,
            'is_looping': is_loop,
            'frames': frames
        }
    )


def restore_from_loaded_json(data):
    global next_id
    global frames
    global _active_frame
    global is_loop

    data = json.loads(data)
    next_id = data['next_id']
    is_loop = data['is_looping']
    frames = data['frames']
    _active_frame = frames[0]['id']


def init():
    global next_id
    global frames
    global _active_frame
    global is_loop

    next_id = 2
    frames = [
        {
            'id': 1,
            'length': 50
        }
    ]
    is_loop = False
    _active_frame = 1


def active_frame():
    return _active_frame


def get_new_frame():
    global next_id

    frame = {
        'id': next_id,
        'length': 50
    }
    next_id += 1
    return frame


def get_frame(frame_id):
    for frame in frames:
        if frame['id'] == frame_id:
            return frame
    return None


def get_frame_from_pos(i):
    if i in range(0, len(frames)):
        return frames[i]
    return None


def get_frame_position(frame_id):
    for i in range(0, len(frames)):
        if frames[i]['id'] == frame_id:
            return i
    return None

