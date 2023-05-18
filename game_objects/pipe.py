import pygame
import random
import os

# load the image for the pipe
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))

class Pipe:
    GAP = 200
    # VELOCITY = 5
    # VELOCITY = 32.5

    def __init__(self, x, vel):
        self.vel = vel
        self.x = x
        self.height = 0
        self.gap = 100
        self.top = 0
        self.bottom = 0
        self.IMG_PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.IMG_PIPE_BOTTOM = PIPE_IMG
        # True if the bird has passed between the pipes
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.IMG_PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        # self.x -= self.VELOCITY
        self.x -= self.vel

    def draw(self, window):
        window.blit(self.IMG_PIPE_TOP, (self.x, self.top))
        window.blit(self.IMG_PIPE_BOTTOM, (self.x, self.bottom))

    # perfect pixel collision detection with masks
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_pipe_mask = pygame.mask.from_surface(self.IMG_PIPE_TOP)
        bottom_pipe_mask = pygame.mask.from_surface(self.IMG_PIPE_BOTTOM)

        #calculate distance between masks
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        #point of collision, returns None if no collision
        top_point = bird_mask.overlap(top_pipe_mask, top_offset)
        bottom_point = bird_mask.overlap(bottom_pipe_mask, bottom_offset)

        if top_point or bottom_point:
            return True

        return False
