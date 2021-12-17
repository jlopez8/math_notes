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
    filename = "tests/data/img_x.png"

    # Call _ocr_request_button with test_mode to avoid
    # pinging the prediction service, which is tested
    # in `tests_predict.py`.
    backend._ocr_request_button(filename, test_mode=True)

    path = Path("math_notes/temp_files/cv_predict.csv")
    file = open(path)
    csv_reader = csv.reader(file)

    next(csv_reader)

    rows = []
    for row in csv_reader:
        rows.append(row)
    file.close()

    assert rows[0][0] == "x"


def test_save_canvas():
    canvas_image = PIL.Image.new("RGB", (width, height), white)
    draw = ImageDraw.Draw(canvas_image)

    # Draw an x by specifying some lines.
    coords = [275, 165, 604, 390]
    draw.line(
        coords,
        fill="BlACK",
        width=3,
        joint=None,
    )

    coords = [coords[0], coords[3], coords[2], coords[1]]
    draw.line(
        coords,
        fill="BlACK",
        width=3,
        joint=None,
    )

    filename["path"] = Path("tests/data/")
    filename["filename"] = "test_save_canvas_x.png"
    backend._save_canvas(filename, canvas_image)

    file = filename["path"] / filename["filename"]

    assert file.is_file()


def test_save_predictions():
    predictions = ["x", "\\int_0^\\intfy 1/x^2 dx", "ax+b=y"]
    path = Path("temp_files/cv_saved_predict.csv")
    backend._save_predictions(predictions, path=path)

    file = open(path)
    csv_reader = csv.reader(file)

    next(csv_reader)

    rows = []
    for row in csv_reader:
        rows.append(row)
    file.close()

    for i in range(len(rows)):
        assert rows[i][0] == predictions[i]

    assert path.is_file()
