import pygame
import sys 
import random
from Button import Button

pygame.init()

SW, SH = 700, 700  #screen width and height
BG = pygame.image.load("Background.png")

counter = 1                                        #variable defining (counter for plum, auxilary value for score)
aux_score = 0
BLOCK_SIZE = 50   
FONT = pygame.font.Font("font.ttf", BLOCK_SIZE*2)   #font used for score
flag = False                 
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Snake!")    #game name
clock = pygame.time.Clock()     #game clock
difficulty_handler = 9          # variable for difficulty (snake speed)

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE     #snake head size
        self.xdir = 1                               # default direction (going to the right)
        self.ydir = 0                               # default direction
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
    
    def update(self):
        global apple       # when game restarts apple changes position
        global aux_score
        global counter
        global flag
        for square in self.body:                                            #dying conditions(touching yourself & touching barrier)
            if self.head.x == square.x and self.head.y == square.y:             
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True
        
        if self.dead:                                                       #conditions after game restarts(snake len = 2 & default direction)
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = 1
            self.ydir = 0
            counter = 1
            flag = False
            apple = Fruit()
        
        self.body.append(self.head)                                 # conditions for snake to move continuously
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

class Fruit:                                                                   
    def __init__(self):                                                  #apple conditions (random spawn point & dimensions)
        self.x = int(random.randint(0, SW)/BLOCK_SIZE) * BLOCK_SIZE 
        self.y = int(random.randint(0, SH)/BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    
    def update_apple(self):                                          #apple
        pygame.draw.rect(screen, "orange", self.rect)
    def update_plum(self):                                           #plum
        pygame.draw.rect(screen, "blue", self.rect)

def drawGrid():                                              #grey grid conditions
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)

def get_font(size):                                          # font used for main menu
    return pygame.font.Font("font.ttf", size)
def get_font2(size):                                         #font used for game over screen
    return pygame.font.Font("ARCADECLASSIC.TTF", size)

snake = Snake()
apple = Fruit()
drawGrid()
score = FONT.render("1", True, "white")                            # score font and color
score_rect = score.get_rect(center=(SW/2, SH/18))                  # score placement and dimensions

# Program has three main loops. play() -> game ;  difficulty() -> change difficulty ; main_menu() -> Core of the app. Used to go to game and difficulty menu or exit.

def play():                                                       
    global flag                              # use variables in the function
    global aux_score
    global apple
    global counter
    global flag
    global difficulty_handler
    while True:                              # play() main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:               # top right corner x quits the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:                                   # keys to change snake direction (awds or keys)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake.ydir = 1
                    snake.xdir = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake.ydir = -1
                    snake.xdir = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake.ydir = 0
                    snake.xdir = 1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake.ydir = 0
                    snake.xdir = -1
                elif event.key == pygame.K_SPACE:                             #key to pause game
                    paused()
                    
        snake.update()
        
        screen.fill('black')
        drawGrid()

        if flag == False: apple.update_apple()                       # conditions apple XOR plum
        else: apple.update_plum()

        score = FONT.render(str(aux_score), True, "white")                   #score increment

        pygame.draw.rect(screen, "green", snake.head)                      # draw snake in the game

        for square in snake.body:                                          # draw snake in the game
            pygame.draw.rect(screen, "green", square)

        screen.blit(score, score_rect)                                     # draw the score in the game

        if flag == True and snake.head.x == apple.x and snake.head.y == apple.y:      # consequences of eating a plum
            aux_score += 9
            flag = False
            counter = 0

        if snake.head.x == apple.x and snake.head.y == apple.y:                       # consequences of eating an apple
            aux_score += 1
            snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            apple = Fruit()
            counter += 1
            if counter == 5:
                flag = True
        
        if snake.dead == True:                                              # condition for game over to pop up
            game_over()
            
        pygame.display.update()
        clock.tick(difficulty_handler)                     #game tick rate (Changes based on difficulty. The higher, the quicker the snake moves)
    
