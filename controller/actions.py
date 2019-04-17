from model import actions as model
from .helpers import actions as helper

menu_view = None
actions_view = None


def init(main_view):
    global menu_view
    global actions_view

    menu_view = main_view.get_menu()
    actions_view = main_view.get_actions_panel()


def undo():
    helper.undo()


def redo():
    helper.redo()


def set_action_index(i):
    if model.current_action > i:
        while model.current_action != i:
            undo()
    elif model.current_action < i:
        while model.current_action < i:
            redo()


def get_action_index():
    return model.current_action


def update_view():
    if model.current_action is not None and model.current_action in range(0, len(model.actions)):
        menu_view.set_undo_action(model.actions[model.current_action]['type'])
        if model.current_action+1 in range(0, len(model.actions)):
            menu_view.set_redo_action(model.actions[model.current_action+1]['type'])
        else:
            menu_view.set_redo_action('')

        al = [a['type'] for a in model.actions]
        actions_view.set_action_list(al)
        actions_view.set_active(model.current_action)
    else:
        menu_view.set_undo_action('')
        menu_view.set_redo_action('')
        actions_view.clear()


def add_action(action):
    if model.current_action is not None and model.current_action < len(model.actions)-1:
        model.actions = model.actions[:model.current_action+1]
    model.actions.append(action)
    model.current_action = len(model.actions)-1
    update_view()


def dirty_state():
    if model.current_action is not None:
        return model.actions[model.current_action]['type'] != 'save'
    return False


def reset():
    model.actions = []
    model.current_action = None
    update_view()


def add_image_action(image_id):
    action = {
        'type': 'add_image',
        'data': {
            'id': image_id  # Don't bother with file, cannot redo add
        }
    }
    add_action(action)


def delete_image_action():
    action = {
        'type': 'delete_image',
        'data': {}
    }
    add_action(action)


def add_piece_action(frame_id, piece):
    action = {
        'type': 'add_piece',
        'data': {
            'piece': dict(piece),
            'frame_id': frame_id
        }
    }
    add_action(action)


def update_piece_action(frame_id, old_piece, new_piece):
    action = {
        'type': 'update_piece',
        'data': {
            'old': dict(old_piece),
            'new': dict(new_piece),
            'frame_id': frame_id
        }
    }
    add_action(action)


def move_piece_action(frame_id, piece_id, index_change):
    action = {
        'type': 'move_piece',
        'data': {
            'frame_id': frame_id,
            'piece_id': piece_id,
            'index_change': index_change
        }
    }
    add_action(action)


def delete_piece_action(frame_id, piece):
    action = {
        'type': 'delete_piece',
        'data': {
            'piece': dict(piece),
            'frame_id': frame_id
        }
    }
    add_action(action)


def add_frame_action(frame, index, pieces):
    action = {
        'type': 'add_frame',
        'data': {
            'frame': dict(frame),
            'index': index,
            'pieces': list(pieces)
        }
    }
    add_action(action)


def move_frame_action(frame_id, index_change):
    action = {
        'type': 'move_frame',
        'data': {
            'frame_id': frame_id,
            'index_change': index_change
        }
    }
    add_action(action)


def update_frame_action(frame_id, old_len, new_len):
    action = {
        'type': 'update_frame',
        'data': {
            'frame_id': frame_id,
            'old_len': old_len,
            'new_len': new_len
        }
    }
    if old_len != new_len:
        add_action(action)


def delete_frame_action(frame, index, pieces):
    action = {
        'type': 'delete_frame',
        'data': {
            'frame': dict(frame),
            'index': index,
            'pieces': list(pieces)
        }
    }
    add_action(action)


def save_action():
    action = {
        'type': 'save',
        'data': {}
    }
    add_action(action)


def batch_action(sframe, eframe, percent, frame_len, xpos, ypos, xscale, yscale, alpha, rot):
    action = {
        'type': 'batch',
        'data': {
            'start_frame': sframe,
            'end_frame': eframe,
            'percent': percent,
            'frame_len': frame_len,
            'xpos': xpos,
            'ypos': ypos,
            'xscale': xscale,
            'yscale': yscale,
            'alpha': alpha,
            'rot': rot
        }
    }
    add_action(action)


def interpolate_action(start_fid, end_fid, total_time, frame_len):
    action = {
        'type': 'interpolate',
        'data': {
            'start_frame': start_fid,
            'end_frame': end_fid,
            'total_time': total_time,
            'frame_len': frame_len
        }
    }
    add_action(action)
