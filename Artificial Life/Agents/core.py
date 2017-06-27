import pygame
import random
import numpy as np
import math


class Something(object):
    """
    Something is the first basic living being
    sensors : 8 * 360 sonars
    actions : accelerate, decelerate, right, left
    """
    def __init__(self, id, random_agent=False, size=None, position=None, speed=None,
                 angle=None, density=None, mass=None, elasticity=0.9):

        self.type = "something"
        self.id = self.type + "_{0}".format(id)
        self.random_agent = random_agent
        self.count_frame = 0
        self.health_limits = (0, 200)
        self.health = 200
        self.rewards = 0
        self.size = size
        self.position = position
        self.speed = speed
        self.angle = angle
        self.density = density
        self.mass = mass

        self.reaction_time = 6
        self.speed_limits = (0, 4)
        self.actions = ["accelerate", "decelerate", "right", "left", "random"]

        # body
        if self.size is None:
            self.size = 3

        # sensors
        self.sensors_length = int(0.25*self.size)
        self.sensors_range = 15
        self.sensors = {"f1": {"color": (0,0,0), "coord": None},
                        "f2": {"color": (0,0,0), "coord": None},
                        "f3": {"color": (0,0,0), "coord": None},
                        "f4": {"color": (0,0,0), "coord": None},
                        "b1": {"color": (0,0,0), "coord": None},
                        "b2": {"color": (0,0,0), "coord": None},
                        "b3": {"color": (0,0,0), "coord": None},
                        "b4": {"color": (0,0,0), "coord": None}}
        self.f_sensors_color = (255,0,255)
        self.b_sensors_color = (0,255,255)

        # physics
        self.elasticity = elasticity

        self.display_position = None
        self.display_size = None

    def create_body(self):
        self.display_position = int(self.screen_controller.mx + (self.screen_controller.dx + self.position[0])
                                    * self.screen_controller.magnification), \
                                int(self.screen_controller.my + (self.screen_controller.dy + self.position[1])
                                    * self.screen_controller.magnification)
        self.display_size = int(self.size * self.screen_controller.magnification)
        if self.health < self.health_limits[0]:
            self.health = self.health_limits[0]
        elif self.health > self.health_limits[1]:
            self.health = self.health_limits[1]
        self.body_color = (200 - self.health, self.health, 0)
        if self.display_size < 2:
            pygame.draw.rect(self.environment,
                             self.body_color,
                             (self.display_position[0], self.display_position[1], 2, 2))
        else:
            pygame.draw.circle(self.environment,
                                self.body_color,
                                (self.display_position[0], self.display_position[1]),
                                self.display_size, 3)

    def create_sensors(self):
        display_length = self.display_size

        a = self.angle - math.pi/2 - math.pi/4
        for i in range(4):

            # real process
            name = "f{0}".format(i + 1)
            x = self.position[0] + math.cos(a) * self.sensors_length
            y = self.position[1] + math.sin(a) * self.sensors_length
            self.sensors[name]["coord"] = (x, y)

            # display process
            display_x = self.display_position[0] + math.cos(a) * display_length
            display_y = self.display_position[1] + math.sin(a) * display_length
            pygame.draw.line(self.environment,
                             self.sensors[name]["color"],
                             (self.display_position[0], self.display_position[1]),
                             (display_x, display_y),
                             2)
            a += math.pi/6


        a = self.angle + math.pi/2 + math.pi/4
        for i in range(4):

            # real process
            name = "b{0}".format(i + 1)
            x = self.position[0] + math.cos(a) * self.sensors_length
            y = self.position[1] + math.sin(a) * self.sensors_length
            self.sensors[name]["coord"] = (x, y)

            # display process
            display_x = self.display_position[0] + math.cos(a) * display_length
            display_y = self.display_position[1] + math.sin(a) * display_length
            pygame.draw.line(self.environment,
                             self.sensors[name]["color"],
                             (self.display_position[0], self.display_position[1]),
                             (display_x, display_y),
                             2)
            a -= math.pi/6

    def choose_action(self, type):

        assert type in self.actions
        if type == "random":
            type = self.actions[random.randint(0, len(self.actions)-1)]

        if type == "accelerate":
            self.speed += 0.2
            if self.speed > self.speed_limits[1]:
                self.speed = self.speed_limits[1]
        elif type == "decelerate":
            self.speed -= 0.2
            if self.speed < self.speed_limits[0]:
                self.speed = self.speed_limits[0]
        elif type == "right":
            self.angle += math.pi/6
        else:
            self.angle -= math.pi/6

    def move(self):
        self.position[0] += math.sin(self.angle) * self.speed
        self.position[1] -= math.cos(self.angle) * self.speed
        self.position = [int(self.position[0]), int(self.position[1])]

    def get_sensors_values(self, obj_list):
        distances = []
        for name, sensor in self.sensors.iteritems():
            x, y = sensor["coord"]
            sensor_d = []
            danger = False

            # calculating the distances between all objects
            for obj in obj_list:
                if obj.type == "seed" or obj.id == self.id:
                    continue
                d = math.sqrt((x-obj.position[0])**2 + (y-obj.position[1])**2)
                if d < self.sensors_range*self.size:
                    danger = True
                    sensor_d.append(d)

            # displaying color of sensors
            if danger:
                if name[0] == "f":
                    sensor["color"] = self.f_sensors_color
                else:
                    sensor["color"] = self.b_sensors_color
            else:
                sensor["color"] = (0,0,0)

            # finding the nearest distance
            if sensor_d == []:
                distances.append(-1)
            else:
                distances.append(min(sensor_d))
        return np.reshape(np.array(distances), (1, len(self.sensors)))

    def eat(self, seed):
        if abs(self.position[0] - seed.position[0]) < 4 and abs(self.position[1] - seed.position[1]) < 4:
            self.health += 10 * seed.size
            self.rewards += 10 * seed.size
            return True
        return False

    def init(self, environment, environment_size):
        self.environment = environment
        self.environment_size = environment_size

        if self.position is None:
            self.position = [random.uniform(self.size, self.environment_size[0] - self.size),
                             random.uniform(self.size, self.environment_size[1] - self.size)]
        if self.speed is None:
            self.speed = random.uniform(2,4)
        if self.angle is None:
            self.angle = random.uniform(0, math.pi*2)

        if self.mass is None:
            if self.density is None:
                self.density = random.randint(1, 20)
            self.mass = self.density * self.size**2

        #print "Agent {0} -->\tspeed : {1}\tangle : {2}".format(self.id, self.speed, self.angle)

    def display(self):
        self.create_body()
        self.create_sensors()

    def run(self, screen_controller, objects):
        self.screen_controller = screen_controller
        self.count_frame += 1

        # choose an action in the set of actions every "reaction_time" frames
        if self.count_frame % self.reaction_time == 0:
            if self.random_agent:
                self.choose_action("random")

        # update real values
        self.move()

        # display the agent with fake values
        self.display()