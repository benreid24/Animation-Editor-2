import tkinter as tk

from controller import actions as controller
from controller import files as files_controller
from controller import frames as frames_controller


class Actions(tk.LabelFrame):
    def _check(self):
        try:
            sel = int(self.action_list.curselection()[0])
            if sel != self.last_selection:
                self.last_selection = sel
                controller.set_action_index(sel)
        except:
            self.set_active(controller.get_action_index())
        self.after(100, self._check)

    def _loop_chg(self):
        frames_controller.update_looping(self.looping_type.get())

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text='Extras', padx=3, pady=3)

        self.pos_label = tk.Label(self, text='Mouse Position: ()')
        self.pos_label.grid(row=0, column=3, columnspan=1)

        self.undo_button = tk.Button(self, text='Undo', command=controller.undo)
        self.redo_button = tk.Button(self, text='Redo', command=controller.redo)
        self.preview_button = tk.Button(self, text='Preview', command=files_controller.preview, background='#5555ff')
        self.undo_button.grid(row=1, column=1, pady=4, padx=3)
        self.redo_button.grid(row=1, column=2, pady=4, padx=3)
        self.preview_button.grid(row=1, column=3, padx=60)

        self.looping_type = tk.IntVar()
        self.loop_but = tk.Checkbutton(self, text='Loop on Finish', variable=self.looping_type, command=self._loop_chg)
        self.loop_but.grid(row=2, column=3)

        self.action_list_frame = tk.LabelFrame(self, text='Actions')
        self.scrollbar = tk.Scrollbar(self.action_list_frame)

        self.action_list = tk.Listbox(self.action_list_frame, yscrollcommand=self.scrollbar.set, exportselection=False)
        self.action_list.pack(side=tk.LEFT, fill=tk.BOTH)

        self.after(100, self._check)
        self.last_selection = 0

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.action_list.yview)
        self.action_list_frame.grid(column=0, row=0, rowspan=3, padx=3)

        self.grid(row=4, column=0, padx=3, pady=20)

    def set_action_list(self, al):
        self.action_list.delete(0, tk.END)
        self.action_list.selection_clear(0, tk.END)
        for a in al:
            self.action_list.insert(tk.END, a)

    def set_active(self, i):
        self.action_list.selection_clear(0, tk.END)
        if i in range(0, self.action_list.size()):
            self.action_list.select_set(i)
            self.last_selection = i

    def clear(self):
        self.action_list.delete(0, tk.END)
        self.last_selection = 0

    def set_pos(self, x, y):
        self.pos_label.config(text='Mouse Position: ({}, {})'.format(x, y))

    def set_is_loop(self, is_loop):
        self.looping_type.set(1 if is_loop else 0)
