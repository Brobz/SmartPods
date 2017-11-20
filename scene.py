from serializer import *
from button import *


class Scene(object):
    def __init__(self, update, draw):
        self.update = update
        self.draw = draw


    def tick(self, APP):
        self.update(APP)
        self.draw(APP)
