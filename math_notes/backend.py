import base64
from pathlib import Path

import pandas as pd
from tkinter import filedialog
from PIL import Image

from math_notes import predict


def _browse_files(filename, text=""):
    """Opens a file system dialogue allowing a user to specify a file
    to send to the prediction service. Sets some parameters for the
    filename dictionary. Updates the text displayed with the chosen filename.

    :param filename: A dictionary of filename parameters
    for saving or supporting running predictions for the math canvas.
    :type filename: dictionary

    :param text: String variable object to display prediction result on canvas.
    :type text: tkinter StringVar object

    :return: none
    :rtype: none
    """

    new_text = ""

    init_browse_dir = Path.cwd()
    filename["filename"] = {}.get(filename["filename"], "")
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
        new_text = "File Chosen: " + filename["filename"]
    else:
        new_text = "File Chosen: No file selected."

    _update_prediction_label(text, new_text)


def _delete_folder(path):
    """Delete a directory

    :param path: Path do remove.
    :type path: pathlib.Path()

    :return: none
    :rtype: none
    """

    # Remove files and files in subdirectories.
    for sub in path.iterdir():
        if sub.is_dir():
            # Recursive call, DFS.
            _delete_folder(sub)
        else:
            sub.unlink()
    path.rmdir()


def _save_predictions(predictions, filename="cv_predict.csv"):
    """Save a list of LaTeX predictions to a csv.

    :param predictions: A list of strings of the latex predictions.
    :type predictions: List[str]

    :return: none
    :rtype: none
    """

    path = Path("math_notes/predictions/")
    if not path.exists():
        path.mkdir()

    saveas = path / filename

    headers = ["latex"]
    data = predictions

    df = pd.DataFrame(data=data, columns=headers)
    df.to_csv(saveas, index=False)


def _update_prediction_label(text, new_text):
    """Update the text label of the label on the tkinter window.

    :param text: String variable object to display on the canvas.
    :type text: tkinter StringVar object

    :param new_text: Text to modify object text with.
    :type new_text: str

    :return: none
    :rtype: none
    """

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
    isExist = directory.exists()
    if not isExist:
        directory.mkdir()

    filename_temp = "temp_saved_canvas.png"

    saveas = directory / filename_temp
    canvas_image.save(str(saveas))

    return filename_temp


def _ocr_request_button(
    filename,
    canvas_image=Image.new("RGB", (100, 100), (255, 255, 255)),
    test_mode=False,
    text="",
):
    """Calls the prediction service using the given filename in
    the temp_files directory.

    :param filename: Dictionary with the filename image location for the API.
    :type filename: dict of str

    :param test_mode: Boolean for testing mode. Use 'True' in
    test_mode to avoid pinging the API for costs.
    :type test_mode: Bool

    :param text: String variable object to display prediction result
    on canvas.
    :type text: tk.StringVar object

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
    temp_predict_path = Path("./math_notes/temp_files/")
    if temp_predict_path.exists():
        _delete_folder(temp_predict_path)

    _save_predictions(latex_return)

    # Print a success message.
    new_text = "Prediction complete: " + latex_return[0]
    _update_prediction_label(text, new_text)


def _quit(root):
    """Closes the canvas.

    :return: none
    :rtype: none
    """

    root.after(1, root.destroy())
