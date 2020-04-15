import numpy as np


class Vector:
    """ implementation of Eucledian vector"""

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        return Vector(x, y)

    def __str__(self):
        return "(" + str(self.x) + " " + str(self.y) + ")"

    # equivalent of Vector(0.0, 0.0)
    def nul(self):
        self.x, self.y = 0.0, 0.0

    # calculates the Eucledian distance between 2 vectors
    def dist(self, other):
        x_dist = self.x - other.x
        y_dist = self.y - other.y
        return np.sqrt(x_dist * x_dist + y_dist * y_dist)

    # transforms the vector to a tuple containing integer values
    # the offset is added to the components of the vector
    def tuple_int(self, offset=0.0):
        return int(self.x + offset), int(self.y + offset)

    # creates a vector with random initial values
    @staticmethod
    def random():
        return Vector(np.random.uniform(0, 2.0) - 1.0, np.random.uniform(0, 2.0) - 1.0)
