# This was directly imported from http://localhost:8888/lab/tree/work_book/end_to_end_script.py

# Change it up to remove unecesary components, clean up code, remove unused functionality

import os
import sys
import base64

from pathlib import Path

import csv

import tkinter as tk
from tkinter import Tk, Canvas, ttk, Button, filedialog, Label
from tkinter import constants as con

from PIL import ImageGrab, ImageTk, ImageDraw, Image

import requests
import json

import backend as be

import config as cfg

def open_canvas(width=1200,
                 height=400,
                 linewidth=3,
                 linecolor="BLACK"):
    
    """Opens a canvas widget using tkinter that allows a user to save their work.

    :param width: Canvas width, defaults to 800.
    :type width: int, optional

    :param height: Canvas height, defaults to 600.
    :type height: int, optional

    :param linewidth: Canvas marker linewidth, defaults to 3.
    :type linewidth: int, optional

    :param linecolor: Canvas marker linecolor, defaults to black.
    :type linecolor: str, optional

    :return: Dictionary of filename where canvas was saved.
    :rtype: dict
    """

    offset = linewidth / 2
    filename = {}
    
    root = Tk()
    canvas_dimensions = str(width) + "x" + str(int(height*1.5))
    root.geometry(canvas_dimensions)

    # Instantiate the tkinter canvas to draw on.
    canvas = Canvas(root, bg="white", width=width, height=height)
    canvas.pack()

    # PIL create an empty image and draw object to draw on memory only.  It is not visible.
    canvas_image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(canvas_image)

    canvas.pack(expand=True, fill="both")
    canvas.bind("<Button-1>", be.save_posn)
    canvas.bind("<B1-Motion>", be.add_line)

    # Buttons to save canvas, quit canvas, browse images.
    button_explore = Button(root, text="Browse Files", command=be.browse_files)
    button_save = Button(text="Save Image", command=lambda: be.save_canvas(canvas_image=canvas_image))
    button_quit = Button(text="Quit", command=lambda: be.quit(root))
    
    # >> This will complicate the way things are done
    button_predict = Button(
        text="Predict LaTeX!",
        command=lambda: be.ocr_request_button(filename=filename["name"]),
    )

    button_explore.pack()
    button_save.pack()
    button_quit.pack()
    button_predict.pack()

    root.mainloop()
    
# This modifier may be needed for the actual testing???
def start_application():
#     root = tk.Tk()
    app = open_canvas()
    return app
    #return app # will return the application without starting the main loop.

if __name__ == '__main__':
    start_application()
#     app