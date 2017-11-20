import parameters as PARAM
import math
from sfml import sf

class Obstacle(object):
    def __init__(self, pos, size, acc, ang_speed, color = sf.Color.BLACK):
        self.params = [pos, size, acc, ang_speed, 0]

        self.acceleration = acc
        self.angular_speed = ang_speed

        self.speed = 0
        self.velocity = sf.Vector2(0, 0)

        self.rect = sf.RectangleShape(size)
        self.rect.fill_color = color
        self.rect.outline_color = sf.Color.BLACK
        self.rect.outline_thickness = 0
        self.rect.position = pos
        self.rect.origin = (size[0] / 2.0, size[1] / 2.0)

        self.calculateCorners()
        self.calculateAxis()

        self.ID = -1


    def getParams(self):
        self.params = [(self.rect.position.x, self.rect.position.y), (self.rect.size.x, self.rect.size.y), self.acceleration, self.angular_speed, self.rect.rotation]

    def calculateCorners(self):
        self.theta = - self.rect.rotation * math.pi / 180.0

        self.top_left_corner_x = self.rect.position.x - self.rect.size.x / 2.0 * math.cos(self.theta) - self.rect.size.y / 2.0 * math.sin(self.theta)
        self.top_left_corner_y = self.rect.position.y + self.rect.size.x / 2.0 * math.sin(self.theta) - self.rect.size.y / 2.0 * math.cos(self.theta)

        self.top_right_corner_x = self.rect.position.x + self.rect.size.x / 2.0 * math.cos(self.theta) - self.rect.size.y / 2.0 * math.sin(self.theta)
        self.top_right_corner_y = self.rect.position.y - self.rect.size.x / 2.0 * math.sin(self.theta) - self.rect.size.y / 2.0 * math.cos(self.theta)

        self.bot_right_corner_x = self.rect.position.x + self.rect.size.x / 2.0 * math.cos(self.theta) + self.rect.size.y / 2.0 * math.sin(self.theta)
        self.bot_right_corner_y = self.rect.position.y - self.rect.size.x / 2.0 * math.sin(self.theta) + self.rect.size.y / 2.0 * math.cos(self.theta)

        #self.bot_left_corner_x = self.rect.position.x - self.rect.size.x / 2.0 * math.cos(self.theta) + self.rect.size.y / 2.0 * math.sin(self.theta)
        #self.bot_left_corner_y = self.rect.position.y + self.rect.size.x / 2.0 * math.sin(self.theta) + self.rect.size.y / 2.0 * math.cos(self.theta)

        self.corners = [sf.Vector2(self.top_left_corner_x, self.top_left_corner_y), sf.Vector2(self.top_right_corner_x, self.top_right_corner_y), sf.Vector2(self.bot_right_corner_x, self.bot_right_corner_y)]# sf.Vector2(self.bot_left_corner_x, self.bot_left_corner_y)]

    def calculateAxis(self):
        self.AB_axis = sf.Vector2(self.top_right_corner_x - self.top_left_corner_x, self.top_right_corner_y - self.top_left_corner_y)
        self.BC_axis = sf.Vector2(self.bot_right_corner_x - self.top_right_corner_x, self.bot_right_corner_y - self.top_right_corner_y)

        self.axis = [self.AB_axis, self.BC_axis]

    def isPointInside(self, m):
        AM_axis = sf.Vector2(m.x - self.top_left_corner_x, m.y - self.top_left_corner_y)
        BM_axis = sf.Vector2(m.x - self.top_right_corner_x, m.y - self.top_right_corner_y)
        AB_AM_dot = self.AB_axis.x * AM_axis.x + self.AB_axis.y * AM_axis.y
        BC_BM_dot = self.BC_axis.x * BM_axis.x + self.BC_axis.y * BM_axis.y

        if 0 <= AB_AM_dot and AB_AM_dot <= self.AB_axis.x ** 2 + self.AB_axis.y ** 2 and 0 <= BC_BM_dot and BC_BM_dot <= self.BC_axis.x ** 2 + self.BC_axis.y ** 2:
            return True

        return False

    def reset(self, pos):
        self.speed = 0
        self.velocity = sf.Vector2(0, 0)
        self.rect.position = pos
        self.rect.rotation = 0

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

        self.rect.move((self.velocity.x, self.velocity.y))

    def draw(self, window):
        window.draw(self.rect)

    def collides(self, entity):
        ## COLLISION METHOD VERSION 2.0
        ## -----------------------
        ## VERSION HISTORY
        ## VERSION 1: LINE INTERSECTION CHECKS (SELF-DEVISED)
        ## VERSION 2: SEPARATING AXIS THEOREM

        ## CHECK IF YOUR DISTANCE TO ENTITY (Origin to Origin) IS
        ## BIG ENOUGH TO EVEN CONSIDER A COLLISION

        _dist = (entity.rect.position.x - self.rect.position.x) ** 2 + (entity.rect.position.y - self.rect.position.y) ** 2

        # GET RADIUSES OF RECTS (DIAGONAL / 2)
        r1, r2 = self.rect.size.x ** 2 + self.rect.size.y ** 2 / 2.0, entity.rect.size.x ** 2 + entity.rect.size.y ** 2 / 2.0

        if _dist >  r1 + r2:
            ## TOO FAR AWAY FOR A COLLISION TO BE EVEN CONSIDERED
            return False

        ## CHECK IF ENTITY MOVES
        entity_moves = (math.fabs(entity.acceleration) or math.fabs(entity.angular_speed))

        ## GET ALL 4 OWN CORNERS
        self.calculateCorners()

        ## GET ALL 2 OWN NON-PERPENDICULAR AXIS
        self.calculateAxis()

        ## IF ENTITY MOVES:
        if entity_moves:
            ## GET ALL 4 ENTITY CORNERS
            entity.calculateCorners()
            ## GET ALL 2 ENTITY NON-PERPENDICULAR AXIS
            entity.calculateAxis()

        ## PROJECT ALL 6 CORNERS ONTO EACH OF THE 4 AXIS
        all_axis = self.axis + entity.axis

        projected_corners = []
        for i in xrange(len(all_axis)):
            projected_corners.append([])
            projected_corners[i].append([])
            projected_corners[i].append([])
            for corner in self.corners:
                _proj = (corner.x * all_axis[i].x + corner.y * all_axis[i].y) / (all_axis[i].x ** 2 + all_axis[i].y ** 2)
                projected_corners[i][0].append(_proj)
            for corner in entity.corners:
                _proj = (corner.x * all_axis[i].x + corner.y * all_axis[i].y) / (all_axis[i].x ** 2 + all_axis[i].y ** 2)
                projected_corners[i][1].append(_proj)

        ## NOW projected_corners IS POPULATED AS FOLLOWS:
        ## projected_corners[i][j][k]
        ## axis_i.ent_j.corner_k

        ## NOW, GIVEN ONLY A SINGLE AXIS WITH NO DOMAIN INTERSECTIONS,
        ## A COLLISION IS IMPOSSIBLE

        ## CHECK FOR DOMAIN INTERSECTIONS ON ALL 4 AXIS
        for i in xrange(len(projected_corners)):
            if not(min(projected_corners[i][1]) <= max(projected_corners[i][0]) and max(projected_corners[i][1]) >= min(projected_corners[i][0])):
                ## NO OVERLAP ON THIS AXIS;
                ## MEANING NO COLLISION
                return False

        ## ALL AXIS OVERLAPPED;
        ## MEANING COLLISION
        return True

