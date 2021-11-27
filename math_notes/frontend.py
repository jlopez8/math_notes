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

# Mathpix API key details.
app_id = cfg.APP_ID
app_key = cfg.APP_KEY

def open_canvas(master,
                 width=800,
                 height=600,
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





    def save():
        """Saves a canvas file after appending with string of N
         random characters for uniquness.

        :param N: Number of random characters to append, defaults to 5.
        :type N: int
        """

        filename["name"] = "temp_files/cv_temp.png"
        canvas_image.save(filename["name"])

        text = Label(
            text="File was saved as: " + filename["name"], font=("helvetica", 25)
        )
        text.pack()

    def save_posn(event):
        """Saves positional coordinates of object event.

        :param event: Recorded mouse-click events for drawing.
        :type event: class tkinter.Event

        :return: none
        :rtype: none
        """

        global lastx, lasty
        lastx, lasty = event.x, event.y

    def quit():
        root.destroy()

    def add_line(event):
        """Adds a line connection previous location of event to current event location.
        Event here is where the mouse was and is located. Also draws the same line
        on a PIL image which represents the image drawn on the tkinter canvas by the
        user. This is the image that will actually be saved and used by the OCR.

        :param event: Recorded mouse-click events for drawing.
        :type event: class tkinter.Event

        :return: none
        :rtype: none
        """

        # This canvas call is what the user sees on the screen.
        canvas.create_line(
            (lastx, lasty, event.x, event.y),
            smooth=True,
            width=linewidth,
            fill=linecolor,
        )

        # The draw call is in the background (invisible)
        # capturing what will actually get converted to an image.
        draw.line(
            [lastx, lasty, event.x, event.y],
            fill=linecolor,
            width=linewidth,
            joint="curve",
        )
        save_posn(event)

    offset = linewidth / 2
    filename = {}

    root = Tk()
    root.geometry("900x800")

    # Instantiate the tkinter canvas to draw on.
    canvas = Canvas(root, bg="white", width=width, height=height)
    canvas.pack()

    # PIL create an empty image and draw object to draw on memory only.  It is not visible.
    canvas_image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(canvas_image)

    canvas.pack(expand=True, fill="both")
    canvas.bind("<Button-1>", save_posn)
    canvas.bind("<B1-Motion>", add_line)

    # Buttons to save canvas, quit canvas, browse images.
    button_explore = Button(root, text="Browse Files", command=browseFiles)
    button_save = Button(text="Save Image", command=save)
    button_quit = Button(text="Quit", command=quit)
    button_predict = Button(
        text="Predict LaTeX!",
        command=lambda: ocr_request_button(filename=filename["name"]),
    )

    button_explore.pack()
    button_save.pack()
    button_quit.pack()
    button_predict.pack()

    root.mainloop()
    
# This modifier may be needed for the actual testing???
def start_application() -> pilot_canvas:
    root = tk.Tk()
    app = pilot_canvas(master=root)
    return app # will return the application without starting the main loop.
