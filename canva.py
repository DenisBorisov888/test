import tkinter

oval_id = None

def create_ball() :
    global oval_id
    if oval_id is None :
        oval_id = canvas.create_oval(10, 10, 20, 20, fill = "green")
    else :
        print("ПРЕДУПРЕЖДЕНИЕ: Овал уже создан! Не надо сюда кликать!")

def delete_ball() :
    global oval_id
    print("В этот момент исчезает...")
    canvas.delete(oval_id)
    oval_id = None

root = tkinter.Tk("Главное окно")
root.geometry("640x480")

canvas = tkinter.Canvas(root)
canvas.pack()

button_start = tkinter.Button(root, text="Start", command=create_ball)
button_start.pack()



root.mainloop()