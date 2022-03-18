import pygame
from copy import deepcopy
from random import choice, randrange

W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 940
FPS = 60

pygame.init()
sc = pygame.display.set_mode(RES)
pygame.display.set_caption("Tetris")
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

bg = pygame.image.load('img/img.jpg').convert()
game_bg = pygame.image.load('img/img1.jpg').convert()

pygame.mixer.music.load("snd/music.mp3")
pygame.mixer.music.play(-1)
sound = pygame.mixer.Sound("snd/sound.ogg")

main_font = pygame.font.Font('font/MarckScript-Regular.ttf', 75)
font = pygame.font.Font('font/MarckScript-Regular.ttf', 75)

title_tetris = main_font.render('TETRIS', True, pygame.Color('sienna2'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('steelblue2'))

get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))
color = get_color()

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def button(screen, position, text):
    text_render = font.render(text, 1, 'cyan')
    x, y, w, h = text_render.get_rect()
    x, y = position
    return screen.blit(text_render, (x, y))


def start():
    return True


def start_sc():
    start_sc_bg = pygame.image.load('img/start_sc.jpg').convert()
    sc.blit(start_sc_bg, (0, 0))
    title_menu = font.render('Welcome to the Tetris!!!', True, pygame.Color('Yellow'))
    sc.blit(title_menu, (20, 100))
    owner_font = pygame.font.Font('font/MarckScript-Regular.ttf', 25)
    title_owner = owner_font.render("©Elissara", True, pygame.Color('White'))
    sc.blit(title_owner, (600, 850))
    quit_bt = button(sc, (310, 400), 'Quit')
    start_bt = button(sc, (300, 300), 'Start')
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_TAB:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_bt.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                else:
                    return True
        pygame.display.update()


def game_over_sc():
    game_over = pygame.font.Font('font/Rubik_Black_Italic.ttf', 125)
    title_game_over1 = game_over.render('GAME', True, pygame.Color('Darkred'))
    title_game_over2 = game_over.render('OVER', True, pygame.Color('Darkred'))
    sc.blit(title_game_over1, (85, 290))
    sc.blit(title_game_over2, (17, 470))
    quit_bt = button(sc, (540, 865), 'Quit')
    start_bt = button(sc, (520, 795), 'Start')
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_TAB:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_bt.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                else:
                    return True
        pygame.display.update()


def paused():
    pause = pygame.image.load('img/pause.jpg').convert()
    sc.blit(pause, (170, 395))
    sc.blit(title_tetris, (475, 7))
    sc.blit(title_score, (525, 640))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 695))
    sc.blit(title_record, (525, 510))
    sc.blit(font.render(str(record), True, pygame.Color('gold')), (550, 565))
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(sc, next_color, figure_rect)

    while pause:
        pygame.display.set_caption("Tetris")
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        quit_bt = button(sc, (550, 865), 'Quit')
        continue_bt = button(sc, (485, 795), 'Continue')
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_SPACE:
                        return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_bt.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                    else:
                        return False
        pygame.display.update()



def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


start_sc()
while True:
    record = get_record()
    dx, rotate = 0, False
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))
    # delay for null lines
    for i in range(lines):
        pygame.time.wait(200)
    # control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True
            elif event.key == pygame.K_SPACE:
                paused()
    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    # move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break
    # rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure_old = deepcopy(figure_old)
                break
    # check lines
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1
            sound.play()
    # compute score
    score += scores[lines]
    # draw grid    sc.blit(title_tetris, (475, 7))
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)
    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)
    # draw next figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(sc, next_color, figure_rect)
    # draw titles
    sc.blit(title_tetris, (475, 7))
    sc.blit(title_score, (525, 640))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 695))
    sc.blit(title_record, (525, 510))
    sc.blit(font.render(str(record), True, pygame.Color('gold')), (550, 565))
    # game over
    for i in range(W):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (20, 20))
                pygame.display.flip()
                clock.tick(200)
            game_over_sc()

    pygame.display.flip()
    clock.tick(FPS)
