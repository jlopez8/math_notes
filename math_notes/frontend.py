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

from math_notes import config as cfg

# Mathpix API key details.
app_id = cfg.APP_ID
app_key = cfg.APP_KEY


def ocr_request(filename):
    """Sends an API request to MathPix API to be handled by the OCR.

    :param filename: Filename of the image to be sent to the MathPix API for a LaTeX prediction.
    :type filename: str

    :return: Latex-formatted string.
    :rtype: str
    """

    dict_request = {
        "src": "data:image/png",
        "formats": ["text", "data", "html"],
        "data_options": {"include_asciimath": True, "include_latex": True},
    }

    # Put desired filename from earlier.
    image_uri = (
        "data:image/png;base64,"
        + base64.b64encode(open(filename, "rb").read()).decode()
    )

    # Send the request.
    r = requests.post(
        "https://api.mathpix.com/v3/text",
        data=json.dumps({"src": image_uri}),
        headers={
            "app_id": app_id,
            "app_key": app_key,
            "Content-type": "application/json",
        },
    )

    json_return = json.loads(r.text)
    latex_return = json_return.get("latex_styled")

    return latex_return


def pilot_canvas(master,
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


    
    def browseFiles():
        init_browse_dir = os.getcwd()
        filename["name"] = filedialog.askopenfilename(
            initialdir=init_browse_dir,
            title="Select a File",
            filetypes=(
                ("png files", ".png"),
                ("jpg files", ".jpg"),
                ("all files", "*.*"),
            ),
        )

        canvas.destroy()
        text = Label(text=filename, font=("helvetica", 18))
        text.pack()

    def ocr_request_button(filename):
        """Calls the ocr_request function defined above. This prints the returned LaTeX to
        the command line.

        :param filename: String with the filename image location to be sent to the API.
        :type filename: str
        """

        latex_return = ocr_request(filename)
        print("latex_return: ")
        print(latex_return)

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
