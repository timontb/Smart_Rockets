import numpy as np
from vector import Vector


class Rocket:

    def __init__(self, life_time):
        self.location = Vector(300, 500)
        self.acceleration = Vector()
        self.velocity = Vector()

        # this flag is set to False after the rocket did collide with an obstacle
        self.is_alive = True
        self.has_landed = False

        self.forces = []
        self.length = life_time

        for i in range(0, life_time):
            self.forces.append(Vector.random())

    # applies a force vector to the rocket's acceleration
    def apply_force(self, force):
        self.acceleration += force

    # applies a force vector to the rocket's acceleration
    # the force value is taken from the self.forces array
    def apply_force_at(self, at):
        self.acceleration += self.forces[at]

    # updates the location of the rocket
    def update(self):
        # update the velocity of the rocket
        self.velocity += self.acceleration

        # update the location of the rocket
        self.location += self.velocity

        # the acceleration of the rocket is set to 0.0
        self.acceleration.nul()

    # calculates the fitness of a Rocket
    # it is recommended to be called after every force vector was added to the rocket
    def fitness(self, target):
        # the fitness value is basically the distance of the rocket from the target point
        # because we want to have a smaller fitness value for larger distances,
        # the inverse value of the distance is used
        inv_dist_to_target = 1.0 / self.location.dist(target)

        # if a collision was detected with an obstacle, penalize the fitness value
        fitness_rate = 1.0
        if not self.is_alive:
            fitness_rate = 0.0000000000000000001

        return inv_dist_to_target * fitness_rate

    # does the recombination between to elements of the population
    def crossover(self, other):
        # a new child is created
        child = Rocket(self.length)
        # generate a random midpoint
        midpoint = np.random.random_integers(1, other.length)

        for i in range(0, other.length):
            # do the recombination by taking force vectors from both elements
            if i < midpoint:
                child.forces[i] = self.forces[i]
            else:
                child.forces[i] = other.forces[i]
        return child

    # mutates the current force vector according to the current mutation rate
    def mutate(self, mutation_rate):
        for i in range(0, self.length):
            rand_value = np.random.rand()
            if rand_value < mutation_rate:
                self.forces[i] = Vector.random()

