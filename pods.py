import parameters as PARAM
from nn import *
from sfml import sf

class SmartPod(object):
    def __init__(self, nn, pos, size, acc, ang_speed, color = sf.Color.BLACK):
        self.nn = nn

        self.acceleration = acc
        self.angular_speed = ang_speed

        self.mutation_rate = random.random()
        self.cross_rate = random.random()

        self.dead = False
        self.hit_target = False
        self.collided = False
        self.fitness = 0
        self.ticks = 0

        self.speed = 0
        self.velocity = sf.Vector2(0, 0)

        self.rect = sf.RectangleShape(size)
        self.rect.fill_color = color
        self.rect.outline_color = sf.Color.BLACK
        self.rect.outline_thickness = 0.2
        self.rect.position = pos
        self.rect.origin = (size.x / 2.0, size.y / 2.0)

        self.engines = [0, 0, 0]
        self.hasFiredMainEngine = False

        self.calculateCorners()
        self.calculateAxis()
        self.calculateSenserPoints()

    def calculateCorners(self):
        self.theta = - self.rect.rotation * math.pi / 180.0

        self.top_left_corner_x = self.rect.position.x - self.rect.size.x / 2.0 * math.cos(self.theta) - self.rect.size.y / 2.0 * math.sin(self.theta)
        self.top_left_corner_y = self.rect.position.y + self.rect.size.x / 2.0 * math.sin(self.theta) - self.rect.size.y / 2.0 * math.cos(self.theta)

        self.top_right_corner_x = self.rect.position.x + self.rect.size.x / 2.0 * math.cos(self.theta) - self.rect.size.y / 2.0 * math.sin(self.theta)
        self.top_right_corner_y = self.rect.position.y - self.rect.size.x / 2.0 * math.sin(self.theta) - self.rect.size.y / 2.0 * math.cos(self.theta)

        self.bot_right_corner_x = self.rect.position.x + self.rect.size.x / 2.0 * math.cos(self.theta) + self.rect.size.y / 2.0 * math.sin(self.theta)
        self.bot_right_corner_y = self.rect.position.y - self.rect.size.x / 2.0 * math.sin(self.theta) + self.rect.size.y / 2.0 * math.cos(self.theta)

        self.bot_left_corner_x = self.rect.position.x - self.rect.size.x / 2.0 * math.cos(self.theta) + self.rect.size.y / 2.0 * math.sin(self.theta)
        self.bot_left_corner_y = self.rect.position.y + self.rect.size.x / 2.0 * math.sin(self.theta) + self.rect.size.y / 2.0 * math.cos(self.theta)

        self.corners = [sf.Vector2(self.top_left_corner_x, self.top_left_corner_y), sf.Vector2(self.top_right_corner_x, self.top_right_corner_y), sf.Vector2(self.bot_right_corner_x, self.bot_right_corner_y), sf.Vector2(self.bot_left_corner_x, self.bot_left_corner_y)]

    def calculateAxis(self):
        self.AB_axis = sf.Vector2(self.top_right_corner_x - self.top_left_corner_x, self.top_right_corner_y - self.top_left_corner_y)
        self.BC_axis = sf.Vector2(self.bot_right_corner_x - self.top_right_corner_x, self.bot_right_corner_y - self.top_right_corner_y)

        self.axis = [self.AB_axis, self.BC_axis]

    def calculateSenserPoints(self):
        self.senser_layers = 4
        self.senser_dist = 5
        self.angle_variance = 15
        self.angle_span = 90
        self.angle_variance_rad = self.angle_variance * math.pi / 180.0
        self.theta = - self.rect.rotation * math.pi / 180.0
        self.senser_origin = sf.Vector2(self.rect.position.x - math.sin(self.theta) * self.rect.size.y / 2.0, self.rect.position.y - math.cos(self.theta) * self.rect.size.y  / 2.0)

        self.senser_points = []
        for i in xrange(self.senser_layers):
            self.senser_points.append([])
            for j in xrange(self.angle_span / self.angle_variance):
                theta_p = (-self.theta - 90 * math.pi / 180.0 - self.angle_variance_rad * (self.angle_span / self.angle_variance * 0.5)) + self.angle_variance_rad * j
                senser_pos = sf.Vector2(self.senser_origin.x + self.senser_dist * (i + 1) * math.cos(theta_p), self.senser_origin.y + self.senser_dist * (i + 1) * math.sin(theta_p))
                self.senser_points[i].append(senser_pos)

        PARAM.CIRCLES = [(self.senser_points[i][j].x, self.senser_points[i][j].y) for j in xrange(self.angle_span / self.angle_variance) for i in xrange(self.senser_layers)]
    def getSenserInfo(self, colliders):
        _info = []
        self.calculateCorners()
        self.calculateAxis()
        for i in xrange(len(self.senser_points)):
            for m in self.senser_points[i]:
                for c in colliders:
                    c.calculateCorners()
                    c.calculateAxis()
                    if c.isPointInside(m):
                        ## SENSOR IS INSIDE SMTH;
                        ## ADD INFO TO _INFO ARRAY
                        print "IN"


        return _info

    def isPointInside(self, m):
        AM_axis = sf.Vector2(m.x - self.top_left_corner_x, m.y - self.top_left_corner_y)
        BM_axis = sf.Vector2(m.x - self.top_right_corner_x, m.y - self.top_right_corner_y)
        AB_AM_dot = self.AB_axis.x * AM_axis.x + self.AB_axis.y * AM_axis.y
        BC_BM_dot = self.BC_axis.x * BM_axis.x + self.BC_axis.y * BM_axis.y

        if 0 <= AB_AM_dot and AB_AM_dot <= self.AB_axis.x ** 2 + self.AB_axis.y ** 2 and 0 <= BC_BM_dot and BC_BM_dot <= self.BC_axis.x ** 2 + self.BC_axis.y ** 2:
            return True

        return False

    def reset(self, pos):
        self.dead = False
        self.hit_target = False
        self.collided = False
        self.ticks = 0
        self.speed = 0
        self.velocity = sf.Vector2(0, 0)
        self.rect.position = pos
        self.rect.rotation = 0
        self.engines = [0, 0, 0]
        self.hasFiredMainEngine = False

    def switchEngine(self, index, state):
        if index == 2 and state:
            self.hasFiredMainEngine = True

        self.engines[index] = state

    def addSpeed(self, s):
        self.speed += s

    def update(self, g, ar, colliders = None):
        # This causes a "always on reverse" effect. Pretty Cool
        self.addSpeed(g)

        if self.engines[0]:
            self.rect.rotation -= self.angular_speed
        if self.engines[1]:
            self.rect.rotation += self.angular_speed
        if self.engines[2]:
            self.addSpeed(-self.acceleration)

        self.addSpeed(-self.speed * ar)

        if math.fabs(self.speed) < 0.1 and not self.engines[2]:
              self.speed = 0

        self.velocity.x = self.speed * math.sin(- self.rect.rotation * math.pi / 180)
        self.velocity.y = self.speed * math.cos(- self.rect.rotation * math.pi / 180)

        # This causes a more "gravity-like" feeling. Weird behaviour when turning.
        # Gets weirder for higher levels of g.
        #self.velocity.y += g

        self.rect.move((self.velocity.x, self.velocity.y))

        if math.sqrt( (PARAM.GOAL[0] - self.rect.position.x) ** 2 + (PARAM.GOAL[1] - self.rect.position.y) ** 2) <= 3:
            self.hit_target = True

        if self.rect.position.x > PARAM.WIDTH or self.rect.position.x < 0 or self.rect.position.y > PARAM.HEIGHT or self.rect.position.y < 0:
            self.rect.position.x = 0 if self.rect.position.x < 0 else PARAM.WIDTH if self.rect.position.x > PARAM.WIDTH else self.rect.position.x
            self.rect.position.y = 0 if self.rect.position.x < 0 else PARAM.HEIGHT if self.rect.position.x > PARAM.HEIGHT else self.rect.position.x
            self.dead = True

        if colliders == None:
            return

        for c in colliders:
            if self.collides(c):
                self.dead = True
                break

    def getFitness(self, GEN_TICKS):
        distance_from_goal = math.sqrt( (PARAM.GOAL[0] - self.rect.position.x) ** 2 + (PARAM.GOAL[1] - self.rect.position.y) ** 2)
        self.fitness = 1000.0 - distance_from_goal


        if self.dead:
            self.fitness *= 0.95

        if not self.hasFiredMainEngine:
            self.fitness = 0

        self.fitness +=  PARAM.TRAINING_TIME - GEN_TICKS

        return self.fitness

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

        _dist = math.sqrt( (entity.rect.position.x - self.rect.position.x) ** 2 + (entity.rect.position.y - self.rect.position.y) ** 2)

        # GET RADIUSES OF RECTS (DIAGONAL / 2)
        r1, r2 = math.sqrt(self.rect.size.x ** 2 + self.rect.size.y ** 2) / 2.0, math.sqrt(entity.rect.size.x ** 2 + entity.rect.size.y ** 2) / 2.0

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

        ## PROJECT ALL 8 CORNERS ONTO EACH OF THE 4 AXIS
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

