from model import pieces as model
from model import images as images_model
from model import frames as frames_model
from controller import actions as actions_controller

images_view = None
pieces_view = None
canvas_view = None
active_piece = None


def init(main_view):
    global images_view
    global pieces_view
    global canvas_view
    global active_piece

    images_view = main_view.get_image_list()
    pieces_view = main_view.get_piece_controls()
    canvas_view = main_view.get_main_canvas()
    active_piece = None


def reset():
    global active_piece

    clear_active()
    canvas_view.clear()
    model.pieces = {}
    model.next_id = 1


def update_view():
    clear_active()
    canvas_view.clear()
    if frames_model.active_frame() in model.pieces.keys():
        for piece in model.pieces[frames_model.active_frame()]:
            piece['img'] = images_model.get_image(piece['image_id'])
            canvas_view.add_piece(piece)


def add_from_image():
    image_id = images_view.get_selected_image()
    img = images_model.get_image(image_id)
    piece_id = model.add_from_image(image_id, img, frames_model.active_frame())
    piece = model.get_piece(frames_model.active_frame(), piece_id)
    canvas_view.add_piece(piece)
    actions_controller.add_piece_action(frames_model.active_frame(), piece)


def add_from_piece():
    if active_piece is not None:
        piece = model.get_piece(frames_model.active_frame(), active_piece)
        if piece is not None:
            piece = dict(piece)
            piece['x'] = 100
            piece['y'] = 100
            pid = model.add_from_piece(frames_model.active_frame(), piece)
            piece = model.get_piece(frames_model.active_frame(), pid)
            canvas_view.add_piece(piece)
            actions_controller.add_piece_action(frames_model.active_frame(), piece)


def update_piece(old_piece, new_piece):
    actions_controller.update_piece_action(frames_model.active_frame(), old_piece, new_piece)
    fid = frames_model.active_frame()
    model.update_piece(fid, new_piece)
    canvas_view.update_piece(new_piece)
    pieces_view.update_piece(new_piece)
    _reorder_canvas()


def _estimate_new_scale(oldimg, newimg, piece):
    old = oldimg.copy()
    new = newimg.copy()

    old = old.resize(
        (int(old.size[0] * piece['x_scale']),
         int(old.size[1] * piece['y_scale']))
    )
    old = old.rotate(piece['rotation'], expand=True)
    oldw, oldh = old.size
    oldw *= 1 - piece['right_crop'] - piece['left_crop']
    oldh *= 1 - piece['top_crop'] - piece['bottom_crop']

    new = new.rotate(piece['rotation'], expand=True)
    nw, nh = new.size
    nw *= 1 - piece['right_crop'] - piece['left_crop']
    nh *= 1 - piece['top_crop'] - piece['bottom_crop']

    return oldw/nw, oldh/nh


def change_image(piece):
    old = dict(piece)
    oldimg = piece['img'].copy()
    piece['image_id'] = images_view.get_selected_image()
    piece['img'] = images_model.get_image(piece['image_id'])
    piece['x_scale'], piece['y_scale'] = _estimate_new_scale(oldimg, piece['img'], piece)

    pieces_view.update_piece(piece)
    canvas_view.update_piece(piece)
    model.update_piece(frames_model.active_frame(), piece)
    actions_controller.update_piece_action(frames_model.active_frame(), old, piece)
    _reorder_canvas()


def remove_piece(piece_id=None):
    if piece_id is not None:
        for fid in model.pieces.keys():
            piece = model.get_piece(fid, piece_id)
            if piece is not None:
                actions_controller.delete_piece_action(fid, piece)
            model.remove_piece(fid, piece_id)
        canvas_view.delete_piece(piece_id)
        if active_piece == piece_id:
            clear_active()

    elif active_piece is not None:
        piece = model.get_piece(frames_model.active_frame(), active_piece)
        if piece is not None:
            actions_controller.delete_piece_action(frames_model.active_frame(), piece)
        model.remove_piece(frames_model.active_frame(), active_piece)
        canvas_view.delete_piece(active_piece)
        clear_active()


def get_pieces_using_image(image_id):
    id_list = []
    for k, piece_list in model.pieces.items():
        for piece in piece_list:
            if piece['image_id'] == image_id:
                id_list.append(piece['id'])
    return id_list


def activate_piece(piece_id):
    global active_piece

    active_piece = piece_id
    piece = model.get_piece(frames_model.active_frame(), piece_id)
    pieces_view.update_piece(piece)


def clear_active():
    global active_piece
    pieces_view.clear()
    active_piece = None


def move_piece_up():
    if active_piece is not None:
        fid = frames_model.active_frame()
        if fid in model.pieces.keys():
            index = None
            for i in range(0, len(model.pieces[fid])):
                if model.pieces[fid][i]['id'] == active_piece:
                    index = i
                    break
            if index is not None:
                ni = index + 1
                if ni < len(model.pieces[fid]):
                    temp = model.pieces[fid][index]
                    model.pieces[fid][index] = model.pieces[fid][ni]
                    model.pieces[fid][ni] = temp
                    actions_controller.move_piece_action(frames_model.active_frame(), active_piece, 1)
                    _reorder_canvas()


def move_piece_down():
    if active_piece is not None:
        fid = frames_model.active_frame()
        if fid in model.pieces.keys():
            index = None
            for i in range(0, len(model.pieces[fid])):
                if model.pieces[fid][i]['id'] == active_piece:
                    index = i
                    break
            if index is not None:
                ni = index - 1
                if ni >= 0:
                    temp = model.pieces[fid][index]
                    model.pieces[fid][index] = model.pieces[fid][ni]
                    model.pieces[fid][ni] = temp
                    actions_controller.move_piece_action(frames_model.active_frame(), active_piece, -1)
                    _reorder_canvas()


def change_active_frame(old_frame, new_frame):
    clear_active()
    if old_frame in model.pieces.keys():
        for p in model.pieces[old_frame]:
            canvas_view.delete_piece(p['id'])
    if new_frame in model.pieces.keys():
        for p in model.pieces[new_frame]:
            canvas_view.add_piece(p)


def _reorder_canvas():
    for p in model.pieces[frames_model.active_frame()]:
        canvas_view.update_piece(p)
