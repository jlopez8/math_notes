import os
import csv
import base64

from pathlib import Path

from tkinter import Tk, Canvas, ttk, Button, Label, filedialog
from tkinter import constants as con

from PIL import Image

# from math_notes import predict
import predict

filename = {}
filename["path"] = Path("temp_files/")
if not os.path.isdir(filename["path"]):
    os.mkdir(filename["path"])


def browse_files():
    """Opens a file system dialogue allowing a user to specify a file to send to the prediction service."""

    init_browse_dir = os.getcwd()
    filename = filedialog.askopenfilename(
        initialdir=init_browse_dir,
        title="Select a File",
        filetypes=(
            ("png files", ".png"),
            ("jpg files", ".jpg"),
            ("all files", "*.*"),
        ),
    )
    text = "filename = " + filename
    text = Label(text=text, font=("helvetica", 18))
    text.pack()


def save_predictions(predictions, path=Path("temp_files/cv_predict.csv")):
    """Save a list of LaTeX predictions to a csv.

    :param predictions: A list of strings of the latex predictions.
    :type predictions: List[str]

    :return: none
    :rtype: none
    """

    filename = path
    headers = ["latex"]
    data = predictions
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(headers)
        for i in range(len(data)):
            latex = data[i]
            writer.writerow([latex])
    file.close()


def save_canvas(
    canvas_image=Image.new("RGB", (100, 100), (255, 255, 255)),
    path=Path("temp_files/cv_temp.png"),
):
    """Saves a canvas file to a temporary directory.

    :param canvas_image: Image to capture drawing.
    :type canvas_image: Pil image object
    """

    filename = path
    canvas_image.save(filename)
    text = Label(
        text="File was saved as: " + str(filename), font=("helvetica", 25)
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


def ocr_request_button(filename="temp_files/canvas_temp.png", test_mode=False):
    """Calls the prediction service using the given filename in the temp_files directory.

    :param filename: String with the filename image location to be sent to the API.
    :type filename: str

    :param test_mode: Boolean for testing mode. Use 'True' in test_mode to avoid pinging the API unnecessary multiple costs.
    :type test_mode: Bool
    """

    image_uri = (
        "data:image/png;base64,"
        + base64.b64encode(open(filename, "rb").read()).decode()
    )
    images = [image_uri]
    if not test_mode:
        latex_return = predict.predict(images)
    else:
        latex_return = ["x"]

    save_predictions(latex_return)


def quit(root):
    root.destroy()
