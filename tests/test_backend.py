import os

import csv
from pathlib import Path

from math_notes import backend

from PIL import ImageDraw
import PIL

width = 1200
height = 400
center = height // 2
white = (255, 255, 255)

filename = {}


def test_submission():
    # Mimics browsing for a file.
    file = "img_x.png"
    path = Path("./tests/data/")
    path_predictions = Path("./math_notes/predictions/")

    filename = {"filename": file, "path": path, "path_predictions": path_predictions}

    # Call _ocr_request_button with test_mode to avoid
    # pinging the prediction service, which is tested
    # in `tests_predict.py`.
    backend._ocr_request_button(filename, test_mode=True)

    filename_predictions = "cv_predict.csv"
    predict_file = path_predictions / filename_predictions
    file = open(predict_file)
    csv_reader = csv.reader(file)

    next(csv_reader)

    rows = []
    for row in csv_reader:
        rows.append(row)
    file.close()

    assert rows[0][0] == "x"

    os.remove(os.path.join(path_predictions, filename_predictions))


def test_save_predictions():
    predictions = ["x", "\\int_0^\\intfy 1/x^2 dx", "ax+b=y"]

    path_predictions = Path("./math_notes/predictions/")
    filename = "test_cv_saved_predict.csv"
    backend._save_predictions(predictions, path=path_predictions, filename=filename)

    filepath = path_predictions / filename
    file = open(filepath)
    csv_reader = csv.reader(file)

    next(csv_reader)

    rows = []
    for row in csv_reader:
        rows.append(row)
    file.close()

    for i in range(len(rows)):
        assert rows[i][0] == predictions[i]

    assert filepath.is_file()

    os.remove(os.path.join(path_predictions, filename))
