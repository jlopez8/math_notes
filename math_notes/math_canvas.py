import os
import base64

from pathlib import Path

import csv

import tkinter as tk
from tkinter import Tk, Canvas, ttk, Button, filedialog, Label
from tkinter import constants as con

from PIL import ImageGrab, ImageTk, ImageDraw, Image

import requests
import json

from math_notes import backend as be


def open_canvas(
    filename={"filename": ""}, width=1200, height=400, linewidth=3, linecolor="BLACK"
):
    """Opens a canvas widget using tkinter that allows a user to
    save their work.

    :param filename: Filename dictionary for parameters to access
                     where documents are saved, etc.
    :type filename: {}, optional

    :param width: Canvas width, defaults to 800.
    :type width: int, optional

    :param height: Canvas height, defaults to 600.
    :type height: int, optional

    :param linewidth: Canvas marker linewidth, defaults to 3.
    :type linewidth: int, optional

    :param linecolor: Canvas marker linecolor, defaults to black.
    :type linecolor: str, optional

    :return: none
    :rtype: none
    """

    def _save_posn(event):
        """Saves positional coordinates while drawing on canvas.

        :param event: Recorded mouse-click events for drawing.
        :type event: class tkinter.Event

        :return: none
        :rtype: none
        """

        global lastx, lasty
        lastx, lasty = event.x, event.y

    def _add_line(event):
        """Adds a line connection previous location while drawing to current location.

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
        _save_posn(event)

    global lastx, lasty

    # Define the supporting paths.
    filename["path"] = Path("./math_notes/temp_files/")

    # Create the canvas.
    root = Tk()
    canvas_dimensions = str(width) + "x" + str(int(height * 1.5))
    root.geometry(canvas_dimensions)

    # Instantiate the tkinter canvas for users to draw on.
    canvas = Canvas(root, bg="white", width=width, height=height)
    canvas.pack()

    # PIL create an empty image and draw object to memory only.
    # It is not visible.
    canvas_image = Image.new("RGB", (width, int(height * 1.5)), (255, 255, 255))
    draw = ImageDraw.Draw(canvas_image)
    canvas.pack(expand=True, fill="both")

    # Capturing mouse motion.
    canvas.bind("<Button-1>", _save_posn)
    canvas.bind("<B1-Motion>", _add_line)

    # Buttons to save canvas, quit canvas, browse images.
    button_explore = Button(
        root, text="Browse Files", command=lambda: be._browse_files(filename)
    )

    button_quit = Button(text="Quit", command=lambda: be._quit(root))

    button_predict = Button(
        text="Predict LaTeX!",
        command=lambda: be._ocr_request_button(filename, canvas_image=canvas_image),
    )

    # Layout.
    button_predict.pack()
    button_explore.pack()
    button_quit.pack()

    root.mainloop()


def main():
    FILENAME = {}
    open_canvas(FILENAME)


if __name__ == "__main__":
    main()
