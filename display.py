import pygame
from config import window_size

pygame.init()

window = pygame.display.set_mode(window_size, flags=pygame.DOUBLEBUF)
display = pygame.Surface(
    (int(window.get_width()*0.5), int(window.get_height()*0.5)))
