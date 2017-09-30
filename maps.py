from pods import *
from goal import *


class Map(object):
    def __init__(self, obstacles, goals):
        self.obstacles = obstacles
        self.goals = goals
        self.ents = obstacles + goals


    def makeObs(self, params):
        for p in params:
            new_o = Obstacle(p[0], p[1], p[2], p[3])
            new_o.rect.rotation = p[4]

            new_o.calculateCorners()
            new_o.calculateAxis()

            self.obstacles.append(new_o)

        self.ents = self.obstacles + self.goals

    def makeGoals(self, params):
        for p in params:
            self.goals.append(Goal(p[0], p[1], p[2]))

        self.ents = self.obstacles + self.goals

    def draw(self, window):
        for e in self.ents:
            e.draw(window)


    def tick(self):
        for o in self.obstacles:
            o.rect.rotation += o.angular_speed


    def getObsParams(self):
        params = []
        for o in self.obstacles:
            o.getParams()
            params.append(o.params)

        return params

    def getGoalsParams(self):
        params = []
        for g in self.goals:
            params.append(g.params)

        return params

    def addObstacle(self, o):
        self.obstacles.append(o)
        self.ents = self.obstacles + self.goals

    def addGoal(self, g):
        self.goals.append(g)
        self.ents = self.obstacles + self.goals
