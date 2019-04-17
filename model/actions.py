import json

current_action = None
actions = []

action_template = {
    'type': 'action_name',
    'data': {
        'old_state': 'Just an example',
        'new_state': 'Not all actions would be like this'
    }
}

VALID_TYPES = [
    'save',

    'add_piece',
    'delete_piece',
    'update_piece',
    'move_piece',

    'add_image',
    'delete_image',

    'add_frame',
    'move_frame',
    'delete_frame',
    'update_frame',

    'batch',
    'interpolate'
]


def get_as_json():
    global current_action

    def blank(obj):
        return 'unserializable'

    if current_action is not None:
        return json.dumps(actions[:current_action+1], default=blank)
    return '[]'


def restore_from_loaded_json(data):
    global current_action
    global actions

    actions = json.loads(data)
    current_action = len(actions)-1
