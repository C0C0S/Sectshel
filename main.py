import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y_dash in range(self.width):
            for x_dash in range(self.height):
                x = self.left + self.cell_size * y_dash
                y = self.top + self.cell_size * x_dash
                if self.board[x_dash][y_dash] == 0:
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, self.cell_size, self.cell_size), 1)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, self.cell_size, self.cell_size), 0)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size

        if 0 <= cell_x < self.width and 0 <= cell_y < self.height:
            return cell_x, cell_y
        return None

    def on_click(self, cell):
        if cell:
            for i in range(self.width):
                self.board[cell[1]][i] = (self.board[cell[1]][i] + 1) % 2
            for j in range(self.height):
                if cell[1] != j:
                    self.board[j][cell[0]] = (self.board[j][cell[0]] + 1) % 2
        print(cell)


pygame.init()
size = widgh, height = 600, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Under World')

board = Board(10, 10)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
