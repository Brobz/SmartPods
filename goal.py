import parameters as PARAM
from nn import *
import math
from sfml import sf

class Goal(object):
    def __init__(self, pos, radius, acc, color = sf.Color.BLACK):
        self.acceleration = acc

        self.speed = 0
        self.velocity = sf.Vector2(0, 0)

        self.circle = sf.CircleShape(radius)
        self.circle.origin = ((radius / 2.0, radius / 2.0))
        self.circle.fill_color = sf.Color.RED
        self.circle.outline_color = color
        self.circle.outline_thickness = 1
        self.circle.position = pos

        self.ID = 1


    def isPointInside(self, m):
        _dist = math.sqrt( (m.x - self.circle.position.x) ** 2 + (m.y - self.circle.position.y) ** 2 )
        if _dist < self.circle.radius + 1:
            return True

        return False

    def reset(self, pos):
        self.speed = 0
        self.velocity = sf.Vector2(0, 0)
        self.circle.position = pos

    def addSpeed(self, s):
        self.speed += s

    def update(self, g, ar, colliders = None):
        # This causes a "always on reverse" effect. Pretty Cool
        self.addSpeed(g)

        self.addSpeed(-self.speed * ar)

        self.velocity.x = self.speed * math.sin(- self.rect.rotation * math.pi / 180)
        self.velocity.y = self.speed * math.cos(- self.rect.rotation * math.pi / 180)

        # This causes a more "gravity-like" feeling. Weird behaviour when turning.
        # Gets weirder for higher levels of g.
        #self.velocity.y += g

        self.circle.move((self.velocity.x, self.velocity.y))

    def draw(self, window):
        window.draw(self.circle)

GOAL = Goal(PARAM.GOAL, 2, 0, sf.Color.RED)