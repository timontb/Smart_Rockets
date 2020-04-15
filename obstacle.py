from vector import Vector


class Obstacle:
    """ the Obstacle is a rectangle whit which the Rocket can collide
        self.a (type Vector) - contains the point for the upper left corner of the rectangle
        self.b (type Vector) - contains the point for the lower right corner of the rectangle
    """

    def __init__(self, x1, y1, x2, y2):
        self.a = Vector(x1, y1)
        self.b = Vector(x2, y2)

    # return true if the rocket's position is inside the obstacle's rectangle
    def collision(self, rocket):
        x1 = self.a.x
        x2 = x1 + self.b.x
        y1 = self.a.y
        y2 = y1 + self.b.y
        return x1 < rocket.location.x < x2 and y1 < rocket.location.y < y2

    # transforms the vector to a tuple containing integer values
    # the offset is added to the components of the vector
    def tuple_int(self, offset):
        return self.a.tuple_int(offset), self.b.tuple_int(offset)
