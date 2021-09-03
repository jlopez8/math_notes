from pathlib import Path

from math_notes.predict import predict

from PIL import ImageGrab, ImageTk, ImageDraw
import PIL

def test_save():
    filename = "tests/test_save.png"
    my_file = Path(filename)
    canvas_image = PIL.Image.new("RGB", (600, 400), (255, 255, 255))
    canvas_image.save(filename)
    
    assert my_file.is_file()

    
    
    >> # delete the image in this case
    
# def test_paint():
    
# def test_save_posn():
    
# def test_add_line():
    
# def test_save_predictions():
    
# def test_user_input():
    
    