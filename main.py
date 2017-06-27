from Agents.core import Something
from Simulator.environment import Environment
from Simulator.objects import Seed, Asteroid


agents = [Something(id=i+1, random_agent=True, size=3) for i in range(20)]
objects = [Asteroid(id=i+1, size_bank=[10, 15, 25, 30]) for i in range(20)] + \
          [Seed(id=i+1, size_bank=[2, 3, 4]) for i in range(100)]

universe = Environment(title="Artificial Environment", size=(1080, 720), agents=agents, objects=objects)
universe.run()