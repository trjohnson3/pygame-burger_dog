import pygame, random

#initialize game
pygame.init()

#Set display surface
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Burger Dog')

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Set game values
PLAYER_STARTING_LIVES = 3
PLAYER_NORMAL_VELOCITY = 5
PLAYER_BOOST_VELOCITY = 10
STARTING_BOOST_LEVEL = 100
STARTING_BURGER_VELOCITY = 3
BURGER_ACCELERATION = .25
BUFFER_DISTANCE = 100

score = 0
burger_points = 0
burgers_eaten = 0

player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_NORMAL_VELOCITY

boost_level = STARTING_BOOST_LEVEL
burger_velocity = STARTING_BURGER_VELOCITY

#Set colors
ORANGE = (246, 170, 54)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Set fonts
font = pygame.font.Font('fonts/washYourHand.ttf', 32)

#Set text
points_text = font.render("Burger Points: " + str(burger_points), True, ORANGE)
points_rect = points_text.get_rect()
points_rect.topleft = (10, 10)

score_text = font.render("Score: " + str(score), True, ORANGE)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 50)

title_text = font.render("Burger Dog" , True, ORANGE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 10

eaten_text = font.render("Burgers Eaten: " + str(burgers_eaten), True, ORANGE)
eaten_rect = eaten_text.get_rect()
eaten_rect.centerx = WINDOW_WIDTH//2
eaten_rect.y = 50

lives_text = font.render("Lives: " + str(player_lives), True, ORANGE)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

boost_text = font.render("Boost: " + str(boost_level), True, ORANGE)
boost_rect = boost_text.get_rect()
boost_rect.topright = (WINDOW_WIDTH - 10, 50)

game_over_text = font.render("Boost: " + str(score), True, ORANGE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to play again...", True, ORANGE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

#Set sounds and music
bark_sound = pygame.mixer.Sound('./sounds/bark.wav')
miss_sound = pygame.mixer.Sound('./sounds/miss.wav')
pygame.mixer.music.load('./sounds/song.wav')

#Set images
player_image_right = pygame.image.load('./images/dog_right.png')
player_image_left = pygame.image.load('./images/dog_left.png')

player_image = player_image_left
player_rect = player_image.get_rect()
player_rect.centerx = WINDOW_WIDTH//2
player_rect.bottom = WINDOW_HEIGHT

burger_image = pygame.image.load('./images/burger.png')
burger_rect = burger_image.get_rect()
burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 32), -BUFFER_DISTANCE)

#Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Move the player, press and hold key
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_velocity
        player_image = player_image_left
    if keys[pygame.K_RIGHT] and player_rect.right < WINDOW_WIDTH:
        player_rect.x += player_velocity
        player_image = player_image_right
    if keys[pygame.K_UP] and player_rect.top > 103:
        player_rect.y -= player_velocity
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += player_velocity

    #Engage boost
    if keys[pygame.K_SPACE]:
        if boost_level > 0:
            player_velocity = PLAYER_BOOST_VELOCITY
            boost_level -= 1
        else:
            player_velocity = PLAYER_NORMAL_VELOCITY
    else:
        boost_level += .1

    #Move burger and update burger points
    burger_rect.y += burger_velocity
    burger_points = int(burger_velocity * (WINDOW_HEIGHT - burger_rect.y + 10) / 10)
    
    #Player missed burger
    if burger_rect.y > WINDOW_HEIGHT:
        player_lives -= 1
        miss_sound.play()
        burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 32), -BUFFER_DISTANCE)
        burger_velocity = STARTING_BURGER_VELOCITY
        player_rect.centerx = WINDOW_WIDTH//2
        player_rect.bottom = WINDOW_HEIGHT
        boost_level = STARTING_BOOST_LEVEL

    #Fill the display
    display.fill(BLACK)

    #Blit the HUD
    display.blit(points_text, points_rect)
    display.blit(score_text, score_rect)
    display.blit(title_text, title_rect)
    display.blit(eaten_text, eaten_rect)
    display.blit(lives_text, lives_rect)
    display.blit(boost_text, boost_rect)
    pygame.draw.line(display, WHITE, (0,100), (WINDOW_WIDTH, 100), 3)

    #Blit assets
    display.blit(player_image, player_rect)
    display.blit(burger_image, burger_rect)

    #Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

#Quit game
pygame.quit()
