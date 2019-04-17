import tkinter as tk

from controller import actions as actions_controller
from controller import pieces as pieces_controller
from controller import frames as frames_controller
from model import frames as frames_model
from model import pieces as pieces_model
from view import util as view_util


def batch_edit(start_frame, end_frame, percent, frame_len, xpos, ypos, xscale, yscale, alpha, rot):
    if start_frame not in range(0, len(frames_model.frames)) or end_frame not in range(-1, len(frames_model.frames)):
        view_util.error('Invalid frame range')
        return

    if end_frame == -1:
        end_frame = len(frames_model.frames)-1
    elif end_frame < start_frame:
        temp = end_frame
        end_frame = start_frame
        start_frame = temp

    if percent == 0:
        if frame_len < 0:
            view_util.error(
                'All frames have their length set to the input length\n'
                'This is not a shift, so it must be greater than 0'
            )
            return
        if frame_len > 0:
            res = view_util.yesnobox(
                'WARNING: Setting all frame lengths via batch edit cannot be undo\n'
                'Do it anyways?'
            )
            if res == tk.NO:
                return
        batch_shift(start_frame, end_frame, frame_len, xpos, ypos, xscale, yscale, alpha, rot)
    else:
        percent_shift(start_frame, end_frame, frame_len, xscale, yscale, alpha, rot)

    actions_controller.batch_action(
        start_frame, end_frame, percent, frame_len, xpos, ypos, xscale, yscale, alpha, rot
    )


def batch_shift(start_frame, end_frame, frame_len, xpos, ypos, xscale, yscale, alpha, rot):
    xscale /= 100
    yscale /= 100

    for fi in range(start_frame, end_frame+1):
        if frame_len > 0:
            frames_model.frames[fi]['length'] = frame_len
        fid = frames_model.get_frame_from_pos(fi)['id']
        if fid in pieces_model.pieces.keys():
            for i in range(0, len(pieces_model.pieces[fid])):
                nxs = pieces_model.pieces[fid][i]['x_scale'] + xscale
                nxs = 0.1 if nxs <= 0 else nxs
                nys = pieces_model.pieces[fid][i]['y_scale'] + yscale
                nys = 0.1 if nys <= 0 else nys
                na = pieces_model.pieces[fid][i]['alpha'] + alpha
                na = 0 if na < 0 else na
                na = 255 if na > 255 else na
                nr = int(pieces_model.pieces[fid][i]['rotation'] + rot) % 360

                pieces_model.pieces[fid][i]['x'] += xpos
                pieces_model.pieces[fid][i]['y'] += ypos
                pieces_model.pieces[fid][i]['x_scale'] = nxs
                pieces_model.pieces[fid][i]['y_scale'] = nys
                pieces_model.pieces[fid][i]['alpha'] = na
                pieces_model.pieces[fid][i]['rotation'] = nr

    pieces_controller.update_view()
    frames_controller.update_view()


def percent_shift(start_frame, end_frame, frame_len, xscale, yscale, alpha, rot):
    frame_len /= 100
    xscale /= 100
    yscale /= 100
    alpha /= 100
    rot /= 100

    for fi in range(start_frame, end_frame+1):
        fl = frames_model.frames[fi]['length']
        frames_model.frames[fi]['length'] = fl+int(fl*frame_len)
        if frames_model.frames[fi]['length'] < 5:
            frames_model.frames[fi]['length'] = 5

        fid = frames_model.get_frame_from_pos(fi)['id']
        if fid in pieces_model.pieces.keys():
            for i in range(0, len(pieces_model.pieces[fid])):
                nxs = pieces_model.pieces[fid][i]['x_scale'] + pieces_model.pieces[fid][i]['x_scale']*xscale
                nxs = 0.1 if nxs <= 0 else nxs
                nys = pieces_model.pieces[fid][i]['y_scale'] + pieces_model.pieces[fid][i]['y_scale']*yscale
                nys = 0.1 if nys <= 0 else nys
                na = pieces_model.pieces[fid][i]['alpha'] + int(pieces_model.pieces[fid][i]['alpha']*alpha)
                na = 0 if na < 0 else na
                na = 255 if na > 255 else na
                nr = (pieces_model.pieces[fid][i]['rotation'] + int(pieces_model.pieces[fid][i]['rotation']*rot)) % 360

                pieces_model.pieces[fid][i]['x_scale'] = nxs
                pieces_model.pieces[fid][i]['y_scale'] = nys
                pieces_model.pieces[fid][i]['alpha'] = na
                pieces_model.pieces[fid][i]['rotation'] = nr

    pieces_controller.update_view()
    frames_controller.update_view()