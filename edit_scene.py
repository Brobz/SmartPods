from scene import *

back_text = UIText(UIText.FONT, "Back", sf.Color.GREEN, sf.Vector2(0, 0), 15)
back_button = Button(sf.Color.BLACK, sf.Color.RED, back_text, sf.Vector2(50, PARAM.HEIGHT - 20), sf.Vector2(80, 20), 0)

BUTTONS = [back_button]
TEXTS = []


def update(APP):
    Editor.editingLoop(APP.window)

    for b in BUTTONS:
        b.update(APP.window, sf.Mouse.get_position(APP.window))
        if APP.mouse_buttons[0] and b.hovered:
            """" DO BUTTON ACTION """
            APP.goToScene(b.scene_id)

def draw(APP):
    Serializer.MAPS[PARAM.MAP_INDEX].tick()
    Serializer.MAPS[PARAM.MAP_INDEX].draw(APP.window)

    for t in TEXTS:
        t.render(APP.window)

    for b in BUTTONS:
        b.render(APP.window)

    START_POINT.draw(APP.window)
    
EDIT_SCENE = Scene(update, draw)
