#
import pygame
from queue import PriorityQueue


#######################
# Global Constants
#######################
WIDTH = 800
ROWS = 50
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finder")

###########################
# Color Palette Constants
###########################

RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
TEAL = (64, 224, 208)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.color = WHITE
        self.x = row * width  # Pygame Window location
        self.y = col * width  # Pygame window location
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def __lt__(self, other):
        return False

    def get_pos(self):
        """Returns """
        return self.row, self.col

    def is_closed(self):
        """Has this node been visited before. If visited color will change to red"""
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_wall(self):
        return self.color == BLACK

    def is_head(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TEAL

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_wall(self):
        self.color = BLACK

    def make_end(self):
        self.color = TEAL

    def make_head(self):
        self.color = ORANGE

    def make_path(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        # Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])

        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])

        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])

        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

def a_star(draw, grid, head, end):
    draw()
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, head))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[head] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[head] = heuristic(head.get_pos(), end.get_pos())

    open_set_hash = {head}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If you hit x Pygame Quits
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            head.make_head()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.make_open()

        draw()

        if current != head:
            current.make_closed()

    return False

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()



def heuristic(p1, p2):
    """

    :param p1:
    :param p2:
    :return:
    """
    # Utilizes Manhattan distance
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


def make_grid(rows, width):
    """

    :param rows:
    :param width:
    :return:
    """
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(window, rows, width):
    """ 
    :param window:
    :param rows:
    :param width:
    :return:
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GRAY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, GRAY, (j * gap, 0), (j * gap, width))


def draw(window, grid, rows, width):
    """

    :param window:
    :param grid:
    :param rows:
    :param width:
    :return:
    """
    window.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()


def get_mouse_pos(pos, rows, width):
    """

    :param pos: Mouse location
    :param rows: Total Rows
    :param width: Width of Window
    :return: x and y position of the mouse
    """
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


def main(window, width):
    grid = make_grid(ROWS, width)

    head = None
    end = None

    run = True

    while run:
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # If left button clicked
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                node = grid[row][col]
                if not head and node != end:
                    head = node
                    head.make_head()
                elif not end and node != head:
                    end = node
                    end.make_end()
                elif node != end and node != head:
                    node.make_wall()

            elif pygame.mouse.get_pressed()[2]:  # If right button clicked
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == head:
                    head = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and head and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    a_star(lambda: draw(window, grid, ROWS, width), grid, head, end)

                if event.key == pygame.K_c:
                    head = None
                    end = None
                    grid = make_grid(ROWS, width)


    pygame.quit()


main(WINDOW, WIDTH)
