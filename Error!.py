import pygame as pg
import pygame.display
import math as m
import random as r
import time as t
import pyautogui as pa

pg.init()

RED = (255, 0, 0)
screen_width, screen_height = pa.size()
screen_size = (screen_width, screen_height)
WINDOW_TITLE = "Error!"

HORIZONTAL = 1
UP = 2
DOWN = 0

FRAME_RATE = 60
ANIMATION_FRAME_RATE = 8

WINDOW = pg.display.set_mode((screen_size))
pg.display.set_caption(WINDOW_TITLE)

CLOCK = pg.time.Clock()

background = pg.transform.scale(pg.image.load("Entry.png"), screen_size)

objects = []

class Object:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.velocity = [0, 0]
        self.position = [(self.x + self.width / 2), (self.y - self.height / 2)]
        self.area = [None, None]
        self.area[0] = ((self.position[0] - self.width / 2), (self.position[0] + self.width / 2))
        self.area[1] = ((self.position[1] - self.height / 2), (self.position[1] + self.height / 2))

        objects.append(self)
    def check_for_collissions(self):
        for o in objects:
            if  self.area[0][0] >= o.position[0] >= self.area[0][1] and self.area[1][0] >= o.position[1] >= self.area[1][1]:
                print("colliding")

    def draw(self):
        self.position = [(self.x + self.width / 2), (self.y - self.height / 2)]
        WINDOW.blit(pg.transform.scale(self.image, (self.width, self.height)), self.position)

    def update(self):
        self.velocity[0] = self.directionADWS[1] - self.directionADWS[0]
        self.velocity[1] = self.directionADWS[3] - self.directionADWS[2]

        if self.velocity[0] % 1 == 0 and self.velocity[0] != 0 and self.velocity[1] % 1 == 0 and self.velocity[1] != 0:
            self.velocity[0] = self.velocity[0] / m.sqrt(2)
            self.velocity[1] = self.velocity[1] / m.sqrt(2)

        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed
        self.draw()
        self.area[0] = ((self.position[0] + self.width), (self.position[0] - self.width))
        self.area[1] = ((self.position[1] + self.height), (self.position[1] - self.height))
        self.check_for_collissions()


