from scene import *

select_map_text = UIText(UIText.FONT, "Select Map", sf.Color.GREEN, sf.Vector2(PARAM.WIDTH / 2.0, PARAM.HEIGHT / 6.0), 75)

back_text = UIText(UIText.FONT, "Back", sf.Color.GREEN, sf.Vector2(0, 0), 15)
back_button = Button(sf.Color.BLACK, sf.Color.RED, back_text, sf.Vector2(50, PARAM.HEIGHT - 20), sf.Vector2(80, 20), 0)

BUTTONS = [back_button]
MAP_BUTTONS = []
TEXTS = [select_map_text]
MAP_BUTTONS = []

def makeButtons():
    global MAP_BUTTONS
    MAP_BUTTONS = []
    for i in xrange(len(Serializer.MAPS)):
        _text = UIText(UIText.FONT, "MAP " + str(i), sf.Color.GREEN, sf.Vector2(0, 0), 20)
        _button = Button(sf.Color.BLACK, sf.Color.RED, _text, sf.Vector2(PARAM.WIDTH / 2.0, 200 + i * 50), sf.Vector2(120, 24), i)

        MAP_BUTTONS.append(_button)

def update(APP):
    if APP.makeButtons:
        makeButtons()
        APP.makeButtons = False

    for b in BUTTONS:
        b.update(APP.window, sf.Mouse.get_position(APP.window))
        if APP.mouse_buttons[0] and b.hovered:
            """" DO BUTTON ACTION """
            APP.goToScene(b.scene_id)

    for b in MAP_BUTTONS:
        b.update(APP.window, sf.Mouse.get_position(APP.window))
        if APP.mouse_buttons[0] and b.hovered:
            """" DO BUTTON ACTION """
            PARAM.MAP_INDEX = b.scene_id
            APP.goToScene(2)

def draw(APP):
    for t in TEXTS:
        t.render(APP.window)

    for b in BUTTONS + MAP_BUTTONS:
        b.render(APP.window)

makeButtons()
SELECT_EVOLUTION_SCENE = Scene(update, draw)
