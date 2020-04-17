import numpy as np
from rocket import Rocket
from vector import Vector


class Population:

    def __init__(self, size=10, life_time=60, origin=None, target=None, prev_child=None):
        if origin is None:
            origin = [300, 500]
        if target is None:
            target = [300, 100]
        self.origin = origin
        self.prev_child = prev_child
        self.mutation_rate = 0.05
        self.average_fitness = 0
        self.highest_average_fitness = 1
        self.fitness_graph = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.size = size
        self.life_time = life_time
        self.target = Vector(target[0], target[1])
        self.best_child = Rocket(self.life_time)
        self.members = []
        for member in range(0, self.size):
            self.members.append(Rocket(self.life_time, origin=self.origin, prev_genes=self.prev_child))

    # start the main loop
    def next_gen(self):
        # define aux variables for genetic algorithm
        mating_pool = []
        new_generation = []

        for member in self.members:

            # calculate the fitness for every member from the population
            fitness = (member.fitness(self.target)) * 1000
            self.average_fitness += fitness

            # save the member with the best fitness
            if self.best_child.fitness(self.target) * 1000 < fitness:
                self.best_child = member

            # create the mating pool using every member's fitness
            # the recombination will use roulette method which means every member
            # is added to the mating pool multiple times depending on its fitness value
            for i in range(0, int(fitness)):
                mating_pool.append(member)

        self.average_fitness /= len(self.members)
        self.fitness_graph.insert(0, self.average_fitness)
        self.fitness_graph.pop()
        if self.average_fitness > self.highest_average_fitness:
            self.highest_average_fitness = self.average_fitness

        if len(mating_pool) > 0:
            for i in range(0, self.size):
                # the recombination is done selecting to random members from the mating pool
                first = np.random.random_integers(0, len(mating_pool) - 1)
                second = np.random.random_integers(0, len(mating_pool) - 1)
                child = mating_pool[first].crossover(mating_pool[second])

                # the child will suffer a mutation according to the probability of the mutation rate
                child.mutate(self.mutation_rate)

                # the newer generation will represent the population for the next iteration
                new_generation.append(child)
        else:
            new_generation = []
            for member in range(0, self.size):
                new_generation.append(Rocket(self.life_time, origin=self.origin, prev_genes=self.prev_child))

        self.members = new_generation
