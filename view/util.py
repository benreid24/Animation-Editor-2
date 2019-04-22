import os

import tkinter.messagebox as mbox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter as tk

EXPORT_DIR = os.getcwd() + '/Resources/Media/Animations'
print(EXPORT_DIR)


def popup(title, message):
    mbox.showinfo(title, message)


def error(message):
    mbox.showerror('Error', message)


def yesnobox(question):
    return mbox.askyesno('WTF', question) == tk.YES


def get_image_file():
    return askopenfilename(
        title='Add Image',
        filetypes=[
            ('Images', '*.jpg *.png')
        ]
    )


def get_open_anim_file(folder=''):
    return askopenfilename(
        title='Open Animation',
        filetypes=[('DevAnims', '*.danim')],
        initialdir=folder
    )


def get_save_devanim_file(folder=''):
    return asksaveasfilename(
        title='Save Animation',
        defaultextension='.danim',
        filetypes=[('DevAnims', '*.danim')],
        initialdir=folder
    )


def get_export_file(folder=''):
    return asksaveasfilename(
        title='Export Animation',
        defaultextension='.anim',
        filetypes=[('Animations', '*.anim')],
        initialdir=EXPORT_DIR
    )
