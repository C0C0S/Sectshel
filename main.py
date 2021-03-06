import pygame
import sqlite3
import os
import sys
import random

pygame.init()
size = widgh, height = 600, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sectshel')


def load_image(name, colorkey=None):
    fullname = os.path.join('img', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Board:
    # создание поля
    def __init__(self, width, height, login, board_id, diary, hero_pos, hero_group, road_group, enemy_group):
        self.flag = 0
        self.width = width
        self.height = height
        self.login = login
        self.cords = []

        self.road_gr = road_group
        self.enemy_gr = enemy_group

        self.hero_pos = hero_pos.split()
        self.hero = Hero(hero_group, int(self.hero_pos[1]), int(self.hero_pos[0]))
        print(self.hero_pos)
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
        # 1 - герой; 2 - кликабельный дом; 3 - входные ворота; 4 - дорога; 5 - переход на дороге; 6 - враг;
        # 21 - разрушенный дом; 22 - мусор; 23 - разрушенный забор
        self.flag = 0
        print(self.road_gr)
        for sprite in self.road_gr:
            if isinstance(sprite, Road):
                sprite.kill()
        for sprite in self.enemy_gr:
            if isinstance(sprite, Enemy):
                sprite.kill()
        self.enemy = None
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
            self.hero_pos[0], self.hero_pos[1] = '5', '5'
            self.hero.update(self.hero_pos, self.enemy)

        elif self.board_id == -1:
            self.board_id = 0
            self.generate_board()

        elif self.board_id == 1:
            for i in range(0, 11):
                for j in range(4, 7):
                    self.board[i][j] = 4
            self.board[int(self.hero_pos[0])][int(self.hero_pos[1])] = 1
            self.hero.update(self.hero_pos, self.enemy)
            for i in range(4, 7):
                self.board[0][i] = 5
            for i in range(1, 4):
                for j in range(1, 4):
                    self.board[i][j] = 2
            # сделать проверку убит ли этот моб
            self.board[1][5] = 6
            self.enemy = [Enemy(self.enemy_gr, 5, 1, 'ожившие_доспехи.png'),
                          Enemy(self.enemy_gr, 4, 1, 'enemy_vision.png'),
                          Enemy(self.enemy_gr, 6, 1, 'enemy_vision.png')]

        elif self.board_id == 3:
            for i in range(0, 11):
                for j in range(4, 7):
                    self.board[i][j] = 4
            self.board[int(self.hero_pos[0])][int(self.hero_pos[1])] = 1
            self.hero.update(self.hero_pos, self.enemy)
            for i in range(4, 7):
                self.board[0][i] = 5
                self.board[10][i] = 5
            for i in range(5, 8):
                for j in range(8, 11):
                    self.board[i][j] = 2
        print(self.board)

    def render_board(self, screen, mouse_pos):
        x = self.cell_size * self.width
        y = self.cell_size * self.height
        pygame.draw.rect(screen, (255, 255, 255), (self.left - 1, self.top - 1, x + 2, y + 2), 1)
        for i in range(11):
            for j in range(11):
                if self.board[i][j] == 2:
                    pygame.draw.rect(screen, (255, 255, 255), (self.left + self.cell_size * j,
                                                               self.top + self.cell_size * i, self.cell_size,
                                                               self.cell_size), 0)

                elif self.board[i][j] == 3:
                    pygame.draw.rect(screen, (0, 255, 255), (self.left + self.cell_size * j,
                                                             self.top + self.cell_size * i, self.cell_size,
                                                             self.cell_size), 0)
                elif self.board[i][j] in [4, 5, 1, 6]:
                    if self.flag == 0:
                        Road(self.road_gr, j, i)
        self.flag = 1
        if mouse_pos:
            self.cell_vision(mouse_pos)

    def on_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            print(cell, self.board[cell[1]][cell[0]])
            for i in range(int(self.hero_pos[0]), cell[1]):
                for j in range(int(self.hero_pos[1]), cell[0]):
                    pass
                    # столкновение с врагом

            if self.board[cell[1]][cell[0]] == 3:
                if self.cords[1] % self.cell_size == 0 or self.cords[3] % self.cell_size == 1:
                    if self.board_id == 0:
                        print('0')
                        self.board_id = 1
                        self.cur.execute(f"""UPDATE data SET board_id='{self.board_id}'
                                                WHERE login='{self.login}'""")
                        self.con.commit()
                self.generate_board()

            elif self.board[cell[1]][cell[0]] in [4, 5, 6]:
                # сделать анимацию
                a, b = int(self.hero_pos[0]), int(self.hero_pos[1])
                if a < cell[1]:
                    for i in range(a + 1, cell[1] + 1):
                        if b < cell[0]:
                            for j in range(b + 1, cell[0] + 1):
                                self.hero_pos[1] = str(j)
                                if self.hero.update(self.hero_pos, self.enemy):
                                    self.hero_pos = [str(a), str(b)]
                                    self.hero.change(self.hero_pos)
                                    return None
                        elif b > cell[0]:
                            for j in range(b - 1, cell[0] - 1, -1):
                                self.hero_pos[1] = str(j)
                                if self.hero.update(self.hero_pos, self.enemy):
                                    self.hero_pos = [str(a), str(b)]
                                    self.hero.change(self.hero_pos)
                                    return None
                        self.hero_pos[0] = str(i)
                        if self.hero.update(self.hero_pos, self.enemy):
                            self.hero_pos = [str(a), str(b)]
                            self.hero.change(self.hero_pos)
                            return None
                elif a > cell[1]:
                    for i in range(a - 1, cell[1] - 1, -1):
                        print(i)
                        if b < cell[0]:
                            for j in range(b + 1, cell[0] + 1):
                                self.hero_pos[1] = str(j)
                                if self.hero.update(self.hero_pos, self.enemy):
                                    self.hero_pos = [str(a), str(b)]
                                    self.hero.change(self.hero_pos)
                                    return None
                        elif b > cell[0]:
                            for j in range(b - 1, cell[0] - 1, -1):
                                self.hero_pos[1] = str(j)
                                if self.hero.update(self.hero_pos, self.enemy):
                                    self.hero_pos = [str(a), str(b)]
                                    self.hero.change(self.hero_pos)
                                    return None

                        self.hero_pos[0] = str(i)
                        if self.hero.update(self.hero_pos, self.enemy):
                            self.hero_pos = [str(a), str(b)]
                            self.hero.change(self.hero_pos)
                            return None

                else:
                    if b < cell[0]:
                        for j in range(b + 1, cell[0] + 1):
                            self.hero_pos[1] = str(j)
                            if self.hero.update(self.hero_pos, self.enemy):
                                self.hero_pos = [str(a), str(b)]
                                self.hero.change(self.hero_pos)
                                return None

                    elif b > cell[0]:
                        for j in range(b - 1, cell[0] - 1, -1):
                            self.hero_pos[1] = str(j)
                            if self.hero.update(self.hero_pos, self.enemy):
                                self.hero_pos = [str(a), str(b)]
                                self.hero.change(self.hero_pos)
                                return None

                if self.board[cell[1]][cell[0]] == 5:
                    print(self.cords)
                    if cell[1] == 10:
                        if self.board_id == 0:
                            end_1 = \
                                self.cur.execute(f"""SELECT end1 FROM data WHERE login='{self.login}'""").fetchall()[0][
                                    0]
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
                        if self.board_id == 3:
                            self.hero_pos[0], self.hero_pos[1] = '0', '5'
                            if self.hero.update(self.hero_pos, self.enemy):
                                self.hero_pos = [str(a), str(b)]
                                self.hero.change(self.hero_pos)
                                return None
                            self.board_id = 1
                            self.cur.execute(f"""UPDATE data SET board_id='{self.board_id}'
                                                                            WHERE login='{self.login}'""")
                            self.con.commit()
                            self.generate_board()

                    elif cell[1] == 0:
                        if self.board_id == 1:
                            self.hero_pos[0], self.hero_pos[1] = '10', '5'
                            if self.hero.update(self.hero_pos, self.enemy):
                                self.hero_pos = [str(a), str(b)]
                                self.hero.change(self.hero_pos)
                                return None
                            self.board_id = 3
                            self.cur.execute(f"""UPDATE data SET board_id='{self.board_id}'
                                                                            WHERE login='{self.login}'""")
                            self.con.commit()
                            self.generate_board()
                    elif cell[0] == 0:
                        pass
                    elif cell[0] == 10:
                        pass
                print(self.hero_pos[0] + ' ' + self.hero_pos[1])
                self.cur.execute(f"""UPDATE data SET hero_pos='{self.hero_pos[0] + ' ' + self.hero_pos[1]}'
                                                            WHERE login='{self.login}'""")
                self.con.commit()
                self.board[int(self.hero_pos[0])][int(self.hero_pos[1])] = 1
                if a in [0, 10]:
                    self.board[a][b] = 5
                else:
                    self.board[a][b] = 4
                if self.hero.update(self.hero_pos, self.enemy):
                    self.hero_pos = [str(a), str(b)]
                    self.hero.change(self.hero_pos)
                    return None

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size

        if 0 <= cell_x < self.width and 0 <= cell_y < self.height:
            return cell_x, cell_y
        return None

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

            elif self.board[cell[1]][cell[0]] == 6:
                x = cell[0] * self.cell_size + self.left
                y = cell[1] * self.cell_size + self.top
                self.cords = [x, y, self.cell_size, self.cell_size]
                pygame.draw.rect(screen, (255, 0, 0), (x, y, self.cell_size, self.cell_size), 1)

            elif self.board[cell[1]][cell[0]] == 1:
                x = cell[0] * self.cell_size + self.left
                y = cell[1] * self.cell_size + self.top
                self.cords = [x, y, self.cell_size, self.cell_size]
                pygame.draw.rect(screen, (0, 255, 0), (x, y, self.cell_size, self.cell_size), 1)


class Hero(pygame.sprite.Sprite):
    image = load_image('hero/hero_stay_0.png')

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = x * 30 + 135
        self.rect.y = y * 30 + 30
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, pos, enemy):
        if enemy is not None:
            for obj in enemy:
                if pygame.sprite.collide_mask(self, obj):
                    fight = Fight()
                    run = True
                    while run:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                                return True
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                print(event.button)
                            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                                screen.fill((0, 0, 0))
                                board.cell_vision(event.pos)
                                pos = event.pos
                                arrow.rect.x = event.pos[0]
                                arrow.rect.y = event.pos[1]
                        screen.fill(pygame.Color('Black'))
                        fight.render(screen)
                        if pygame.mouse.get_focused():
                            pygame.mouse.set_visible(False)
                            arrow_sprites.draw(screen)
                        '''
                        if fight.flag == 1:
                            for e in enemy:
                                e.kill()
                            #заносим данные в бд
                            run = False
                        '''
                        pygame.display.flip()
                        clock.tick(fps)
            self.rect.x = int(pos[1]) * 30 + 135
            self.rect.y = int(pos[0]) * 30 + 30
            return False

    def change(self, pos):
        self.rect.x = int(pos[1]) * 30 + 135
        self.rect.y = int(pos[0]) * 30 + 30


