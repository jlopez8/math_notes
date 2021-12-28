from pathlib import Path

import csv

from IPython.core.magic import register_line_magic

from IPython.display import Markdown as md

import tkinter as tk
from tkinter import Tk, Canvas, Button
import tkinter.font as font

from PIL import ImageDraw, Image

from math_notes import backend as be


def open_canvas(
    filename={"filename": ""}, width=1200, height=400, linewidth=3, linecolor="BLACK"
):
    """Opens a canvas widget using tkinter that allows a user to
    save their work.

    :param filename: Filename dictionary for parameters to access
                     where documents are saved, etc.
    :type filename: {}, optional

    :param width: Canvas width, defaults to 800.
    :type width: int, optional

    :param height: Canvas height, defaults to 600.
    :type height: int, optional

    :param linewidth: Canvas marker linewidth, defaults to 3.
    :type linewidth: int, optional

    :param linecolor: Canvas marker linecolor, defaults to black.
    :type linecolor: str, optional

    :return: List of string of latex prediciton.
    :rtype: [str]
    """

    def _latex_read():
        """Reads in prediction string saved by the backend ocr mechanism.

        :return: List of string of latex prediciton.
        :rtype: [str]
        """

        latex_readin = []
        filename = "cv_predict.csv"
        path = Path("./math_notes/predictions/")
        filepath = path / filename

        try:
            with open(filepath, newline="") as csvfile:
                csv_reader = csv.reader(csvfile)
                csv_reader.__next__()
                for row in csv_reader:
                    latex_readin.append(row[0])
        finally:
            return latex_readin

    def _save_posn(event):
        """Saves positional coordinates while drawing on canvas.

        :param event: Recorded mouse-click events for drawing.
        :type event: class tkinter.Event

        :return: none
        :rtype: none
        """

        global lastx, lasty
        lastx, lasty = event.x, event.y

    def _add_line(event):
        """Adds a line connection previous location while drawing to current location.

        Event here is where the mouse was and is located. Also draws the same line
        on a PIL image which represents the image drawn on the tkinter canvas by the
        user. This is the image that will actually be saved and used by the OCR.

        :param event: Recorded mouse-click events for drawing.
        :type event: class tkinter.Event

        :return: none
        :rtype: none
        """

        # This canvas call is what the user sees on the screen.
        canvas.create_line(
            (lastx, lasty, event.x, event.y),
            smooth=True,
            width=linewidth,
            fill=linecolor,
        )

        # The draw call is in the background (invisible)
        # capturing what will actually get converted to an image.
        draw.line(
            [lastx, lasty, event.x, event.y],
            fill=linecolor,
            width=linewidth,
            joint="curve",
        )
        _save_posn(event)

    global lastx, lasty

    root = Tk()
    root.title("Math Canvas")

    text = tk.StringVar()
    text.set("Prediction (ready): ")

    # Define the supporting paths.
    filename["path"] = Path("./math_notes/temp_files/")

    # Create the canvas.
    canvas_dimensions = str(width) + "x" + str(int(height * 1.5))
    root.geometry(canvas_dimensions)

    # Instantiate the tkinter canvas for users to draw on.
    canvas = Canvas(root, bg="white", width=width, height=height)
    canvas.grid(row=0, column=0)

    # PIL create an empty image and draw object to memory only.
    # It is not visible.
    canvas_image = Image.new("RGB", (width, int(height * 1.5)), (255, 255, 255))
    draw = ImageDraw.Draw(canvas_image)

    # Capturing mouse motion.
    canvas.bind("<Button-1>", _save_posn)
    canvas.bind("<B1-Motion>", _add_line)

    # Labels for readouts.
    row = 10
    label = tk.Label(root, textvariable=text, font=("helvetica", 18))
    label.grid(row=row + 3, column=0)

    # Buttons to save canvas, quit canvas, browse images.
    myFont = font.Font(family="SFMono-Regular", size=11)

    button_explore = Button(
        root,
        text="Select a file",
        command=lambda: be._browse_files(filename),
        height="2",
        width="12",
        font=myFont,
    )

    button_predict = Button(
        text="Predict LaTeX!",
        command=lambda: be._ocr_request_button(
            filename, canvas_image=canvas_image, text=text
        ),
        height="2",
        width="12",
        font=myFont,
    )

    button_quit = Button(
        text="Quit", command=lambda: be._quit(root), height="2", width="12", font=myFont
    )

    button_predict.grid(row=row, column=0)
    button_explore.grid(row=row + 1, column=0)
    button_quit.grid(row=row + 2, column=0)

    # Execute tkinter commands.
    root.mainloop()

    return _latex_read()


@register_line_magic
def mathnotes(line):
    filename = {"filename": ""}

    latex_return = []
    if line != "" and isinstance(line, str):
        filename = {"filename": line}
        latex_return = open_canvas(filename=filename)
    else:
        latex_return = open_canvas(filename={"filename": ""})

    if len(latex_return) > 0:
        latex_prediction = latex_return[0]
        latex_raw = " $ {latex_prediction} $ ".format(latex_prediction=latex_prediction)
        print("Raw LaTeX Prediction: ", latex_raw)
        print("\n\n")

        return md("$$ \\Huge {} $$".format(latex_prediction))
    
    return


if __name__ == "__main__":
    mathnotes()
