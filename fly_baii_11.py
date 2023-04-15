import tkinter
import time
from random import randint

#Режим игры - игра идёт или нет
game_began = False
sleep_time = 50 #Милисекунды
scores = 0



#------------------GAME CONTROLLER--------------------
def tick() :
    time_label.after(sleep_time, tick)
    time_label["text"] = time.strftime("%H:%M:%S")
    if game_began:
        game_step()



def button_game_start_handler () :
    global game_began
    if not game_began:
        game_start()
    game_began = True


def button_game_stop_handler () :
    global game_began
    if game_began:
        game_stop()
        game_began = False


#-----------GAME MODEL:-----------
initial_balls_number = 5
balls = []


def game_start() :
    for i in range(initial_balls_number):
        ball = Ball()
        balls.append(ball)


def game_stop() :
    for ball in balls:
        ball.delete()


def game_step() :
    for ball in balls:
        ball.step()

class Ball:
    def __init__(self) :
        self.r = randint(10, 30)
        self.x = randint(0 + self.r, 639 - self.r)
        self.y = randint(0 + self.r, 479 - self.r)
        self.dx = randint(-4, 4)
        self.dy = randint(-4, 4)
        self.oval_id = canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill = "green")

def delete(self) :
    canvas.delete(self.oval_id)
    self.oval_id = None

def step(self):
    """
    Сдвигет шарик в соответствии с его скоростью
    """
    if self.oval_id is not None:
        self.x += self.dx
        self.y += self.dy
        if self.x + self.r >= 639 or self.x - self.r <= 0:
            self.dx = -self.dx
        if self.y + self.r >= 479 or self.y - self.r <= 0:
            self.dy = -self.dy
        canvas.coords(self.oval_id, (self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r))

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


#-------------GAME VIEW-------------------
root = tkinter.Tk("Лопни шарик!")
root.geometry("640x480")

buttons_panel = tkinter.Frame(bg = "gray", width = "640")
buttons_panel.pack(side=tkinter.TOP, anchor="nw", fill=tkinter.X)
button_start = tkinter.Button(buttons_panel, text = "Start", command = button_game_start_handler)
button_start.pack (side = tkinter.LEFT)
button_stop = tkinter.Button(buttons_panel, text = "Stop", command = button_game_stop_handler)
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