class Fight:
    def __init__(self):
        self.flag = 0

    def render(self, screen):
        if self.flag == 0:
            pass
        self.flag = 1


class Road(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = load_image(random.choice(
            ['road/floor_1.png', 'road/floor_3.png', 'road/floor_4.png', 'road/floor_5.png', 'road/floor_6.png',
             'road/floor_7.png', 'road/floor_8.png']))
        self.rect = self.image.get_rect()
        self.rect.x = x * 30 + 135
        self.rect.y = y * 30 + 30

    def update(self):
        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, x, y, sprite):
        super().__init__(group)

        self.image = load_image(sprite)
        self.rect = self.image.get_rect()
        self.rect.x = x * 30 + 135
        self.rect.y = y * 30 + 30
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


con = sqlite3.connect("data_db.sqlite")
cur = con.cursor()
data = cur.execute("SELECT login, password, board_id, diary, hero_pos FROM data").fetchall()
print(data)
con.close()

road_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
hero_sprites = pygame.sprite.Group()

board = Board(11, 11, data[0][0], data[0][2], data[0][3], data[0][4], hero_sprites, road_sprites, enemy_sprites)
fps = 45
clock = pygame.time.Clock()

image = load_image('mouse/cur.png')
arrow_image = pygame.transform.scale(image, (30, 25))
arrow_sprites = pygame.sprite.Group()

arrow = pygame.sprite.Sprite(arrow_sprites)
arrow.image = arrow_image
arrow.rect = arrow.image.get_rect()

running = True
pos = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            screen.fill((0, 0, 0))
            board.on_click(event.pos)

        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            screen.fill((0, 0, 0))
            board.cell_vision(event.pos)
            pos = event.pos
            arrow.rect.x = event.pos[0]
            arrow.rect.y = event.pos[1]
    screen.fill(pygame.Color('Black'))
    road_sprites.draw(screen)
    board.render_board(screen, pos)
    hero_sprites.draw(screen)
    enemy_sprites.draw(screen)
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
        arrow_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(fps)
