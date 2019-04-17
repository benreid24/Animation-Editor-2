import tkinter as tk

from controller import frames as controller


class FrameOptions(tk.LabelFrame):
    def _check(self):
        try:
            sel = int(self.frame_list.curselection()[0])
            if sel != self.last_selection:
                self.last_selection = sel
                controller.change_active_frame()
        except:
            self.set_active(controller.active_frame_index())
        self.after(100, self._check)

    def _entry_updated(self, _1, _2, _3):
        if len(self.time_val.get()) > 0:
            controller.update_frame()

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text='Frame Options', padx=3, pady=3)

        self.ins_button = tk.Button(self, text='New (insert)', command=controller.new_frame_insert)
        self.app_button = tk.Button(self, text='New (append)', command=controller.new_frame_append)
        self.clone_button = tk.Button(self, text='Clone Current', command=controller.clone_frame)
        self.delete_button = tk.Button(self, text='Delete Current', command=controller.delete_frame)
        self.up_button = tk.Button(self, text='Move Up', command=controller.move_frame_up)
        self.down_button = tk.Button(self, text='Move Down', command=controller.move_frame_down)
        self.ins_button.grid(row=0, column=0, pady=4, padx=3)
        self.app_button.grid(row=0, column=1)
        self.clone_button.grid(row=0, column=2)
        self.delete_button.grid(row=1, column=2)
        self.up_button.grid(row=0, column=3)
        self.down_button.grid(row=1, column=3)

        self.time_val = tk.StringVar()
        self.time_val.trace('w', self._entry_updated)
        self.len_label = tk.Label(self, text='Length(ms):')
        self.len_entry = tk.Entry(self, textvariable=self.time_val)
        self.len_label.grid(row=2, column=1)
        self.len_entry.grid(row=2, column=2)

        self.frame_list_frame = tk.LabelFrame(self, text='Frames')
        self.scrollbar = tk.Scrollbar(self.frame_list_frame)

        self.frame_list = tk.Listbox(self.frame_list_frame, yscrollcommand=self.scrollbar.set, exportselection=False)
        self.frame_list.insert(tk.END, '1')
        self.frame_list.select_set(0)
        self.frame_list.pack(side=tk.LEFT, fill=tk.BOTH)

        self.set_active(0)
        self.after(100, self._check)
        self.last_selection = 0

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.frame_list.yview)
        self.frame_list_frame.grid(column=4, row=0, rowspan=3, padx=3)

        self.grid(row=0, column=0, padx=3, pady=20)

    def set_frame_count(self, c):
        if c < self.frame_list.size():
            self.frame_list.delete(c, tk.END)
        else:
            for i in range(self.frame_list.size(), c):
                self.frame_list.insert(tk.END, str(i+1))

    def set_active(self, i):
        self.frame_list.selection_clear(0, tk.END)
        self.frame_list.select_set(i)
        self.last_selection = i

    def get_selected_index(self):
        selected = self.frame_list.curselection()
        return int(selected[0])

    def clear(self):
        self.frame_list.delete(0, tk.END)
        self.frame_list.insert(tk.END, '1')
        self.frame_list.select_set(0)
        self.time_val.set('50')
        self.last_selection = 0

    def get_length_str(self):
        return self.time_val.get()

    def set_length(self, l):
        self.time_val.set(str(l))