class Entity(Object):
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, None)
        self.speed = speed

        self.tileset = load_tileset(tileset, 32, 32)
        self.direction = 0
        self.flipX = False
        self.frame = 0
        self.frames = [0, 1, 0, 2]
        self.frame_timer = 0
        self.directionADWS = [False, False, False, False]

        self.area = [None, None]
        self.top_side = [None, None]
        self.bottom_side = [None, None]
        self.right_side = [None, None]
        self.left_side = [None, None]
        self.area[0] = ((self.position[0] - self.width / 2), (self.position[0] + self.width / 2))
        self.area[1] = ((self.position[1] - self.height / 2), (self.position[1] + self.height / 2))

        self.top_side[0] = ((self.position[0] - self.width / 2), (self.position[0] + self.width / 2))
        self.top_side[1] = ((self.position[1]), (self.position[1] - self.height))

        self.bottom_side[0] = ((self.position[0] - self.width / 2), (self.position[0] + self.width / 2))
        self.bottom_side[1] = ((self.position[1]), (self.position[1] + self.height / 2))

        self.right_side[0] = ((self.position[0]), (self.position[0] + self.width / 2))
        self.right_side[1] = ((self.position[1] - self.height / 2), (self.position[1] + self.height / 2))

        self.left_side[0] = ((self.position[0] - self.width / 2), (self.position[0]))
        self.left_side[1] = ((self.position[1] - self.height / 2), (self.position[1] + self.height / 2))



    def check_for_collissions(self):
        for o in objects:
            if o.position == self.position:
                pass
            else:
                if self.area[0][0] >= o.position[0] >= self.area[0][1] and self.area[1][0] >= o.position[1] >= self.area[1][1]:
                    if (self.position[0] - self.width / 2) <= o.position[0] <= (self.position[0] + self.width / 2) and  (self.position[1] - self.height / 2 - 2) <= o.position[1] - o.height / 2 <= (self.position[1] - self.height / 2 + 2):
                        print(self.position)
                        self.position[1] = o.position[1] - o.height / 2 - self.speed
                        print("Touched top side of the object")
                        print(self.position)
                        self.y = self.position[1] - self.height / 2

                    if (self.position[0] - self.width / 2) <= o.position[0] <= (self.position[0] + self.width / 2) and  (self.position[1] + self.height / 2 - 2) <= o.position[1] - o.height / 2 <= (self.position[1] + self.height / 2+ 2):
                        print("Touched bottom side of the object")
                        print(self.position)
                        self.position[1] = o.position[1] + o.height / 2 + self.speed
                        print(self.position)
                        self.y = self.position[1] - self.height / 2

    def change_direction(self):
        if self.velocity[0] < 0:
            self.direction = HORIZONTAL
            self.flipX = True
        elif self.velocity[0] > 0:
            self.direction = HORIZONTAL
            self.flipX = False
        elif self.velocity[1] > 0:
            self.direction = DOWN
        elif self.velocity[1] < 0:
            self.direction = UP

    def draw(self):
        self.position = [(self.x + self.width / 2), (self.y - self.height / 2)]
        image = pg.transform.scale(self.tileset[self.frames[self.frame]][self.direction], (self.width, self.height))

        self.change_direction()

        image = pg.transform.flip(image, self.flipX, False)

        WINDOW.blit(image, self.position)

        if self.velocity[0] == 0 and self.velocity[1] == 0:
            self.frame = 0
            return


        self.frame_timer += 1

        if self.frame_timer < ANIMATION_FRAME_RATE:
            return

        self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0

        self.frame_timer = 0

    def update(self):
        self.position = [(self.x + self.width / 2), (self.y - self.height / 2)]
        self.top_side[0] = ((self.position[0] - self.width / 2), (self.position[0] + self.width / 2))
        self.top_side[1] = ((self.position[1]), (self.position[1] - self.height))

        self.bottom_side[0] = ((self.position[0] - self.width / 2), (self.position[0] + self.width / 2))
        self.bottom_side[1] = ((self.position[1]), (self.position[1] + self.height / 2))

        self.right_side[0] = ((self.position[0]), (self.position[0] + self.width / 2))
        self.right_side[1] = ((self.position[1] - self.height / 2), (self.position[1] + self.height / 2))

        self.left_side[0] = ((self.position[0] - self.width / 2), (self.position[0]))
        self.left_side[1] = ((self.position[1] - self.height / 2), (self.position[1] + self.height / 2))

        self.velocity[0] = self.directionADWS[1] - self.directionADWS[0]
        self.velocity[1] = self.directionADWS[3] - self.directionADWS[2]

        self.check_for_collissions()

        if self.velocity[0] % 1 == 0 and self.velocity[0] != 0 and self.velocity[1] % 1 == 0 and self.velocity[1] != 0:
            self.velocity[0] = self.velocity[0] / m.sqrt(2)
            self.velocity[1] = self.velocity[1] / m.sqrt(2)

        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed
        self.draw()
        self.area[0] = ((self.position[0] + self.width), (self.position[0] - self.width))
        self.area[1] = ((self.position[1] + self.height), (self.position[1] - self.height))


class Player(Entity):
    def __init__(self, x, y, width, height, tileset, speed):
        super().__init__(x, y, width, height, tileset, speed)




    def sprint(self, value):
        if value:
            self.speed = self.speed * 1.7
        else:
            self.speed = self.speed / 1.7

def check_input(key, value):
    if key == pygame.K_a:
        player1.directionADWS[0] = value
    elif key == pygame.K_s:
        player1.directionADWS[3] = value
    elif key == pygame.K_w:
        player1.directionADWS[2] = value
    elif key == pygame.K_d:
        player1.directionADWS[1] = value
    elif key == pygame.K_LEFT:
        player2.directionADWS[0] = value
    elif key == pygame.K_DOWN:
        player2.directionADWS[3] = value
    elif key == pygame.K_UP:
        player2.directionADWS[2] = value
    elif key == pygame.K_RIGHT:
        player2.directionADWS[1] = value
    elif key == pygame.K_ESCAPE:
        exit()
    elif key == pygame.K_LSHIFT:
        player1.sprint(value)
    elif key == pygame.K_RSHIFT:
        player2.sprint(value)



def load_tileset(filename, width, height):
    image = pg.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tileset = []
    for tile_x in range(0, image_width // width):
        line = []
        tileset.append(line)
        for tile_y in range(0, image_height // height):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(image.subsurface(rect))
    return tileset




#Objects
player1 = Player(screen_size[0] / 4, screen_size[1] / 4, 75, 75, "player.png", 2)
player2 = Player(screen_size[0]*3 / 4 , screen_size[1] / 4, 75, 75, "player.png", 2)
Box = Entity(screen_size[0]/2 , screen_size[1] / 2, 32, 32, "Wood_box.png",0)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:
            check_input(event.key, True)
        elif event.type == pg.KEYUP:
            check_input(event.key, False)

    WINDOW.blit(background, (0, 0))

    for obj in objects:
        obj.update()

    CLOCK.tick(FRAME_RATE)
    pg.display.update()