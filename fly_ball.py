import tkinter
import time
from random import randint

#Режим игры - игра идёт или нет
game_began = False
sleep_time = 50 #Милисекунды
scores = 0

oval_id = None
# single_ball = [x, y, dx, dy, r, oval_id]
single_ball = [10, 20, 4, 2, 10, None]
scores = 0


def tick() :
    time_label.after(sleep_time, tick)
    time_label["text"] = time.strftime("%H:%M:%S")
    if game_began:
        ball_step(single_ball)


def ball_step(ball):
    """
    Сдвигет шарик в соответствии с его скоростью
    :param ball: список [x, y, dx, dy, r, oval_id]
    """
    x, y, dx, dy, r, oval_id = ball
    if oval_id is not None:
        x += dx
        y += dy
        if x + r >= 639 or x - r <= 0:
            dx = -dx
        if y + r >= 479 or y - r <= 0:
            dy = -dy
        canvas.coords(oval_id, (x - r, y - r, x + r, y + r))
    ball[:] = x, y, dx, dy, r, oval_id


def button_start_game_handler () :
    global game_began
    if not game_began:
        start_game()
    game_began = True


def button_stop_game_handler () :
    global game_began
    if game_began:
        stop_game
        game_began = False


def start_game() :
    global single_ball
    ball_create(single_ball)


def stop_game() :
    ball_delete(single_ball)


def ball_create(ball) :
    x, y, dx, dy, r, oval_id = ball
    if oval_id is None:
        r = randint(10, 30)
        x = randint(0 + r, 639 - r)
        y = randint(0 + r, 479 - r)
        oval_id = canvas.create_oval(x - r, y - r, x + r, y + r, fill = "green")
    ball[:] = x, y, dx, dy, r, oval_id


def ball_delete() :
    #print("В этот момент исчезает...")
    canvas.delete(oval_id)
    oval_id = None
    ball[:] = x, y, dx, dy, r, oval_id


def click_handler(event) :
    global  x, y, r, scores_text, scores
    print(event.x, event.y)
    if oval_id is not None :
        if ((event.x - x)**2 + (event.y - y)**2) <= r**2 :
            print ("Попал!")
            scores += 100
            scores_text["text"] = "Ващи очки: " + str(scores)
            r = randint(10, 30)
            x = randint(0 + r, 639 - r)
            y = randint(0 + r, 479 - r)
        canvas.coords(oval_id, (x - r, y - r, x + r, y + r))


root = tkinter.Tk("Лопни шарик!")
root.geometry("640x480")

buttons_panel = tkinter.Frame(bg = "gray", width = "640")
buttons_panel.pack(side=tkinter.TOP, anchor="nw", fill=tkinter.X)
button_start = tkinter.Button(buttons_panel, text = "Start", command = button_start_game_handler)
button_start.pack (side = tkinter.LEFT)
button_stop = tkinter.Button(buttons_panel, text = "Stop", command = button_stop_game_handler)
button_stop.pack(side = tkinter.LEFT)

time_label = tkinter.Label(font = "sans 14")
time_label.pack(side = tkinter.LEFT)


scores_text = tkinter.Label(buttons_panel, text = "Ваши очки: 0")
scores_text.pack(side = tkinter.RIGHT)

canvas = tkinter.Canvas(root, bg = "lightgray")
canvas.pack(anchor = "nw", fill = tkinter.BOTH, expand = 1)
canvas.bind("<Button>", click_handler)

time_label.after_idle(tick)

root.mainloop()