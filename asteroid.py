import math
import random

import pyxel

from utils import check_bounds, rotate_around_origin, Point
import constants


class Asteroid:
    asteroids = []

    def __init__(
        self,
        size=constants.ASTERPOD_INITIAL_SIZE,
        radius=constants.ASTEROID_RADIUS,
        position=None,
    ):

        if position:
            x, y = position
            self.x = x
            self.y = y
        else:
            ship_x = Asteroid.ship.x
            ship_y = Asteroid.ship.y

            while True:
                self.x = random.randint(0, pyxel.width)
                self.y = random.randint(0, pyxel.height)

                if (
                    math.hypot(self.x - ship_x, self.y - ship_y)
                    > constants.ASTEROID_SPAWN_BUFFER
                ):
                    break

        self.colour = constants.ASTEROID_COLOUR
        self.size = size
        self.radius = radius

        self.direction = random.random() * math.pi * 2
        self.velocity = rotate_around_origin(
            (0, -constants.ASTEROID_VELOCITY), self.direction
        )

        self.spin_direction = random.choice((-1, 1))

        asteroid_points = random.choice(constants.ASTEROID_SHAPES)
        scale = radius / constants.ASTEROID_RADIUS

        self.points = []
        for x, y in asteroid_points:
            point_new = Point(x * scale, y * scale)
            point_new.rotate_point(self.direction)
            self.points.append(point_new)

        Asteroid.asteroids.append(self)

    @classmethod
    def init_class(cls, ship):
        cls.ship = ship

    def update(self):

        rotation_angle = constants.ASTEROID_ROTATION * self.spin_direction

        for point in self.points:
            point.rotate_point(rotation_angle)

        x_vol, y_vol = self.velocity
        self.x += x_vol
        self.y += y_vol

        self.x = check_bounds(self.x, pyxel.width, constants.ASTEROID_BUFFER)
        self.y = check_bounds(self.y, pyxel.height, constants.ASTEROID_BUFFER)

    def destroy(self):
        if self.size > 0:
            for _ in range(constants.ASTEROID_SPLITS):
                Asteroid(self.size - 1, self.radius / 2, (self.x, self.y))

        Asteroid.asteroids.remove(self)
        del self

    def display(self):
        for point1, point2 in zip(self.points, self.points[1:] + [self.points[0]]):
            pyxel.line(
                x1=point1.x + self.x,
                y1=point1.y + self.y,
                x2=point2.x + self.x,
                y2=point2.y + self.y,
                col=self.colour,
            )

    @staticmethod
    def initiate_game():
        for _ in range(constants.ASTEROID_INITIAL_QUANTITY):
            Asteroid()

    @staticmethod
    def update_all():
        for asteroid in Asteroid.asteroids:
            asteroid.update()

    @staticmethod
    def display_all():
        for asteroid in Asteroid.asteroids:
            asteroid.display()
