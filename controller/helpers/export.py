import struct
import os
import math

from PIL import Image

MAX_SPRITESHEET_WIDTH = 4000
FIELD_TYPE_MAP = {
    'texture': 'string',
    'loop': '=B',
    'numFrames': '=H',
    'length': '=I',
    'numPieces': '=H',
    'sourceX': '=I',
    'sourceY': '=I',
    'width': '=I',
    'height': '=I',
    'scaleX': '=I',
    'scaleY': '=I',
    'xOff': '=i',
    'yOff': '=i',
    'rotation': '=I',
    'alpha': '=B'
}


def _pack_field(name, value):
    fmt = FIELD_TYPE_MAP[name]
    if fmt == 'string':
        ret = struct.pack('=I', len(value))
        fmt = '={}s'.format(len(value))
        return ret + struct.pack(fmt, value.encode())
    return struct.pack(fmt, value)


def create_sprite_sheet(image_list):
    image_list = sorted(image_list, key=lambda k: k['img'].size[1])
    image_rects = {}  # image_id -> (x, y, w, h)
    total_width = 0
    total_height = 0
    row_width = 0
    row_height = 0

    for img in image_list:
        nw = row_width + img['img'].size[0]
        if nw <= MAX_SPRITESHEET_WIDTH:
            if img['img'].size[1] > row_height:
                row_height = img['img'].size[1]
        else:
            if row_width > total_width:
                total_width = row_width
            nw = 0
            total_height += row_height
            row_height = img['img'].size[1]

        image_rects[img['id']] = [
            row_width,
            total_height,
            img['img'].size[0],
            img['img'].size[1]
        ]
        row_width = nw

    total_height += row_height
    if row_width > total_width:
        total_width = row_width

    sheet = Image.new('RGBA', (total_width, total_height))
    sheet.putalpha(0)
    for img in image_list:
        sheet.paste(img['img'], (image_rects[img['id']][0], image_rects[img['id']][1]))

    return image_rects, sheet


def save_anim(path, anim_name, frames, pieces, images, is_loop):
    images_list = [v for k, v in images.items()]
    image_rects, sheet = create_sprite_sheet(images_list)
    sheet_file = os.path.join(path, anim_name+'.png')
    anim_file = os.path.join(path, anim_name+'.anim')

    with open(anim_file, 'wb') as file:
        data = _pack_field('texture', anim_name+'.png')
        data += _pack_field('loop', is_loop)
        data += _pack_field('numFrames', len(frames))
        for frame in frames:
            data += _pack_field('length', frame['length'])
            pcs = []
            if frame['id'] in pieces.keys():
                pcs = pieces[frame['id']]

            data += _pack_field('numPieces', len(pcs))
            for piece in pcs:
                rect = list(image_rects[int(piece['image_id'])])
                rect[0] += rect[2] * piece['left_crop']
                rect[1] += rect[3] * piece['top_crop']
                rect[2] *= (1 - piece['left_crop'] - piece['right_crop'])
                rect[3] *= (1 - piece['top_crop'] - piece['bottom_crop'])
                x = piece['x'] + piece['x_scale']*rect[2]/2 - rect[2]/2
                y = piece['y'] + piece['y_scale']*rect[3]/2 - rect[3]/2
                r = (-int(piece['rotation'])) % 360  # Got it backwards, oops

                data += _pack_field('sourceX', int(rect[0]))
                data += _pack_field('sourceY', int(rect[1]))
                data += _pack_field('width', int(rect[2]))
                data += _pack_field('height', int(rect[3]))
                data += _pack_field('scaleX', int(piece['x_scale']*100))
                data += _pack_field('scaleY', int(piece['y_scale']*100))
                data += _pack_field('xOff', int(x))
                data += _pack_field('yOff', int(y))
                data += _pack_field('rotation', r)
                data += _pack_field('alpha', int(piece['alpha']))
        file.write(data)
        sheet.save(sheet_file)