def difficulty():                                          
    global difficulty_handler                         
    while True:                                               # difficulty() main loop
        DIFFICULTY_MOUSE_POS = pygame.mouse.get_pos()
       
        screen.blit(BG, (-300, 0))

        DIFFICULTY_TEXT = get_font(55).render("Choose the DIFFICULTY.", True, "White")                 #frontend aspcets related to difficulty menu
        DIFFICULTY_RECT = DIFFICULTY_TEXT.get_rect(center=(350, 70))
        screen.blit(DIFFICULTY_TEXT, DIFFICULTY_RECT)

        EASY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(350,200),                   # "EASY" button specifications (eg. position, default and hovering color, font)
        text_input="EASY", font=get_font(50), base_color="#d7fcd4", hovering_color="Green")
        NORMAL_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(350,350),                   # "MEDIUM" button specifications (eg. position, default and hovering color, font)
        text_input="NORMAL", font=get_font(50), base_color="#d7fcd4", hovering_color="Green")
        HARD_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(350,500),                   # "HARD" button specifications (eg. position, default and hovering color, font)
        text_input="HARD", font=get_font(50), base_color="#d7fcd4", hovering_color="Green")

        for button in [EASY_BUTTON,NORMAL_BUTTON,HARD_BUTTON]:                           
            button.changeColor(DIFFICULTY_MOUSE_POS)
            button.update(screen)

        DIFFICULTY_BACK = Button(image=None, pos=(350, 630), 
        text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        DIFFICULTY_BACK.changeColor(DIFFICULTY_MOUSE_POS)
        DIFFICULTY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if DIFFICULTY_BACK.checkForInput(DIFFICULTY_MOUSE_POS):
                    main_menu()
                if EASY_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):
                    difficulty_handler = 5
                    main_menu()
                if NORMAL_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):
                    difficulty_handler = 9
                    main_menu()
                if HARD_BUTTON.checkForInput(DIFFICULTY_MOUSE_POS):
                    difficulty_handler = 17
                    main_menu()
        pygame.display.update()

def main_menu():
    while True:                                # main_menu() main loop
        screen.blit(BG, (-300, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")                                  # "main menu" specifications
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 100))

        CONTROLS_TEXT = get_font(30).render("Move: WASD or Arrow keys    Pause: SpaceBar", True, "white")                                  # "main menu" specifications
        CONTROLS_RECT = MENU_TEXT.get_rect(center=(300, 680))
                                                                                                        
        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(350,250),                   # play button specifications (eg. position, default and hovering color, font)
            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")
        DIFFICULTY_BUTTON = Button(image=pygame.image.load("Options Rect.png"), pos=(350, 400),            # options button specifications
            text_input="DIFFICULTY", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")
        QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(350, 550),                  # quit button specifications
            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(CONTROLS_TEXT,CONTROLS_RECT)

        for button in [PLAY_BUTTON, DIFFICULTY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():                            # when we click a button redirects to appropriate function/loop
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if DIFFICULTY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    difficulty()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def paused():
    
    paused = True
    
    while paused:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (-300, 0))
        BUTTON_PAUSED = get_font(100).render("PAUSED", True, "#b68f40")
        BUTTON_RECT = BUTTON_PAUSED.get_rect(center=(350, 100))
        screen.blit(BUTTON_PAUSED, BUTTON_RECT)

        RESUME_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(350,300),                   # "RESUME" button specifications (eg. position, default and hovering color, font)
        text_input="RESUME", font=get_font(50), base_color="#d7fcd4", hovering_color="Green")
        RETURN_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(350,500),                   # "RETURN" button specifications (eg. position, default and hovering color, font)
        text_input="RETURN TO MAIN MENU", font=get_font(40), base_color="#d7fcd4", hovering_color="Green")

        for button in [RESUME_BUTTON,RETURN_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():                           
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                        paused = False
                    if RETURN_BUTTON.checkForInput(MENU_MOUSE_POS):
                        snake.dead = True                                     #restarts game when we return to main menu
                        main_menu()
        pygame.display.update()

def game_over():
    global aux_score
    while True:
        FONT2 = pygame.font.Font("ARCADECLASSIC.TTF", 130)                                   # game over menu font
        game_over_text = FONT2.render("GAME OVER", True, "green")                            # game over text and color
        GAME_OVER_MOUSE_POS = pygame.mouse.get_pos()
        score = FONT.render(str(aux_score), True, "white")

        screen.fill('black')
        screen.blit(score, (310,250))
        screen.blit(game_over_text,(55,100))
        RESTART_BUTTON = Button(image= None, pos=(350,450),                   
        text_input="RESTART", font=get_font2(75), base_color="#d7fcd4", hovering_color="Green")
        MAIN_MENU_BUTTON = Button(image= None, pos=(350, 550),                     
        text_input="MAIN MENU", font=get_font2(75), base_color="#d7fcd4", hovering_color="Green")

        for button in [RESTART_BUTTON,MAIN_MENU_BUTTON]:
            button.changeColor(GAME_OVER_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():                           
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                snake.dead = False
                if RESTART_BUTTON.checkForInput(GAME_OVER_MOUSE_POS):
                    aux_score = 0
                    play()
                if MAIN_MENU_BUTTON.checkForInput(GAME_OVER_MOUSE_POS):
                    aux_score = 0
                    main_menu()

        pygame.display.update()

main_menu()                     # calls the main_menu