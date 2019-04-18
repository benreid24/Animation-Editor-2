import tkinter as tk
from .editable_piece import EditablePiece
from PIL import Image, ImageTk

from controller import pieces as controller


class EditCanvas(tk.Frame):
    def _disable_all(self):
        for piece in self.pieces:
            piece.set_active(False)

    def _check_click(self, event):
        items = self.canvas.find_overlapping(event.x, event.y, event.x+2, event.y+2)
        if len(items) <= 2:
            self._disable_all()
            controller.clear_active()
        else:
            for piece in self.pieces:
                if piece.contains(event.x, event.y):
                    piece.set_active(True)
                    break

    def __init__(self, master):
        tk.Frame.__init__(self, master, bd=2)

        self.background_list = {
            '250x250 Blank': 'zoomed_blank',
            '250x250 Lines': 'zoomed_lines',
            '250x250 Grid': 'zoomed_grid',
            'Fullscreen Blank': 'fullscreen_blank',
            'Fullscreen Lines': 'fullscreen_lines',
            'Fullscreen Grid': 'fullscreen_grid'
        }
        self.images = {
            v: ImageTk.PhotoImage(Image.open('resources/{}.png'.format(v))) for k, v in self.background_list.items()
        }
        self.current_background = 'fullscreen_grid'

        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.grid()

        self.white_rect = self.canvas.create_rectangle(0, 0, 800, 600, fill='white')
        self.background = self.canvas.create_image(2, 2, image=self.images[self.current_background], anchor=tk.NW)
        self.canvas.tag_bind(self.background, '<Button-1>', self._check_click)

        self.pieces = []

        self.grid(row=0, column=0, pady=3, padx=3)

    def set_background(self, background):
        self.canvas.delete(self.background)
        self.canvas.delete(self.white_rect)
        self.current_background = background

        w = 800 if 'fullscreen' in background else 250
        h = 600 if 'fullscreen' in background else 250
        self.white_rect = self.canvas.create_rectangle(0, 0, w, h, fill='white')
        self.background = self.canvas.create_image(2, 2, image=self.images[self.current_background], anchor=tk.NW)
        self.canvas.tag_bind(self.background, '<Button-1>', self._check_click)

    def add_piece(self, piece):
        self.pieces.append(EditablePiece(self, self.canvas, piece))

    def update_piece(self, piece):
        for p in self.pieces:
            if p.piece_id() == piece['id']:
                p.update(piece)
                break

    def delete_piece(self, piece_id):
        for p in self.pieces:
            if p.piece_id() == piece_id:
                p.clear()
        self.pieces = [p for p in self.pieces if p.piece_id() != piece_id]

    def clear(self):
        for p in self.pieces:
            p.clear()
        self.pieces = []

    def active_piece(self):
        for p in self.pieces:
            if p.is_active():
                return p.piece_id()
        return None
