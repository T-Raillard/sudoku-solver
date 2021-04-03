import pygame
from sudoku_consts import *

pygame.font.init()
FONT = pygame.font.Font(r'C:\Users\Tristan Raillard\Documents\Python\pygame\assets\Roboto-Regular.ttf', 30)
FONT20 = pygame.font.Font(r'C:\Users\Tristan Raillard\Documents\Python\pygame\assets\Roboto-Regular.ttf', 20)

class Button:
    """Buttons on the right of the screen; all is an array of all instances"""

    all = []

    def __init__(self, msg, fct):
        """Message gets printed on the button, fct is the the callback fonction when the the button is clicked"""
        self.msg = msg
        self.coord_x = 0
        self.coord_y = 0
        self.click = fct
        Button.all.append(self)
    
    def draw(self, win):
        """Call while drawing the window on the instance to add it to the caption"""
        self.coord_x = WIDTH / 2 - OFFSET * 2.5
        self.coord_y = (HEIGHT - BUTTON_HEIGHT) / 2 + (Button.all.index(self) - (len(Button.all) - 1) / 2) * BUTTON_HEIGHT * 1.7
        pygame.draw.rect(win, BUTTON_COLOR, pygame.Rect(self.coord_x, self.coord_y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=15)

        msg = FONT20.render(self.msg, False, BUTTON_FONT_COLOR)
        win.blit(msg, (self.coord_x + (BUTTON_WIDTH - msg.get_rect().width) / 2, self.coord_y + (BUTTON_HEIGHT - msg.get_rect().height) / 2))
    
    def check_clicked(self, x, y):
        """Check from coordinates if they correspond to the instance's location"""
        return self.coord_x < x < self.coord_x + SQUARE_WIDTH and self.coord_y < y < self.coord_y + SQUARE_WIDTH


class Square:
    """A square designed to fit in a nine by nine sudoku grid of squares"""

    all = [[]]
    all_unordered = []

    def __init__(self, x, y, row, column):
        """Must pass coordinates and their index(row, column) in oreder to draw properly"""
        self.coord_x = x
        self.coord_y = y
        self.row = row
        self.column = column
        self.nine_square = row // 3 + (column // 3 * 3)
        self.value = ""
        self.legal = True
        self.selected = False
        self.impossible_values = []
        self.color = SQUARE_COLOR
        self.number_color = SQUARE_FONT_COLOR

        # append the instance to all and all_unordered when created
        if len(Square.all[-1]) % 9 == 0 and len(Square.all[-1]) != 0:
            Square.all.append([self])
        else:
            Square.all[-1].append(self)
        Square.all_unordered.append(self)

    def __repr__(self):
        """Prettify for debugging"""
        return f"{self.row}, {self.column}"

    def draw(self, win):
        """Call while drawing the window on the instance to add it to the caption"""
        pygame.draw.rect(win, self.color, pygame.Rect(self.coord_x, self.coord_y, SQUARE_WIDTH, SQUARE_WIDTH))
        value = FONT.render(str(self.value), False, self.number_color)
        win.blit(value, (self.coord_x + (SQUARE_WIDTH - value.get_rect().width) / 2, self.coord_y + (SQUARE_WIDTH - value.get_rect().height) / 2))

    def check_clicked(self, x, y):
        """Check from coordinates if they correspond to the instance's location"""
        return self.coord_x < x < self.coord_x + SQUARE_WIDTH and self.coord_y < y < self.coord_y + SQUARE_WIDTH
    
    def seen(self):
        """Return an array of instances which are "seen" by this instance"""
        rv = []

        # look in the row
        for square in Square.all[self.row]:
            if square != self and square.value != "":
                rv.append(square)
        
        # look in the column
        for row in Square.all:
            square = row[self.column]
            if square != self and square.value != "":
                rv.append(square)
        
        # look in the 3x3 square
        for square in Square.all_unordered:
            if square != self and square.nine_square == self.nine_square and square.value != "":
                rv.append(square)

        return rv

    def write(self, value):
        """Change the value of a square and check if it is a legal move"""
        self.value = value
        
        for square in self.seen():
            if self.value == square.value:
                self.legal = False
                square.legal = False
    
    def clear(self):
        """Errase a value and set accordingly all seen square's "legality" """
        for square in self.seen():
            if self.value == square.value:
                now_legal = True

                for seen_square in square.seen():
                    if seen_square.value == square.value and seen_square != self:
                        now_legal = False

                square.legal = now_legal
                square.number_color = SQUARE_FONT_COLOR if now_legal else square.number_color
                        
        self.value = ""
        self.legal = True
        self.number_color = SQUARE_FONT_COLOR
    
    def solve(self, unsolved, WIN):
        """recursively called to solve the puzzle"""
        index = unsolved.index(self)
 
        for sol in range(1, 10):
            pygame.display.update()
            pygame.time.wait(5)

            self.value = sol
            imp = [x.value for x in self.seen()]
            imp.extend(list(self.impossible_values))

            if sol in imp:
                self.number_color = RED
                self.draw(WIN) 
            else:
                self.number_color = GREEN
                self.draw(WIN)
                for square in unsolved[index + 1:]:
                    square.impossible_values = []
                break
            
        if sol == 9 and self.number_color == RED:
            self.value = ""
            self.draw(WIN)
            former = unsolved[index - 1]
            former.impossible_values.append(former.value)
            return former.solve(unsolved, WIN)
        elif Square.all_unordered.index(self) == 80:
            return True
        else:
            return unsolved[index + 1].solve(unsolved, WIN)  