width = 600
height = 400
center = height//2
white = (255, 255, 255)
background = 'white'
green = (0,128,0)

def save():
    filename = rnd_image_filename(N=5)
    canvas_image.save(filename)

def paint(event):
    # python_green = "#476042"
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    cv.create_oval(x1, y1, x2, y2,fill="black",width=2)
    draw.line([x1, y1, x2, y2],fill="black",width=2)

root = Tk()

# Tkinter create a canvas to draw on
cv = Canvas(root, width=width, height=height, bg=background)
cv.pack()

# PIL create an empty image and draw object to draw on
# memory only, not visible
canvas_image = PIL.Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(canvas_image)

# do the Tkinter canvas drawings (visible)
# cv.create_line([0, center, width, center], fill='green')

cv.pack(expand=True, fill="both")
cv.bind("<B1-Motion>", paint)

# do the PIL image/draw (in memory) drawings
# draw.line([0, center, width, center], green)

# PIL image can be saved as .png .jpg .gif or .bmp file (among others)
# filename = "my_drawing.png"
# image1.save(filename)
button=Button(text="save",command=save)
button.pack()
root.mainloop()

print("Complete canvas input and image save.")
