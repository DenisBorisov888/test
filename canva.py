import tkinter

def create_ball() :
    canvas.create_oval(100, 100, 200, 200)

root = tkinter.Tk("Главное окно")
root.geometry("640x480")

canvas = tkinter.Canvas(root)
canvas.pack()

button_start = tkinter.Button(root, text="Start", command=create_ball)
button_start.pack()



root.mainloop()