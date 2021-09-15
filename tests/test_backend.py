import os
from pathlib import Path

import csv

from math_notes import predict, backend

from tkinter import Tk, Canvas
from PIL import ImageGrab, ImageTk, ImageDraw
import PIL

width = 600
height = 400
center = height // 2
white = (255, 255, 255)    

def test_save():
    canvas_image = PIL.Image.new("RGB", (width, height), white)
    backend.save_canvas(canvas_image)
    assert backend.filename["name"].is_file()
    

def test_save_predictions():
    predictions = ["x", "\\int_0^\\intfy 1/x^2 dx"]
    backend.save_predictions(predictions)
    filename = "outputs.csv"
    my_file = Path(filename)
    os.remove(my_file)


def test_user_input():
    path = backend.user_input(user_choice=3)
    print("path is path:", path)
    assert "" == path