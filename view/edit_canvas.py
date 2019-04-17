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
        if len(items) <= 1:
            self._disable_all()
            controller.clear_active()
        else:
            for piece in self.pieces:
                if piece.contains(event.x, event.y):
                    piece.set_active(True)
                    break

    def __init__(self, master):
        tk.Frame.__init__(self, master, bd=2)

        self.vgrid = ImageTk.PhotoImage(Image.open('resources/grid.png'))
        self.battle = ImageTk.PhotoImage(Image.open('resources/battle.png'))
        self.battlegrid = ImageTk.PhotoImage(Image.open('resources/battlegrid.png'))

        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.grid()
        self.background = self.canvas.create_image(2, 2, image=self.battle, anchor=tk.NW)
        self.canvas.tag_bind(self.background, '<Button-1>', self._check_click)

        self.pieces = []

        self.grid(row=0, column=0, pady=3, padx=3)

    def set_blank(self):
        self.canvas.delete(self.background)
        self.background = self.canvas.create_rectangle(0, 0, 800, 600, fill='white')
        self.canvas.tag_bind(self.background, '<Button-1>', self._check_click)

    def set_battle(self):
        self.canvas.delete(self.background)
        self.background = self.canvas.create_image(2, 2, image=self.battle, anchor=tk.NW)
        self.canvas.tag_bind(self.background, '<Button-1>', self._check_click)

    def set_grid(self):
        self.canvas.delete(self.background)
        self.background = self.canvas.create_image(2, 2, image=self.vgrid, anchor=tk.NW)
        self.canvas.tag_bind(self.background, '<Button-1>', self._check_click)

    def set_battle_grid(self):
        self.canvas.delete(self.background)
        self.background = self.canvas.create_image(2, 2, image=self.battlegrid, anchor=tk.NW)
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
