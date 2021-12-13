import pygame
import sqlite3
import os


class Board:
    # создание поля
    def __init__(self, width, height, login, board_id, diary):
        self.width = width
        self.height = height
        self.login = login
        self.cords = []
        if diary == 'None':
            diary = ''
        if not diary:
            diary = ''
        self.diary = diary
        self.con = sqlite3.connect("data_db.sqlite")
        self.cur = self.con.cursor()
        self.board = [[0] * width for _ in range(height)]
        self.board_id = board_id
        self.left = 135
        self.top = 30
        self.cell_size = 30
        self.generate_board()

    def generate_board(self):
        self.board = [[0] * self.width for _ in range(self.height)]
        if self.board_id == 0:
            print('ok')
            for i in range(2):
                for j in range(len(self.board)):
                    self.board[i][j] = 3
            for i in range(2, 11):
                for j in range(4, 7):
                    self.board[i][j] = 4
            for j in range(4, 7):
                self.board[10][j] = 5

            self.board.append(-1)
            self.board.append(1)
            self.board[5][5] = 1

        elif self.board_id == -1:
            self.board_id = 0
            self.generate_board()

        elif self.board_id == 1:
            for i in range(0, 11):
                for j in range(4, 7):
                    self.board[i][j] = 4
        print(self.board)

    def render_board(self, screen, mouse_pos):
        x = self.cell_size * self.width
        y = self.cell_size * self.height
        pygame.draw.rect(screen, (255, 255, 255), (self.left - 1, self.top - 1, x + 2, y + 2), 1)
        for i in range(11):
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
                    pygame.draw.rect(screen, (0, 255, 255), (self.left + self.cell_size * j,
                                                             self.top + self.cell_size * i, self.cell_size,
                                                             self.cell_size), 0)
                elif self.board[i][j] == 4 or self.board[i][j] == 5:
                    pygame.draw.rect(screen, (255, 0, 255), (self.left + self.cell_size * j,
                                                             self.top + self.cell_size * i, self.cell_size,
                                                             self.cell_size), 0)
        if mouse_pos:
            self.cell_vision(mouse_pos)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        print(cell, self.board[cell[1]][cell[0]])
        if self.board[cell[1]][cell[0]] == 5:
            print(self.cords)
            if cell[1] == 10:
                if self.board_id == 0:
                    end_1 = self.cur.execute(f"""SELECT end1 FROM data WHERE login='{self.login}'""").fetchall()[0][0]
                    # добавить анимацию как чел идёт
                    if end_1 == "FALSE":
                        self.board_id = -1
                        self.diary += (
                            "В прошлый свой визит, я не осмелился войти в этот пугающий город. "
                            "Уходя, недалеко от ворот я споткнулся о скелет и уведел у него в руках какую-то книгу. "
                            "Это было учение некой секты. "
                            "Единственное что удалось из него узнать, то что секта покланялась какому-то "
                            "высшему существу и описания в учении напоминали дьявола. Это одновременно интригует "
                            "и пугает, возможно вы ещё вернётесь сюда в поисках истины, но не сейчас. /")
                        self.cur.execute(f"""UPDATE data SET diary='{self.diary}', end1='TRUE' 
                        WHERE login='{self.login}'""")
                        self.con.commit()
                        self.generate_board()
            elif cell[1] == 0:
                pass
            elif cell[0] == 0:
                pass
            elif cell[0] == 10:
                pass

        elif self.board[cell[1]][cell[0]] == 3:
            if self.cords[1] % self.cell_size == 0 or self.cords[3] % self.cell_size == 1:
                if self.board_id == 0:
                    print('0')
                    self.board_id = 1
                    self.cur.execute(f"""UPDATE data SET board_id='{self.board_id}'
                                            WHERE login='{self.login}'""")
                    self.con.commit()
                    self.generate_board()

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
            if self.board[cell[1]][cell[0]] in [0, 4, 5]:
                x = cell[0] * self.cell_size + self.left
                y = cell[1] * self.cell_size + self.top
                self.cords = [x, y, self.cell_size, self.cell_size]
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
                self.cords = [x_min, y_min, x, y]
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
                self.cords = [x_min, y_min, x, y]
                pygame.draw.rect(screen, (255, 255, 0), (x_min, y_min, x, y), 1)

            elif self.board[cell[1]][cell[0]] == 1:
                x = cell[0] * self.cell_size + self.left
                y = cell[1] * self.cell_size + self.top
                self.cords = [x, y, self.cell_size, self.cell_size]
                pygame.draw.rect(screen, (255, 255, 0), (x, y, self.cell_size, self.cell_size), 1)


class Hero:
    pass


class Enemy:
    pass


pygame.init()
size = widgh, height = 600, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sectshel')
try:
    os.mkdir("upload")

except Exception:
    pass

con = sqlite3.connect("data_db.sqlite")
cur = con.cursor()
data = cur.execute("SELECT login, password, board_id, diary FROM data").fetchall()
print(data)
con.close()
board = Board(11, 11, data[0][0], data[0][2], data[0][3])
fps = 30
clock = pygame.time.Clock()

running = True
pos = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            screen.fill((0, 0, 0))
            board.get_click(event.pos)
        if event.type == pygame.MOUSEMOTION:
            screen.fill((0, 0, 0))
            board.cell_vision(event.pos)
            pos = event.pos
    board.render_board(screen, pos)
    pygame.display.flip()
    clock.tick(fps)
