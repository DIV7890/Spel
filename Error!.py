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

FRAME_RATE = 144
ANIMATION_FRAME_RATE = 8

WINDOW = pg.display.set_mode((screen_size))
pg.display.set_caption(WINDOW_TITLE)

CLOCK = pg.time.Clock()

background = pg.transform.scale(pg.image.load("Entry.png"), screen_size)

objects = []

class Object():
    def __init__(self, x, y, width, height, image, hasCollisions, interactable):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pg.transform.scale(pg.image.load(image), (64, 64))
        self.velocity = [0, 0]
        self.position = [(self.x + self.width / 2), (self.y - self.height / 2)]
        self.area = [None, None]
        self.area[0] = ((self.position[0] - self.width / 2), (self.position[0] + self.width / 2))
        self.area[1] = ((self.position[1] - self.height / 2), (self.position[1] + self.height / 2))
        self.hasCollisions = hasCollisions
        self.interactable = interactable
        self.interacting = False

        self.top_side = self.area[1][0]
        self.bottom_side = self.area[1][1]
        self.right_side = self.area[0][1]
        self.left_side = self.area[0][0]

        objects.append(self)

    def draw(self):

        self.position = [(self.x + self.width / 2), (self.y - self.height / 2)]
        WINDOW.blit(self.image, self.position)

        self.position = [(self.x + self.width / 2), (self.y - self.height / 2)]
        self.area[0] = ((self.position[0] - self.width / 2), (self.position[0] + self.width / 2))
        self.area[1] = ((self.position[1] - self.height / 2), (self.position[1] + self.height / 2))

        self.top_side = self.area[1][0]
        self.bottom_side = self.area[1][1]
        self.right_side = self.area[0][1]
        self.left_side = self.area[0][0]

    def update(self):
        self.draw()

    def check_for_collissions(self):
        for o in objects:
            if o.position == self.position:
                pass
            else:
                if ((self.right_side >= o.left_side >= self.left_side) or (self.right_side >= o.right_side >= self.left_side)) and ((self.bottom_side >= o.top_side >= self.top_side) or (self.bottom_side >= o.bottom_side >= self.top_side)) and o.hasCollisions == True:
                    self.directionADWS = [False, False, False, False]
                    self.velocity[0] = self.velocity[0] * -1
                    self.velocity[1] = self.velocity[1] * -1
                if ((self.right_side >= o.left_side >= self.left_side) or (self.right_side >= o.right_side >= self.left_side)) and ((self.bottom_side >= o.top_side >= self.top_side) or (self.bottom_side >= o.bottom_side >= self.top_side)) and o.hasCollisions == False and o.interactable == False:
                    exit()
                if ((self.right_side >= o.left_side >= self.left_side) or (self.right_side >= o.right_side >= self.left_side)) and ((self.bottom_side >= o.top_side >= self.top_side) or (self.bottom_side >= o.bottom_side >= self.top_side)) and o.hasCollisions == False and o.interactable == True and self.interacting == True:
                    exit()

class Entity(Object):
    def __init__(self, x, y, width, height, image, hasCollisions, interactable, speed):
        super().__init__(x, y, width, height, image, hasCollisions, interactable)
        self.speed = speed

        self.tileset = load_tileset(image, 18, 28)
        self.direction = 0
        self.flipX = False
        self.frame = 0
        self.frames = [0, 1, 0, 2]
        self.frame_timer = 0
        self.directionADWS = [False, False, False, False]

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
        self.velocity[0] = self.directionADWS[1] - self.directionADWS[0]
        self.velocity[1] = self.directionADWS[3] - self.directionADWS[2]

        self.check_for_collissions()

        if self.velocity[0] % 1 == 0 and self.velocity[0] != 0 and self.velocity[1] % 1 == 0 and self.velocity[1] != 0:
            self.velocity[0] = self.velocity[0] / m.sqrt(2)
            self.velocity[1] = self.velocity[1] / m.sqrt(2)

        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed
        self.draw()
        self.area[0] = ((self.position[0] - self.width / 2), (self.position[0] + self.width / 2))
        self.area[1] = ((self.position[1] - self.height / 2), (self.position[1] + self.height / 2))

        self.top_side = self.area[1][0]
        self.bottom_side = self.area[1][1]
        self.right_side = self.area[0][1]
        self.left_side = self.area[0][0]

class Player(Entity):
    def __init__(self, x, y, width, height, image, hasCollisions, interactable, speed):
        super().__init__(x, y, width, height, image, hasCollisions, interactable, speed)

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
    elif key == pygame.K_o:
        camera_shake()
    elif key == pygame.K_e:
        for o in objects:
            o.interacting = value

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

def camera_shake():
    i = 0
    while i < 10:
        if i % 2 == 0:
            print("1")
            for o in objects:
                o.x += 100
                o.y += 100
                o.update()
        else:
            print("2")
            for o in objects:
                o.x += -100
                o.y += -100
                o.update()
        i += 1

# Objects
Knapp = Object(600, 600, 54, 54, "Pressure_plate.png", False, False)
Spak = Object(1200, 400, 54, 54, "spak.png", False, True)
player1 = Player(screen_size[0] / 4, screen_size[1] / 4, 54, 84, "player_test.png", True, False, 4)
player2 = Player(screen_size[0] * 3 / 4, screen_size[1] / 4, 54, 84, "player_test.png", True, False, 4)
Box = Object(screen_size[0]/2, screen_size[1] / 2, 54, 54, "Wood_box.png", True, False)

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
