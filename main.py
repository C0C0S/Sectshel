import pygame
import sqlite3


class Board:
    # создание поля
    def __init__(self, width, height, id, board_id):
        self.width = width
        self.height = height
        if board_id == 0:
            self.board = [[0] * width for _ in range(height)]
            self.board[5][5] = 1
            for i in range(2):
                for j in range(len(self.board)):
                    self.board[i][j] = 3
        print(self.board)
        self.left = 135
        self.top = 30
        self.cell_size = 30

    def render(self, screen, mouse_pos):
        x = self.cell_size * self.width
        y = self.cell_size * self.height
        pygame.draw.rect(screen, (255, 255, 255), (self.left - 1, self.top - 1, x + 2, y + 2), 1)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 2:
                    pygame.draw.rect(screen, (255, 255, 255), (self.left + self.cell_size * j,
                                                               self.top + self.cell_size * i, self.cell_size,
                                                               self.cell_size), 0)
                elif self.board[i][j] == 1:
                    pygame.draw.rect(screen, (255, 255, 255), (self.left + self.cell_size * j,
                                                               self.top + self.cell_size * i, self.cell_size,
                                                               self.cell_size), 0)
                elif self.board[i][j] == 3:
                    pygame.draw.rect(screen, (255, 255, 255), (self.left + self.cell_size * j,
                                                               self.top + self.cell_size * i, self.cell_size,
                                                               self.cell_size), 0)
        if mouse_pos:
            self.cell_vision(mouse_pos)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        print(cell)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size

        if 0 <= cell_x < self.width and 0 <= cell_y < self.height:
            return cell_x, cell_y
        return None

    def on_click(self, cell):
        pass

    def cell_vision(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            if self.board[cell[1]][cell[0]] == 0:
                x = cell[0] * self.cell_size + self.left
                y = cell[1] * self.cell_size + self.top
                pygame.draw.rect(screen, (255, 255, 0), (x, y, self.cell_size, self.cell_size), 1)

            elif self.board[cell[1]][cell[0]] == 2:
                mas_i = [cell[1]]
                mas_j = [cell[0]]
                flag = True
                if cell[1] - 2 >= 0:
                    f1 = cell[1] - 2
                else:
                    f1 = 0
                if cell[1] + 2 < 11:
                    f2 = cell[1] + 3
                else:
                    f2 = 11

                for i in range(f1, f2):
                    if cell[0] - 2 >= 0:
                        t1 = cell[0] - 2
                    else:
                        t1 = 0
                    if cell[0] + 2 < 11:
                        t2 = cell[0] + 3
                    else:
                        t2 = 11

                    for j in range(t1, t2):
                        if self.board[i][j] == 2:
                            if flag:
                                mas_i.append(i)
                                flag = False
                            mas_j.append(j)
                    flag = True
                x_min = min(mas_j) * self.cell_size + self.left
                y_min = min(mas_i) * self.cell_size + self.top
                x = (max(mas_j) - min(mas_j) + 1) * self.cell_size
                y = (max(mas_i) - min(mas_i) + 1) * self.cell_size
                pygame.draw.rect(screen, (255, 255, 0), (x_min, y_min, x, y), 1)

            elif self.board[cell[1]][cell[0]] == 3:
                t = 1
                x_min = self.left
                y_min = cell[1] * self.cell_size + self.top
                x = 11 * self.cell_size
                if (cell[1] - 1) >= 0:
                    if self.board[cell[1] - 1][cell[0]] == 3:
                        t += 1
                        y_min = (cell[1] - 1) * self.cell_size + self.top
                if (cell[1] + 1) < 11:
                    if self.board[cell[1] + 1][cell[0]] == 3:
                        t += 1
                y = t * self.cell_size
                pygame.draw.rect(screen, (255, 255, 0), (x_min, y_min, x, y), 1)

            elif self.board[cell[1]][cell[0]] == 1:
                x = cell[0] * self.cell_size + self.left
                y = cell[1] * self.cell_size + self.top
                pygame.draw.rect(screen, (255, 255, 0), (x, y, self.cell_size, self.cell_size), 1)


class Hero:
    pass


class Enemy:
    pass


pygame.init()
size = widgh, height = 600, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Under World')

board = Board(11, 11, 0, 0)
running = True
pos = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
        if event.type == pygame.MOUSEMOTION:
            screen.fill((0, 0, 0))
            board.cell_vision(event.pos)
            pos = event.pos
    board.render(screen, pos)
    pygame.display.flip()
