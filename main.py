import os.path
from population import Population
from obstacle import Obstacle
from interface import *

# The button can be styled in a manner similar to CSS.
GO_STYLE = {"hover_color": BRIGHT_GREEN,
            "clicked_color": GREEN,
            "clicked_font_color": BLACK,
            "hover_font_color": BLACK}
SPEEDUP_STYLE = {"hover_color": BRIGHT_GREEN,
                 "clicked_color": GREEN,
                 "clicked_font_color": BLACK,
                 "hover_font_color": BLACK,
                 "call_on_release": False}
QUIT_STYLE = {"hover_color": RED,
              "clicked_color": RED,
              "clicked_font_color": BLACK,
              "hover_font_color": BLACK}

# define window parameters
width = 1200
height = 800
title = "Smart Rockets"

life_time = 200
pop_size = 100
obstacles = [(width * 0.5 - 150, height * 0.5 - 25, 300, 50)]
target = [width * 0.5, 100]
origin = [width * 0.5, height * 5 / 6]

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
        self.speedup_done = False
        self.fps = 60.0
        self.iter_cnt = 0
        self.counter = 0
        self.color = BLACK
        self.population = None
        self.obstacles = []
        self.init_buttons(gobutton='on', quitbutton='off', prev_childbutton='on', speedupbutton='off')

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

    def init_buttons(self, gobutton='off', quitbutton='off', prev_childbutton='off', speedupbutton='off'):
        if gobutton == 'on':
            self.gobutton = Button((0, 0, 50, 50), RED, self.game_loop,
                                   text="GO!", **GO_STYLE)
            self.gobutton.rect.center = (self.screen_rect.centerx, 100)
        else:
            self.gobutton = None
        if quitbutton == 'on':
            self.quitbutton = Button((0, 0, 28, 28), RED, self.exit_loop,
                                     text="Quit", **QUIT_STYLE)
            self.quitbutton.rect.center = (self.screen_rect.centerx, 100)
        else:
            self.quitbutton = None
        if prev_childbutton == 'on':
            self.prev_childbutton = Button((0, 0, 250, 50), ORANGE, self.import_best_child,
                                           text="Start with previous best child", **GO_STYLE)
            self.prev_childbutton.rect.center = (self.screen_rect.centerx, 300)
        else:
            self.prev_childbutton = None
        if speedupbutton == 'on':
            self.speedupbutton = Button((150, 3, 100, 30), GREEN, self.speedup,
                                        text="Speed Up", **SPEEDUP_STYLE)
            self.speedupbutton.on_release = self.exit_speedup
        else:
            self.speedupbutton = None

    def game_loop(self, prev_child=None):
        self.init_buttons(gobutton='off', quitbutton='on', prev_childbutton='off', speedupbutton='on')
        # set a counter for handling genetic algorithm steps at given moments
        self.counter = 0
        # iteration counter
        self.iter_cnt = 0
        # initialize population
        self.population = Population(size=pop_size, life_time=life_time, origin=origin, target=target,
                                     prev_child=prev_child)
        self.game_loop_done = False

        while not self.game_loop_done:
            # handle input events
            self.event_loop()
            # clear the playground
            self.screen.fill(self.color)

            if self.counter == life_time:
                # reset the counter to 0
                self.counter = 0
                # increment iter
                self.iter_cnt += 1
                # compute the newer generation of the population
                self.population.next_gen()

            for member in self.population.members:
                # check if rocket did not collide before
                if member.is_alive and not member.has_landed:
                    # calculate the new position for every rocket
                    member.apply_force_at(self.counter)
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
                    if (math.pow((member.location.x - target[0]), 2) +
                            math.pow((member.location.y - target[1]), 2)) < math.pow(20, 2):
                        member.has_landed = True
                        member.landed_at = self.counter

                # display the rockets
                drawRocket(self.screen, member)

            # draw the obstacles
            for obs in self.obstacles:
                pg.draw.rect(self.screen, WHITE, obs.tuple_int(0))

            # Draw red target
            pg.draw.circle(self.screen, RED, target, 20)
            self.quitbutton.update(self.screen)
            self.speedupbutton.update(self.screen)
            self.game_info()

            self.counter += 1
            pg.display.update()
            self.clock.tick(self.fps)
        self.init_buttons(gobutton='on', quitbutton='off', prev_childbutton='on', speedupbutton='off')

    def exit_loop(self):
        if os.path.isfile("best_child.txt"):
            with open("best_child.txt", "r") as reader:
                fitness = float(reader.readline().partition(':')[2][1:])
        else:
            fitness = 0
        if fitness < self.population.best_child.fitness(self.population.target) * 1000:
            with open("best_child.txt", "w") as writer:
                writer.write(f"Fitness: {str(self.population.best_child.fitness(self.population.target) * 1000)}\n"
                             f"Genes: ")
                for vector in self.population.best_child.genes:
                    writer.write(str(vector))
        self.game_loop_done = True

    def exit_speedup(self, event):
        self.speedup_done = True

    def import_best_child(self):
        if os.path.isfile("best_child.txt"):
            with open("best_child.txt", "r") as reader:
                txt_genes = list(filter(None, reader.readlines()[1].partition(":")[2][1:]
                                        .replace('(', ' ').replace(')', ' ').split(' ')))
            genes = [float(gene) for gene in txt_genes]
            return self.game_loop(prev_child=genes)
        else:
            return self.game_loop()

    # this method computes the routes of the rockets without using visual simulation
    def speedup(self):
        self.speedup_done = False
        while not self.speedup_done:
            # handle input events
            self.event_loop()
            # clear the playground
            self.screen.fill(self.color)
            # apply all forces for every member
            for member in self.population.members:
                self.counter = 0
                for force in member.genes:
                    # do not update the rockets position if there was a collision with an obstacle
                    if member.is_alive and not member.has_landed:
                        # apply force to the rocket
                        member.apply_force(force)
                        # update rocket's position
                        member.update()
                        # check member's collision with window
                        if (width < member.location.x) or (member.location.x < 0) or \
                                (height < member.location.y) or (member.location.y < 0):
                            member.is_alive = False
                        # check member's collision with the obstacles
                        for obs in self.obstacles:
                            if obs.collision(member):
                                member.is_alive = False
                        if (math.pow((member.location.x - target[0]), 2) +
                                math.pow((member.location.y - target[1]), 2)) < math.pow(20, 2):
                            member.has_landed = True
                            member.landed_at = self.counter
                    self.counter += 1

                # display the rockets
                drawRocket(self.screen, member)

                # draw the obstacles
            for obs in self.obstacles:
                pg.draw.rect(self.screen, WHITE, obs.tuple_int(0))
            pg.draw.circle(self.screen, RED, target, 20)

            # increment iter
            self.iter_cnt += 1
            self.counter = 0
            # compute the newer generation of the population
            self.population.next_gen()
            self.speedupbutton.update(self.screen)
            self.game_info()
            pg.display.update()
            self.clock.tick(self.fps)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
                self.game_loop_done = True
            if self.gobutton is not None:
                self.gobutton.check_event(event)
            if self.quitbutton is not None:
                self.quitbutton.check_event(event)
            if self.speedupbutton is not None:
                self.speedupbutton.check_event(event)
            if self.prev_childbutton is not None:
                self.prev_childbutton.check_event(event)

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.screen.fill(self.color)
            self.gobutton.update(self.screen)
            self.prev_childbutton.update(self.screen)
            pg.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    run_it = Control()
    run_it.main_loop()
    pg.quit()
    quit()
