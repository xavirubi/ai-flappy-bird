import pygame
import os

# load the image for the bird
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))]

# define a Bird and its movements
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        # keep track of where it jumped from
        self.height = self.y

    def move(self):
        self.tick_count += 1

        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2
        # limit max downwards velocity and adjust upwards velocity
        if displacement > 16: displacement = 16
        elif displacement < 0: displacement -= 2

        self.y = self.y + displacement
        # if moving up or still above where it jumped from, bird img is tilted up
        # else it is progressively tilted down
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                 self.tilt -= self.ROTATION_VELOCITY

    def draw_fly_animation(self, window):
        self.img_count += 1
        # every *ANIMATION_TIME* the img of the bird changes so it looks like is moving the wings
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # if the bird is plummeting the wings don't move
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            # set img_count that if it jumps the animation restarts with the wings moving down
            self.img_count = self.ANIMATION_TIME * 2

        # rotate the img in the direction it is moving and then draw it
        # self.tilt are the degrees
        # adjust to center as it rotates from the topleft
        # finally put rotated image in the new rect
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        window.blit(rotated_img, new_rect.topleft)

    def get_mask(self):
        # collision control function
        return pygame.mask.from_surface(self.img)
