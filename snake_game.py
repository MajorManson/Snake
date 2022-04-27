from math import floor
import pygame
from random import uniform

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

WIDTH = 800
HEIGHT = 600
FPS = 15

RUNNING = True
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.update()

score_font = pygame.font.SysFont('arial', 35)


class Snake(object):

    def __init__(self, x: int, y: int, size: int) -> None:
        self.x = x
        self.y = y
        self.size = size

        self.tail = [{'x': x, 'y': y}]

        self.dirX = 0
        self.dirY = 1

        self.grow = False
    
    def move(self):
        newBlock = {'x': self.tail[-1]['x'] + self.size * self.dirX,
                    'y': self.tail[-1]['y'] + self.size * self.dirY}
        self.tail.append(newBlock)

        if not self.grow: self.tail = self.tail[1:]
        else: self.grow = False


class Apple(object):
    
    def __init__(self) -> None:

        self.color = RED

        while True:
            self.x = floor(uniform(0., 1.) * WIDTH / SNAKE.size) * SNAKE.size
            self.y = floor(uniform(0., 1.) * HEIGHT / SNAKE.size) * SNAKE.size

            touching = False
            for block in SNAKE.tail:
                if self.x == block['x'] and self.y == block['y']:
                    touching = True
                    break
            
            if not touching: break

        self.size = SNAKE.size


def gameloop():
    clock = pygame.time.Clock()

    while RUNNING:
        keypress()
        SNAKE.move()
        eatenApple()
        checkCollide()
        draw()

        clock.tick(FPS)
    pygame.quit()


def eatenApple():
    head = SNAKE.tail[-1]
    global APPLE
    if head['x'] == APPLE.x and head['y'] == APPLE.y:
        SNAKE.grow = True
        APPLE = Apple()

def checkCollide():
    head = SNAKE.tail[-1]
    
    if head in SNAKE.tail[:-1]:
        global RUNNING
        RUNNING = False
        return

    if head['x'] < 0:
        head['x'] = WIDTH - SNAKE.size
    elif head['x'] >= WIDTH:
        head['x'] = 0
    elif head['y'] < 0:
        head['y'] = HEIGHT - SNAKE.size
    elif head['y'] >= HEIGHT:
        head['y'] = 0


def draw():
    WIN.fill(BLACK)
    for body in SNAKE.tail:
        pygame.draw.rect(WIN, GREEN, (body['x'], body['y'],
                                      SNAKE.size, SNAKE.size))
    
    pygame.draw.rect(WIN, APPLE.color, (APPLE.x, APPLE.y,
                                        APPLE.size, APPLE.size))

    WIN.blit(score_font.render(f'Score: {len(SNAKE.tail)}',
                               True, BLUE),
             [0, 0])
    pygame.display.update()


def keypress():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global RUNNING
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not SNAKE.dirX:
                SNAKE.dirX = -1
                SNAKE.dirY = 0
                break
            elif event.key == pygame.K_RIGHT and not SNAKE.dirX:
                SNAKE.dirX = 1
                SNAKE.dirY = 0
                break
            elif event.key == pygame.K_UP and not SNAKE.dirY:
                SNAKE.dirX = 0
                SNAKE.dirY = -1
                break
            elif event.key == pygame.K_DOWN and not SNAKE.dirY:
                SNAKE.dirX = 0
                SNAKE.dirY = 1
                break


if __name__ == '__main__':
    SNAKE = Snake(x=300, y=300, size=20)
    APPLE = Apple()
    gameloop()
