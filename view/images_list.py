import tkinter as tk
from PIL import ImageTk

from controller import images as controller
from controller import pieces as pieces_controller


class ImageList(tk.LabelFrame):
    def _repack(self):
        for k, v in self.but_ids.items():
            self.images_list.delete(v)

        i = 1
        for k, but in self.image_buts.items():
            self.images_list.create_window(i*120, 100, window=but, width=120, height=120)
            i += 1

        self.images_list.configure(scrollregion=self.images_list.bbox('all'), xscrollcommand=self.scrollbar.set)

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text='Images', height=250)

        self.button_frame = tk.Frame(self)
        self.add_but = tk.Button(self.button_frame, text='Add to Frame', command=pieces_controller.add_from_image)
        self.import_but = tk.Button(self.button_frame, text='Import', command=controller.import_image, background='#ff5555')
        self.delete_but = tk.Button(self.button_frame, text='Delete', command=controller.delete_image)
        self.vert_but = tk.Button(self.button_frame, text='Clone via Vertical Flip', command=controller.clone_vertical)
        self.hori_but = tk.Button(self.button_frame, text='Clone via Horizontal Flip', command=controller.clone_horizontal)
        self.add_but.grid(row=0, column=0, pady=5, padx=3)
        self.import_but.grid(row=0, column=1, pady=5, padx=3)
        self.delete_but.grid(row=0, column=2, pady=5, padx=3)
        self.vert_but.grid(row=0, column=3, pady=5, padx=3)
        self.hori_but.grid(row=0, column=4, pady=5, padx=3)
        self.button_frame.pack(side='top')

        self.list_frame = tk.Frame(self)
        self.images_list = tk.Canvas(self.list_frame)
        self.scrollbar = tk.Scrollbar(self.list_frame, orient='horizontal', command=self.images_list.xview)

        self.selected_image = tk.IntVar()
        self.tk_images = {}  # image_id -> PhotoImage
        self.image_buts = {}  # image_id -> RadioButton
        self.but_ids = {}  # image_id -> canvas id

        self.images_list.pack(fill='both', expand=True, side='top')
        self.scrollbar.pack(fill='both', expand=True, side='bottom')
        self.list_frame.pack(fill='both', expand=True, side='bottom')

        self.grid(row=1, column=0, sticky=tk.W+tk.E)

    def get_selected_image(self):
        return self.selected_image.get()

    def add_image(self, image_id, img):
        self.tk_images[image_id] = ImageTk.PhotoImage(img.resize((100, 100)))
        img = self.tk_images[image_id]
        self.image_buts[image_id] = tk.Radiobutton(self, image=img, value=image_id, variable=self.selected_image)
        self.but_ids[image_id] = self.images_list.create_window(
            len(self.image_buts)*120,
            100,
            window=self.image_buts[image_id],
            width=120,
            height=120
        )
        self.images_list.configure(scrollregion=self.images_list.bbox('all'), xscrollcommand=self.scrollbar.set)

    def remove_image(self, image_id):
        canvas_id = self.but_ids[image_id]
        self.images_list.delete(canvas_id)
        del self.but_ids[image_id]
        del self.image_buts[image_id]
        del self.tk_images[image_id]
        self._repack()

    def clear(self):
        for k, v in self.but_ids.items():
            self.images_list.delete(v)
        self.but_ids = {}
        self.tk_images = {}
        self.image_buts = {}
