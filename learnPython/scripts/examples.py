import pygame
import sys
import time

class eightQueens:

    def __init__(self):

        self.queen_count = 0

        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]

    def add_queen(self, x, y):

        """
        This function adds a queen to the board.
        """

        if self.in_range(x, y):
            self.board[y][x] = 1
            self.queen_count += 1

    def remove_queen(self, x ,y):

        """
        This function adds a queen to the board.
        """

        if self.in_range(x, y):
            self.board[y][x] = 0
            self.queen_count -= 1

    def in_range(self, x, y):

        """
        This function checks if a coordinate is in range.
        """

        return 0 <= x < 8 and 0 <= y < 8

    def in_check(self, x, y):

        """
        This function checks if a coordinate is in check.
        """

        if 1 in self.board[y]:
            return True

        for row in self.board:
            if row[x] == 1:
                return True

        if self.board[y][x] == 1:
            return True

        x_modifier, y_modifier = 0, 0
        while True:
            x_modifier += 1
            y_modifier += 1
            if self.in_range(x + x_modifier, y + y_modifier):
                if self.board[y + y_modifier][x + x_modifier] == 1:
                    return True
            if self.in_range(x - x_modifier, y - y_modifier):
                if self.board[y - y_modifier][x - x_modifier] == 1:
                    return True
            if self.in_range(x - x_modifier, y + y_modifier):
                if self.board[y + y_modifier][x - x_modifier] == 1:
                    return True
            if self.in_range(x + x_modifier, y - y_modifier):
                if self.board[y - y_modifier][x + x_modifier] == 1:
                    return True
            elif x - x_modifier < 0 and x + x_modifier > 7:
                return False

sw = 1000
sh = 1000

square_width = int(1000/8)

class eightQueensGUI:

    def __init__(self):

        self.screen = pygame.display.set_mode((sw, sh))
        self.game = eightQueens()
        self.clock = pygame.time.Clock()
        pygame.init()
        self.font = pygame.font.SysFont("monospace", 60)
        self.counter = 0
        self.board_positions = []
        self.recursivley_solve()
        self.run()


    def run(self):

        counter = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            self.setup_board(eval(self.board_positions[counter % len(self.board_positions)]))
            counter += 1

            label = self.font.render(str(counter), 1, (255, 0, 0))
            self.screen.blit(label, (500, 100))

            if 10 < counter < 30:
                label = self.font.render("We try all combinations", 1, (255, 0, 0))
                self.screen.blit(label, (100, 300))

            if counter == 30:
                counter = len(self.board_positions) - 30

            if counter == len(self.board_positions):
                label = self.font.render("Now all 8 queens are coexisting", 1, (255, 0, 0))
                self.screen.blit(label, (100, 300))

            if counter >= len(self.board_positions):
                counter -= 1

            self.clock.tick(60)
            pygame.display.update()

    def recursivley_solve(self):
        for x in range(8):
            for y in range(8):
                if not self.game.in_check(x, y):
                    # choose
                    self.game.add_queen(x, y)

                    self.board_positions.append(str(self.game.board))
                    # explore
                    self.recursivley_solve()
                    if self.game.queen_count == 8:
                        return
                    # unchoose
                    self.game.remove_queen(x, y)


    @staticmethod
    def quit():

        pygame.display.quit()
        pygame.quit()

    def setup_board(self, board):

        self.screen.fill((0, 0, 0))
        for x in range(8):
            for y in range(8):
                self.draw_square(x, y)
                if board[y][x] == 1:
                    self.draw_piece(x, y)
        pygame.display.update()

    def draw_piece(self, x, y):

        piece = pygame.image.load("queen.png")
        piece = pygame.transform.scale(piece, (square_width, square_width))
        self.screen.blit(piece, (x * square_width, y * square_width))

    def draw_square(self, x, y):

        white = (255, 255, 255)
        green = (152, 251, 152)
        color = green
        if (x + y) % 2 == 0:
            color = white
        pygame.draw.rect(self.screen, color, (x * square_width, y * square_width, square_width, square_width))
