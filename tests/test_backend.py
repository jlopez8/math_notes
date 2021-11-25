import os

import csv
from pathlib import Path

from math_notes import predict, backend

from tkinter import Tk, Canvas
from PIL import ImageGrab, ImageTk, ImageDraw
import PIL

width = 1200
height = 400
center = height // 2
white = (255, 255, 255)

def test_submission():
    # Mimics browsing for a file.
    backend.filename["name"] = "tests/data/img_for_testing.png"
    backend.ocr_request_button(backend.filename["name"])
    
    # >>DEV
    # here test this file resulted in a saved prediction. 
    # math_notes(project)/temp_files/cv_predict.csv
    
    path = Path("temp_files/cv_predict.csv")
    file = open(path)

    csv_reader = csv.reader(file)

    header = []
    header = next(csv_reader)

    rows = []
    for row in csv_reader:
        rows.append(row)
    file.close()
    
    assert rows[0][0] == 'x'
        
def test_save_canvas():
    # Draw on a canvas.
    canvas_image = PIL.Image.new("RGB", (width, height), white)
    
    # 
    
    backend.save_canvas(canvas_image)
    assert backend.filename["name"].is_file()
    
# def test_save_file

# def test_save_predictions():
#     predictions = ["x", "\\int_0^\\intfy 1/x^2 dx"]
#     backend.save_predictions(predictions)
#     filename = "outputs.csv"
#     my_file = Path(filename)
#     os.remove(my_file)


# def test_user_input():
#     path = backend.user_input(user_choice=3)
#     print("path is path:", path)
#     assert "" == path
