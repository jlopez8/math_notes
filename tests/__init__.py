"""Unit test package for math_notes."""
import os
from pathlib import Path
import shutil

import pytest


@pytest.fixture(scope="module")
def cfg_setup():

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


@pytest.fixture(scope="module")
def cfg_teardown():

    # For now this is in configs.
    path = Path("./tests_configs/")

    # Teardown.
    if os.path.isdir(path):
        shutil.rmtree(path)
