import os
from pathlib import Path
import base64
import shutil

import pytest

from math_notes import predict


@pytest.fixture(scope="module")
def cfg_setup_teardown():

    # For now this is in configs.
    path = Path("./tests_configs/")

    # Setup.
    if not os.path.isdir(path):
        os.mkdir(path)

    filename = "app_key2.txt"
    filepath = path / filename
    mode = "w+"
    file_object = open(filepath, mode)
    for i in range(1):
        file_object.write("app_dummy_email_dot_com")
    file_object.close()

    filename = "app_id2.txt"
    filepath = path / filename
    mode = "w+"
    file_object = open(filepath, mode)
    for i in range(1):
        file_object.write("ABCDEFGHIJKLMNOP1234567890")
    file_object.close()

    yield

    # For now this is in configs.
    path = Path("./tests_configs/")

    # Teardown.
    if os.path.isdir(path):
        shutil.rmtree(path)


def test_prediction_single(cfg_setup_teardown):

    filename = "tests/data/integral_to_transform_1.png"
    true_latex_string = "f(x)=\\int_{a}^{x} t^{3}+1 d t"

    image_uri = []
    image_uri.append(
        "data:image/png;base64,"
        + base64.b64encode(open(filename, "rb").read()).decode()
    )
    latex_return = predict._predict(image_uri)

    assert latex_return[0] == true_latex_string


def test_prediction_multiple(cfg_setup_teardown):

    filenames = [
        "tests/data/integral_to_transform_1.png",
        "tests/data/integral_to_transform_2.png",
        "tests/data/integral_to_transform_3.png",
    ]

    true_latex_strings = ["f(x)=\\int_{a}^{x} t^{3}+1 d t", "x^{2}+1=0", "a x+b=y"]

    image_uri = []
    for file in filenames:
        image_uri.append(
            "data:image/png;base64,"
            + base64.b64encode(open(file, "rb").read()).decode()
        )
    latex_returns = predict._predict(image_uri)

    assert latex_returns == true_latex_strings
