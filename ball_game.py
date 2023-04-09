import tkinter

def hello(event) :
    print("Left click at:{0}, {1}".format(event.x, event.y))

def bye(event) :
    print("Bye, World!")

root = tkinter.Tk() #Создание главного окна
button1 = tkinter.Button(master = root, text = "Нажми меня!")
button1.pack()

root.bind("<Button-1>", hello)
root.bind("<Button-3>", bye)

 

root.mainloop()
