import pygame as pg
import random

pg.init()
Display = {"width" :650, "height" :650}
display = pg.display.set_mode((Display["width"], Display["height"]))
transparent = pg.Surface((Display["width"], Display["height"]), pg.SRCALPHA, 32)
transparent = transparent.convert_alpha()
clock = pg.time.Clock()
FPS = 60
pop = pg.mixer.Sound("pop.mp3")
explosion = pg.mixer.Sound("explosion.mp3")
eat = pg.mixer.Sound("eat.mp3")
font = pg.font.SysFont('arialbold', 30)


def board_gen():
    global board
    board = []
    for y in range(0,21):
        board.append([])
        for x in range(0,21):
            board[y].append(0)


class Snake():
    def __init__(self):
        self.x = 10
        self.y = 10
        self.width = 25
        self.length = 4
        self.charge = 4
        self.velo_x = 0
        self.velo_y = 0
        self.velo_que = [(0,0)]
        self.speed = 10
        self.sprinting = 0
        board[self.x][self.y] = "H"
    def move(self):
        global fn, sn, score
        if len(self.velo_que) > 0:
            directions = self.velo_que[0]
            if abs(self.velo_x) != abs(directions[0]):
                self.velo_x = directions[0]
            if abs(self.velo_y) != abs(directions[1]):
                self.velo_y = directions[1]
            self.velo_que.pop(0)
        next_x = self.x + self.velo_x
        next_y = self.y + self.velo_y
        if next_y == 21:
            next_y = 0
        elif next_y == -1:
            next_y = 20
        if next_x == 21:
            next_x = 0
        elif next_x == -1:
            next_x = 20
        if (board[next_y][next_x] in (0, "F", "BF", "GF")) & (((self.velo_x != 0) | (self.velo_y != 0)) & (self.charge >= 1)):
            board[self.y][self.x] = 1
            self.charge = self.charge - 1
        self.y = next_y
        self.x = next_x
        if board[self.y][self.x] == 0:
            board[self.y][self.x] = "H"
        elif board[self.y][self.x] == "F":
            board[self.y][self.x] = "H"
            self.charge += 1
            self.length += 1
            fn -= 1
            score += 1
            pg.mixer.Sound.play(eat)
        elif board[self.y][self.x] == "GF":
            board[self.y][self.x] = "H"
            global max_food
            max_food += 1
            fn -= 1
            sn -= 1
            score += 1
            pg.mixer.Sound.play(eat)
        elif board[self.y][self.x] == "BF":
            board[self.y][self.x] = "H"
            self.speed += 1
            fn -= 1
            sn -= 1
            score += 1
            pg.mixer.Sound.play(eat)
        elif (self.velo_x != 0) | (self.velo_y != 0):
            pg.mixer.Sound.play(explosion)
            pg.time.wait(1000)
            return game_over_screen()
        self.wait_time = round(2200//(self.speed * (1 + self.sprinting)))
        pg.time.wait(self.wait_time)
    def draw(self):
        for y in range(21):
            for x in range(21):
                value = board[y][x]
                if value != 0:
                    pg.draw.rect(display, (0, 0, 0), ((x) * 25 + 60, (y) * 25 + 60, self.width + 6, self.width + 6))
        for y in range(21):
            for x in range(21):
                value = board[y][x]
                if value in range(1,101):
                    if value % 2 == 1:
                        pg.draw.rect(display, (50, 255, 50), ((x)*25+63, (y)*25+63, self.width, self.width))
                    else:
                        pg.draw.rect(display, (0, 230, 0), ((x)*25+63, (y)*25+63, self.width, self.width))
                    board[y][x] = value + 1
                    if board[y][x] == self.length:
                        board[y][x] = 0
                        self.charge += 1

                elif value == "H":
                    pg.draw.rect(display, (255, 0, 0), ((x)*25+63, (y)*25+63, self.width, self.width))

                elif value == "F":
                    pg.draw.rect(display, (255, 100, 0), ((x)*25+63, (y)*25+63, self.width, self.width))

                elif value == "GF":
                    pg.draw.rect(display, (255, 200, 0), ((x)*25+63, (y)*25+63, self.width, self.width))

                elif value == "BF":
                    pg.draw.rect(display, (200, 200, 255), ((x)*25+63, (y)*25+63, self.width, self.width))


def food_gen(max_food, speed):
    global fn, sn
    if (fn < max_food) | ((score % 10 == 0) & (score > 0) & (sn < max_special_food)):
        x = random.randint(0,20)
        y = random.randint(0,20)
        if board[y][x] == 0:
            if (sn < max_special_food) & (score % 10 == 0) & (score > 0):
                if (random.randint(0,max_food**2) in (0,1)) & (sn < 1):
                    board[y][x] = "GF"
                    fn += 1
                    sn += 1
                    pg.mixer.Sound.play(pop)
                elif random.randint(0, speed) in range(5):
                    board[y][x] = "BF"
                    fn += 1
                    sn += 1
                    pg.mixer.Sound.play(pop)
            elif sn == 0:
               board[y][x] = "F"
               fn += 1
               pg.mixer.Sound.play(pop)
        else:
            return food_gen(max_food,speed)


class Gui():
    def __init__(self):
        self.x = 50
        self.y = 15
    def update(self):
        self.text = font.render('Score : ' + str(score) + '    Speed : ' + str(snake.speed) + '    Max Food : ' + str(max_food), True, (255,255,255))
        self.text_box = self.text.get_rect()
        self.text_box.x = self.x
        self.text_box.y = self.y
        display.blit(self.text, self.text_box)


def pause_menu():
    global paused
    paused = 1
    snake.draw()
    pause_text_1 = font.render('Game is Paused', True, (255,255,255))
    pause_text_2 = font.render('Press "ESC" to Continue', True, (255,255,255))
    text_box_1 = pause_text_1.get_rect()
    text_box_1.center = (Display["width"]/2, Display["height"]/2-10)
    text_box_2 = pause_text_2.get_rect()
    text_box_2.center = (Display["width"]/2, Display["height"]/2+10)
    transparent = pg.Surface((Display["width"],Display["height"]))
    transparent.set_alpha(100)
    transparent.fill((0,0,0))
    display.blit(transparent, (0,0))
    display.blit(pause_text_1, text_box_1)
    display.blit(pause_text_2, text_box_2)
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    paused = 0
                    return main_loop()


def game_over_screen():
    snake.draw()
    text_1 = font.render('You Lose', True, (255,255,255))
    text_2 = font.render('Press "Space" to Restart', True, (255,255,255))
    text_3 = font.render('Press "Esc" to Quit', True, (255,255,255))
    text_box_1 = text_1.get_rect()
    text_box_1.center = (Display["width"]/2, Display["height"]/2-20)
    text_box_2 = text_2.get_rect()
    text_box_2.center = (Display["width"]/2, Display["height"]/2)
    text_box_3 = text_2.get_rect()
    text_box_3.center = (Display["width"]/2, Display["height"]/2+20)
    transparent = pg.Surface((Display["width"],Display["height"]))
    transparent.set_alpha(100)
    transparent.fill((100,0,0))
    display.blit(transparent, (0,0))
    display.blit(text_1, text_box_1)
    display.blit(text_2, text_box_2)
    display.blit(text_3, text_box_3)
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return 1
                if event.key == pg.K_SPACE:
                    return main()


def main_loop():
    global key_que
    while True:
        display.fill((180 , 255 , 180))
        pg.draw.rect(display, (100, 255, 100), (50, 50, 550, 550))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    snake.velo_que.append((0,-1))
                if event.key == pg.K_LEFT:
                    snake.velo_que.append((-1,0))
                if event.key == pg.K_DOWN:
                    snake.velo_que.append((0,1))
                if event.key == pg.K_RIGHT:
                    snake.velo_que.append((1,0))
                if event.key == pg.K_SPACE:
                    snake.sprinting = 1
                if event.key == pg.K_ESCAPE:
                    return pause_menu()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    snake.sprinting = 0
        if snake.move():
            return

        food_gen(max_food,snake.speed)

        snake.draw()
        gui.update()
        pg.display.update()
        clock.tick(FPS)

def main():
    global snake, gui, fn, sn, score, max_food, max_special_food, paused
    fn = 0
    sn = 0
    score = 0
    max_food = 2
    max_special_food = 2
    paused = 0
    board_gen()
    snake = Snake()
    gui = Gui()
    main_loop()
    pg.quit()

main()
