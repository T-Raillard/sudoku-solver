from os import sys, environ
import copy
import pygame
from sudoku_classes import Square, Button
from sudoku_consts import *

# initialize the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("    Sudoku Solver")
icon = pygame.image.load(r'C:\Users\Tristan Raillard\Documents\Python\pygame\assets\ksudoku_103845 (1).ico')
pygame.display.set_icon(icon)

# initiate a list of last 10 state of the grid for the "back" button
saved = []

# initiate the PRETTY variables
PRETTY = True

# create all 81 squares
border_offset_x = 0
border_offset_y = 0
for i in range(9):
    if i % 3 == 0 and i != 0:
        border_offset_x += 1

    for j in range(9):
        if j % 3 == 0 and j != 0:
            border_offset_y += 1

        x = GRID_x + EXT_BORDER + i * (SQUARE_WIDTH + INN_BORDER) + border_offset_x
        y = GRID_y + EXT_BORDER + j * (SQUARE_WIDTH + INN_BORDER) + border_offset_y
        Square(x, y, i, j)

    border_offset_y = 0

def main():
    """Main fonction, loops through every frame"""
    solve_button = Button("BACK", back)
    clear_button = Button("CLEAR", clear)
    check_button = Button("CHECK", check)
    solve_button = Button("SOLVE", solve)

    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(*event.pos)
            
            if event.type == pygame.KEYDOWN:
                handle_key(event.key)
    
        draw_window()
    
def draw_window():
    """Called with each frame to draw the window"""
    # background
    WIN.fill(BG_COLOR)

    # external border
    pygame.draw.rect(WIN, EXT_BORDER_COLOR, pygame.Rect(GRID_x, GRID_y, GRID_WIDTH, GRID_WIDTH))

    # inner border
    for i in range(3):
        for j in range(3):
            x = GRID_x + EXT_BORDER + i * (3 * SQUARE_WIDTH + 4 * INN_BORDER)
            y = GRID_y + EXT_BORDER + j * (3 * SQUARE_WIDTH + 4 * INN_BORDER)
            width = 3 * SQUARE_WIDTH + 2 * INN_BORDER
            pygame.draw.rect(WIN, INN_BORDER_COLOR, pygame.Rect(x, y, width, width))

    # squares
    for square in Square.all:
        square.draw(WIN)

    # buttons
    for button in Button.all:
        button.draw(WIN)

    # "pretty" checkbox
    pygame.draw.rect(WIN, PRETTY_CIRCLE_COLOR, pygame.Rect(
        ((WIDTH + GRID_WIDTH) / 2 + OFFSET + WIDTH) / 2 - BUTTON_WIDTH + 10,
        HEIGHT / 2 + (len(Button.all) / 2) * BUTTON_HEIGHT * 2 - 10,
        20,
        20,
    ), border_radius=10)
    if PRETTY:
        pygame.draw.rect(WIN, PRETTY_CIRCLE_SEL_COLOR, pygame.Rect(
            ((WIDTH + GRID_WIDTH) / 2 + OFFSET + WIDTH) / 2 - BUTTON_WIDTH + 12,
            HEIGHT / 2 + (len(Button.all) / 2) * BUTTON_HEIGHT * 2 - 8,
            16,
            16,
        ), border_radius=8)
    pretty_txt = FONT20.render("show solving", False, BUTTON_COLOR)
    WIN.blit(pretty_txt, (
        ((WIDTH + GRID_WIDTH) / 2 + OFFSET + WIDTH) / 2 - BUTTON_WIDTH / 2,
        HEIGHT / 2 + (len(Button.all) / 2) * BUTTON_HEIGHT * 2 - pretty_txt.get_rect().height / 2
    ))

    pygame.display.update()

def handle_click(x, y):
    """handles the event MOUSEBUTTONDOWN"""
    global PRETTY

    # unselect squares, then looks if clicked
    for square in Square.all:
        if square.check_clicked(x, y):
            square.selected = not square.selected
            square.color = SEL_SQUARE_COLOR if square.selected else SQUARE_COLOR
        else:
            square.selected = False
            square.color = SQUARE_COLOR    

    # looks if a button is clicked
    for button in Button.all:
        if button.check_clicked(x, y):
            if button.msg != "BACK":
                save()
            button.click()
    
    # looks if the checkbox is clicked
    if (((WIDTH + GRID_WIDTH) / 2 + OFFSET + WIDTH) / 2 - BUTTON_WIDTH + 10) < x < (((WIDTH + GRID_WIDTH) / 2 + OFFSET + WIDTH) / 2 - BUTTON_WIDTH + 30) and (HEIGHT / 2 + (len(Button.all) / 2) * BUTTON_HEIGHT * 2 - 10) < y < (HEIGHT / 2 + (len(Button.all) / 2) * BUTTON_HEIGHT * 2 + 10):
        PRETTY = not PRETTY

def handle_key(key):
    """handles the event KEYDOWN"""
    # selects only numbers or backspace, or returns
    key = pygame.key.name(key).strip('[').strip(']')
    try:
        if key != "backspace":
            key = int(key)
            assert key != 0
    except (ValueError, AssertionError):
        return
    # looks for a selected square and writes key in it
    for square in Square.all:
        if square.selected:
            save()
            if key == "backspace":
                square.clear()
            else:
                square.write(key)
            return

def save():
    """when a change is made, copies the former grid in saved"""
    if len(saved) == 10:
        saved.pop(0)
    saved.append(copy.deepcopy(Square.all))

def back(): 
    """Callback fonction for button Back"""
    if len(saved) == 0:
        return
    former = saved.pop()
    for i in range(81):
       Square.all[i] = former[i]

def clear():
    """Callback fonction for button Clear"""
    for square in Square.all:
        square.clear()

def check():
    """Callback fonction for button Check"""
    all_legal = True
    for square in Square.all:
        if not square.legal:
            square.number_color = RED
            all_legal = False
    
    return all_legal

def solve():
    """Callback fonction for button Solve"""
    if not check():
        return
 
    # set impossible values
    unsolved = Square.all.copy()
    for square in Square.all:
        if square.value != "":
            unsolved.remove(square)
    
    index = 0
    while index < len(unsolved):
        index = unsolved[index].solve(unsolved, WIN, PRETTY)
    print("solved !")

if __name__ == "__main__":
    main()