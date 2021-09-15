import os

import csv

from tkinter import Tk, Canvas, ttk, Button
from tkinter import constants as con

from pathlib import Path

from math_notes import predict

filename = {}

def browseFiles():
    """Opens a file system dialogue allowing a user to specify a file to send to the prediction service. 
    """
    
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
    text = "filename = " + filename["name"]
    text = Label(text=text, font=("helvetica", 18))
    text.pack()

def save_canvas():
    """Saves a canvas file.
    """
    
    filename["name"] = Path("temp_files/cv_temp.png")
    filename["path"] = Path("temp_files/")

    if not os.path.isdir( filename["path"]):
        os.mkdir(filename["path"])
    
    canvas_image.save(str(filename["name"]))
    text = Label(
        text="File was saved as: " + str(filename["name"]), font=("helvetica", 25)
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
        
        
def quit():
    root.destroy()