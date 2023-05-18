import pygame
import neat
import os

# import pickle
# import visualize

from game_objects.bird import Bird
from game_objects.pipe import Pipe
from game_objects.base import Base

from draw_window import draw_window

# define window game size
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 800

GEN = 0
LAST_SCORE = 0
MAX_SCORE = 0


def eval_genomes(genomes, config):
    global GEN, MAX_SCORE, LAST_SCORE
    GEN += 1
    # keep track of the neural network that controls each bird
    neural_nets = []
    # keep track of the genomes to change their fitness
    gens = []
    # keep track of each bird
    birds = []

    for _, gen in genomes:
        net = neat.nn.FeedForwardNetwork.create(gen, config)
        neural_nets.append(net)
        birds.append(Bird(230, 350))
        gen.fitness = 0
        gens.append(gen)

    pipes = [Pipe(680, 10)]
    base = Base(730)
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    score = 0
    while run:
        clock.tick(30)
        base.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # which pipe is used for nn input, default 0, if passed then 1
        pipe_idx = 0
        if len(birds) > 0:
            if len(pipes) > 0 and birds[0].x > pipes[0].x + pipes[0].IMG_PIPE_BOTTOM.get_width():
                pipe_idx = 1
        else:
            LAST_SCORE = score
            run = False
            break

        # move the birds and add 0.1 fitness for every frame that the bird stays alive
        # encouraging it to stay alive as long as possible
        # 30 frames a second so 3 fitness points per second
        for idx, bird in enumerate(birds):
            bird.move()
            gens[idx].fitness += 0.1

            # pass the inputs through the neural network to get the output
            output = neural_nets[idx].activate((bird.y, abs(bird.y - pipes[pipe_idx].height), abs(bird.y - pipes[pipe_idx].bottom)))

            if output[0] > 0.5:
                bird.jump()

        passed_pipes = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            for idx, bird in enumerate(birds):
                if pipe.collide(bird):
                    gens[idx].fitness -= 1
                    birds.pop(idx)
                    neural_nets.pop(idx)
                    gens.pop(idx)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.IMG_PIPE_BOTTOM.get_width() < 0:
                passed_pipes.append(pipe)

        if add_pipe:
            score += 1
            # increase velocity and pipe separation
            veloc = 10 + score * 0.23
            pipe_sep = 680 + score * 5.5
            for gen in gens:
                gen.fitness += 5
            # max velocity and pipe separation
            if veloc > 32:
                veloc = 32
            if pipe_sep > 1200:
                pipe_sep = 1200
            base.VELOCITY = veloc
            pipes.append(Pipe(pipe_sep, veloc))

        for pipe in passed_pipes:
            pipes.remove(pipe)

        for idx, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= base.y or bird.y < 0:
                birds.pop(idx)
                neural_nets.pop(idx)
                gens.pop(idx)

        if score > MAX_SCORE:
            LAST_SCORE = score
            MAX_SCORE = score

        draw_window(window, birds, pipes, base, score, GEN, len(birds), pipe_idx, MAX_SCORE, LAST_SCORE)

        # stop if goal is reached and save the neural network of the best bird
        # if score == 200:
        #     pickle.dump(neural_nets[0], open("best.pickle", "wb"))


def run(config_path):
    # load the neat config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    # create a population based on the specified config
    population = neat.Population(config)

    #print population stats
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # set fitness function, run to up to 50 generations
    winner = population.run(eval_genomes, 50)

    # to visualize the nn, fitness stats and species stats
    '''
    visualize.draw_net(config, winner,)
    visualize.plot_stats(stats, ylog=False)
    visualize.plot_species(stats)
    '''

    # show final stats
    # print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    # set path to config file here so script runs successfully regardless of current working dir
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
