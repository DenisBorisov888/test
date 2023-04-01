from graphics import *

win_width = 600
win_height = 500

def main() :
    picture_backbround()
    draw_cloud(100, 100)
    draw_sun()
    draw_house(win_width//3, win_height*2//3, 150, 200)
    draw_tree()

def picture_backbround() :
    sky = Rectangle(Point(0,0), Point(win_width, win_height//2))
    sky.setWidth(0)
    sky.setFill("blue")
    sky.draw(win)
    ground = Rectangle(Point(0,win_height//2), Point(win_width, win_height//2))
    ground.setWidth(0)
    ground.setFill("lightgray")
    ground.draw(win)
    
def draw_cloud(x0, y0) :
    cloud_circles = [(x0 - 30, y0, 40), (x0, y0 - 10, 50), (x0 + 30, y0, 40)]
    for x, y, r in cloud_circles:
        c_circle = Circle(Point(x,y), r)
        c_circle.setFill("white")
        c_circle.draw(win)


def draw_sun() :
    pass

def draw_house(x0, y0, width, height) :
    walls_height = height*2//3
    roof_height = height - walls_height
    draw_walls(x0, y0, width, walls_height)
    draw_window(x0, y0 - walls_height//3, width, walls_height//3)
    draw_roof(x0, y0 - walls_height, width, roof_height)

def draw_walls(x0, y0, width, height) :
    walls = Rectangle(Point(x0 - width//2, y0 - height), Point(x0 + width//2, y0//2))
    walls.setWidth(0)
    walls.setFill("gray")
    walls.draw(win)

def draw_window(x0, y0, width, height) :
    window = Rectangle(Point(x0 - width//2, y0 - height), Point(x0 + width//2, y0//2))
    window.setWidth(3)
    window.setFill("yellow")
    window.draw(win)

def draw_roof(x0, y0, width, height) :
    coordinates = [(x0 - width//2, y0), (x0, y0 - height), (x0+width//2, y0)]
    points = [Point(x, y) for x, y in coordinates]
    roof = Polygon(points)
    roof.setFill("darkred")
    roof.draw(win)

    

def draw_tree() :
    pass

win = GraphWin("Картина", 600, 400)
main()       
cursor_point = win.getMouse()
win.close()
