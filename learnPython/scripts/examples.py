import pygame
import sys
import time
import random
import math
from pygame.locals import *

clock = pygame.time.Clock()

square_width = int(1000/8)
pygame.init()

class bubble_sort:

    def __init__(self, size):

        pygame.init()
        self.screen = pygame.display.set_mode((1440, 900), FULLSCREEN)
        self.sw = self.screen.get_rect().width
        self.sh = self.screen.get_rect().height
        self.font = pygame.font.SysFont("monospace", 60)
        self.array = list(range(size))
        self.nodes = [None] * size
        self.labels = [None] * size
        sorted_array = list(self.array)
        random.shuffle(self.array)
        self.size = size
        self.selected = (None, None) # Tuple of the last 2 selected values.
        self.num_processes = 0
        self.solved = False
        print(self.array)
        self.draw_circles()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.sort()
            if self.array == sorted_array:
                self.solved = True
            clock.tick(14)

    def draw_circles(self):

        self.screen.fill((255, 255, 255))

        radius = (self.sw // self.size) // 4
        for elem in self.array:
            if elem in self.selected:
                 color =(50, 255, 50)
            else:
                color = (0, 0, 0)

            posx = radius * 2 + self.array.index(elem) * 4 * radius
            posy = self.sh // 2

            pygame.draw.circle(self.screen,
                               color,
                               (posx, posy),
                               radius,
                               1)
            label = self.font.render(str(elem), 1, (0, 0, 0))
            size = self.font.size(str(elem))
            self.screen.blit(label,
                        (posx - size[0]/2, posy - size[1]/2))
        self.display_stats()
        pygame.display.flip()

    def display_stats(self):

        label = self.font.render("Num Elements : " + str(self.size), 5, (0,0,0))
        size = self.font.size("Num Elements : " + str(self.size))
        self.screen.blit(label,
                    (self.sw / 2 - size[0]/2, self.sh / 3))
        label = self.font.render("Num proccesses : " + str(self.num_processes), 5, (0, 0, 0))
        size = self.font.size("Num proccesses : " + str(self.num_processes))
        self.screen.blit(label,
                    (self.sw / 2 - size[0] / 2, self.sh / 4))
        label = self.font.render("Bubble time complexity : o(N^2) ", 5, (0, 0, 0))
        size = self.font.size("Bubble time complexity : o(N^2) ")
        self.screen.blit(label,
                    (self.sw / 2 - size[0] / 2, self.sh/4 - (self.sh/3 - self.sh/4)))

    def sort(self):
        for i in range(self.size - 1):
            self.wait_for_key()
            if not self.solved:
                self.num_processes += 1
            self.selected = (self.array[i], self.array[i + 1])
            self.draw_circles()
            if self.array[i] > self.array[i + 1]:
                self.wait_for_key()
                self.swap_nodes(self.array[i], self.array[i+1])
                self.array[i], self.array[i + 1] = self.array[i + 1], self.array[i]
                if not self.solved:
                    self.num_processes += 1
            self.draw_circles()



    def swap_nodes(self, node1, node2):

        """
        This function creates an animation which swaps two nodes.
        """

        radius = (self.sw // self.size) // 4

        angle = 0

        while angle <= 180:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()

            self.screen.fill((255, 255, 255))
            print(angle)

            posx1 = radius * 2 + self.array.index(node1) * 4 * radius
            posy1 = self.sh // 2
            posx2 = radius * 2 + self.array.index(node2) * 4 * radius
            posy2 = self.sh // 2

            x = int(math.sin((angle * math.pi) / 180) * 2 * radius)
            y = int(math.sin((angle * math.pi) / 180) * 2 * radius)

            if angle >= 90:
                circle1 = posx2 - x
                circle2 = posx1 + x
            else:
                circle1 = posx1 + x
                circle2 = posx2 - x

            print(circle1, circle2, angle)

            # circle 1
            pygame.draw.circle(self.screen, (50, 255, 50), (circle1, posy1 + y), radius, 1)
            label = self.font.render(str(node1), 1, (0, 0, 0))
            size = self.font.size(str(node1))
            self.screen.blit(label,
                        (circle1 - size[0] / 2, posy1 + y - size[1] / 2))

            # circle 2
            pygame.draw.circle(self.screen, (50, 255, 50), (circle2, posy2 - y), radius, 1)
            label = self.font.render(str(node2), 1, (0, 0, 0))
            size = self.font.size(str(node2))
            self.screen.blit(label,
                        (circle2 - size[0] / 2, posy2 - y - size[1] / 2))

            temp = list(self.array)
            temp.remove(node1)
            temp.remove(node2)

            for elem in temp:
                i = self.array.index(elem)

                posx = radius * 2 + i * 4 * radius
                posy = self.sh // 2

                pygame.draw.circle(self.screen,
                                   (0, 0, 0),
                                   (radius * 2 + i * 4 * radius, self.sh // 2),
                                    radius,
                                   1)
                label = self.font.render(str(elem), 1, (0, 0, 0))
                size = self.font.size(str(elem))
                self.screen.blit(label,
                            (posx - size[0] / 2, posy - size[1] / 2))
            self.display_stats()
            clock.tick(120)
            angle += 5
            pygame.display.flip()



    def wait_for_key(self):

        """
        This function keeps the frame running until the user presses the right arrow.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                if event.type == pygame.QUIT:
                    pygame.quit()

class queue:

    def __init__(self):

        self.queue = []

    def enqueue(self, elem):

        self.queue.append(elem)

    def dequeue(self):

        return self.queue.pop()



class adjacency_matrix:

    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.adj = {}
        self.setup_table()
        print(self.adj)

    def setup_table(self):

        for node in range(self.num_nodes):
            self.adj[node] = []
        for node in range(self.num_nodes):
            for connection in range(random.randint(1, 3)):
                random_connection = random.choice(range(self.num_nodes))
                duplicate = False
                for tuple in self.adj[node]:
                    if random_connection == tuple[0]:
                        duplicate = True
                if (not duplicate) and (len(self.adj[node]) <= 2) and (node != random_connection):
                    random_weight = random.randint(1, 5)
                    self.adj[node].append((random_connection, random_weight))
                    self.adj[random_connection].append((node, random_weight))

    def distance(self, node1, node2):

        for tuple in self.adj[node1]:
            if tuple[0] == node2:
                return tuple[1]
        return 20

class dijkstra:

    def __init__(self, num_nodes):
        pygame.init()
        self.screen = pygame.display.set_mode((1440, 900), FULLSCREEN)
        self.sw = self.screen.get_rect().width
        self.sh = self.screen.get_rect().height
        self.sw = pygame.display.get_r
        self.node_count = num_nodes
        self.matrix = adjacency_matrix(num_nodes)
        self.queue = queue() # Max priority queue
        self.setup_table()
        self.get_shortest_path()

    def setup_table(self):



    def get_shortest_path(self):

        self.distances = [None] * self.node_count
        self.path = [None] * self.node_count
        for i in range(self.node_count):
            self.distances[i] = 20
            self.path[i] = -1
            self.queue.enqueue(i)
        self.queue.queue.reverse()
        self.distances[0] = 0
        while len(self.queue.queue) > 0:
            u = self.queue.dequeue()
            rq = list(self.queue.queue)
            rq.reverse()
            for v in rq:
                if self.matrix.distance(u, v) > 0:
                    a = self.distances[u] + self.matrix.distance(u, v)
                    if a < self.distances[v]:
                        self.distances[v] = a
                        self.path[v] = u

        return self.distances[-1], self.path

dijkstra(6)
#bubble_sort(10)


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

            label = self.font.render("num of tries = " + str(counter), 1, (255, 0, 0))
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
