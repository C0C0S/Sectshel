import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.board[5][5] = 1
        self.board[0][0] = 2
        self.board[0][1] = 2
        self.board[1][1] = 2
        self.board[1][0] = 2
        print(self.board)
        self.left = 135
        self.top = 30
        self.cell_size = 30

    def render(self, screen):
        x = self.cell_size * self.width
        y = self.cell_size * self.height
        pygame.draw.rect(screen, (255, 255, 255), (self.left, self.top, x, y), 1)

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
                pygame.draw.rect(screen, (100, 110, 255), (x, y, self.cell_size, self.cell_size), 1)

            elif self.board[cell[1]][cell[0]] == 2:
                if cell[1] - 3 >= 0:
                    f1 = cell[1] - 3
                else:
                    f1 = 0
                if cell[1] + 3 <= 11:
                    f2 = cell[1] + 3
                else:
                    f2 = 11

                for i in range(f1, f2):
                    if cell[0] - 3 >= 0:
                        t1 = cell[0] - 3
                    else:
                        t1 = 0
                    if cell[0] + 3 <= 11:
                        t2 = cell[0] + 3
                    else:
                        t2 = 11

                    for j in range(t1, t2):
                        if self.board[i][j] != 0:
                            x = j * self.cell_size + self.left
                            y = i * self.cell_size + self.top
                            pygame.draw.rect(screen, (100, 110, 255), (x, y, self.cell_size, self.cell_size), 1)


class Hero:
    pass


class Enemy:
    pass


pygame.init()
size = widgh, height = 600, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Under World')

board = Board(11, 11)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
        if event.type == pygame.MOUSEMOTION:
            screen.fill((0, 0, 0))
            board.cell_vision(event.pos)
    board.render(screen)
    pygame.display.flip()
