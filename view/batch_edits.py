import tkinter as tk

from view import util
from controller import batch as controller


class BatchEdits(tk.LabelFrame):
    def _change_ranges(self, _1, _2, _3):
        if self.change_type.get() == 0:
            self.rotation_scale.config(from_=-180, to=180)
            self.rotation_scale.set(0)
            self.trans_scale.config(from_=-255, to=255)
            self.trans_scale.set(0)
        else:
            self.rotation_scale.config(from_=-100, to=100)
            self.rotation_scale.set(0)
            self.trans_scale.config(from_=-100, to=100)
            self.trans_scale.set(0)

    def _clear(self):
        self.change_type.set(0)
        self.xpos.set('')
        self.ypos.set('')
        self.fframe.set('')
        self.lframe.set('')
        self.xscale.set('')
        self.yscale.set('')
        self.frame_len.set('')

    def _apply(self):
        start_frame = self.fframe.get() if self.fframe.get() else 0
        end_frame = self.lframe.get() if self.lframe.get() else 0
        frame_len = self.frame_len.get() if self.frame_len.get() else 0
        xpos = self.xpos.get() if self.xpos.get() else 0
        ypos = self.ypos.get() if self.ypos.get() else 0
        xscale = self.xscale.get() if self.xscale.get() else 0
        yscale = self.yscale.get() if self.yscale.get() else 0
        alpha = self.trans_scale.get()
        rot = self.rotation_scale.get()

        try:
            start_frame = int(start_frame)
            end_frame = int(end_frame)
            frame_len = int(frame_len)
            xpos = float(xpos)
            ypos = float(ypos)
            xscale = float(xscale)
            yscale = float(yscale)
        except:
            util.error('Input needs to be blank or numerical')
            return

        start_frame = start_frame-1 if start_frame != 0 else start_frame
        end_frame = end_frame - 1
        controller.batch_edit(
            self.frame_sel.get(), start_frame, end_frame, self.change_type.get(),
            frame_len, xpos, ypos, xscale, yscale, alpha, rot
        )

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text='Batch Edit')

        self.frame_sel = tk.IntVar()
        self.frame_but = tk.Checkbutton(self, text='Selected Piece Only', variable=self.frame_sel)
        self.frame_but.grid(row=0, column=0)

        self.clear_but = tk.Button(self, text='Clear', command=self._clear)
        self.clear_but.grid(row=0, column=1, padx=3)
        self.apply_but = tk.Button(self, text='Apply', command=self._apply, background='#ff5555')
        self.apply_but.grid(row=0, column=2, padx=3)

        self.change_type = tk.IntVar()
        self.change_type.trace('w', self._change_ranges)
        self.type_box = tk.Checkbutton(self, text='Percent Change', var=self.change_type)
        self.type_box.grid(row=0, column=3, rowspan=1, pady=10)

        self.fframe = tk.StringVar()
        self.lframe = tk.StringVar()
        self.fframe_label = tk.Label(self, text='First Frame:')
        self.fframe_entry = tk.Entry(self, textvariable=self.fframe)
        self.fframe_label.grid(row=1, column=0)
        self.fframe_entry.grid(row=1, column=1)
        self.lframe_label = tk.Label(self, text='Last Frame:')
        self.lframe_entry = tk.Entry(self, textvariable=self.lframe)
        self.lframe_label.grid(row=1, column=2)
        self.lframe_entry.grid(row=1, column=3)

        self.frame_len = tk.StringVar()
        self.frame_len_label = tk.Label(self, text='Frame Length:')
        self.frame_len_entry = tk.Entry(self, textvariable=self.frame_len)
        self.frame_len_entry.grid(row=2, column=1)
        self.frame_len_label.grid(row=2, column=0)

        self.xpos = tk.StringVar()
        self.ypos = tk.StringVar()
        self.xpos_label = tk.Label(self, text='X Pos:')
        self.xpos_entry = tk.Entry(self, textvariable=self.xpos)
        self.xpos_label.grid(row=3, column=0)
        self.xpos_entry.grid(row=4, column=0)
        self.ypos_label = tk.Label(self, text='Y Pos:')
        self.ypos_entry = tk.Entry(self, textvariable=self.ypos)
        self.ypos_label.grid(row=3, column=1)
        self.ypos_entry.grid(row=4, column=1)

        self.xscale = tk.StringVar()
        self.yscale = tk.StringVar()
        self.xscale_label = tk.Label(self, text='X Scale %:')
        self.xscale_entry = tk.Entry(self, textvariable=self.xscale)
        self.xscale_label.grid(row=3, column=2)
        self.xscale_entry.grid(row=4, column=2)
        self.yscale_label = tk.Label(self, text='Y Scale %:')
        self.yscale_entry = tk.Entry(self, textvariable=self.yscale)
        self.yscale_label.grid(row=3, column=3)
        self.yscale_entry.grid(row=4, column=3)

        self.rotation_scale = tk.Scale(self, from_=-180, to=180, resolution=1, orient=tk.HORIZONTAL, label='Rotation')
        self.rotation_scale.set(0)
        self.rotation_scale.grid(row=2, column=2)
        self.trans_scale = tk.Scale(self, from_=-255, to=255, resolution=1, orient=tk.HORIZONTAL, label='Opacity')
        self.trans_scale.set(0)
        self.trans_scale.grid(row=2, column=3)

        self.grid(row=2, column=0, columnspan=2, pady=20)
