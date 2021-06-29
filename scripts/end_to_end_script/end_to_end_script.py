import os
import sys
import base64
from pathlib import Path

import csv

from tkinter import Tk, Canvas, ttk, Button
from tkinter import constants as con

from PIL import ImageGrab, ImageTk, ImageDraw, Image

import requests
import json

sys.path.insert(1, '../../configs/')
import config as cfg

# Mathpix API key details.
app_id = cfg.math_pix_key["app_id"]  
app_key = cfg.math_pix_key["app_key"]

def ocr_request(filename):
    """Sends an API request to MathPix API to be handled by the OCR .
    
    :param filename: Filename of the image to be sent to the MathPix API for a LaTeX prediction.
    :type filename: str
 
    :return: Latex-formatted string.
    :rtype: str
    """
    
    dict_request={
            "src": "data:image/png",
            "formats": ["text", "data", "html"],
            "data_options": {
            "include_asciimath": True,
            "include_latex": True
            }
        }

    # Put desired filename from earlier.
    image_uri = "data:image/png;base64," + base64.b64encode(open(filename, "rb").read()).decode()

    # Send the request.
    r = requests.post("https://api.mathpix.com/v3/text",
                      data=json.dumps({'src': image_uri}),
                      headers={"app_id": app_id, 
                               "app_key": app_key,
                               "Content-type": "application/json"})
    
    json_return = json.loads(r.text)
    latex_return = json_return.get("latex_styled")
    
    return latex_return

def pilot_canvas(width=800, height=600, linewidth = 3, linecolor="BLACK"):
    """Opens a canvas widget using tkinter that allows a user to save their work.
    
    :param width: Canvas width, defaults to 800.
    :type width: int, optional
     
    :param height: Canvas height, defaults to 600.
    :type height: int, optional
        
    :param linewidth: Canvas marker linewidth, defaults to 3.
    :type linewidth: int, optional
     
    :param linecolor: Canvas marker linecolor, defaults to black.
    :type linecolor: str, optional
    
    :return: Dictionary of filename where canvas was saved.
    :rtype: dict
    """
    
    def save():
        """Saves a canvas file after appending with string of N 
         random characters for uniquness.
    
        :param N: Number of random characters to append, defaults to 5.
        :type N: int
        """
        
        filename= "temp_files/cv_temp.png"
        canvas_image.save(filename)
        print("File was saved as: ", filename)

    def save_posn(event):
        """Saves positional coordinates of object event.
        
        :param event: Recorded mouse-click events for drawing.
        :type event: class tkinter.Event
        
        :return: none
        :rtype: none
        """

        global lastx, lasty
        lastx, lasty = event.x, event.y
    
    def quit():
        root.destroy()

    def add_line(event):
        """Adds a line connection previous location of event to current event location.
        Event here is where the mouse was and is located. Also draws the same line
        on a PIL image which represents the image drawn on the tkinter canvas by the 
        user. This is the image that will actually be saved and used by the OCR.
        
        :param event: Recorded mouse-click events for drawing.
        :type event: class tkinter.Event
        
        :return: none
        :rtype: none
        """
        # This canvas call is what the user sees on the screen. 
        canvas.create_line((lastx, lasty, event.x, event.y),
                           smooth=True, width=linewidth, fill=linecolor)
        
        # The draw call is in the background (invisible) 
        # capturing what will actually get converted to an image.
        draw.line([lastx, lasty, event.x, event.y], fill=linecolor, width=linewidth, joint='curve')
        save_posn(event)
        
    offset = (linewidth)/2
    filename = {}

    root = Tk()

    # Instantiate the tkinter canvas to draw on. 
    canvas = Canvas(root, bg="white", width=width, height=height)
    canvas.pack()
    
    # PIL create an empty image and draw object to draw on memory only.  It is not visible.
    canvas_image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(canvas_image)

    canvas.pack(expand=True, fill="both")
    canvas.bind("<Button-1>", save_posn)
    canvas.bind("<B1-Motion>", add_line)
    
    button_save = Button(text="Save Image", command=save)
    button_quit = Button(text="Quit", command=quit)
    button_save.pack()
    button_quit.pack()

    root.mainloop()
    
def save_predictions(predictions):
    """Save a list of LaTeX predictions to a csv.
    
    :param predictions: A list of strings of the latex predictions.
    :type predictions: List[str]
    
    :return: none
    :rtype: none
    """
    headers = ["latex"]
    with open('outputs.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)   
        for i in range(len(predictions)):
            latex = predictions[i]
            writer.writerow(latex)
            
        file.close()

def user_input():
    """Promptes the user to decide how they would like to provide an image to the math OCR. They can decide to write on a canvas and save the file for predictions or to specify a directory with multiple images
    
    :param width: Canvas width, defaults to 800.
    :type width: int, optional
    
    :return: Path containing images for prediction. 
    :rtype: str
    """
    
    user_choice = int(input("Enter '1' for receiving a handraw canvas or '2' provide an image path for Math OCR or '3' to exit: \n"))
    
    if user_choice == 1:
        pilot_canvas()
        path = "./temp_files"
    elif user_choice==2:
        path = input("Provide image directory: ")
    elif user_choice == 3:
        path = "" 
    return path
    
def main(path):
    """Initiates mechanisms for converting hand-written math to Latex.
    
    :param path: Path to image(s) to pass-on to the API.
    :type path: str
    
    :return: none
    :rtype: none
    """
    if path == "":
        print("Exit code 0.")
    else:
        predictions = []

        for image in Path(path).iterdir():
            if image.is_file():
                latex_pred = [ocr_request(image)]
                predictions.append(latex_pred)
            
        save_predictions(predictions)
            
if __name__ == '__main__':
    path = user_input()
    main(path=path)