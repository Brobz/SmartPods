import parameters as PARAM
import math, random
from sfml import sf

class Point(object):
    def __init__(self, pos, radius, color = sf.Color.BLACK):

        self.circle = sf.CircleShape(radius)
        self.circle.origin = ((radius / 2.0, radius / 2.0))
        self.circle.fill_color = sf.Color.BLUE
        self.circle.outline_color = color
        self.circle.outline_thickness = 1
        self.circle.position = pos

    def draw(self, window):
        window.draw(self.circle)

START_POINT = Point((PARAM.START_POSITION[0], PARAM.START_POSITION[1]), 2)
