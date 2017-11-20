from main_menu_scene import *
from select_evolution_scene import *
from evolve_scene import *
from sandbox_scene import *
from edit_scene import *
from select_edit_scene import *

class App(object):
    def __init__(self, scenes):
        ## SET WINDOW VARIABLES AND PARAMETERS
        self.window = sf.RenderWindow(sf.VideoMode(PARAM.WIDTH, PARAM.HEIGHT), unicode("SmartPods"), sf.Style.CLOSE)
        self.window.framerate_limit = PARAM.MAX_FRAMERATE
        self.window.key_repeat_enabled = False

        self.scenes = scenes
        self.current_scene = 0

        self.mouse_buttons = [0, 0, 0]

        self.makeButtons = False


    def run(self):
        while self.window.is_open:
            self.window.clear(sf.Color.WHITE)

            self.mouse_buttons = [0, 0, 0]

            for event in self.window.events:
                if event.type == sf.Event.CLOSED:
                    self.window.close()

                if event.type == sf.Event.MOUSE_BUTTON_PRESSED:
                    self.mouse_buttons[event["button"]] = 1

                if event.type == sf.Event.GAINED_FOCUS:
                    Editor.HAS_FOCUS = True

                if event.type == sf.Event.LOST_FOCUS:
                    Editor.HAS_FOCUS = False

            Editor.MOUSE_BUTTONS = self.mouse_buttons

            self.scenes[self.current_scene].tick(self)

            self.window.display()

    def goToScene(self, scene):
        self.current_scene = scene

        self.makeButtons = True

    def nextScene(self):
        self.current_scene += 1
        if self.current_scene > len(self.scenes) - 1:
            self.current_scene = 0


        self.makeButtons = True


    def prevScene(self):
        self.current_scene -= 1
        if self.current_scene < 0:
            self.current_scene = len(self.scenes) - 1


        self.makeButtons = True
