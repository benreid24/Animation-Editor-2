import tkinter as tk
from view import util
from controller import interpolate as controller


class InterpolateControls(tk.LabelFrame):
    def _apply(self):
        try:
            total_time = int(self.time.get())
            frame_len = int(self.frame_len.get())
            frame = int(self.frame.get()) - 1
        except:
            util.error('Input must be integers')
            return

        if total_time <= 0 or frame_len <= 0:
            util.error('Times must be greater than 0')
        controller.apply(frame, total_time, frame_len)

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text='Interpolate Frames')

        self.time = tk.StringVar()
        self.time_label = tk.Label(self, text='Time (ms):')
        self.time_entry = tk.Entry(self, textvariable=self.time)
        self.time_label.grid(row=0, column=0)
        self.time_entry.grid(row=0, column=1)

        self.frame_len = tk.StringVar()
        self.len_label = tk.Label(self, text='Frame Length (ms):')
        self.len_entry = tk.Entry(self, textvariable=self.frame_len)
        self.len_entry.insert(0, '16')
        self.len_label.grid(row=0, column=2)
        self.len_entry.grid(row=0, column=3)

        self.frame = tk.StringVar()
        self.frame_label = tk.Label(self, text='Start Frame (interpolates to following frame):')
        self.frame_entry = tk.Entry(self, textvariable=self.frame)
        self.frame_label.grid(row=1, column=0, columnspan=2)
        self.frame_entry.grid(row=1, column=2)

        self.apply_but = tk.Button(self, text='Generate Frames', command=self._apply, background='#ff5555')
        self.apply_but.grid(row=1, column=3, padx=5)

        self.grid(row=3, column=0)
