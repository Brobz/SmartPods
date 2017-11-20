from sfml import sf

class UIText(object):
    FONT  = sf.Font.from_file("Welbut.ttf")
    def __init__(self, font, text, color, position, size):
        self.font = font
        self.label = sf.Text()
        self.label.font = self.font
        self.text = text
        self.label.string = unicode(self.text)
        self.color = color
        self.label.color = self.color
        self.position = position
        self.size = size
        self.label.character_size = self.size
        self.hover_color = sf.Color.CYAN

        self.centerText()
        self.setPosition(self.position)

    def render(self, window, hovered = False):
        if(hovered):
            self.label.color = self.hover_color
        window.draw(self.label)
        self.label.color = self.color

    def setPosition(self, new_pos):
        self.position = new_pos
        self.label.position = self.position

    def setText(self, new_text):
        self.text = new_text
        self.label.string = unicode(self.text)

    def setSize(self, _size):
        self.size = _size
        self.label.character_size = self.size
        
    def centerText(self):
        text_rect = self.label.local_bounds
        self.label.origin = (text_rect.left + text_rect.width / 2.0, text_rect.top + text_rect.height / 2.0)
