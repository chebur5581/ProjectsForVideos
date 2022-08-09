import pygame as pg
from random import randint, uniform
from remap import remap
import math


class Dot():
    def __init__(self, pos, angle, speed):
        self.x, self.y = pos
        self.angle = angle
        self.speed = speed

    def move(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        self.x += -self.speed * cos_a
        self.y += self.speed * sin_a


class App():
    def __init__(self, WIDTH=1300, HEIGHT=700):
        pg.init()
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT

        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()

        self.pause = False
        self.pause_pressed = False

        self.max_dist = 100
        self.max_line_width = 4

    def restart_dots(self):  # Функция рестарта точек которая создаёт нужные нам массивы с данными
        self.dots = []  # массив точек
        self.rows = randint(15, 18)  # количество строк с точками
        self.cols = randint(15, 18)  # количество столбиков с точками
        self.angles = [randint(0, 360) for i in range(0, self.rows * self.cols)]  # углы под которыми точки летят
        self.speeds = [uniform(0.1, 1.5) for i in
                       range(0, self.rows * self.cols)]  # скорости с которыми точки двигаются

        for y in range(0, self.rows):
            for x in range(0, self.cols):
                self.dots.append([y * self.rows * 4.5, x * self.cols * 4.5])

    def keys(self):
        key = pg.key.get_pressed()
        if key[pg.K_g]:
            self.restart_dots()
        if key[pg.K_h]:
            self.dots.clear()
            self.speeds.clear()
            self.angles.clear()
        if key[pg.K_SPACE] and not self.pause_pressed:
            self.pause_pressed = True
            self.pause = not self.pause
        if not key[pg.K_SPACE] and self.pause_pressed:
            self.pause_pressed = False

    def run(self):
        self.restart_dots()
        while True:
            self.screen.fill((200, 200, 200))

            self.keys()

            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
                if i.type == pg.MOUSEBUTTONDOWN:
                    if i.button == 1:
                        self.dots.append([pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]])
                        self.angles.append(randint(0, 360))
                        self.speeds.append(uniform(0.1, 1.5))

            for m_dot in self.dots:
                for dot in self.dots:
                    distance = int(math.sqrt(((m_dot[0] - dot[0]) ** 2) + ((m_dot[1] - dot[1]) ** 2)))
                    if distance <= 130:
                        pg.draw.line(self.screen, (100, 100, 100), m_dot, dot,
                                     int(remap(distance, 0, self.max_dist, self.max_line_width, 0)))

            for dts in enumerate(self.dots):
                dot = Dot(dts[1], self.angles[dts[0]], self.speeds[dts[0]])

                if not self.pause:
                    dot.move()

                if dot.x >= self.WIDTH:
                    dot.angle = 0
                if dot.x < 0:
                    dot.angle = 91.1
                if dot.y < 0:
                    dot.angle = 300
                if dot.y >= self.HEIGHT:
                    dot.angle = 290.5

                self.dots[dts[0]] = [dot.x, dot.y]
                pg.draw.circle(self.screen, (220, 50, 130), (dot.x, dot.y), 4)

            pg.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()
