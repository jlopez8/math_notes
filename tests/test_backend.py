from pathlib import Path

import pandas as pd
from math_notes import backend

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

    df = pd.DataFrame()
    df = pd.read_csv(r"{filepath}".format(filepath=predict_file))

    assert df["latex"][0] == "x"
    backend._delete_folder(path_predictions)


def test_save_predictions():
    predictions = ["x", "\\int_0^\\intfy 1/x^2 dx", "ax+b=y"]

    filename = "test_cv_saved_predict.csv"
    path_predictions = Path("./math_notes/predictions/")

    backend._save_predictions(predictions, filename=filename)

    filepath = path_predictions / filename
    df = pd.DataFrame()
    df = pd.read_csv(r"{filepath}".format(filepath=filepath))

    for i in range(len(df.index)):
        assert df["latex"][i] == predictions[i]

    assert filepath.is_file()
    backend._delete_folder(path_predictions)
