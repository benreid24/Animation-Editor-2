from model import frames as model
from model import pieces as pieces_model
from controller import pieces as pieces_controller
from controller import actions as actions_controller
from view import util

view_options = None


def init(main_view):
    global view_options

    view_options = main_view.get_frame_controls()
    view_options.set_length(model.frames[0]['length'])
    model.init()


def reset():
    model.init()
    view_options.set_length(model.frames[0]['length'])
    update_view()


def active_frame_index():
    return model.get_frame_position(model.active_frame())


def update_view():
    i = model.get_frame_position(model.active_frame())
    if i is None:
        i = 0
        model._active_frame = model.frames[0]['id']
    length = model.get_frame_from_pos(i)['length']
    view_options.set_frame_count(len(model.frames))
    view_options.set_active(i)
    view_options.set_length(length)


def new_frame_append():
    frame = model.get_new_frame()
    model.frames.append(frame)
    update_view()
    actions_controller.add_frame_action(frame, len(model.frames)-1, {})


def new_frame_insert():
    i = model.get_frame_position(model.active_frame())
    frame = model.get_new_frame()
    model.frames.insert(i, frame)
    update_view()
    actions_controller.add_frame_action(frame, i, {})


def clone_frame():
    i = model.get_frame_position(model.active_frame())
    frame = dict(model.get_frame(model.active_frame()))
    frame['id'] = model.next_id
    model.next_id += 1
    model.frames.insert(i+1, frame)
    if model.active_frame() in pieces_model.pieces.keys():
        pieces_model.pieces[frame['id']] = [dict(p) for p in pieces_model.pieces[model.active_frame()]]
    update_view()
    actions_controller.add_frame_action(frame, i+1, pieces_model.pieces[frame['id']])


def delete_frame():
    if len(model.frames) > 1:
        i = model.get_frame_position(model.active_frame())
        frame = model.get_frame(model.active_frame())
        actions_controller.delete_frame_action(frame, i, pieces_model.pieces[frame['id']])

        ni = i + 1
        if ni >= len(model.frames):
            ni = len(model.frames) - 2  # Deleting last, next is second last
        model._active_frame = model.get_frame_from_pos(ni)['id']

        pieces_controller.change_active_frame(frame['id'], model.active_frame())
        model.frames.remove(frame)
        if frame['id'] in pieces_model.pieces.keys():
            del pieces_model.pieces[frame['id']]

        update_view()

    else:
        util.error('You need to have at least one frame, jackass')


def move_frame_up():
    i = model.get_frame_position(model.active_frame())
    ni = i - 1
    if ni >= 0:
        actions_controller.move_frame_action(model.get_frame_from_pos(i)['id'], -1)
        temp = model.frames[ni]
        model.frames[ni] = model.frames[i]
        model.frames[i] = temp
        update_view()


def move_frame_down():
    i = model.get_frame_position(model.active_frame())
    ni = i + 1
    if ni < len(model.frames):
        actions_controller.move_frame_action(model.get_frame_from_pos(i)['id'], 1)
        temp = model.frames[ni]
        model.frames[ni] = model.frames[i]
        model.frames[i] = temp
        update_view()


def change_active_frame():
    old = model.active_frame()
    model._active_frame = model.get_frame_from_pos(view_options.get_selected_index())['id']
    pieces_controller.change_active_frame(old, model.active_frame())
    update_view()


def update_frame():
    new_len = view_options.get_length_str()
    try:
        new_len = int(new_len)
    except:
        util.error('Frame length must be an integer')
        return
    if new_len <= 0:
        util.error('Frame length <= 0 ?!')
        return
    i = model.get_frame_position(model.active_frame())
    actions_controller.update_frame_action(model.active_frame(), model.frames[i]['length'], new_len)
    model.frames[i]['length'] = new_len
