import pygame
import random
import os
import time

pygame.init()
pygame.mixer.init()

# images
snake_img = pygame.image.load("snake.png")
apple_img = pygame.image.load("apple.png")
icon = pygame.image.load("front.jpg")


# colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (255, 201, 14)   # please do not change this color this is snakes color
blue = (0, 0, 140)
unc = (255, 0, 255)

# Font sizes
smallFont = 40
mediumFont = 50
largeFont = 150

# Game specific variables
screen_width = 1000
screen_height = 600

# Creating window
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snakes")
pygame.display.set_icon(icon)
pygame.display.update()
clock = pygame.time.Clock()


def text_to_button(text, color, bx, by, bw, bh, size=smallFont): # This is used To print text at center of button
    font = pygame.font.SysFont('Times New Roman', size)
    txt_surface = font.render(text, True, color)
    txt_rect = txt_surface.get_rect()
    txt_rect.center = int(bx + bw/2), int(by + bh/2)
    gameWindow.blit(txt_surface, txt_rect)


def centeredText(size, text, color, excess):  # This method is used for printing centered text
    font = pygame.font.SysFont("Times New Roman", size)
    txt_surface = font.render(text, True, color)
    txt_rect = txt_surface.get_rect()
    txt_rect.center = (screen_width / 2), (screen_height / 2 + excess)
    gameWindow.blit(txt_surface, txt_rect)


def text_screen(text, color, x, y, size=smallFont): # This method is used to print text at any position
    font = pygame.font.SysFont('Times New Roman', size)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def button(text, color, bx, by, bw, bh, action="None"): # This is used for drawing button show movement on button
    cord = pygame.mouse.get_pos()                       # and for proving actions to button
    click = pygame.mouse.get_pressed()
    if bx + bw > cord[0] > bx and by + bh > cord[1] > by:
        pygame.draw.rect(gameWindow, black, [bx, by, bw, bh], 5)
        if click[0] == 1 and action != "None":
            pygame.mixer.music.load("direction.mp3")
            pygame.mixer.music.play()
            time.sleep(0.5)
            if action == "play":
                gameLoop()
            elif action == "exit":
                pygame.quit()
                quit()
            elif action == "controls":
                controls()
            elif action == "back":
                welcome()
    else:
        pygame.draw.rect(gameWindow, color, [bx, by, bw, bh])
    text_to_button(text, black, bx, by, bw, bh)


def plot_snake(game_window, color, snk_list1, snake_size1):  # By this method we plot snake and change direction of
    head = 0                                                 # head of snake
    if direction == "right":
        head = pygame.transform.rotate(snake_img, 270)
    elif direction == "left":
        head = pygame.transform.rotate(snake_img, 90)
    elif direction == "up":
        head = pygame.transform.rotate(snake_img, 0)
    elif direction == "down":
        head = pygame.transform.rotate(snake_img, 180)

    gameWindow.blit(head, (snk_list1[-1][0], snk_list1[-1][1]))
    for x, y in snk_list1[:-1]:
        pygame.draw.rect(game_window, color, [x, y, snake_size1, snake_size1])


def pause(): # This method is used for creating pause window
    paused = True
    centeredText(largeFont, "Paused", red, -100)
    centeredText(smallFont, "Press enter to restart or Q to quit", black, 100)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def controls():  # This method is used for creating control window
    gControls = False

    while not gControls:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gControls = True

        gameWindow.fill(white)

        centeredText(largeFont, "Controls", green, -200)
        centeredText(smallFont, "Arrow keys to move", black, -100)
        centeredText(smallFont, "P : pause", black, -50)

        button("Back", unc, 425, 350, 150, 50, "back")

        pygame.display.update()
        clock.tick(10)
    pygame.quit()
    quit()


def welcome(): # This method is used for creating welcome window
    exit_game = False

    while not exit_game:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                exit_game = True

        gameWindow.fill(white)

        centeredText(largeFont, "SNAKES", green, -200)
        centeredText(smallFont, "Welcome, In this game You have to eat red apples", black, -100)
        centeredText(smallFont, "More apples you eat more you live", black, -50)
        centeredText(smallFont, "If you run into yourself or the edges you die", black, 0)

        button("Play", red, 425, 350, 150, 50, "play")
        button("Controls", blue, 425, 420, 150, 50, "controls")
        button("Exit", green, 425, 490, 150, 50, "exit")

        pygame.display.update()
        clock.tick(10)
    pygame.quit()
    quit()


def gameLoop(): # This is most important part of game here we are
    exit_game = False # doing work which is needed to do repeatedly
    game_over = False
    snake_x = 100
    snake_y = 100
    snake_size = 20
    food_size = 30
    fps = 20
    init_velocity = 20
    velocity_x = 20
    velocity_y = 0
    food_x = random.randint(50, screen_width - 50)   # This are initialize here to make
    food_y = random.randint(50, screen_height - 50)  # First random food
    snk_list = []
    snk_size = 1
    score = 0
    global direction
    direction = "right"

    if not os.path.exists("highscore.txt"): # This is helpful if highscore file is not present
        with open("highscore.txt", "w") as f:  # This creates highscore.txt file and assigns highscore as 0
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()

    # Loop in game which will do main work
    while not exit_game:
        if game_over:
            pygame.mixer.music.load("falling.mp3")
            pygame.mixer.music.play()
            centeredText(largeFont, "GAME OVER", red, -100)
            centeredText(mediumFont, "Press Enter to continue or q to Quit", black, 100)
            pygame.display.update()
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))                 # Here we write highscore in file
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if pygame.KEYDOWN == event.type:
                        if event.key == pygame.K_RETURN:
                            gameLoop()
                        if event.key == pygame.K_q:
                            pygame.quit()
                            quit()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                        direction = "right"
                    elif event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                        direction = "left"
                    elif event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = -init_velocity
                        direction = "up"
                    elif event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = init_velocity
                        direction = "down"
                    if event.key == pygame.K_p:
                        pause()
                    if event.key == pygame.K_a:  # This is cheat code press 'a' to increase your score
                        score += 10

            # This gives velocity to snake
            snake_x += velocity_x
            snake_y += velocity_y

            # This checks if food is touches by snake if yes then increases score then
            # sets food to random value and then increases snake size
            if food_x < snake_x < food_x + food_size or food_x < snake_x + snake_size < food_x + food_size:
                if food_y < snake_y < food_y + food_size or food_y < snake_y + snake_size < food_y + food_size:
                    pygame.mixer.music.load("appleEating.mp3")
                    pygame.mixer.music.play()
                    score = score + 10
                    food_x = random.randint(50, screen_width - 50)
                    food_y = random.randint(50, screen_height - 50)
                    snk_size += 3                                        # This increases snake size by given value
                    if score > int(highscore):
                        highscore = score

            # Here we are doing graphics part
            gameWindow.fill(white)                                       # fills screen with white
            text_screen("HIGHSCORE : " + str(highscore), black, 300, 10)
            text_screen("SCORE : " + str(score), black, 10, 10)          # shows text on screen
            gameWindow.blit(apple_img, (food_x, food_y))                 # draws food

            # Below are used to show size of snake
            head = [snake_x, snake_y]
            snk_list.append(head)
            if len(snk_list) > snk_size:                                 # This controls snakes size
                del snk_list[0]
            plot_snake(gameWindow, green, snk_list, snake_size)

            # This will check about snake falls on wall of screen or not
            if snake_x >= screen_width or snake_y >= screen_height or snake_x == 0 or snake_y == 0:
                game_over = True

            # This will check about snakes head touches his body
            if head in snk_list[:-1]:
                game_over = True

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()