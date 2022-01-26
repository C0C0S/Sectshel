import pygame
import os
import sys
import sqlite3
from pygame.locals import *

WIDTH = 700
HEIGHT = 500


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


pygame.init()
screen_size = (700, 500)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption('Перемещение героя')

FPS = 50


def start_screen():
    login = ''
    words = 'qwertyuiopasdfghjklzxcvbmn_-)(1234567890йцукенгшщзхъэждлорпавыфячсмитьбю '
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(login) > 0:
                    login = login[:-1]
                elif event.unicode in words or event.unicode in words.upper():
                    if len(login) < 20:
                        login += event.unicode
                elif event.key == pygame.K_RETURN:
                    return login
            fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))

            font = pygame.font.Font("StayPixelRegular.ttf", 70)
            string_rendered = font.render("The DUNGEON", 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 50
            intro_rect.x = 175
            screen.blit(string_rendered, intro_rect)

            font2 = pygame.font.Font("Fifaks10Dev1.ttf", 30)
            string_rendered = font2.render('Enter login: ', 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 250
            intro_rect.x = 100
            screen.blit(string_rendered, intro_rect)

            string_rendered = font2.render('After entering the login, click "ENTER"', 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 350
            intro_rect.x = 25
            screen.blit(string_rendered, intro_rect)

            font3 = pygame.font.Font("Fifaks10Dev1.ttf", 18)
            string_rendered = font3.render('*Login is a means of user authorization*', 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 450
            intro_rect.x = 165
            screen.blit(string_rendered, intro_rect)

            if len(login) <= 20:
                string_rendered = font2.render(login, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = 250
                intro_rect.x = 280
                screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(FPS)


def end_lvl_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
            fon = pygame.transform.scale(load_image('end_fon.png'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))

            font = pygame.font.Font("StayPixelRegular.ttf", 70)
            string_rendered = font.render("The DUNGEON", 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 50
            intro_rect.x = 175
            screen.blit(string_rendered, intro_rect)

            font2 = pygame.font.Font("Fifaks10Dev1.ttf", 45)
            string_rendered = font2.render(f'Level: {level}', 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 250
            intro_rect.x = 240
            screen.blit(string_rendered, intro_rect)

            string_rendered = font2.render(f'Moneys: {moneys}', 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 350
            intro_rect.x = 230
            screen.blit(string_rendered, intro_rect)

            font3 = pygame.font.Font("Fifaks10Dev1.ttf", 24)
            string_rendered = font3.render('Click "ENTER" to continue', 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 450
            intro_rect.x = 200
            screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
            fon = pygame.transform.scale(load_image('end__fon.png'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))

            font = pygame.font.Font("StayPixelRegular.ttf", 70)
            string_rendered = font.render("The DUNGEON", 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 50
            intro_rect.x = 175
            screen.blit(string_rendered, intro_rect)

            font2 = pygame.font.Font("Fifaks10Dev1.ttf", 42)
            string_rendered = font2.render(f'Total Moneys:', 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 200
            intro_rect.x = 220
            screen.blit(string_rendered, intro_rect)

            font4 = pygame.font.Font("Fifaks10Dev1.ttf", 60)
            string_rendered = font4.render(f'{moneys}', 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 250
            intro_rect.x = 345
            screen.blit(string_rendered, intro_rect)

            font3 = pygame.font.Font("Fifaks10Dev1.ttf", 18)
            string_rendered = font3.render('Click "ENTER" to start from the beginning', 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 450
            intro_rect.x = 165
            screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, ','), level_map))


tile_images = {
    'wall': load_image('brick.png'),
    'empty': load_image('wall.png')
}
tile_width = tile_height = 50

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
moneys_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '=':
                Door(x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                Money(x, y)
    return new_player, x, y


class Money(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(moneys_group, all_sprites)
        self.frames = ['Coin_1.png', 'Coin_2.png', 'Coin_3.png', 'Coin_4.png', 'Coin_5.png', 'Coin_6.png', 'Coin_7.png',
                       'Coin_8.png', 'Coin_9.png', 'Coin_10.png', 'Coin_11.png', 'Coin_12.png']
        self.cur_frame = 0
        self.image = pygame.transform.scale(load_image(self.frames[self.cur_frame]), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * 50 + 10
        self.rect.y = pos_y * 50 + 10
        self.mask = pygame.mask.from_surface(self.image)
        self.f = 0

    def update(self):
        if self.f == 5:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(load_image(self.frames[self.cur_frame]), (30, 30))
            self.f = 0
        else:
            self.f += 1


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(door_group, all_sprites)
        self.image = pygame.transform.scale(load_image('ladder.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * 50
        self.rect.y = pos_y * 50
        self.mask = pygame.mask.from_surface(self.image)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * 50
        self.rect.y = pos_y * 50
        if tile_type == 'wall':
            self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.idle_frames = ['Warrior_Idle_1.png', 'Warrior_Idle_2.png', 'Warrior_Idle_3.png', 'Warrior_Idle_4.png',
                            'Warrior_Idle_5.png', 'Warrior_Idle_6.png']
        self.move_frames = ['Warrior_Run_1.png', 'Warrior_Run_2.png', 'Warrior_Run_3.png', 'Warrior_Run_4.png',
                            'Warrior_Run_5.png', 'Warrior_Run_6.png', 'Warrior_Run_7.png', 'Warrior_Run_8.png', ]
        self.cur_frame = 0
        self.cur_move_frame = 0
        self.f = 0

        self.image = load_image(self.idle_frames[self.cur_frame])
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * 50
        self.rect.y = pos_y * 50
        self.pos = (pos_x * 50, pos_y * 50)
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = 'right'

    def move(self, shift_x, shift_y, obj, direction, door_group, money_group):
        self.cur_frame = 0
        self.rect.x += shift_x
        self.rect.y += shift_y
        for o in obj:
            try:
                if o.mask:
                    if pygame.sprite.collide_mask(self, o):
                        self.rect.x -= shift_x * 2
                        self.rect.y -= shift_y * 2
            except:
                pass

        for o in door_group:
            if pygame.sprite.collide_mask(self, o):
                global level
                level = level_now + 1

        for o in money_group:
            if pygame.sprite.collide_mask(self, o):
                global moneys
                moneys += 1
                o.kill()

        self.direction = direction
        if self.f == 5:
            self.cur_move_frame = (self.cur_move_frame + 1) % len(self.move_frames)
            if direction == 'right':
                self.image = load_image(self.move_frames[self.cur_move_frame])
            elif direction == 'left':
                self.image = pygame.transform.flip(load_image(self.move_frames[self.cur_move_frame]), True, False)
            self.f = 0
        else:
            self.f += 1

    def idle(self):
        self.cur_move_frame = 0
        self.cur_frame = (self.cur_frame + 1) % len(self.idle_frames)
        if self.direction == 'left':
            self.image = pygame.transform.flip(load_image(self.idle_frames[self.cur_frame]), True, False)
        else:
            self.image = load_image(self.idle_frames[self.cur_frame])


def move(hero, movement):
    if movement == "up":
        hero.move(0, -2, tiles_group, 'right', door_group, moneys_group)
    elif movement == "down":
        hero.move(0, 2, tiles_group, 'left', door_group, moneys_group)
    elif movement == "left":
        hero.move(-1.5, 0, tiles_group, 'left', door_group, moneys_group)
    elif movement == "right":
        hero.move(2, 0, tiles_group, 'right', door_group, moneys_group)
    elif movement == "ru":
        hero.move(2, -2, tiles_group, 'right', door_group, moneys_group)
    elif movement == "lu":
        hero.move(-1.5, -2, tiles_group, 'left', door_group, moneys_group)
    elif movement == "ld":
        hero.move(-1.5, 2, tiles_group, 'left', door_group, moneys_group)
    elif movement == "rd":
        hero.move(2, 2, tiles_group, 'right', door_group, moneys_group)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 700 // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - 500 // 2)


login = start_screen()

con = sqlite3.connect("data_base.sqlite")
cur = con.cursor()
data = cur.execute(f"SELECT login, level, moneys FROM users WHERE login='{login}'").fetchall()
if not data:
    cur.execute(f"INSERT INTO users (login, level, moneys) VALUES ('{login}', {0}, {0})")
    con.commit()
    data = cur.execute(f"SELECT login, level, moneys FROM users WHERE login='{login}'").fetchall()
data = data[0]

level_now = data[1]
level = data[1]
moneys = data[2]
moneys_now = data[2]
level_map = load_level(f'{level}.txt')

player, max_x, max_y = generate_level(level_map)
running = True
camera = Camera()
flag = 0
flag2 = 0
while running:
    if level != level_now:
        all_sprites = pygame.sprite.Group()
        tiles_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        door_group = pygame.sprite.Group()
        moneys_group = pygame.sprite.Group()
        try:
            level_map = load_level(f'{level}.txt')
            level_now = level
            cur.execute(f"""UPDATE users SET level='{level}', moneys='{moneys}' WHERE login='{data[0]}'""")
            con.commit()
            end_lvl_screen()
        except:
            level = 0
            level_now = 0
            level_map = load_level(f'{level}.txt')
            cur.execute(f"""UPDATE users SET level='{level}', moneys='{moneys}' WHERE login='{data[0]}'""")
            con.commit()
            end_screen()
        player, max_x, max_y = generate_level(level_map)
        camera = Camera()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                fon = pygame.transform.scale(load_image('black.png'), (WIDTH, HEIGHT))
                screen.blit(fon, (0, 0))
                r = True
                while r:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            r = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                r = False

                    font5 = pygame.font.Font("Fifaks10Dev1.ttf", 70)
                    string_rendered2 = font5.render(f'Pause', 1, pygame.Color('white'))
                    intro_rect2 = string_rendered2.get_rect()
                    intro_rect2.top = 200
                    intro_rect2.x = 265
                    screen.blit(string_rendered2, intro_rect2)

                    font6 = pygame.font.Font("Fifaks10Dev1.ttf", 30)
                    string_rendered2 = font6.render(f'Press "ESCAPE" to continue', 1, pygame.Color('white'))
                    intro_rect2 = string_rendered2.get_rect()
                    intro_rect2.top = 400
                    intro_rect2.x = 165
                    screen.blit(string_rendered2, intro_rect2)

                    pygame.display.flip()
                    clock.tick(FPS)

    if pygame.key.get_pressed()[K_d] and pygame.key.get_pressed()[K_w]:
        move(player, "ru")
    elif pygame.key.get_pressed()[K_a] and pygame.key.get_pressed()[K_w]:
        move(player, "lu")
    elif pygame.key.get_pressed()[K_a] and pygame.key.get_pressed()[K_s]:
        move(player, "ld")
    elif pygame.key.get_pressed()[K_d] and pygame.key.get_pressed()[K_s]:
        move(player, "rd")
    elif pygame.key.get_pressed()[K_w] and not pygame.key.get_pressed()[K_s]:
        move(player, "up")
    elif pygame.key.get_pressed()[K_s] and not pygame.key.get_pressed()[K_w]:
        move(player, "down")
    elif pygame.key.get_pressed()[K_a] and not pygame.key.get_pressed()[K_d]:
        move(player, "left")
    elif pygame.key.get_pressed()[K_d] and not pygame.key.get_pressed()[K_a]:
        move(player, "right")
    else:
        if flag == 5:
            player.idle()
            flag = 0
        else:
            flag += 1

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill((21, 23, 25))
    tiles_group.draw(screen)
    door_group.draw(screen)
    player_group.draw(screen)
    for money in moneys_group:
        money.update()
    moneys_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
