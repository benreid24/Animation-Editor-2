import tkinter as tk

from .edit_canvas import EditCanvas
from .menu_bar import MenuBar
from .controls import Controls
from .images_list import ImageList


class AnimationEditor:
    def _mouse_motion(self, event):
        self.controls.actions.set_pos(event.x, event.y)

    def __init__(self):
        self.TK_ROOT = tk.Tk()
        self.TK_ROOT.title('Animation Editor')
        self.TK_ROOT.resizable(True, True)
        self.TK_ROOT.iconbitmap('resources/icon.ico')

        self.canvas = tk.Canvas(self.TK_ROOT)
        self.x_scrollbar = tk.Scrollbar(self.TK_ROOT, orient='horizontal', command=self.canvas.xview)
        self.y_scrollbar = tk.Scrollbar(self.TK_ROOT, orient='vertical', command=self.canvas.yview)
        self.inner_frame = tk.Frame(self.canvas)

        self.menu_bar = MenuBar(self.inner_frame)
        self.edit_canvas = EditCanvas(self.inner_frame)
        self.controls = Controls(self.inner_frame)
        self.image_list = ImageList(self.inner_frame)

        self.wid = self.canvas.create_window(0, 0, window=self.inner_frame)

        self.y_scrollbar.pack(fill='y', expand=False, side='right')
        self.x_scrollbar.pack(fill='x', expand=False, side='bottom')
        self.canvas.pack(fill='both', expand=True, side='top')

        self.TK_ROOT.configure(menu=self.menu_bar)
        self.menu_bar.set_editor(self)

        self.old_width = 0
        self.old_height = 0
        self.edit_canvas.canvas.bind('<Motion>', self._mouse_motion)

        self.TK_ROOT.update()
        self.canvas.configure(
            scrollregion=self.canvas.bbox('all'),
            xscrollcommand=self.x_scrollbar.set,
            yscrollcommand=self.y_scrollbar.set
        )

    def get_image_list(self):
        return self.image_list

    def get_main_canvas(self):
        return self.edit_canvas

    def get_piece_controls(self):
        return self.controls.piece_settings

    def get_frame_controls(self):
        return self.controls.frame_options

    def get_menu(self):
        return self.menu_bar

    def get_actions_panel(self):
        return self.controls.actions

    def get_interpolation_controls(self):
        return self.controls.interp_controls

    def mainloop(self):
        self.TK_ROOT.mainloop()
