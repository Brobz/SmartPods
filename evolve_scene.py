from scene import *

fps_text = UIText(UIText.FONT, "FPS: 0", sf.Color.RED, sf.Vector2(30, 12), 12)
generation_text = UIText(UIText.FONT, "Generation: 0", sf.Color.BLACK, sf.Vector2(53, 25), 12)

back_text = UIText(UIText.FONT, "Back", sf.Color.GREEN, sf.Vector2(0, 0), 15)
back_button = Button(sf.Color.BLACK, sf.Color.RED, back_text, sf.Vector2(50, PARAM.HEIGHT - 20), sf.Vector2(80, 20), 0)


BUTTONS = [back_button]
TEXTS = [fps_text, generation_text]



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
TICKS = 0

BEST_POOL = 2

BEST_FITNESSES = [0 for i in xrange(BEST_POOL)]
BEST_BRAINS = [copy.deepcopy(TRAINING_PODS[i].nn.weights) for i in xrange(BEST_POOL)]


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

def evolve(APP):
    global PODS, TRAINING_PODS, GEN_TICKS, BEST_FITNESSES, BEST_BRAINS, DEAD_PODS

    if PARAM.EDITING:
        Editor.editingLoop(APP.window)
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
        p.draw(APP.window)


    Serializer.MAPS[PARAM.MAP_INDEX].tick()
    Serializer.MAPS[PARAM.MAP_INDEX].draw(APP.window)

def update(APP):
    global TICKS, DELTA_TIME, DELTA_CLOCK, GEN_TICKS

    evolve(APP)

    for b in BUTTONS:
        b.update(APP.window, sf.Mouse.get_position(APP.window))
        if APP.mouse_buttons[0] and b.hovered:
            """" DO BUTTON ACTION """
            APP.prevScene()

    DELTA_TIME = DELTA_CLOCK.restart()
    if not TICKS % 10:
        fps_text.setText("FPS: " + str(math.floor(1 / DELTA_TIME.seconds)))
        generation_text.setText("Generation: " + str(GEN_TICKS / PARAM.POD_POPULATION))
        #sys.stdout.write("\rFPS: " + str(1 / DELTA_TIME.seconds) + " | Generation: " + str(GEN_TICKS / PARAM.POD_POPULATION))
        #sys.stdout.flush()

    TICKS += 1

def draw(APP):
    for t in TEXTS:
        t.render(APP.window)

    for b in BUTTONS:
        b.render(APP.window)

    START_POINT.draw(APP.window)

EVOLVE_SCENE = Scene(update, draw)