TRAINING_OBSTACLES = []
"""
TRAINING_OBSTACLE_0 = Obstacle((PARAM.WIDTH  / 2.0, - 20), (PARAM.WIDTH, 50), 0.0, 0.0)
TRAINING_OBSTACLE_1 = Obstacle((PARAM.WIDTH  / 2.0, PARAM.HEIGHT + 20), (PARAM.WIDTH, 50), 0.0, 0.0)
TRAINING_OBSTACLE_2 = Obstacle((- 20, PARAM.HEIGHT  / 2.0), (50, PARAM.HEIGHT), 0.0, 0.0)
TRAINING_OBSTACLE_3 = Obstacle((PARAM.WIDTH + 20, PARAM.HEIGHT  / 2.0), (50, PARAM.HEIGHT), 0.0, 0.0)


# TRAINING_OBSTACLES = [TRAINING_OBSTACLE_0, TRAINING_OBSTACLE_1, TRAINING_OBSTACLE_2, TRAINING_OBSTACLE_3, TRAINING_OBSTACLE_6]
TRAINING_OBSTACLES = [TRAINING_OBSTACLE_0, TRAINING_OBSTACLE_1, TRAINING_OBSTACLE_2, TRAINING_OBSTACLE_3]

for to in TRAINING_OBSTACLES:
    to.calculateCorners()
    to.calculateAxis()
    to.getParams()
"""
