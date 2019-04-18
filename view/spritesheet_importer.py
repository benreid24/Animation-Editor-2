import tkinter as tk
from PIL import ImageTk

from view import util
from controller import images as controller


class SpritesheetImporter(tk.Toplevel):
    def _validate_input(self):
        x = self.x_entry.get()
        y = self.y_entry.get()
        w = self.w_entry.get()
        h = self.h_entry.get()
        rows = self.row_entry.get()
        cols = self.col_entry.get()

        try:
            x = int(x)
            y = int(y)
            w = int(w)
            h = int(h)
            rows = int(rows)
            cols = int(cols)
        except:
            util.error('Input must be integers')
            return None

        if x < 0 or y < 0 or w <= 0 or h <= 0 or rows <= 0 or cols <= 0:
            util.error('Input must be positive')
            return None

        return x, y, w, h, rows, cols

    def _clear_grid(self):
        for line_id in self.line_ids:
            self.canvas.delete(line_id)
        self.line_ids = []

    def _preview(self):
        user_input = self._validate_input()
        if user_input:
            x, y, w, h, rows, cols = user_input
            self._clear_grid()

            width = cols * w
            height = rows * h
            for row in range(0, rows+1):
                self.line_ids.append(
                    self.canvas.create_line(
                        x,
                        y + row * h,
                        x + width,
                        y + row * h,
                        fill='#ff2222',
                        width=3
                    )
                )
            for col in range(0, cols+1):
                self.line_ids.append(
                    self.canvas.create_line(
                        x + col * w,
                        y,
                        x + col * w,
                        y + height,
                        fill='#ff2222',
                        width=3
                    )
                )

    def _import(self):
        user_input = self._validate_input()
        if user_input:
            x, y, w, h, rows, cols = user_input
            controller.import_spritesheet(self.file, self.sheet, x, y, w, h, rows, cols)
            self.destroy()

    def __init__(self, root, sheet_file, sheet):
        tk.Toplevel.__init__(self, root)
        self.title('Import Spritesheet')
        self.iconbitmap('resources/icon.ico')

        self.but_frame = tk.Frame(self)
        self.file = sheet_file
        self.sheet = sheet
        self.sheet_tk = ImageTk.PhotoImage(self.sheet)

        w, h = self.sheet.size
        self.canvas = tk.Canvas(self, width=w, height=h)
        self.sheet_id = self.canvas.create_image(0, 0, image=self.sheet_tk, anchor=tk.NW)
        self.line_ids = []

        self.x_label = tk.Label(self.but_frame, text="Start X")
        self.y_label = tk.Label(self.but_frame, text="Start Y")
        self.x_entry = tk.Entry(self.but_frame)
        self.y_entry = tk.Entry(self.but_frame)
        self.x_entry.insert(0, '0')
        self.y_entry.insert(0, '0')
        self.x_label.grid(row=0, column=0, padx=3, pady=2)
        self.x_entry.grid(row=1, column=0, padx=3, pady=2)
        self.y_label.grid(row=0, column=1, padx=3, pady=2)
        self.y_entry.grid(row=1, column=1, padx=3, pady=2)

        self.w_label = tk.Label(self.but_frame, text="Cell Width")
        self.h_label = tk.Label(self.but_frame, text="Cell Height")
        self.w_entry = tk.Entry(self.but_frame)
        self.h_entry = tk.Entry(self.but_frame)
        self.w_label.grid(row=0, column=2, padx=3, pady=2)
        self.w_entry.grid(row=1, column=2, padx=3, pady=2)
        self.h_label.grid(row=0, column=3, padx=3, pady=2)
        self.h_entry.grid(row=1, column=3, padx=3, pady=2)

        self.row_label = tk.Label(self.but_frame, text="# Rows")
        self.col_label = tk.Label(self.but_frame, text="# Columns")
        self.row_entry = tk.Entry(self.but_frame)
        self.col_entry = tk.Entry(self.but_frame)
        self.row_label.grid(row=0, column=4, padx=3, pady=2)
        self.row_entry.grid(row=1, column=4, padx=3, pady=2)
        self.col_label.grid(row=0, column=5, padx=3, pady=2)
        self.col_entry.grid(row=1, column=5, padx=3, pady=2)

        self.prev_but = tk.Button(self.but_frame, text='Show Cells', command=self._preview, background='#55ff55')
        self.import_but = tk.Button(self.but_frame, text='Import', command=self._import, background='#ff5555')
        self.prev_but.grid(row=0, column=6, padx=3, pady=2)
        self.import_but.grid(row=1, column=6, padx=3, pady=2)

        self.but_frame.pack()
        self.canvas.pack()
        self.update()