PLAYER_POD = SmartPod(NN(PARAM.NN_LAYOUT), sf.Vector2(PARAM.WIDTH / 2.0, PARAM.HEIGHT / 2.0), sf.Vector2(0.8, 8), 0.05, 3, sf.Color.CYAN)
PLAYER_POD.calculateSenserPoints()

SCREEN_OUTLINE = SmartPod(NN(PARAM.NN_LAYOUT), sf.Vector2(PARAM.WIDTH / 2.0, PARAM.HEIGHT / 2.0), sf.Vector2(PARAM.WIDTH - 2, PARAM.HEIGHT - 2), 0.0, 0.0)

SCREEN_OUTLINE.rect.fill_color = sf.Color.TRANSPARENT
SCREEN_OUTLINE.rect.outline_color = sf.Color.RED
SCREEN_OUTLINE.rect.outline_thickness = 2


TEST_POD_0 = SmartPod(NN(PARAM.NN_LAYOUT), sf.Vector2(100, 100), sf.Vector2(10, 200), 0.0, 0.0)
TEST_POD_0.rect.rotation = -60
TEST_POD_1 = SmartPod(NN(PARAM.NN_LAYOUT), sf.Vector2(300, 200), sf.Vector2(10, 100), 0.5, 0.5)
TEST_POD_2 = SmartPod(NN(PARAM.NN_LAYOUT), sf.Vector2(PARAM.WIDTH / 2.0, PARAM.HEIGHT / 2.0), sf.Vector2(PARAM.WIDTH, PARAM.HEIGHT), -0.2, -0.2)
TEST_POD_2.rect.fill_color = sf.Color.TRANSPARENT
TEST_POD_2.rect.outline_thickness = 2

