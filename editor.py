from maps import *

import serializer as  serial

class Editor(object):
    CURRENT_ENT = None
    HAS_FOCUS = False

    @classmethod
    def editingLoop(cls, window):
        if not cls.HAS_FOCUS:
            return


        if cls.CURRENT_ENT == None:
            if sf.Mouse.is_button_pressed(0):
                cls.CURRENT_ENT = Obstacle((sf.Mouse.get_position(window).x, sf.Mouse.get_position(window).y), (PARAM.WIDTH  / 5.0, PARAM.HEIGHT / 50.0), 0.0, 0.0)

        else:
            cls.CURRENT_ENT.draw(window)
            cls.CURRENT_ENT.rect.position = sf.Mouse.get_position(window)
            if sf.Mouse.is_button_pressed(1):
                cls.CURRENT_ENT.rect.rotation += 2
            if not sf.Mouse.is_button_pressed(0):
                cls.CURRENT_ENT.calculateCorners()
                cls.CURRENT_ENT.calculateAxis()
                cls.CURRENT_ENT.getParams()
                serial.Serializer.MAPS[PARAM.MAP_INDEX].addObstacle(cls.CURRENT_ENT)
                cls.CURRENT_ENT = None



DEFAULT_MAP = Map(TRAINING_OBSTACLES, GOALS)
