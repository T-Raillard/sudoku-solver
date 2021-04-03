from os import sys, environ
import pygame
from sudoku_classes import Square, Button
from sudoku_consts import *

# initialize the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("    Sudoku Solver")
icon = pygame.image.load(r'C:\Users\Tristan Raillard\Documents\Python\pygame\assets\ksudoku_103845 (1).ico')
pygame.display.set_icon(icon)

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
    for square in Square.all_unordered:
        square.draw(WIN)

    # buttons
    for button in Button.all:
        button.draw(WIN)

    pygame.display.update()

def handle_click(x, y):
    """handles the event MOUSEBUTTONDOWN"""
    # unselect squares, then looks if clicked
    for square in Square.all_unordered:
        if square.check_clicked(x, y):
            square.selected = not square.selected
            square.color = SEL_SQUARE_COLOR if square.selected else SQUARE_COLOR
        else:
            square.selected = False
            square.color = SQUARE_COLOR    

    # looks if a button is clicked
    for button in Button.all:
        if button.check_clicked(x, y):
            button.click()

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
    for square in Square.all_unordered:
        if square.selected:
            if key == "backspace":
                square.clear()
            else:
                square.write(key)
            return

def back():
    """Callback fonction for button Back"""
    print("back called !")

def clear():
    """Callback fonction for button Clear"""
    for square in Square.all_unordered:
        square.clear()

def check():
    """Callback fonction for button Check"""
    all_legal = True
    for square in Square.all_unordered:
        if not square.legal:
            square.number_color = RED
            all_legal = False
    
    return all_legal

def solve():
    """Callback fonction for button Solve"""
    if not check():
        return
 
    # set impossible values
    unsolved = Square.all_unordered.copy()
    for square in Square.all_unordered:
        if square.value != "":
            unsolved.remove(square)
    
    # launch recursiveness !
    if unsolved[0].solve(unsolved, WIN):
        print("solved !")

    


if __name__ == "__main__":
    main()