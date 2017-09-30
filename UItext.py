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
        self.label.position = self.position.x, self.position.y
        self.size = size
        self.label.character_size = self.size
        self.hover_color = sf.Color.CYAN
        self.label.origin = (self.size / 2.0 * len(text), self.size / 2.0)


    def render(self, window, hovered = False):
        if(hovered):
            self.label.color = self.hover_color
        window.draw(self.label)
        self.label.color = self.color

test_txt = UIText(UIText.FONT, "TEST", sf.Color.GREEN, sf.Vector2(50, 50), 10)
