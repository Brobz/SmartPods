from app import *


def natural_selection(brains):
    # CROSSOVER
    if PARAM.RANDOM_START:
        new_pos = (float(random.randrange(100, 700)), float(random.randrange(100, 400)))
    else:
        new_pos = (PARAM.START_POSITION[0], PARAM.START_POSITION[1])
    new_pod = SmartPod(NN(PARAM.NN_LAYOUT), new_pos, (PARAM.POD_SIZE[0], PARAM.POD_SIZE[1]), PARAM.POD_ACCELERATION, PARAM.POD_ANGULAR_SPEED)
    index_1 = 0
    index_2 = 0
    while index_1 == index_2:
        index_1 = random.randrange(len(brains))
        index_2 = random.randrange(len(brains))
    for i in xrange(len(new_pod.nn.weights)):
        for j in xrange(len(new_pod.nn.weights[i])):
            new_pod.nn.weights[i][j] = copy.deepcopy(brains[random.choice([index_1, index_2])][i][j])

    # MUTATION
    for i in xrange(len(new_pod.nn.weights)):
        for j in xrange(len(new_pod.nn.weights[i])):
            for k in xrange(len(new_pod.nn.weights[i][j])):
                r = random.randrange(0, math.floor(100 / PARAM.MUTATON_RATE))
                if r <= 1:
                    new_pod.nn.weights[i][j][k] = random.randrange(-2, 2)
                elif r <= 2:
                    new_pod.nn.weights[i][j][k] *= -1
                elif r <= 4:
                    new_pod.nn.weights[i][j][k] = random.random() - 0.5
                elif r <= 6:
                    new_pod.nn.weights[i][j][k] *= random.random() + 1
                elif r <= 8:
                    new_pod.nn.weights[i][j][k] *= random.random()
                elif r <= 10:
                    new_pod.nn.weights[i][j][k] += (random.random() - 0.5) * 0.5


    return new_pod



# SET GLOBAL VARIABLES
WINDOW = sf.RenderWindow(sf.VideoMode(PARAM.WIDTH, PARAM.HEIGHT), unicode("SmartPods"))
WINDOW.framerate_limit = PARAM.MAX_FRAMERATE
WINDOW.key_repeat_enabled = False
PODS = [SmartPod(NN(PARAM.NN_LAYOUT), (PARAM.START_POSITION[0], PARAM.START_POSITION[1]), (PARAM.POD_SIZE[0], PARAM.POD_SIZE[1]), PARAM.POD_ACCELERATION, PARAM.POD_ANGULAR_SPEED) for i in xrange(PARAM.POD_POPULATION)]
TRAINING_PODS = list(PODS)
DEAD_PODS = []
FITNESSES = []
DELTA_CLOCK = sf.Clock()
DELTA_TIME = sf.Time()
MAX_FPS = 0
GENERATION = -1
TRAINING = False

GEN_TICKS = 0

TEMP_GOAL = Goal((PARAM.GOAL[0], PARAM.GOAL[1]), 2, 0, sf.Color.RED)
Serializer.MAPS[PARAM.MAP_INDEX].addGoal(TEMP_GOAL)

BEST_FITNESSES = [0 for i in xrange(PARAM.POD_POPULATION / 2)]
BEST_BRAINS = [copy.deepcopy(TRAINING_PODS[i].nn.weights) for i in xrange(PARAM.POD_POPULATION / 2)]


SANDBOX_PODS = []
SANDBOX_CIRCLES = []

for c in PARAM.CIRCLES:
    radius = 0.5
    circ = sf.CircleShape(radius, 20)
    circ.origin = ((radius, radius))
    circ.fill_color = sf.Color.RED
    circ.outline_color = sf.Color.YELLOW
    circ.outline_thickness = 0
    circ.position = c
    SANDBOX_CIRCLES.append(circ)

for w in PARAM.SANDBOX_WEIGHTS:
    np = SmartPod(NN(PARAM.NN_LAYOUT), (PARAM.START_POSITION[0], PARAM.START_POSITION[1]), (PARAM.POD_SIZE[0], PARAM.POD_SIZE[1]), PARAM.POD_ACCELERATION, PARAM.POD_ANGULAR_SPEED, sf.Color.MAGENTA)
    np.nn.weights = w
    SANDBOX_PODS.append(np)

