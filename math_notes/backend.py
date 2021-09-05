import csv

from tkinter import Tk, Canvas, ttk, Button
from tkinter import constants as con

from math_notes import predict


def save(canvas_image, filename="tests/temp_canvas_img.png"):
    """Saves a canvas file after appending with string of
    random characters for uniquness.
    """
    canvas_image.save(filename)


def paint(event):
    """Places a dot at each mouse location corresponding to the click event.
    On the draw object, adds a line connection nearby locations of where the
    event occurs. This latter image is saved and represents the image drawn
    on the tkinter canvas by the user.

    :param event: Recorded mouse-click events for drawing.
    :type event: class tkinter.Event
    """
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    cv.create_oval(x1, y1, x2, y2, fill="black", width=2)
    draw.line([x1, y1, x2, y2], fill="black", width=2)


def save_posn(event):
    """Saves positional coordinates of object event.

    :param event: Recorded mouse-click events for drawing.
    :type event: class tkinter.Event
    """
    global lastx, lasty
    lastx, lasty = event.x, event.y


def add_line(event):
    """Adds a line connection previous location of event to current event location.
    Event here is where the mouse was and is located.

    :param event: Recorded mouse-click events for drawing.
    :type event: class tkinter.Event
    """
    canvas.create_line((lastx, lasty, event.x, event.y))
    save_posn(event)


def save_predictions(predictions):
    """Save a list of LaTeX predictions to a csv.

    :param predictions: A list of strings of the latex predictions.
    :type predictions: List[str]

    :return: none
    :rtype: none
    """
    headers = ["latex"]
    with open("outputs.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for i in range(len(predictions)):
            latex = predictions[i]
            writer.writerow(latex)

        file.close()


def user_input(user_choice=3):
    """Prompts the user to decide how they would like to provide an image to the math OCR.
    They can either write on a canvas and save the file for predictions or
    specify a directory with multiple images

    :param width: Canvas width, defaults to 800.
    :type width: int, optional

    :return: Path containing images for prediction.
    :rtype: str
    """
    if not bool(user_choice):
        user_choice = int(
            input(
                "Enter '1' for receiving a handraw canvas or '2' provide an image path for Math OCR or '3' to exit: \n"
            )
        )

    if user_choice == 1:
        pilot_canvas()
        path = "./temp_files"
    elif user_choice == 2:
        path = input("Provide image directory: ")
    elif user_choice == 3:
        path = ""
    return path


def quit():
    root.destroy()
