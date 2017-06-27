import pygame
import math
import random


class Seed(object):
    def __init__(self, id, position=None, size=None, size_bank=None):
        self.type = "seed"
        self.id = self.type + "_{0}".format(id)
        self.size_bank = size_bank
        if self.size_bank is None:
            self.size_bank = [2, 4, 6, 8, 10]
        self.seed_color = (120, 10, 90)

        self.position = position
        self.size = size

        self.display_position = None
        self.display_size = None

    def init(self, environment, environment_size):
        self.environment = environment
        self.environment_size = environment_size

        if self.size is None:
            self.size = random.choice(self.size_bank)

        if self.position is None:
            self.position = [random.randint(self.size, self.environment_size[0] - self.size),
                    random.randint(self.size, self.environment_size[1] - self.size)]

    def run(self, screen_controller):
        self.screen_controller = screen_controller
        self.display_position = int(self.screen_controller.mx + (self.screen_controller.dx + self.position[0])
                               * self.screen_controller.magnification), \
                           int(self.screen_controller.my + (self.screen_controller.dy + self.position[1])
                               * self.screen_controller.magnification)
        self.display_size = int(self.size * self.screen_controller.magnification)

        pygame.draw.rect(self.environment,
                         self.seed_color,
                         (self.display_position[0], self.display_position[1], self.display_size, self.display_size),
                         self.size / 2)


class Asteroid(object):
    def __init__(self, id, position=None, size=None, size_bank=None, n_corners=None,
                 density=None, mass=None, elasticity=0.2):
        self.type = "asteroid"
        self.id = self.type + "_{0}".format(id)
        self.size_bank = size_bank
        if self.size_bank is None:
            self.size_bank = [20, 30, 40, 60]
        self.asteroid_color = (70, 0, 200)
        self.n_corners = n_corners
        self.density = density
        self.mass = mass
        self.elasticity = elasticity
        self.angle = 0
        self.speed = 0
        self.position = position
        self.size = size

        self.display_position = None
        self.display_size = None

    def init(self, environment, environment_size):
        self.environment = environment
        self.environment_size = environment_size

        if self.size is None:
            self.size = random.choice(self.size_bank)

        if self.position is None:
            self.position = [random.randint(self.size, self.environment_size[0] - self.size),
                    random.randint(self.size, self.environment_size[1] - self.size)]

        if self.n_corners is None:
            self.n_corners = random.randint(7,10)

        if self.mass is None:
            if self.density is None:
                self.density = random.randint(20, 40)
            self.mass = self.density * self.size**2

    def run(self, screen_controller):
        self.screen_controller = screen_controller
        display_point_list = []
        self.display_position = int(self.screen_controller.mx + (self.screen_controller.dx + self.position[0])
                               * self.screen_controller.magnification), \
                           int(self.screen_controller.my + (self.screen_controller.dy + self.position[1])
                               * self.screen_controller.magnification)
        self.display_size = int(self.size * self.screen_controller.magnification)
        for i in range(self.n_corners * 2):
            ang = i * math.pi / self.n_corners
            display_x = self.display_position[0] + int(math.cos(ang) * self.display_size)
            display_y = self.display_position[1] + int(math.sin(ang) * self.display_size)
            display_point_list.append((display_x, display_y))

        pygame.draw.polygon(self.environment, self.asteroid_color, display_point_list, 0)
