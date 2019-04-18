import math

import tkinter as tk
from PIL import ImageTk, Image

from controller import pieces as controller

_TOP = 0
_RIGHT = 1
_BOTTOM = 2
_LEFT = 3


class EditablePiece:
    def _get_scale_rect(self):
        return {
            'x': self.piece['x'] + self.img.width() - 10,
            'y': self.piece['y'] + self.img.height() - 10,
            'w': self.piece['x'] + self.img.width(),
            'h': self.piece['y'] + self.img.height()
        }

    def _get_crop_rect(self, c):
        if c % 2 != 0:
            w = 5
            h = 10
            y = self.piece['y'] + self.img.height()/2 - w/2
            x = self.piece['x']
            if c == 1:
                x += self.img.width() - w
        else:
            w = 10
            h = 5
            x = self.piece['x'] + self.img.width()/2 - w/2
            y = self.piece['y']
            if c == 2:
                y += self.img.height() - h
        return {
            'x': x,
            'y': y,
            'w': x+w,
            'h': y+h
        }

    def _get_crop_box(self):
        return (
            self.raw_image.size[0] * self.piece['left_crop'],
            self.raw_image.size[1] * self.piece['top_crop'],
            self.raw_image.size[0] - self.raw_image.size[0] * self.piece['right_crop'],
            self.raw_image.size[1] - self.raw_image.size[1] * self.piece['bottom_crop']
        )

    def _get_render_offset(self):
        transformed_image = self.raw_image.crop(self._get_crop_box())
        transformed_image = transformed_image.resize(
            (int(transformed_image.size[0] * self.piece['x_scale']),
             int(transformed_image.size[1] * self.piece['y_scale']))
        )
        transformed_image = transformed_image.rotate(self.piece['rotation'], expand=True)
        w, h = transformed_image.size
        return 400 - w/2, 300 - h/2

    def _update_items(self):
        self.clear()

        # Source and crop
        self.transformed_image = self.raw_image.crop(self._get_crop_box())
        self.transformed_image = self.transformed_image.resize(
            (int(self.transformed_image.size[0]*self.piece['x_scale']),
             int(self.transformed_image.size[1]*self.piece['y_scale']))
        )

        # Rotation
        self.transformed_image = self.transformed_image.rotate(self.piece['rotation'], expand=True)

        # Transparency
        temp_img = self.transformed_image.copy()
        temp_img.putalpha(0)
        self.transformed_image = Image.blend(self.transformed_image, temp_img, 1-self.piece['alpha']/256)

        # Render
        # Center of the piece is the origin. No offset in game
        offx, offy = self._get_render_offset()
        x = self.piece['x'] + offx
        y = self.piece['y'] + offy
        self.img = ImageTk.PhotoImage(self.transformed_image)
        self.image_id = self.canvas.create_image(
            x,
            y,
            image=self.img,
            anchor=tk.NW
        )

        self.canvas.tag_bind(self.image_id, '<Button-1>', self._start_move)
        self.canvas.tag_bind(self.image_id, '<B1-Motion>', self._move_drag)
        self.canvas.tag_bind(self.image_id, '<ButtonRelease-1>', self._stop_move)

        self.outline_id = self.canvas.create_rectangle(
            x,
            y,
            self.piece['x']+self.img.width() + offx,
            self.piece['y']+self.img.height() + offy,
            fill=''
        )
        rect = self._get_scale_rect()
        self.scale_id = self.canvas.create_rectangle(
            rect['x'] + offx, rect['y'] + offy, rect['w'] + offx, rect['h'] + offy, fill='black'
        )
        self.canvas.tag_bind(self.scale_id, '<Button-1>', self._start_scale)
        self.canvas.tag_bind(self.scale_id, '<ButtonRelease-1>', self._stop_scale)

        for i in range(0, 4):
            rect = self._get_crop_rect(i)
            self.crop_ids[i] = self.canvas.create_rectangle(
                rect['x'] + offx, rect['y'] + offy, rect['w'] + offx, rect['h'] + offy, fill='black'
            )
            self.canvas.tag_bind(self.crop_ids[i], '<Button-1>', self._start_crop)
            self.canvas.tag_bind(self.crop_ids[i], '<ButtonRelease-1>', self._stop_crop)

        self.set_active(self.state['active'])

    def _move_items(self, dx, dy):
        self.canvas.move(self.image_id, dx, dy)
        self.canvas.move(self.outline_id, dx, dy)
        self.canvas.move(self.scale_id, dx, dy)
        for i in range(0, 4):
            self.canvas.move(self.crop_ids[i], dx, dy)

    def _hide_items(self):
        self.canvas.itemconfig(self.outline_id, state=tk.HIDDEN)
        self.canvas.itemconfig(self.scale_id, state=tk.HIDDEN)
        for i in range(0, 4):
            self.canvas.itemconfig(self.crop_ids[i], state=tk.HIDDEN)

    def _show_items(self):
        self.canvas.itemconfig(self.outline_id, state=tk.NORMAL)
        self.canvas.itemconfig(self.scale_id, state=tk.NORMAL)
        for i in range(0, 4):
            self.canvas.itemconfig(self.crop_ids[i], state=tk.NORMAL)

    def _start_move(self, event):
        self.master._disable_all()
        self.set_active(True)
        self.state['moving'] = True
        self.state['orig_pos'] = (self.piece['x'], self.piece['y'])
        self.state['click_pos'] = (event.x, event.y)

    def _move_drag(self, event):
        if self.state['moving'] and self.state['active']:
            dx = event.x - self.state['click_pos'][0]
            dy = event.y - self.state['click_pos'][1]
            self._move_items(dx, dy)
            self.piece['x'] += dx
            self.piece['y'] += dy
            self.state['click_pos'] = (event.x, event.y)

    def _stop_move(self, event):
        if self.state['moving'] and self.state['active']:
            self.state['moving'] = False
            old = dict(self.piece)
            old['x'] = self.state['orig_pos'][0]
            old['y'] = self.state['orig_pos'][1]
            controller.update_piece(old, self.piece)

    def _start_scale(self, event):
        if self.state['active']:
            self.state['moving'] = False
            self.state['orig_scale'] = (self.piece['x_scale'], self.piece['y_scale'])
            self.state['scaling'] = True

    def _stop_scale(self, event):
        if self.state['scaling'] and self.state['active']:
            self.state['scaling'] = False
            old = dict(self.piece)

            offx, offy = self._get_render_offset()
            nw = event.x - self.piece['x'] - offx
            nh = event.y - self.piece['y'] - offy

            self.piece['x_scale'] = nw / self.raw_image.size[0] /\
                (1 - self.piece['right_crop'] - self.piece['left_crop'])
            self.piece['y_scale'] = nh / self.raw_image.size[1] /\
                (1 - self.piece['top_crop'] - self.piece['bottom_crop'])

            self._update_items()
            controller.update_piece(old, self.piece)

    def _start_crop(self, event):
        if self.state['active']:
            self.state['moving'] = False
            self.state['cropping'] = True
            crop_ids = self.canvas.find_overlapping(event.x, event.y, event.x + 2, event.y + 2)
            for i in range(0, 4):
                if self.crop_ids[i] in crop_ids:
                    active_side = i
                    break
            self.state['acrop'] = ['top_crop', 'right_crop', 'bottom_crop', 'left_crop'][active_side]
            self.state['orig_crop'] = self.piece[self.state['acrop']]
            self.state['click_pos'] = (event.x, event.y)

    def _stop_crop(self, event):
        if self.state['active'] and self.state['cropping']:
            self.state['cropping'] = False

            c = self.state['acrop']
            if c in ['top_crop', 'bottom_crop']:
                perc_showing = 1 - self.piece['top_crop'] - self.piece['bottom_crop']
                d = self.state['click_pos'][1]-event.y
                if c == 'top_crop':
                    d *= -1
                perc_cut = d/self.img.height()
            else:
                perc_showing = 1 -self.piece['right_crop'] - self.piece['left_crop']
                d = self.state['click_pos'][0]-event.x
                if c == 'left_crop':
                    d *= -1
                perc_cut = d/self.img.width()

            perc_cropped = perc_cut / perc_showing
            self.piece[c] += perc_cropped
            if self.piece[c] > 1:
                self.piece[c] = 1
            if self.piece[c] < 0:
                self.piece[c] = 0
            self._update_items()
            old = dict(self.piece)
            old[c] = self.state['orig_crop']
            controller.update_piece(old, self.piece)

    def __init__(self, master, canvas, piece):
        self.master = master
        self.canvas = canvas
        self.state = {
            'active': False,
            'moving': False,
            'scaling': False,
            'cropping': False,
            'orig_pos': (piece['x'], piece['y']),
            'orig_scale': (piece['x_scale'], piece['y_scale']),
            'orig_crop': None,
            'click_pos': (0, 0),
            'acrop': -1
        }
        self.piece = piece
        self.raw_image = piece['img']
        self.transformed_image = self.raw_image.copy()
        self.img = ImageTk.PhotoImage(self.transformed_image)

        self.image_id = 0
        self.outline_id = 0
        self.scale_id = 0
        self.crop_ids = [0, 0, 0, 0]

        self._update_items()

    def update(self, piece):
        self.raw_image = piece['img']
        self.piece = piece
        self._update_items()

    def clear(self):
        self.canvas.delete(self.image_id)
        self.canvas.delete(self.outline_id)
        self.canvas.delete(self.scale_id)
        for i in self.crop_ids:
            self.canvas.delete(i)

    def piece_id(self):
        return self.piece['id']

    def set_active(self, active):
        self.state['active'] = active
        if active:
            self._show_items()
            controller.activate_piece(self.piece['id'])
        else:
            self._hide_items()

    def is_active(self):
        return self.state['active']

    def contains(self, x, y):
        return x in range(self.piece['x'], self.piece['x']+self.img.width()) and \
               y in range(self.piece['y'], self.piece['y']+self.img.height())
