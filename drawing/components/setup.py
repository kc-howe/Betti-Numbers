import pygame

pygame.init()

DISPLAY_INFO = pygame.display.Info()
SIZE = WIDTH, HEIGHT = DISPLAY_INFO.current_w, DISPLAY_INFO.current_h
SCREEN = pygame.display.set_mode(SIZE)

# Define colors
BACKGROUND_COLOR = (244, 244, 249, 255)
LINE_COLOR = (53, 53, 53, 255)
VERTEX_COLOR = (180, 197, 228, 255)
FACE_COLOR = (0, 105, 146, 100)
SOLID_COLOR = (59, 71, 130, 150)
SELECT_COLOR = (255, 73, 92)