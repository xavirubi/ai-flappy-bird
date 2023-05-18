import pygame
import os

# load the image for the background
BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))

# init text font
pygame.font.init()
TEXT_FONT = pygame.font.SysFont("comicsans", 50)

# draw bird vision lines
DRAW_LINES = False


def draw_window(window, birds, pipes, base, score, generation, alive, pipe_idx, max_score, last_score):
    # draw bg into the window at x=0 y=0 (topleft)
    window.blit(BACKGROUND_IMG, (0, 0))

    # create text
    sc = TEXT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    gen = TEXT_FONT.render("Gen: " + str(generation), 1, (255, 255, 255))
    al = TEXT_FONT.render("Alive: " + str(alive), 1, (255, 255, 255))
    ms = TEXT_FONT.render("Max Score: " + str(max_score), 1, (255, 255, 255))
    ls = TEXT_FONT.render("Last Score: " + str(last_score), 1, (255, 255, 255))

    for pipe in pipes:
        pipe.draw(window)

    for bird in birds:
        if DRAW_LINES:
            try:
                pygame.draw.line(window, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_idx].x + pipes[pipe_idx].IMG_PIPE_TOP.get_width()/2, pipes[pipe_idx].height), 5)
                pygame.draw.line(window, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_idx].x + pipes[pipe_idx].IMG_PIPE_BOTTOM.get_width()/2, pipes[pipe_idx].bottom), 5)
            except:
                pass
        bird.draw_fly_animation(window)

    base.draw(window)

	# draw text
    window.blit(sc, (window.get_width() - 10 - sc.get_width(), 10))
    window.blit(ls, (window.get_width() - 10 - ls.get_width(), 20 + sc.get_height()))
    window.blit(ms, (window.get_width() - 10 - ms.get_width(), 30 + sc.get_height() + ls.get_height()))
    window.blit(gen, (10, 10))
    window.blit(al, (10, 20 + gen.get_height()))

    pygame.display.update()
