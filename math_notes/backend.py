import os
import shutil
import base64
from pathlib import Path
import logging

import csv
import tkinter as tk
from tkinter import Tk, Canvas, ttk, Button, Label, filedialog, StringVar
from tkinter import constants as con

from PIL import Image

from math_notes import predict


def _browse_files(filename):
    """Opens a file system dialogue allowing a user to specify a file to send to the prediction service.
    Sets some parameters for the filename dictionary.

    :param filename: A dictionary of filename parameters for saving or supporting running predictions for the math canvas.
    :type filename: dictionary

    :return: none
    :rtype: none
    """

    init_browse_dir = os.getcwd()
    filename["filename"] = get(filename["filename"], "")
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


def _save_predictions(predictions, filename="cv_predict.csv"):
    """Save a list of LaTeX predictions to a csv.

    :param predictions: A list of strings of the latex predictions.
    :type predictions: List[str]

    :return: none
    :rtype: none
    """
    path = Path("math_notes/predictions/")
    if not os.path.isdir(path):
        os.mkdir(path)

    saveas = path / filename

    headers = ["latex"]
    data = predictions
    with open(saveas, "w", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(headers)
        for i in range(len(data)):
            latex = data[i]
            writer.writerow([latex])
    file.close()


def _update_prediction_label(text, new_text):
    if not text == "":
        text.set(new_text)


def _save_canvas_temp(canvas_image):
    """Captures whatever is on the canvas currently for immediate prediction.

    :param canvas_image: Image to capture drawing.
    :type canvas_image: PIL image object

    :return: String of temporary filename.
    :rtype: str
    """

    directory = Path("math_notes/temp_files/")
    if not os.path.isdir(directory):
        os.mkdir(directory)

    filename_temp = "temp_saved_canvas.png"

    saveas = directory / filename_temp
    canvas_image.save(str(saveas))

    return filename_temp


def _latex_read(filename):
    latex_readin = []

    filename = "cv_predict.csv"
    path = Path("./math_notes/predictions/")
    filepath = path / filename
    with open(filepath, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        csv_reader.__next__()
        for row in csv_reader:
            latex_readin.append(row[0])
    
    return latex_readin


def _ocr_request_button(
    filename,
    canvas_image=Image.new("RGB", (100, 100), (255, 255, 255)),
    test_mode=False,
    text="",
):
    """Calls the prediction service using the given filename in the temp_files directory.

    :param filename: Dictionary with the filename image location to be sent to the API.
    :type filename: dict of str

    :param test_mode: Boolean for testing mode. Use 'True' in test_mode to avoid pinging the API unnecessary multiple costs.
    :type test_mode: Bool

    :return: none
    :rtype: none
    """

    latex_return = [""]
    filepath = filename["path"] / filename["filename"]

    # Force saving a canvas if a file wasn't selected by the browser.
    if filename["filename"] == "":
        filename_temp = _save_canvas_temp(canvas_image)
        filepath = Path("./math_notes/temp_files/") / filename_temp

    image_uri = (
        "data:image/png;base64,"
        + base64.b64encode(open(filepath, "rb").read()).decode()
    )
    images = [image_uri]

    if not test_mode:

        latex_return = predict._predict(images)
    else:
        latex_return = ["x"]

    # Remove the temporary directory for storing the canvas image.
    try:
        mydir = Path("./math_notes/temp_files/")
        shutil.rmtree(mydir)
    except OSError as e:
        logging.error("Error: %s - %s." % (e.filename, e.strerror))

    _save_predictions(latex_return)

    # Print a success message.
    new_text = "Prediction complete: " + latex_return[0]
    _update_prediction_label(text, new_text)
    

def _quit(root):
    """Closes down the canvas.

    :return: none
    :rtype: none
    """

    root.destroy()
