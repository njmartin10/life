import pygame
import math

from Simulator.physics import PhysicsEngine


class ScreenController(object):
    """
    store variables of scrolling, zooming, etc
    """
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0

    def scroll(self, dx=0, dy=0):
        self.dx += dx * self.width / (self.magnification * 10)
        self.dy += dy * self.height / (self.magnification * 10)

    def follow(self, dx=0, dy=0):
        self.dx += dx
        self.dy += dy

    def zoom(self, zoom):
        self.magnification *= zoom
        self.mx = (1 - self.magnification) * self.width / 2
        self.my = (1 - self.magnification) * self.height / 2

    def reset(self):
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1.0


key_to_function = {
    pygame.K_LEFT: (lambda x: x.scroll(dx=1)),
    pygame.K_RIGHT: (lambda x: x.scroll(dx=-1)),
    pygame.K_DOWN: (lambda x: x.scroll(dy=-1)),
    pygame.K_UP: (lambda x: x.scroll(dy=1)),
    pygame.K_EQUALS: (lambda x: x.zoom(2)),
    pygame.K_MINUS: (lambda x: x.zoom(0.5)),
    pygame.K_r: (lambda x: x.reset())}


class Environment(object):
    """
    Basic Environment
    """
    def __init__(self, title, agents=None, objects=None, size=(1080, 720), background_color=(0,0,0)):
        self.title = title
        self.size = size
        self.bg_color = background_color
        self.agents = agents
        self.objects = objects

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        self.screen.fill(self.bg_color)

        self.screen_controller = ScreenController(self.size)
        self.physics_engine = PhysicsEngine(self.size)

        # objects init
        if self.objects is not None:
            for object in self.objects:
                object.init(self.screen, self.size)

        # agents init
        if self.agents is not None:
            for agent in self.agents:
                agent.init(self.screen, self.size)

        if self.agents is None:
            self.agents = []
        if self.objects is None:
            self.objects = []
        pygame.display.update()  # Tells pygame to draw

    def update(self):
        delete_obj = []
        sensors_obj = [o for o in (self.agents + self.objects)]
        for i, obj1 in enumerate(self.agents + self.objects):
            if obj1.type == "something":
                #sensors_val = obj1.get_sensors_values(sensors_obj)
                self.physics_engine.bounce(obj1)
            if obj1.type in ["asteroid", "something"]:
                for j, obj2 in enumerate((self.agents + self.objects)[i + 1:]):
                    if obj2.type in ["asteroid", "something"]:
                        if self.physics_engine.collide(obj1, obj2):
                            if obj1.type == "something":
                                obj1.health -= 10
                                obj1.rewards -= 10
                            if obj2.type == "something":
                                obj2.health -= 10
                                obj2.rewards -= 10
                    else:
                        if obj1.type == "something":
                            if obj1.eat(obj2):
                                delete_obj.append(obj2)

            if obj1.type == "something":
                obj1.run(self.screen_controller, sensors_obj)
                #print "position : ", obj1.position
                #print "display position : ", obj1.display_position
                #if obj1.rewards != 0:
                #    print "{0}  -->   health : {1}  rewards : {2}".format(obj1.id, obj1.health, obj1.rewards)
            else:
                obj1.run(self.screen_controller)

            obj1.rewards = 0
        self.objects = [obj for obj in self.objects if obj not in delete_obj]

    def init(self):
        for obj in (self.agents + self.objects):
            if obj.type == "something":
                obj.run(self.screen_controller)

    def findParticle(self, mouse_x, mouse_y):
        for a in self.agents:
            if math.hypot(a.display_position[0] - mouse_x, a.display_position[1] - mouse_y) <= a.display_size:
                return a
        return None

    def run(self):
        clock = pygame.time.Clock()
        paused = False
        running = True
        follow = False
        #self.init()
        while running:
            self.screen.fill(self.bg_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self.screen_controller)
                    elif event.key == pygame.K_SPACE:
                        paused = (True, False)[paused]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    print mouseX, mouseY
                    agent_to_track = self.findParticle(mouseX, mouseY)
                    if agent_to_track:
                        follow = True
                    else:
                        follow = False

            if follow:
                follow_dx = int(self.size[0]/2 - agent_to_track.display_position[0])
                follow_dy = int(self.size[1]/2 - agent_to_track.display_position[1])
                #self.screen_controller.follow(dx=follow_dx, dy=follow_dy)
                print "follow_dx : {0}\t follow_dy : {1}".format(follow_dx, follow_dy)
                smooth_thres = int(5 / self.screen_controller.magnification)
                print "smooth_thres : {0}".format(smooth_thres)
                print "real_position : ", agent_to_track.position
                print "display_position : {0}\tdisplay_size : {1}".format(agent_to_track.display_position, agent_to_track.display_size)
                print "controller_dx : {0}\tcontroller_dy : {1}".format(self.screen_controller.dx, self.screen_controller.dy)
                print
                if follow_dx > smooth_thres and follow_dy > smooth_thres:
                    self.screen_controller.follow(dx=follow_dx, dy=follow_dy)
                elif follow_dx > smooth_thres and follow_dy < smooth_thres:
                    self.screen_controller.follow(dx=follow_dx, dy=0)
                elif follow_dx < smooth_thres and follow_dy > smooth_thres:
                    self.screen_controller.follow(dx=0, dy=follow_dy)

            if not paused:
                self.update()

            pygame.display.flip()
            clock.tick(60)