import tkinter as tk

from controller import actions as actions_controller
from controller import frames as frames_controller
from controller import pieces as pieces_controller
from model import frames as frames_model
from model import pieces as pieces_model
from view import util as view_util

view_panel = None


def init(main_view):
    global view_panel
    view_panel = main_view.get_interpolation_controls()


def apply(frame, total_time, frame_len):
    if frame not in range(0, len(frames_model.frames)-1):
        view_util.error('Invalid frame')
        return

    start_fid = frames_model.get_frame_from_pos(frame)['id']
    end_fid = frames_model.get_frame_from_pos(frame+1)['id']
    start_pieces = pieces_model.pieces[start_fid]
    end_pieces = pieces_model.pieces[end_fid]

    sid_list = [p['id'] for p in start_pieces]
    eid_list = [p['id'] for p in end_pieces]
    if sid_list != eid_list:
        view_util.error(
            'Interpolating between frames requires that they are clones of one another\n'
            'Images can not be added or removed, only modified\n'
            'Image order must be the same (no moving up or down)'
        )
        return

    fc = int(total_time/frame_len+0.999)-1
    res = view_util.yesnobox('This will create {} frames. Continue?'.format(fc))
    if res == tk.YES:
        actions_controller.interpolate_action(start_fid, end_fid, total_time, frame_len)
        interpolate(frame, total_time, frame_len)


def interpolate(frame, total_time, frame_len):
    start_fid = frames_model.get_frame_from_pos(frame)['id']
    end_fid = frames_model.get_frame_from_pos(frame + 1)['id']
    start_pieces = pieces_model.pieces[start_fid]
    end_pieces = pieces_model.pieces[end_fid]
    fc = int(total_time / frame_len + 0.999)
    frame_len = int(total_time/fc+0.5)

    for fi in range(0, fc-1):
        pieces = []
        for i in range(0, len(start_pieces)):
            d = (fi+1)/fc
            piece = dict(start_pieces[i])
            goal = end_pieces[i]
            for k in filter(lambda v: v not in ['id', 'img'], piece.keys()):
                piece[k] += (goal[k] - piece[k]) * d
            pieces.append(piece)
        frame = frames_model.get_new_frame()
        frame['length'] = frame_len
        frames_model.frames.insert(frames_model.get_frame_position(end_fid), frame)
        pieces_model.pieces[frame['id']] = pieces

    frames_controller.update_view()
    pieces_controller.update_view()
