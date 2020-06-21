import pygame
from random import randint
from enum import Enum,unique
from math import sqrt


#@unique
class Color(Enum):
    """颜色"""

    RED = (255,0,0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (242, 242, 242)

    @staticmethod
    def random_color():
        """获得随机颜色"""
        r = randint(0,255)
        g = randint(0,255)
        b = randint(0,255)
        return (r,g,b)

class Ball(object):
    """球"""
    def __init__(self, x, y, radius, sx, sy, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.sx = sx
        self.sy = sy
        self.color = color
        self.alive = True

    def move(self,screen):
        """move"""
        self.x += self.sx
        self.y += self.sy
        if self.x - self.radius <= 0 or self.x + self.radius >= screen.get_width():
            self.sx = -self.sx
        if self.y - self.radius <= 0 or self.y + self.radius >= screen.get_height():
            self.sy = -self.sy

    def eat(self,other):
        """eat other ball"""
        if self.alive and other.alive and self != other:
            dx, dy = self.x - other.x, self.y - other.y
            distance = sqrt(dx ** 2 + dy ** 2)
            if distance < self.radius + other.radius and self.radius > other.radius:
                other.alive = False
                self.radius = self.radius + int(other.radius * 0.144)
    def draw(self, screen):
        """draw the ball on the window"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


def main():
    balls = []
    #初始化导入pygame模块
    pygame.init()
    #初始化游戏的屏幕
    screen = pygame.display.set_mode((1000,750))
    print('The height of the window is %s' %screen.get_height())
    print('The width of the window is %s' %screen.get_width())
    #设置当前窗口的名字
    pygame.display.set_caption('Big ball eats Small ball')
    #初始化球上来的位置
    x,y = 50,50
    #开启一个事件循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #处理鼠标事件
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x,y = event.pos
                radius = randint(10,100)
                sx, sy = randint(-10,10), randint(-10,10)
                color = Color.random_color()
                ball = Ball(x, y, radius, sx, sy, color)
                balls.append(ball)

        screen.fill((120,242,42))

        for ball in balls:
            if ball.alive:
                ball.draw(screen)
            else:
                balls.remove(ball)
        pygame.display.flip()
        #每隔50ms改变球的位置并刷新窗口
        pygame.time.delay(50)
        for ball in balls:
            ball.move(screen)
            for other in balls:
                ball.eat(other)

if __name__ == '__main__':
    main()