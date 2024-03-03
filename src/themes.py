from color import Color


class Theme:
    
    def __init__(self, light_bg, dark_bg) -> None:
        self.bg = Color(light_bg, dark_bg)
        self.move = (128, 128, 128, 100)
        