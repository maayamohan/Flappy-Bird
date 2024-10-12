import os
import random
import pygame


WIDTH, HEIGHT = 500, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
WHITE = (240, 240, 240)
GRAY = (50, 50, 50)
GREEN = (149, 223, 81)
BLACK = (10, 10, 10)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('background.png')), (WIDTH, HEIGHT))

FPS = 60

space = pygame.K_SPACE

BIRD_IMAGE = pygame.image.load(os.path.join('flappybird.png'))
BIRD_WIDTH, BIRD_HEIGHT = 58, 40
BIRD = pygame.transform.scale(BIRD_IMAGE, (BIRD_WIDTH, BIRD_HEIGHT))
BIRD_X = 192
BIRD_FLY = 15
BIRD_VEL = 4

PILLAR_WIDTH = 80
PILLAR_UP_HEIGHT = 0
PILLAR_GAP_HEIGHT = 160
PILLAR_DOWN_HEIGHT = 0
PILLAR_VEL = 3

BIRD_HIT = pygame.USEREVENT + 1
UP_SCORE = pygame.USEREVENT + 2
GAME_OVER = pygame.USEREVENT + 3

SCORE_HEIGHT = 20
GAME_OVER_HEIGHT = 40

pygame.mixer.init()
HIT_SOUND = pygame.mixer.Sound(os.path.join("hit.mp3"))
POINT_SOUND = pygame.mixer.Sound(os.path.join("point.mp3"))


pygame.font.init()
SCORE_FONT = pygame.font.Font("font.ttf", 40)
GAME_OVER_FONT = pygame.font.Font("font.ttf", 50)
game_over_text = GAME_OVER_FONT.render("GAME OVER", 1, GRAY)



def draw_window(bird, pillars_up, pillars_gap, pillars_down, score):
    for pillar_gap in pillars_gap:
        pygame.draw.rect(WIN, WHITE, pillar_gap)

    WIN.blit(BACKGROUND, (0, 0))

    for pillar_up in pillars_up:
        pygame.draw.rect(WIN, GREEN, pillar_up)
        pygame.draw.rect(WIN, GRAY, pillar_up, width = 2)
    for pillar_down in pillars_down:
        pygame.draw.rect(WIN, GREEN, pillar_down)
        pygame.draw.rect(WIN, GRAY, pillar_down, width = 2)


    score_text = SCORE_FONT.render(str(score), 1, GRAY)
    WIN.blit(score_text,(WIDTH//2 - score_text.get_width()//2, SCORE_HEIGHT))

    WIN.blit(BIRD, (BIRD_X, bird.y))

    pygame.display.update()


def handle_crash(pillars_up, pillars_gap, pillars_down, bird):
    for pillar_up in pillars_up:
        pillar_up.x -= PILLAR_VEL
        if bird.colliderect(pillar_up):
            pygame.event.post(pygame.event.Event(BIRD_HIT))
        if pillar_up.x < 0 - PILLAR_WIDTH:
            pillars_up.remove(pillar_up)
    for pillar_gap in pillars_gap:
        pillar_gap.x -= PILLAR_VEL
        if bird.colliderect(pillar_gap):
            pygame.event.post(pygame.event.Event(UP_SCORE))
        if pillar_gap.x < 0 - PILLAR_WIDTH:
            pillars_gap.remove(pillar_gap)
    for pillar_down in pillars_down:
        pillar_down.x -= PILLAR_VEL
        if bird.colliderect(pillar_down):
            pygame.event.post(pygame.event.Event(BIRD_HIT))
        if pillar_down.x < 0 - PILLAR_WIDTH:
            pillars_down.remove(pillar_down)


def game_over(game_over_text):
    GAME_OVER_FONT.render(game_over_text, 1, GRAY)
    WIN.blit(GAME_OVER_FONT, (WIDTH//2 - game_over_text.get_width()//2, GAME_OVER_HEIGHT))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    bird = pygame.Rect(200, 185, BIRD_WIDTH, BIRD_HEIGHT)

    global PILLAR_UP_HEIGHT
    global PILLAR_DOWN_HEIGH
    global PILLAR_VEL
    global BIRD_VEL
    global SCORE_HEIGHT

    score = 0

    pillars_up = []
    pillars_gap = []
    pillars_down = []

    refresh = 0

    clock = pygame.time.Clock()
    run = True
    while run:

        # noinspection PyShadowingNames
        PILLAR_UP_HEIGHT = random.randrange(100, 390)
        PILLAR_DOWN_HEIGHT = HEIGHT - 79 - PILLAR_GAP_HEIGHT - PILLAR_UP_HEIGHT

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        refresh += 1
        if refresh % 120 == 0 and event.type != BIRD_HIT and bird.y != HEIGHT - BIRD_HEIGHT:
            pillar_up = pygame.Rect(WIDTH, 0, PILLAR_WIDTH, PILLAR_UP_HEIGHT)
            pillar_gap = pygame.Rect(WIDTH, PILLAR_UP_HEIGHT, PILLAR_WIDTH, PILLAR_GAP_HEIGHT)
            pillar_down = pygame.Rect(WIDTH, PILLAR_UP_HEIGHT + PILLAR_GAP_HEIGHT, PILLAR_WIDTH, PILLAR_DOWN_HEIGHT)
            pillars_up.append(pillar_up)
            pillars_gap.append(pillar_gap)
            pillars_down.append(pillar_down)
            if event.type == UP_SCORE and bird.y != HEIGHT - BIRD_HEIGHT:
                score += 1
                print(score)
                POINT_SOUND.play()
       
        if bird.y + BIRD_HEIGHT < HEIGHT:
            bird.y += BIRD_VEL
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[space] and bird.y - BIRD_FLY > 0 and event.type != BIRD_HIT:
            bird.y -= BIRD_FLY

        if event.type == BIRD_HIT:
            pygame.event.post(pygame.event.Event(GAME_OVER))
            PILLAR_VEL = 0
            BIRD_VEL = 10
            HIT_SOUND.play()
        if bird.y + BIRD_HEIGHT >= HEIGHT:
            pygame.event.post(pygame.event.Event(GAME_OVER))
            PILLAR_VEL = 0

        if event.type == GAME_OVER:
            pygame.display.update()
            WIN.blit(game_over_text,(WIDTH//2 - game_over_text.get_width()//2, 100))
            SCORE_HEIGHT = 200
            score_text = SCORE_FONT.render("SCORE:" + str(score), 1, GRAY)
            WIN.blit(score_text,(WIDTH//2 - score_text.get_width()//2, SCORE_HEIGHT))
            pygame.display.update()
            pygame.time.delay(5000)

        else:
            handle_crash(pillars_up, pillars_gap, pillars_down, bird)
            draw_window(bird, pillars_up, pillars_gap, pillars_down, score)

    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
    pygame.quit()


if __name__ == "__main__":
    main()
