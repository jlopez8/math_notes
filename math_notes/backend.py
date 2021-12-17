import os
import base64

import csv
from pathlib import Path

from tkinter import Tk, Canvas, ttk, Button, Label, filedialog
from tkinter import constants as con

from PIL import Image

from math_notes import predict


def _browse_files(filename):
    """Opens a file system dialogue allowing a user to
    specify a file to send to the prediction service.6

    :return: none
    :rtype: none
    """

    init_browse_dir = os.getcwd()
    filename["filename"] = ""
    filename["filename"] = filedialog.askopenfilename(
        initialdir=init_browse_dir,
        title="Select a File",
        filetypes=(
            ("png files", ".png"),
            ("jpg files", ".jpg"),
            ("all files", "*.*"),
        ),
    )

    if filename["filename"] != "":
        text = "filename = " + filename["filename"]
    else:
        text = "No file selected."

    text = Label(text=text, font=("helvetica", 18))
    text.pack()


def _save_predictions(predictions, path=Path("math_notes/temp_files/cv_predict.csv")):
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


def _save_canvas(filename, canvas_image=Image.new("RGB", (100, 100), (255, 255, 255))):
    """Saves a canvas file to a temporary directory.

    :param canvas_image: Image to capture drawing.
    :type canvas_image: Pil image object

    :return: none
    :rtype: none
    """

    if not os.path.isdir(filename["path"]):
        directory = "math_notes/temp_files/"
        os.mkdir(directory)

    if filename["filename"] == "":
        filename["filename"] = "/saved_canvas.png"

    saveas = filename["path"] / filename["filename"]
    canvas_image.save(str(saveas))

    text = Label(text="File was saved as: " + str(saveas), font=("helvetica", 25))
    text.pack()


def _ocr_request_button(filename="", test_mode=False):
    """Calls the prediction service using the given filename in the temp_files directory.

    :param filename: String with the filename image location to be sent to the API.
    :type filename: str

    :param test_mode: Boolean for testing mode. Use 'True' in test_mode to avoid pinging the API unnecessary multiple costs.
    :type test_mode: Bool

    :return: none
    :rtype: none
    """

    if filename == "":
        latex_return = [""]

    else:
        image_uri = (
            "data:image/png;base64,"
            + base64.b64encode(open(filename, "rb").read()).decode()
        )
        images = [image_uri]
        if not test_mode:
            latex_return = predict.predict(images)
        else:
            latex_return = ["x"]

    _save_predictions(latex_return)


def _quit(root):
    """Closes down the canvas.

    :return: none
    :rtype: none
    """

    root.destroy()
