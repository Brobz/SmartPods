from pods import *
import sys, time

def natural_selection(pods):
    population = len(pods)
    pods.sort(key = lambda p: p.fitness, reverse = True)
    del pods[-(population / 2):]
    new_pods = list(pods)
    # MUTATION
    for p in xrange(len(pods)):
        pods[p].reset(PARAM.START_POSITION)
        np = SmartPod(NN(PARAM.NN_LAYOUT), sf.Vector2(PARAM.START_POSITION[0], PARAM.START_POSITION[1]), sf.Vector2(PARAM.POD_SIZE[0], PARAM.POD_SIZE[1]), PARAM.POD_ACCELERATION, PARAM.POD_ANGULAR_SPEED)
        np.nn.weights = copy.deepcopy(pods[p].nn.weights)

        for i in xrange(len(np.nn.weights)):
            for j in xrange(len(np.nn.weights[i])):
                for k in xrange(len(np.nn.weights[i][j])):
                    r = random.randrange(0, PARAM.MUTATON_RATE + 1)
                    if r <= 1:
                        np.nn.weights[i][j][k] = random.randrange(-3, 3)
                    elif r <= 2:
                        np.nn.weights[i][j][k] *= -1
                    elif r <= 4:
                        np.nn.weights[i][j][k] = random.random() - 0.5
                    elif r <= 6:
                        np.nn.weights[i][j][k] *= random.random() + 1
                    elif r <= 8:
                        np.nn.weights[i][j][k] *= random.random()




        new_pods.append(np)

    return new_pods

# SET GLOBAL VARIABLES
WINDOW = sf.RenderWindow(sf.VideoMode(PARAM.WIDTH, PARAM.HEIGHT), unicode("SmartPods"))
WINDOW.framerate_limit = PARAM.MAX_FRAMERATE
WINDOW.key_repeat_enabled = False
G_GRAPHIC = sf.CircleShape(2)
G_GRAPHIC.origin = ((1, 1))
G_GRAPHIC.fill_color = sf.Color.RED
G_GRAPHIC.outline_color = sf.Color.BLUE
G_GRAPHIC.outline_thickness = 1
G_GRAPHIC.position = PARAM.GOAL
PODS = [SmartPod(NN(PARAM.NN_LAYOUT), sf.Vector2(PARAM.START_POSITION[0], PARAM.START_POSITION[1]), sf.Vector2(PARAM.POD_SIZE[0], PARAM.POD_SIZE[1]), PARAM.POD_ACCELERATION, PARAM.POD_ANGULAR_SPEED) for i in xrange(PARAM.POD_POPULATION)]
TRAINING_PODS = list(PODS)
FITNESSES = []
DELTA_CLOCK = sf.Clock()
DELTA_TIME = sf.Time()
MAX_FPS = 0
GENERATION = -1
TRAINING = False

GEN_TICKS = 0

SANDBOX_PODS = []
SANDBOX_CIRCLES = []

for c in PARAM.CIRCLES:
    radius = 1
    circ = sf.CircleShape(radius, 10)
    circ.origin = ((radius, radius))
    circ.fill_color = sf.Color.YELLOW
    circ.outline_color = sf.Color.RED
    circ.outline_thickness = 0.5
    circ.position = c
    SANDBOX_CIRCLES.append(circ)

for w in PARAM.SANDBOX_WEIGHTS:
    np = SmartPod(NN(PARAM.NN_LAYOUT), sf.Vector2(PARAM.START_POSITION[0], PARAM.START_POSITION[1]), sf.Vector2(PARAM.POD_SIZE[0], PARAM.POD_SIZE[1]), PARAM.POD_ACCELERATION, PARAM.POD_ANGULAR_SPEED, sf.Color.MAGENTA)
    np.nn.weights = w
    SANDBOX_PODS.append(np)

def evolve():
    global TRAINING, GENERATION, PODS, TRAINING_PODS, PLAYER_POD, GEN_TICKS, FITNESSES

    if not TRAINING:
        if GENERATION > -1:
            print "\n>> Generation", GENERATION
            print ">> Worst Fitness:", FITNESSES[GENERATION][PARAM.POD_POPULATION - 1], "| Median Fitness:", FITNESSES[GENERATION][PARAM.POD_POPULATION / 2 - 1], "| Max Fitness:", FITNESSES[GENERATION][0]
            #a = raw_input(">> Continue?\n-- ")
        FITNESSES.append([])
        TRAINING = True
        GENERATION += 1

    for p in TRAINING_PODS:

        if p.dead or p.hit_target:
            FITNESSES[GENERATION].append(p.getFitness(GEN_TICKS))
            TRAINING_PODS.remove(p)
            continue

        engine_values = p.nn.feedForward([PARAM.GOAL[0] - p.rect.position.x, PARAM.GOAL[1] - p.rect.position.y, p.speed, p.rect.rotation])
        for i in xrange(len(engine_values)):
            if engine_values[i] > 0.5:
                p.switchEngine(i, 1)
            else:
                p.switchEngine(i, 0)

        p.update(PARAM.GRAVITY, PARAM.FRICTION, TRAINING_OBSTACLES)

    if not len(TRAINING_PODS) or (GEN_TICKS >= PARAM.TRAINING_TIME):
        TRAINING = False
        for p in TRAINING_PODS:
            FITNESSES[GENERATION].append(p.getFitness(GEN_TICKS))
            continue

        FITNESSES[GENERATION].sort(reverse = True)
        PODS = list(natural_selection(PODS))
        TRAINING_PODS = list(PODS)

        GEN_TICKS = 0

    GEN_TICKS += 1

    for p in PODS:
        p.draw(WINDOW)

    for to in TRAINING_OBSTACLES:
        to.rect.rotation += to.angular_speed
        to.draw(WINDOW)

