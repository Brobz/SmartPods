from scene import *

smartpods_text = UIText(UIText.FONT, "SmartPods", sf.Color.GREEN, sf.Vector2(PARAM.WIDTH / 2.0, PARAM.HEIGHT / 6.0), 100)

evolve_text = UIText(UIText.FONT, "Evolve", sf.Color.GREEN, sf.Vector2(0, 0), 20)
evolve_button = Button(sf.Color.BLACK, sf.Color.RED, evolve_text, sf.Vector2(PARAM.WIDTH / 2.0, 200), sf.Vector2(120, 24), 1)

sandbox_text = UIText(UIText.FONT, "Sandbox", sf.Color.GREEN, sf.Vector2(0, 0), 20)
sandbox_button = Button(sf.Color.BLACK, sf.Color.RED, sandbox_text, sf.Vector2(PARAM.WIDTH / 2.0, 300), sf.Vector2(120, 24), 4)

edit_text = UIText(UIText.FONT, "Edit", sf.Color.GREEN, sf.Vector2(0, 0), 20)
edit_button = Button(sf.Color.BLACK, sf.Color.RED, edit_text, sf.Vector2(PARAM.WIDTH / 2.0, 400), sf.Vector2(120, 24), 3)


BUTTONS = [evolve_button, edit_button, sandbox_button]
TEXTS = [smartpods_text]


def update(APP):
    for b in BUTTONS:
        b.update(APP.window, sf.Mouse.get_position(APP.window))
        if APP.mouse_buttons[0] and b.hovered:
            """" DO BUTTON ACTION """
            APP.goToScene(b.scene_id)

def draw(APP):
    for t in TEXTS:
        t.render(APP.window)

    for b in BUTTONS:
        b.render(APP.window)

MAIN_MENU_SCENE = Scene(update, draw)
