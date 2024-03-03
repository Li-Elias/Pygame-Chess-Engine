import pygame
import os

from themes import Theme
from sound import Sound
from constants import *


class Config:
    
    def __init__(self) -> None:
        self.themes = []
        self._add_themes()
        self.current_theme_idx = 0
        self.theme = self.themes[self.current_theme_idx]
        self.font_path = f"{PATH}/assets/fonts/Montserrat-ExtraBold.ttf"
        self.move_sound = Sound(os.path.join(f"{PATH}/assets/sounds/standard_move.ogg"))
        self.capture_sound = Sound(os.path.join(f"{PATH}/assets/sounds/standard_capture.ogg"))
    
        
    def _add_themes(self):
        grey = Theme((240, 240, 240), (200, 200, 200))
        
        self.themes = [grey]
        
        
    def get_font(self, font_size):
        return pygame.font.Font(self.font_path, font_size)
        
        
    def change_theme(self):
        self.current_theme_idx += 1
        self.current_theme_idx %= len(self.themes)
        self.theme = self.themes[self.current_theme_idx]
        