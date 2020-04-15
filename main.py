import math
from population import Population
from obstacle import Obstacle
from interface import *

# The button can be styled in a manner similar to CSS.
GO_STYLE = {"hover_color": BRIGHT_GREEN,
            "clicked_color": GREEN,
            "clicked_font_color": BLACK,
            "hover_font_color": BLACK}
QUIT_STYLE = {"hover_color": RED,
              "clicked_color": RED,
              "clicked_font_color": BLACK,
              "hover_font_color": BLACK}

# define window parameters
width = 600
height = 600
title = "Smart Rockets"

life_time = 120
obstacles = [(150, 250, 300, 50)]

# initialize pygame
pg.init()


class Control:
    def __init__(self):
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        self.screen_rect = self.screen.get_rect()
        # get the clock module for handling FPS
        self.clock = pg.time.Clock()
        self.done = False
        self.game_loop_done = False
        self.fps = 60.0
        self.iter_cnt = 0
        self.color = BLACK
        self.population = None
        self.obstacles = []
        self.button = Button((0, 0, 50, 50), RED, self.game_loop,
                             text="GO!", **GO_STYLE)
        self.quitbutton = None
        self.button.rect.center = (self.screen_rect.centerx, 100)

        # create obstacle objects
        for obs in obstacles:
            self.obstacles.append(Obstacle(obs[0], obs[1], obs[2], obs[3]))

    def game_info(self):
        fontsize = 15
        font = pg.font.SysFont(None, fontsize)
        iter_text = font.render(f"Iteration: {str(self.iter_cnt)}", True, YELLOW)
        fitness_text = font.render(f"Average Fitness: {'{:.5f}'.format(self.population.average_fitness)}", True, YELLOW)
        self.screen.blit(iter_text, (0, 0))
        self.screen.blit(fitness_text, (0, 0 + fontsize))
        for i in range(0, len(self.population.fitness_graph)):
            pg.draw.rect(self.screen,
                         (255 - 255 * (self.population.fitness_graph[i] / self.population.highest_average_fitness),
                          255 * (self.population.fitness_graph[i] / self.population.highest_average_fitness), 0),
                         [3 + i * 15, 2 * fontsize,
                          10, 30 * (self.population.fitness_graph[i] / self.population.highest_average_fitness)])

    def game_loop(self):
        self.button = None
        # initialize Quit button
        self.quitbutton = Button((0, 0, 28, 28), RED, self.exit_loop,
                                 text="Quit", **QUIT_STYLE)
        self.quitbutton.rect.center = (self.screen_rect.centerx, 100)
        # set a counter for handling genetic algorithm steps at given moments
        counter = 0
        # iteration counter
        self.iter_cnt = 0
        # initialize population
        self.population = Population(life_time=life_time)
        self.game_loop_done = False

        while not self.game_loop_done:
            # handle input events
            self.event_loop()
            # clear the playground
            self.screen.fill(self.color)

            if counter == life_time:
                # reset the counter to 0
                counter = 0
                # increment iter
                self.iter_cnt += 1
                # compute the newer generation of the population
                self.population.next_gen()

            for member in self.population.members:
                # check if rocket did not collide before
                if member.is_alive and not member.has_landed:
                    # calculate the new position for every rocket
                    member.apply_force_at(counter)
                    # update the rocket's position
                    member.update()

                    # check member's collision with window
                    if (width < member.location.x) or (member.location.x < 0) or \
                            (height < member.location.y) or (member.location.y < 0):
                        member.is_alive = False
                    # check member's collision with the obstacles
                    for obs in self.obstacles:
                        if obs.collision(member):
                            member.is_alive = False
                    if (math.pow((member.location.x - 300), 2) + math.pow((member.location.y - 100), 2)) < math.pow(
                            20, 2):
                        member.has_landed = True

                # display the rockets
                pg.draw.circle(self.screen, WHITE, member.location.tuple_int(0), 5)

            # draw the obstacles
            for obs in self.obstacles:
                pg.draw.rect(self.screen, WHITE, obs.tuple_int(0))

            # Draw red target
            pg.draw.circle(self.screen, RED, [300, 100], 20)
            self.quitbutton.update(self.screen)
            self.game_info()

            counter += 1
            pg.display.update()
            self.clock.tick(self.fps)
        self.button = Button((0, 0, 50, 50), RED, self.game_loop,
                             text="GO!", **GO_STYLE)
        self.button.rect.center = (self.screen_rect.centerx, 100)

    def exit_loop(self):
        self.game_loop_done = True

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
                self.game_loop_done = True
            if self.button is not None:
                self.button.check_event(event)
            if self.quitbutton is not None:
                self.quitbutton.check_event(event)

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.screen.fill(self.color)
            self.button.update(self.screen)
            pg.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    run_it = Control()
    run_it.main_loop()
    pg.quit()
    quit()
