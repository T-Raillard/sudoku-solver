"""initialize constant variables"""
import pygame

# dimensions
TASKBAR = 30
WIDTH, HEIGHT = 1000, 550
GRID_WIDTH = 500
OFFSET = -100
GRID_x = WIDTH / 2 - GRID_WIDTH / 2 + OFFSET 
GRID_y = HEIGHT / 2 - GRID_WIDTH / 2 + TASKBAR
INN_BORDER = 1
EXT_BORDER = 2 * INN_BORDER
SQUARE_WIDTH = round((GRID_WIDTH - 14 * INN_BORDER - 2) / 9)
BUTTON_WIDTH, BUTTON_HEIGHT = 80, 40
PACE_INTERFACE_WIDTH, PACE_INTERFACE_HEIGHT = BUTTON_WIDTH - OFFSET * 2, 50
FPS = 50

# colors
BG_COLOR = (55, 57, 84)
EXT_BORDER_COLOR = (107, 214, 175)
INN_BORDER_COLOR = (113, 199, 199)
BUTTON_COLOR = EXT_BORDER_COLOR
BUTTON_FONT_COLOR = BG_COLOR
SQUARE_COLOR = (66, 74, 99)
SEL_SQUARE_COLOR = (96, 105, 135)
SQUARE_FONT_COLOR = (231, 237, 230)
PACE_INTERFACE_COLOR = (147, 181, 219)
RED = (214, 49, 49)
GREEN = (21, 230, 80)

# fonts
pygame.font.init()
FONT30 = pygame.font.Font(r'C:\Users\Tristan Raillard\Documents\Python\pygame\assets\Roboto-Regular.ttf', 30)
FONT20 = pygame.font.Font(r'C:\Users\Tristan Raillard\Documents\Python\pygame\assets\Roboto-Regular.ttf', 20)
