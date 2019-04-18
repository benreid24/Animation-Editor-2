import tkinter as tk

import view.util as util
from controller import pieces as controller


class PieceSettings(tk.LabelFrame):
    def _apply(self):
        x = self.xpos_entry.get()
        y = self.ypos_entry.get()
        xs = self.xscale_entry.get()
        ys = self.yscale_entry.get()
        r = self.rotation_scale.get()
        xc = self.xcrop_entry.get()
        yc = self.ycrop_entry.get()
        wc = self.wcrop_entry.get()
        hc = self.hcrop_entry.get()
        t = self.trans_scale.get()

        try:
            x = float(x)
            y = float(y)
            xs = float(xs)/100
            ys = float(ys)/100
            xc = float(xc)/100
            yc = float(yc)/100
            wc = float(wc)/100
            hc = float(hc)/100
        except:
            util.error('Input must be numerical')
            return

        if xs <= 0 or ys <= 0 or xc < 0 or yc < 0 or wc < 0 or hc < 0:
            util.error('Input must be positive')
            return

        old = dict(self.piece)
        self.piece['x'] = x
        self.piece['y'] = y
        self.piece['x_scale'] = xs
        self.piece['y_scale'] = ys
        self.piece['rotation'] = r
        self.piece['alpha'] = t
        self.piece['top_crop'] = yc
        self.piece['right_crop'] = wc
        self.piece['bottom_crop'] = hc
        self.piece['left_crop'] = xc
        controller.update_piece(old, self.piece)

    def _chg_img(self):
        x = self.xpos_entry.get()
        y = self.ypos_entry.get()
        xs = self.xscale_entry.get()
        ys = self.yscale_entry.get()
        r = self.rotation_scale.get()
        xc = self.xcrop_entry.get()
        yc = self.ycrop_entry.get()
        wc = self.wcrop_entry.get()
        hc = self.hcrop_entry.get()
        t = self.trans_scale.get()

        try:
            x = float(x)
            y = float(y)
            xs = float(xs) / 100
            ys = float(ys) / 100
            xc = float(xc) / 100
            yc = float(yc) / 100
            wc = float(wc) / 100
            hc = float(hc) / 100
        except:
            util.error('Must have a piece selected')
            return

        self.update_piece(self.piece)
        controller.change_image(self.piece)

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text='Image Options', padx=3, pady=3)
        self.piece = None

        self.clone_but = tk.Button(self, text='Clone', command=controller.add_from_piece)
        self.delete_but = tk.Button(self, text='Delete', command=controller.remove_piece)
        self.update_but = tk.Button(self, text='Update', command=self._apply, background='#ff5555')
        self.image_but = tk.Button(self, text='Change Image', command=self._chg_img, background='#ffff00')
        self.upbut = tk.Button(self, text='Move up', command=controller.move_piece_up)
        self.downbut = tk.Button(self, text='Move down', command=controller.move_piece_down)
        self.clone_but.grid(row=0, column=0, pady=5)
        self.delete_but.grid(row=0, column=1, pady=5)
        self.update_but.grid(row=0, column=2, pady=5)
        self.image_but.grid(row=1, column=2)
        self.upbut.grid(row=0, column=3, pady=1)
        self.downbut.grid(row=1, column=3, pady=1)

        self.xpos_label = tk.Label(self, text='X Pos:')
        self.xpos_entry = tk.Entry(self)
        self.xpos_label.grid(row=2, column=0)
        self.xpos_entry.grid(row=3, column=0)
        self.ypos_label = tk.Label(self, text='Y Pos:')
        self.ypos_entry = tk.Entry(self)
        self.ypos_label.grid(row=2, column=1)
        self.ypos_entry.grid(row=3, column=1)

        self.xscale_label = tk.Label(self, text='X Scale %:')
        self.xscale_entry = tk.Entry(self)
        self.xscale_label.grid(row=2, column=2)
        self.xscale_entry.grid(row=3, column=2)
        self.yscale_label = tk.Label(self, text='Y Scale %:')
        self.yscale_entry = tk.Entry(self)
        self.yscale_label.grid(row=2, column=3)
        self.yscale_entry.grid(row=3, column=3)

        self.rotation_scale = tk.Scale(self, from_=0, to=360, resolution=1, orient=tk.HORIZONTAL, label='Rotation')
        self.rotation_scale.set(0)
        self.rotation_scale.grid(row=4, column=0, columnspan=2)
        self.trans_scale = tk.Scale(self, from_=0, to=255, resolution=1, orient=tk.HORIZONTAL, label='Opacity')
        self.trans_scale.set(256)
        self.trans_scale.grid(row=4, column=2, columnspan=2)

        self.xcrop_label = tk.Label(self, text='Left Crop(%):')
        self.xcrop_entry = tk.Entry(self)
        self.xcrop_label.grid(row=5, column=0)
        self.xcrop_entry.grid(row=6, column=0)
        self.ycrop_label = tk.Label(self, text='Top Crop(%):')
        self.ycrop_entry = tk.Entry(self)
        self.ycrop_label.grid(row=5, column=1)
        self.ycrop_entry.grid(row=6, column=1)

        self.wcrop_label = tk.Label(self, text='Right Crop(%):')
        self.wcrop_entry = tk.Entry(self)
        self.wcrop_label.grid(row=5, column=2)
        self.wcrop_entry.grid(row=6, column=2)
        self.hcrop_label = tk.Label(self, text='Bottom Crop(%):')
        self.hcrop_entry = tk.Entry(self)
        self.hcrop_label.grid(row=5, column=3)
        self.hcrop_entry.grid(row=6, column=3)

        self.grid(row=1, column=0, columnspan=2)

    def update_piece(self, piece):
        self.piece = piece
        self.clear()

        self.xpos_entry.insert(0, str(piece['x']))
        self.ypos_entry.insert(0, str(piece['y']))
        self.xscale_entry.insert(0, str(piece['x_scale']*100))
        self.yscale_entry.insert(0, str(piece['y_scale']*100))
        self.xcrop_entry.insert(0, str(piece['left_crop']*100))
        self.ycrop_entry.insert(0, str(piece['top_crop']*100))
        self.wcrop_entry.insert(0, str(piece['right_crop']*100))
        self.hcrop_entry.insert(0, str(piece['bottom_crop']*100))
        self.rotation_scale.set(piece['rotation'])
        self.trans_scale.set(piece['alpha'])

    def clear(self):
        self.xpos_entry.delete(0, tk.END)
        self.ypos_entry.delete(0, tk.END)
        self.xscale_entry.delete(0, tk.END)
        self.yscale_entry.delete(0, tk.END)
        self.xcrop_entry.delete(0, tk.END)
        self.ycrop_entry.delete(0, tk.END)
        self.wcrop_entry.delete(0, tk.END)
        self.hcrop_entry.delete(0, tk.END)
