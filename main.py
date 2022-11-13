from cmath import rect
from tkinter import Scale
from turtle import Screen
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('hooi')

# set framerate
clock = pygame.time.Clock()
FPS = 100
# define player action variables
moving_left = False
moving_right = False

# define colors
BG = (144, 201, 120)


def draw_bg():
    Screen.fill(BG)


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/{self.char_type}/Idle/{i}.png')
            img = pygame.transform.scale(
                img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f'img/{self.char_type}/Run/{i}.png')
            img = pygame.transform.scale(
                img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0
        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on the current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed  since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        Screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)


pfy = Soldier('player', 200, 200, 2, 3)
enemy = Soldier('enemy', 400, 200, 2, 5)

# variable
x = 200
y = 200

run = True
while run:

    clock.tick(FPS)
    draw_bg()

    pfy.update_animation()
    pfy.draw()
    enemy.draw()
    if moving_left or moving_right:
        pfy.update_action(1)
    else:
        pfy.update_action(0)
    pfy.move(moving_left, moving_right)
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
                moving_right = False
            elif event.key == pygame.K_d:
                moving_right = True
                moving_left = False
            elif event.key == pygame.K_ESCAPE:
                run = False
    pygame.display.update()
pygame.quit()
