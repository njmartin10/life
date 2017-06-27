import math


class PhysicsEngine(object):
    def __init__(self, environment_size, elasticity=1.0, drag=0.999):

        self.environment_size = environment_size

        # friction constants
        self.elasticity = elasticity
        self.drag = drag

    def collide(self, obj1, obj2):
        """ Tests whether two particles overlap
            If they do, make them bounce, i.e. update their angle, speed and position """

        dx = obj1.position[0] - obj2.position[0]
        dy = obj1.position[1] - obj2.position[1]

        dist = math.hypot(dx, dy)
        if dist < obj1.size + obj2.size:
            angle = math.atan2(dy, dx) + 0.5 * math.pi
            total_mass = obj1.mass + obj2.mass

            (obj1.angle, obj1.speed) = self.addVectors((obj1.angle, obj1.speed * (obj1.mass - obj2.mass) / total_mass),
                                              (angle, 2 * obj2.speed * obj2.mass / total_mass))
            (obj2.angle, obj2.speed) = self.addVectors((obj2.angle, obj2.speed * (obj2.mass - obj1.mass) / total_mass),
                                              (angle + math.pi, 2 * obj1.speed * obj1.mass / total_mass))
            elasticity = obj1.elasticity * obj2.elasticity
            obj1.speed *= elasticity
            obj2.speed *= elasticity

            overlap = 0.5 * (obj1.size + obj2.size - dist + 1)
            obj1.position[0] += math.sin(angle) * overlap
            obj1.position[1] -= math.cos(angle) * overlap
            obj2.position[0] -= math.sin(angle) * overlap
            obj2.position[1] += math.cos(angle) * overlap
            return True
        return False

    def addVectors(self, (a1, l1), (a2, l2)):
        x = math.sin(a1) * l1 + math.sin(a2) * l2
        y = math.cos(a1) * l1 + math.cos(a2) * l2

        a = 0.5 * math.pi - math.atan2(y, x)
        l = math.hypot(x, y)

        return (a, l)

    def bounce(self, obj):
        if obj.position[0] > self.environment_size[0] - obj.size:
            obj.position[0] = 2 * (self.environment_size[0] - obj.size) - obj.position[0]
            obj.angle = - obj.angle
            obj.speed *= self.elasticity

        elif obj.position[0] < obj.size:
            obj.position[0] = 2 * obj.size - obj.position[0]
            obj.angle =  - obj.angle
            obj.speed *= self.elasticity

        if obj.position[1] > self.environment_size[1] - obj.size:
            obj.position[1] = 2 * (self.environment_size[1] - obj.size) - obj.position[1]
            obj.angle = math.pi - obj.angle
            obj.speed *= self.elasticity

        elif obj.position[1] < obj.size:
            obj.position[1] = 2 * obj.size - obj.position[1]
            obj.angle = math.pi - obj.angle
            obj.speed *= self.elasticity