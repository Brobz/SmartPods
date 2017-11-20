from point import *

class Goal(Point):
    def __init__(self, pos, radius, acc, color = sf.Color.BLACK):
        Point.__init__(self, pos, radius, color)


        self.circle.fill_color = sf.Color.RED

        self.acceleration = acc

        self.speed = 0
        self.velocity = sf.Vector2(0, 0)

        self.params = [pos, radius, acc]

        self.ID = 100


    def isPointInside(self, m):
        _dist = (m.x - self.circle.position.x) ** 2 + (m.y - self.circle.position.y) ** 2
        if _dist <= (self.circle.radius * 1.2) ** 2:
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

        #self.addSpeed(-self.acceleration * (random.random() - 0.5))

        self.addSpeed(-self.speed * ar)

        self.velocity.x = self.speed * math.sin(- self.circle.rotation * math.pi / 180)
        self.velocity.y = self.speed * math.cos(- self.circle.rotation * math.pi / 180)

        # This causes a more "gravity-like" feeling. Weird behaviour when turning.
        # Gets weirder for higher levels of g.
        #self.velocity.y += g

        self.circle.move((self.velocity.x, self.velocity.y))

TEMP_GOAL = Goal((PARAM.GOAL[0], PARAM.GOAL[1]), 5, 0, sf.Color.RED)
GOALS = [Goal((random.randrange(100, 700), random.randrange(100, 400)), 5, 0.0, sf.Color.RED) for i in xrange(PARAM.GOAL_POPULATION)]
