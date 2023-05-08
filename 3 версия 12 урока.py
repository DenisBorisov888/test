import tkinter
import time
import math
from random import randint


canvas_width = 640
canvas_height = 480
default_initial_balls_number = 10
max_fire_energy = 200 # Условных единиц энергии при стрельбе
max_click_time = 2 #Секунд для набора энергии для выстрела
default_ball_color = "yellow"
missile_color = "red"

#-----------GAME MODEL:-----------
class Game :
    def __init__(self, initial_balls_number):
        self.initial_balls_number = initial_balls_number
        self.balls = [] #Список объектов типа Ball
        self.tank = Tank(canvas_width//2, canvas_height, "darkgreen")
        self.missiles = []

        self.t = 0
        self.dt = 0.05 #Квант модельного (расчётного) времени
        self.paused = True
        for i in range(initial_balls_number):
            ball = Ball(default_ball_color)
            self.balls.append(ball)

        self.click_time = None

    def start(self) :
        self.paused = False

    def stop(self) :
        self.paused = True

    def step(self) :
        global game_began #Доступ к флажку контроллера нужен для передачи ему информации, что игра окончилась
        # рассчет полета каждого шарика:

        for ball in self.balls:
            ball.step(self.dt)
        for missile in self.missiles:
            missile.step(self.dt)
        # рассчет столкновений шариков:
        for i in range(len(self.balls)):
            for k in range(i+1, len(self.balls)):
                if self.balls[i].intersect(self.balls[k]):
                    self.balls[i].collide(self.balls[k])
        #Удаляем шарики, в который попал снаряд
        for k in range(len(self.missiles) - 1, -1, -1):
            for i in range(len(self.balls) - 1, -1, -1):
                if self.missiles[k].intersect(self.balls[i]):
                    self.balls[i].delete()
                    self.balls.pop(i)
                    self.missiles[k].delete()
                    self.missiles.pop(k)
                    break

        #Факт конца игры
        if not self.balls :
            self.game_over()
            game_began = False
        self.t += self.dt

    def click(self, x, y) :
        #Подготовка к выстрелу танка.
        self.click_time = time.time()
        """for i in range(len(self.balls) - 1, -1, -1) :
            if self.balls[i].overlap(x, y) :
                self.balls[i].delete()
                self.balls.pop(i)"""

    def release(self, x, y):
        #Выстрел танка
        delta_t = time.time() - self.click_time #!!!_click или click???
        energy = max_fire_energy * (1 if delta_t > max_click_time else delta_t / max_click_time)

        self.tank.aim(x, y)
        missile = self.tank.fire(energy)
        self.missiles.append(missile)

    def mouse_motion(self, x, y):
        """
        При движении мышкой вызываем для танка его алгоритм прицеливания
        """
        self.tank.aim(x, y)

    def game_over(self) :
        for ball in self.balls:
            ball.delete()
        for missile in self.missiles:
            missile.delete()
        self.tank.delete()
        print("Конец игры!")


class Ball:
    density = 1.0 #Стандартная плотность

    def __init__(self, color) :
        self.r = randint(20, 50)
        self.m = self.density*math.pi*self.r**2 #Масса пропорциональна площади, т.е. квадрату радиуса.
        self.x = randint(0 + self.r, canvas_width - self.r)
        self.y = randint(0 + self.r, canvas_height - self.r)
        self.Vx = randint(-100, 100)
        self.Vy = randint(-100, 100)
        self.oval_id = canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill = color)

    def delete(self) :
        canvas.delete(self.oval_id)
        self.oval_id = None

    def step(self, dt):
        """
        Сдвигет шарик в соответствии с его скоростью
        """
        if self.oval_id is not None:
            Fx, Fy = self.force()
            ax = Fx / self.m
            ay = Fy / self.m

            self.x += self.Vx * dt + ax * dt**2 / 2
            self.y += self.Vy * dt + ay * dt**2 / 2
            self.Vx += ax * dt
            self.Vy += ay * dt

        if self.x + self.r >= canvas_width or self.x - self.r <= 0:
            self.Vx = -self.Vx
        if self.y + self.r >= canvas_height or self.y - self.r <= 0:
            self.Vy = -self.Vy
        canvas.coords(self.oval_id, (self.x - self.r, self.y - self.r,
                                     self.x + self.r, self.y + self.r))

    def force(self) :
        Fx = 0
        Fy = self.m * 9.8 #defauli gravity
        return Fx, Fy

    def overlap(self, x, y) :
        return (self.x - x)**2 + (self.y - y)**2 <= self.r**2

    def intersect(self, other) :
        return (self.x - other.x)**2 + (self.x - other.x)**2 <= (self.r + other.r)**2

    def collide(self, other):
        delta_r = ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
        ix = (other.x - self.x) / delta_r
        iy = (other.y - self.y) / delta_r
        Vself_normal = self.Vx * ix + self.Vy * iy
        Vother_normal = other.Vx * ix + other.Vy * iy
        self.Vx = self.Vx + (Vother_normal - Vself_normal) * ix
        self.Vy = self.Vy + (Vother_normal - Vself_normal) * iy
        other.Vx = other.Vx + (-Vother_normal + Vself_normal) * ix
        other.Vy = other.Vy + (-Vother_normal + Vself_normal) * iy

