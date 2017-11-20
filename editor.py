from maps import *

import serializer as  serial

class Editor(object):
    CURRENT_ENT = None
    HAS_FOCUS = False
    MOUSE_BUTTONS = [0, 0, 0]

    @classmethod
    def editingLoop(cls, window):
        if not cls.HAS_FOCUS or sf.Mouse.get_position(window).y < 5:
            return

        if cls.MOUSE_BUTTONS[2]:
            if cls.CURRENT_ENT == None:
                cls.CURRENT_ENT = Obstacle((sf.Mouse.get_position(window).x, sf.Mouse.get_position(window).y), (PARAM.WIDTH  / 2.0, PARAM.HEIGHT / 45.0), 0.0, 0.0)
            else:
                cls.CURRENT_ENT = None

        if cls.CURRENT_ENT != None:
            cls.CURRENT_ENT.draw(window)
            cls.CURRENT_ENT.rect.position = sf.Mouse.get_position(window)
            if cls.MOUSE_BUTTONS[1]:
                cls.CURRENT_ENT.rect.rotation += 22.5
            if cls.MOUSE_BUTTONS[0]:
                cls.CURRENT_ENT.calculateCorners()
                cls.CURRENT_ENT.calculateAxis()
                cls.CURRENT_ENT.getParams()
                serial.Serializer.MAPS[PARAM.MAP_INDEX].addObstacle(cls.CURRENT_ENT)
                cls.CURRENT_ENT = None



DEFAULT_MAP = Map(TRAINING_OBSTACLES, [TEMP_GOAL])
