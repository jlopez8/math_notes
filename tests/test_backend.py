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
    backend.filename["name"] = "tests/data/img_x.png"
    backend.ocr_request_button(backend.filename["name"])
    
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
    draw = ImageDraw.Draw(canvas_image)
    
    # Draw an x by specifying some lines.
    coords = [275, 165, 604, 390]
    draw.line(
        coords,
        fill='BlACK',
        width=3,
        joint=None,
    )
    coords = [coords[0], coords[3], coords[2], coords[1]]
    draw.line(
        coords,
        fill='BlACK',
        width=3,
        joint=None,
    )
    
    path = Path("temp_files/cv_temp.png")
    backend.save_canvas(canvas_image, path)

    assert path.is_file() 
    
def test_save_predictions():
    predictions = ["x", "\\int_0^\\intfy 1/x^2 dx", "ax+b=y"]
    path = Path("temp_files/cv_saved_predict.csv")
    backend.save_predictions(predictions, path = path)
    
    file = open(path)
    csv_reader = csv.reader(file)

    header = []
    header = next(csv_reader)

    rows = []
    for row in csv_reader:
        rows.append(row)
    file.close()
    
    for i in range(len(rows)):
        assert rows[i][0] == predictions[i]
        
    assert path.is_file()