class Tank:
    """
    Танк, который прицеливается в заданную ему точку и порождает снаряды.
    """
    gun_lenght = 30
    turret_radius = 15
    gun_width = 8

    def __init__(self, x, y, color) :
        """
            x, y - точка центра турели
            dx, dy - вектор ствола танка
        """
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = -1
        self.turret_avatar = canvas.create_arc(self.x - self.turret_radius, self.y + self.turret_radius,
                                              self.x + self.turret_radius, self.y,
                                              start=0., extent = 180., fill = color)
        x1, y1, x2, y2 = self._gun_xy()
        self.gun_avatar = canvas.create_line(x1, y1, x2, y2, width = self.gun_width, fill = color)
        #TODO

    def _gun_xy(self):
        """
        :return: (x1, y1, x2, y2) экранные координаты начала и конца пушки
        """

        x1 = self.x + self.dx * self.turret_radius
        y1 = self.y + self.dy * self.turret_radius
        x2 = self.x + self.dx * self.gun_lenght
        y2 = self.y + self.dy * self.gun_lenght
        return x1, y1, x2, y2

    def aim(self, x, y):
        """Прицеливание ствола в сторону точки"""
        r = ((x - self.x)**2 + (y - self.y)**2)**0.5
        self.dx = (x - self.x) / r
        self.dy = (y - self.y) / r
        x1, y1, x2, y2 = self._gun_xy()
        canvas.coords(self.gun_avatar, x1, y1, x2, y2)

    def fire(self, energy) :
        """
        Стреляет снарядом, пораждая новый объект типа "снаряд"
        :param energy: Энергия выстрела - положительное дробное число
        :return: Снаряд, который будет поражать цели
        """
        missile = Ball(missile_color)
        x1, y1, x2, y2 = self._gun_xy()
        missile.x = x2
        missile.y = y2
        missile.r = self.gun_width // 2
        missile.Vx = self.dx * energy
        missile.Vy = self.dy * energy
        missile.step(0)
        return missile

    def delete(self) :
        canvas.delete(self.gun_avatar)
        self.gun_avatar = None
        canvas.delete(self.turret_avatar)
        self.turret_avatar = None


#------------------GAME CONTROLLER--------------------
#Режим игры - игра идёт или нет
game_began = False
sleep_time = 50 #миллисекунд
scores = 0


def tick() :
    time_label.after(sleep_time, tick)
    time_label["text"] = time.strftime("%H:%M:%S")
    if game_began:
        game.step()

def button_game_start_handler() :
    global game_began
    if not game_began:
        game.start()
        game_began = True

def button_game_stop_handler() :
    global game_began
    if game_began:
        game.stop()
        game_began = False

def mouse_click_handler(event) :
    if game_began :
        game.click(event.x, event.y)

def mouse_release_handler(event) :
    if game_began :
        game.release(event.x, event.y)

def mouse_motion_handler(event):
    if game_began:
        game.mouse_motion(event.x, event.y)

"""
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
"""

#-------------GAME VIEW-------------------

root = tkinter.Tk("Лопни шарик!")
buttons_panel = tkinter.Frame(bg = "gray", width = canvas_width)
buttons_panel.pack(side=tkinter.TOP, anchor="nw", fill=tkinter.X)
button_start = tkinter.Button(buttons_panel, text = "Start", command = button_game_start_handler)
button_start.pack (side = tkinter.LEFT)
button_stop = tkinter.Button(buttons_panel, text = "Stop", command = button_game_stop_handler)
button_stop.pack(side = tkinter.LEFT)
time_label = tkinter.Label(buttons_panel,font = "sans 14")
time_label.pack(side = tkinter.LEFT)
scores_text = tkinter.Label(buttons_panel, text = "Ваши очки: 0")
scores_text.pack(side = tkinter.RIGHT)
canvas = tkinter.Canvas(root, bg = "lightgray", width = canvas_width, height = canvas_height)
canvas.pack(anchor = "nw", fill = tkinter.BOTH, expand = 1)
canvas.bind("<Button - 1>", mouse_click_handler)
canvas.bind("<ButtonRelease - 1>", mouse_release_handler)
canvas.bind("<Motion>", mouse_motion_handler)

game = Game(default_initial_balls_number)

time_label.after_idle(tick)
root.mainloop()