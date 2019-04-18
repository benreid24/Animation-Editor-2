import os
import json
import subprocess
import time

import tkinter as tk
from PIL import Image

from controller import pieces as pieces_controller
from controller import images as images_controller
from controller import frames as frames_controller
from controller import actions as actions_controller
from .helpers import export as export_helper
from model import pieces as pieces_model
from model import frames as frames_model
from model import images as images_model
from model import actions as actions_model
from view import util as view_util

current_file = None
export_file = None


def new_anim():
    global current_file

    if actions_controller.dirty_state():
        c = view_util.yesnobox('Discard unsaved changes?')
        if c == tk.NO:
            return

    current_file = None
    images_controller.reset()
    pieces_controller.reset()
    frames_controller.reset()
    actions_controller.reset()


def open_anim():
    global current_file

    if actions_controller.dirty_state():
        c = view_util.yesnobox('Discard unsaved changes?')
        if c == tk.NO:
            return

    folder = ''
    if current_file is not None:
        folder = os.path.dirname(current_file)

    file = view_util.get_open_anim_file(folder)
    if file is not None and os.path.isfile(file):
        current_file = file
        images_controller.reset()
        pieces_controller.reset()
        frames_controller.reset()
        actions_controller.reset()
        _load(file)


def save():
    global current_file

    if current_file is None:
        current_file = view_util.get_save_devanim_file()

    if current_file is not None:
        actions_controller.save_action()
        _save(current_file)


def save_as():
    global current_file

    folder = ''
    if current_file is not None:
        folder = os.path.dirname(current_file)

    current_file = view_util.get_save_devanim_file(folder)
    if current_file is not None:
        actions_controller.save_action()
        _save(current_file)


def export(file=None):
    if file is None:
        global export_file
        folder = ''
        if export_file is not None:
            folder = os.path.dirname(export_file)
        file = view_util.get_export_file(folder)

    if file:
        base = os.path.basename(file)
        base = os.path.splitext(base)[0]
        folder = os.path.dirname(file)
        export_helper.save_anim(folder, base, frames_model.frames, pieces_model.pieces, images_model.image_list)


def preview():
    file = 'tmp/__preview_temp{}.anim'.format(time.time())
    export(file)
    subprocess.Popen(['Previewer.exe', file])
    time.sleep(0.5)
    os.remove(file)
    os.remove('.'.join(file.split('.')[:-1])+'.png')


def _images_folder_name(file):
    base = os.path.basename(file)
    base = os.path.splitext(base)[0]
    folder = os.path.dirname(file)
    return os.path.join(folder, base + '_imgs')


def _save(file):
    data = {
        'actions': actions_model.get_as_json(),
        'images': images_model.get_as_json(),
        'pieces': pieces_model.get_as_json(),
        'frames': frames_model.get_as_json()
    }
    with open(file, 'w') as of:
        of.write(json.dumps(data, indent=4))

        folder = _images_folder_name(file)
        if not os.path.exists(folder):
            os.makedirs(folder)
        for k, img in images_model.image_list.items():
            img_file = os.path.join(folder, img['file'])
            img['img'].save(img_file)


def _load(file):
    with open(file, 'r') as ifs:
        data = json.load(ifs)
        actions_model.restore_from_loaded_json(data['actions'])
        frames_model.restore_from_loaded_json(data['frames'])
        pieces_model.restore_from_loaded_json(data['pieces'])
        images_model.restore_from_loaded_json(data['images'])

        folder = _images_folder_name(file)
        for k, img in images_model.image_list.items():
            img['img'] = Image.open(os.path.join(folder, img['file'])).convert(mode='RGBA')
        for k, pl in pieces_model.pieces.items():
            for piece in pl:
                piece['img'] = images_model.get_image(piece['image_id'])

        frames_controller.update_view()
        pieces_controller.update_view()
        images_controller.update_view()
        actions_controller.update_view()
