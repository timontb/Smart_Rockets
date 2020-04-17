import numpy as np
import math
from vector import Vector


class Rocket:

    def __init__(self, life_time, origin=None, prev_genes=None):
        if origin is None:
            origin = [300, 500]
        self.origin = origin
        self.location = Vector(origin[0], origin[1])
        self.acceleration = Vector()
        self.velocity = Vector()
        self.direction = 1.5707963267948966
        self.size = 10

        # this flag is set to False after the rocket did collide with an obstacle
        self.is_alive = True
        self.has_landed = False
        self.landed_at = life_time

        self.genes = []
        self.life_time = life_time

        if not prev_genes:
            for i in range(0, life_time):
                self.genes.append(Vector.random())
        else:
            for i in range(0, len(prev_genes), 2):
                self.genes.append(Vector(prev_genes[i], prev_genes[i+1]))

    # applies a force vector to the rocket's acceleration
    def apply_force(self, force):
        self.acceleration += force

    # applies a force vector to the rocket's acceleration
    # the force value is taken from the self.forces array
    def apply_force_at(self, at):
        self.acceleration += self.genes[at]

    # updates the location of the rocket
    def update(self):
        # update the velocity of the rocket
        self.velocity += self.acceleration

        # update the location of the rocket
        self.location += self.velocity

        # update the direction of the rocket
        norme = math.sqrt(self.velocity.x ** 2 + self.velocity.y ** 2)
        cosAngle = self.velocity.x / norme
        sinAngle = -self.velocity.y / norme
        self.direction = math.acos(cosAngle) if math.asin(sinAngle) >= 0 else 2 * math.pi - math.acos(cosAngle)

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
            fitness_rate = 0.000000000000000001
        # if rocket has reached the target, increase the fitness value in accordance with the needed time
        if self.has_landed:
            fitness_rate = 10 * self.life_time/self.landed_at

        return inv_dist_to_target * fitness_rate

    # does the recombination between to elements of the population
    def crossover(self, other):
        # a new child is created
        child = Rocket(self.life_time, origin=self.origin)
        # generate a random midpoint
        midpoint = np.random.random_integers(1, other.life_time)

        for i in range(0, other.life_time):
            # do the recombination by taking force vectors from both elements
            if i < midpoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = other.genes[i]
        return child

    # mutates the current force vector according to the current mutation rate
    def mutate(self, mutation_rate):
        for i in range(0, self.life_time):
            rand_value = np.random.rand()
            if rand_value < mutation_rate:
                self.genes[i] += Vector.random()