def evolve():
    global PODS, TRAINING_PODS, GEN_TICKS, BEST_FITNESSES, BEST_BRAINS

    if PARAM.EDITING:
        Editor.editingLoop(WINDOW)
    looped_pods = []
    for p in TRAINING_PODS:
        looped_pods.append(p)

        if p.dead:
            new_fit = p.getFitness()
            for i in xrange(len(BEST_FITNESSES)):
                if new_fit > BEST_FITNESSES[i]:
                    BEST_FITNESSES[i] = new_fit
                    BEST_BRAINS[i] = copy.deepcopy(p.nn.weights)
                    break

            TRAINING_PODS.remove(p)
            TRAINING_PODS.append(natural_selection(BEST_BRAINS))
            DEAD_PODS.append(p)
            GEN_TICKS += 1
            continue

        p.update(PARAM.GRAVITY, PARAM.FRICTION, Serializer.MAPS[PARAM.MAP_INDEX].goals)

        senser_info = p.getSenserInfo(Serializer.MAPS[PARAM.MAP_INDEX].ents) # + TRAINING_PODS)
        engine_values = p.nn.feedForward([senser_info[i] for i in xrange(len(senser_info))] + [p.speed])
        for i in xrange(len(engine_values)):
            if engine_values[i] > 0.5:
                p.switchEngine(i, 1)
            else:
                p.switchEngine(i, 0)

        p.checkCollisions(Serializer.MAPS[PARAM.MAP_INDEX].obstacles) #+ list(set(TRAINING_PODS) - set(looped_pods)))

    # Fixed, randomized goal population
    """
    while len(Serializer.MAPS[PARAM.MAP_INDEX].goals) < PARAM.GOAL_POPULATION:
        Serializer.MAPS[PARAM.MAP_INDEX].goals.append(Goal((random.randrange(100, 700), random.randrange(100, 400)), 5, 0.0, sf.Color.RED))
    """

    for p in TRAINING_PODS:
        p.draw(WINDOW)


    Serializer.MAPS[PARAM.MAP_INDEX].tick()
    Serializer.MAPS[PARAM.MAP_INDEX].draw(WINDOW)

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

            sp.update(PARAM.GRAVITY, PARAM.FRICTION)
            sp.checkCollisions(TRAINING_OBSTACLES)

        for to in TRAINING_OBSTACLES:
            to.draw(WINDOW)

    if PARAM.SHOW_SANDBOX_CIRCLES:
        for i in xrange(len(SANDBOX_CIRCLES)):
            SANDBOX_CIRCLES[i].position = PARAM.CIRCLES[i]
            WINDOW.draw(SANDBOX_CIRCLES[i])

TICKS = 0

while WINDOW.is_open:

    for event in WINDOW.events:
        if event.type == sf.Event.CLOSED:
            WINDOW.close()

        if event.type == sf.Event.KEY_RELEASED:
            if event["code"] == sf.Keyboard.E:
                PARAM.EDITING = not PARAM.EDITING

        if PARAM.EDITING:
            if event.type == sf.Event.GAINED_FOCUS:
                    Editor.HAS_FOCUS = True
            if event.type == sf.Event.LOST_FOCUS:
                    Editor.HAS_FOCUS = False
            if event.type == sf.Event.KEY_RELEASED:
                if event["code"] == sf.Keyboard.SPACE:
                    print BEST_BRAINS[len(BEST_BRAINS) - 1]

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
                PLAYER_POD.update(PARAM.GRAVITY, PARAM.FRICTION, GOALS)
                PLAYER_POD.checkCollisions(TEST_PODS)
        else:
            if not PLAYER_POD.dead and not PLAYER_POD.hit_target:
                PLAYER_POD.update(PARAM.GRAVITY, PARAM.FRICTION, GOALS)

        PLAYER_POD.getSenserInfo(TEST_PODS + GOALS)

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


    START_POINT.draw(WINDOW)
    TEMP_GOAL.draw(WINDOW)

    WINDOW.display()

    DELTA_TIME = DELTA_CLOCK.restart()
    if not TICKS % 10:
        sys.stdout.write("\rFPS: " + str(1 / DELTA_TIME.seconds) + " | Generation: " + str(GEN_TICKS / PARAM.POD_POPULATION))
        sys.stdout.flush()

    TICKS += 1




Serializer.dump()
