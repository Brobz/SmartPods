from UItext import *

class Button(object):
    def __init__(self, rest_color, hover_color, text, position, size, _id = 0):
        self.rest_color = rest_color
        self.hover_color = hover_color
        self.rect = sf.RectangleShape(size)
        self.rect.outline_color = sf.Color.BLACK
        self.rect.outline_thickness = 2
        self.rect.origin = (self.rect.size.x / 2.0, self.rect.size.y / 2.0)
        self.rect.position = position

        self.text = text
        self.text.setPosition(self.rect.position)
        self.state = True
        self.hovered = False

        self.scene_id = _id

    def isHovered(self, mouse_pos):
        if(mouse_pos.x >= self.rect.position.x - self.rect.size.x / 2.0 and mouse_pos.x <= self.rect.position.x + self.rect.size.x / 2.0 and mouse_pos.y >= self.rect.position.y - self.rect.size.y / 2.0 and mouse_pos.y <= self.rect.position.y + self.rect.size.y / 2.0):
            return True

        return False

    def update(self, window, mouse_pos):
        self.hovered = self.isHovered(mouse_pos)
        self.render(window)


    def render(self, window):
        if(self.state):
            if(self.hovered):
                self.rect.fill_color = self.hover_color
                window.draw(self.rect)
                self.text.render(window, True)
            else:
                self.rect.fill_color = self.rest_color
                window.draw(self.rect)
                self.text.render(window)
