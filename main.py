
import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("first project")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FONT = pygame.font.SysFont("comicsans", 40)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 4

BOARD = pygame.Rect(WIDTH/2 - 5 , 0, 10, HEIGHT)

YELLOW_SPACESHIP_IMG = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP1 = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMG, (55, 40)),90)
RED_SPACESHIP_IMG = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP1 = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG,(55,40)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2



def draw_window(red, yellow, red_bullets, yellow_bullets, RED_HEALTH, YELLOW_HEALTH):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BOARD)

    red_health_text = FONT.render("VIDA:" + str(RED_HEALTH), 1, WHITE)
    yellow_health_text = FONT.render("VIDA:" + str(YELLOW_HEALTH), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP1, (yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP1, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_mov(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_w] and yellow.y + VEL > 0: # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < 500: # down
        yellow.y += VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BOARD.x: # right
        yellow.x += VEL

def red_mov(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL> BOARD.x + BOARD.width: # left
        red.x -= VEL
    if keys_pressed[pygame.K_UP] and red.y + VEL > 0: # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL - red. height < 500: # down
        red.y += VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < 900: # right
        red.x += VEL

def handle_bullets(red_bullets, yellow_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x = bullet.x + BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x = bullet.x - BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)

        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2 , HEIGHT/2 - draw_text.get_width()/2 ))

    pygame.display.update()
    pygame.time.delay(8000)

def main():

    RED_HEALTH = 10
    YELLOW_HEALTH = 10
    winner_text = ""

    red = pygame.Rect(700,300, 55, 40)
    yellow = pygame.Rect(100,300, 55, 40)
    clock = pygame.time.Clock()
    run = True

    red_bullets = []
    yellow_bullets = []

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2-2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2-2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                RED_HEALTH -= 1

            if event.type == YELLOW_HIT:
                YELLOW_HEALTH -= 1
        
            
            if RED_HEALTH == 0:
                winner_text = "Yellow won"

            if YELLOW_HEALTH == 0:
                winner_text = "Red won"

            if winner_text != "":
                draw_winner(winner_text)
                break


        
        keys_pressed = pygame.key.get_pressed()
        yellow_mov(keys_pressed, yellow)
        red_mov(keys_pressed, red)
        handle_bullets(red_bullets, yellow_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, RED_HEALTH, YELLOW_HEALTH)

    pygame.quit()

main()

