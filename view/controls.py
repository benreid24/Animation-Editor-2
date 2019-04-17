import tkinter as tk

from .frame_options import FrameOptions
from .piece_settings import PieceSettings
from .batch_edits import BatchEdits
from .interpolate import InterpolateControls
from .history import Actions


class Controls(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.frame_options = FrameOptions(self)
        self.piece_settings = PieceSettings(self)
        self.batch_edits = BatchEdits(self)
        self.interp_controls = InterpolateControls(self)
        self.actions = Actions(self)

        self.grid(column=1, row=0, rowspan=2, padx=4, sticky=tk.W+tk.E+tk.N+tk.S)