TEST_PODS = [TEST_POD_0]

for tp in TEST_PODS:
    tp.calculateCorners()
    tp.calculateAxis()

TRAINING_OBSTACLE_0 = SmartPod(NN(PARAM.NN_LAYOUT), sf.Vector2(PARAM.WIDTH - 150, 400), sf.Vector2(1, 650), 0.0, 0.0)
TRAINING_OBSTACLE_0.rect.rotation = 10
TRAINING_OBSTACLE_1 = SmartPod(NN(PARAM.NN_LAYOUT), sf.Vector2(PARAM.WIDTH - 100, 50), sf.Vector2(1, 350), 0.0, 0.0)
TRAINING_OBSTACLE_1.rect.rotation = -45
TRAINING_OBSTACLE_2 = SmartPod(NN(PARAM.NN_LAYOUT), sf.Vector2(PARAM.WIDTH / 2.0 - 50, 150), sf.Vector2(1, PARAM.WIDTH), 0.0, 0.0)
TRAINING_OBSTACLE_2.rect.rotation = -75
TRAINING_OBSTACLE_3 = SmartPod(NN(PARAM.NN_LAYOUT), sf.Vector2(PARAM.WIDTH / 2.0 - 50, 0), sf.Vector2(1, PARAM.WIDTH), 0.0, 0.0)
TRAINING_OBSTACLE_3.rect.rotation = 83

TRAINING_OBSTACLES = [TRAINING_OBSTACLE_0, TRAINING_OBSTACLE_1, TRAINING_OBSTACLE_2, TRAINING_OBSTACLE_3]

for to in TRAINING_OBSTACLES:
    to.calculateCorners()
    to.calculateAxis()