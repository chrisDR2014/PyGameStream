from typing import Any
import pygame
from images import *

TITLE = "Name of Game"

MAX_FPS = 60

# COLORS
WHITE = (255, 255, 255)

# WINDOW
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

class Player:
    ACTIONS = {
        "normal": {
            "walk": PLAYER_WALK,
            "run": PLAYER_RUN,
            "jump": PLAYER_JUMP,
            "push": PLAYER_PUSH,
            "pull": PLAYER_FALLING,
            "stand": PLAYER_STAND,
        },
        "weapon": {
            "walk": PLAYER_WALK_WEAPON,
            "run": PLAYER_RUN_WEAPON,
            "jump": PLAYER_JUMP_WEAPON,
            "push": PLAYER_PUSH_WEAPON,
            "pull": PLAYER_FALLING_WEAPON,
            "stand": PLAYER_STAND_WEAPON,
        },
        "attack": {
            "chop": PLAYER_ATTACK_CHOP,
        }
    }
    WALK_VEL = 3
    RUN_VEL = 5

    def __init__(self, x: int, y: int, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.action = "run"
        self.animation_count = 0
        self.frame_duration = 5
        self.img = None
        self.action_type = "weapon"
        self.vel = self.WALK_VEL
        self.set_image()
    
    def set_image(self):
        action = self.ACTIONS[self.action_type][self.action][self.direction]
        if self.animation_count//self.frame_duration >= len(action[1]):
            self.animation_count = 0

            if self.action_type == "attack":
                self.action_type = "weapon"
                self.action = "stand"

        self.img = [layer[self.animation_count//self.frame_duration] for layer in action if layer]


    def draw(self, win):
        for layer in self.img:
            win.blit(layer, (self.x, self.y))
        self.animation_count += 1
        self.set_image()

    def move(self, keys):
        prev_action, prev_direction = self.action, self.direction

        self.handle_attack()
        if self.action_type == "attack":
            return
        
        if keys[pygame.K_a]: #left
            if self.action == "pull":
                self.direction = "right"
            else:
                self.direction = "left"
            if self.action not in ["push", "pull"]:
                self.action = "walk"
            
            self.x -= self.vel
        elif keys[pygame.K_d]: #right
            if self.action == "pull":
                self.direction = "left"
            else:
                self.direction = "right"
            if self.action not in ["push", "pull"]:
                self.action = "walk"
            
            self.x += self.vel
        elif self.action_type != "attack":
            self.action = "stand"
        
        if keys[pygame.K_LSHIFT] and self.action in ["walk", "run"]: #run
            self.action = "run"
            self.vel = self.RUN_VEL
        
        if keys[pygame.K_SPACE]: #up
            self.action = "jump"
        
        if keys[pygame.K_e]: 
            self.action = "pull"
        if keys[pygame.K_f]: 
            self.action = "push"
        
        if self.action != prev_action or self.direction != prev_direction:
            self.animation_count = 0
        
    def handle_attack(self):
        pressed = pygame.mouse.get_pressed()

        if any(pressed):
            self.action_type = "attack"
            self.action = "chop"
    

def draw (win, player):
    win.fill((0,0,0))
    player.draw(win)
    pygame.display.update()

run = True

player = Player(400,500, "right")
clock = pygame.time.Clock()

while run:
    clock.tick(MAX_FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    keys = pygame.key.get_pressed()
    player.move(keys)

    draw(WIN, player)