def sandbox_loop():
    if PARAM.SHOW_SANDBOX_PODS:
        for sp in SANDBOX_PODS:

            sp.draw(WINDOW)

            if sp.dead or sp.hit_target:
                continue

            engine_values = sp.nn.feedForward([PARAM.GOAL[0] - sp.rect.position.x, PARAM.GOAL[1] - sp.rect.position.y, sp.speed, sp.rect.rotation])
            for i in xrange(len(engine_values)):
                if engine_values[i] > 0.5:
                    sp.switchEngine(i, 1)
                else:
                    sp.switchEngine(i, 0)

            sp.update(PARAM.GRAVITY, PARAM.FRICTION, TRAINING_OBSTACLES)

        for to in TRAINING_OBSTACLES:
            to.draw(WINDOW)

    if PARAM.SHOW_SANDBOX_CIRCLES:
        for i in xrange(len(SANDBOX_CIRCLES)):
            SANDBOX_CIRCLES[i].position = PARAM.CIRCLES[i]
            WINDOW.draw(SANDBOX_CIRCLES[i])

while WINDOW.is_open:

    for event in WINDOW.events:
        if event.type == sf.Event.CLOSED:
            WINDOW.close()

        if PARAM.SANDBOX:

            if event.type == sf.Event.KEY_RELEASED:
                if event["code"] == sf.Keyboard.SPACE:
                    PLAYER_POD.reset(PARAM.START_POSITION)
                    for sp in SANDBOX_PODS:
                        sp.reset(PARAM.START_POSITION)

        if PARAM.HUMAN_CONTROLLED_POD:

            if event.type == sf.Event.KEY_PRESSED:
                if event["code"] == sf.Keyboard.LEFT:
                    PLAYER_POD.switchEngine(0, 1)
                if event["code"] == sf.Keyboard.RIGHT:
                    PLAYER_POD.switchEngine(1, 1)
                if event["code"] == sf.Keyboard.UP:
                    PLAYER_POD.switchEngine(2, 1)
            if event.type == sf.Event.KEY_RELEASED:
                if event["code"] == sf.Keyboard.LEFT:
                    PLAYER_POD.switchEngine(0, 0)
                if event["code"] == sf.Keyboard.RIGHT:
                    PLAYER_POD.switchEngine(1, 0)
                if event["code"] == sf.Keyboard.UP:
                    PLAYER_POD.switchEngine(2, 0)

    WINDOW.clear(sf.Color.WHITE)

    if PARAM.HUMAN_CONTROLLED_POD:
        if PARAM.SHOW_TEST_PODS:
            for tp in TEST_PODS:
                tp.rect.rotation += tp.angular_speed
                tp.draw(WINDOW)
            if not PLAYER_POD.dead and not PLAYER_POD.hit_target:
                PLAYER_POD.update(PARAM.GRAVITY, PARAM.FRICTION, TEST_PODS)
        else:
            if not PLAYER_POD.dead and not PLAYER_POD.hit_target:
                PLAYER_POD.update(PARAM.GRAVITY, PARAM.FRICTION)

        PLAYER_POD.calculateSenserPoints()
        PLAYER_POD.getSenserInfo(TEST_PODS)

        PLAYER_POD.draw(WINDOW)

    if not PARAM.SANDBOX:
        if GENERATION <= PARAM.MAX_TRAINING_GENERATION:
            evolve()
        else:
            PODS.sort(key = lambda p: p.fitness, reverse = True)
            print ">> Max Fitness Weights:", PODS[0].nn.weights
            break
    else:
        sandbox_loop()
        GEN_TICKS += 1


    SCREEN_OUTLINE.draw(WINDOW)
    WINDOW.draw(G_GRAPHIC)
    WINDOW.display()

    DELTA_TIME = DELTA_CLOCK.restart()
    if not GEN_TICKS % 10:
        sys.stdout.write("\rFPS: " + str(1 / DELTA_TIME.seconds))
        sys.stdout.flush()
