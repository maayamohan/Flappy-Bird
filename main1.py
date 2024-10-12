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
PILLAR_GAP_HEIGHT = 160
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


def draw_window(bird, pillars_up, pillars_down, score):
    WIN.blit(BACKGROUND, (0, 0))

    for pillar_up in pillars_up:
        pygame.draw.rect(WIN, GREEN, pillar_up)
        pygame.draw.rect(WIN, GRAY, pillar_up, width=2)
    for pillar_down in pillars_down:
        pygame.draw.rect(WIN, GREEN, pillar_down)
        pygame.draw.rect(WIN, GRAY, pillar_down, width=2)

    score_text = SCORE_FONT.render(str(score), 1, GRAY)
    WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, SCORE_HEIGHT))

    WIN.blit(BIRD, (BIRD_X, bird.y))

    pygame.display.update()


def handle_crash(pillars_up, pillars_down, bird):
    for pillar_up in pillars_up:
        pillar_up.x -= PILLAR_VEL
        if bird.colliderect(pillar_up):
            pygame.event.post(pygame.event.Event(BIRD_HIT))
            HIT_SOUND.play()  # Play hit sound when collision occurs
        if pillar_up.x < 0 - PILLAR_WIDTH:
            pillars_up.remove(pillar_up)
    for pillar_down in pillars_down:
        pillar_down.x -= PILLAR_VEL
        if bird.colliderect(pillar_down):
            pygame.event.post(pygame.event.Event(BIRD_HIT))
            HIT_SOUND.play()  # Play hit sound when collision occurs
        if pillar_down.x < 0 - PILLAR_WIDTH:
            pillars_down.remove(pillar_down)


def game_over_display(score):
    WIN.fill(WHITE)
    game_over_text = GAME_OVER_FONT.render("GAME OVER", 1, GRAY)
    WIN.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, GAME_OVER_HEIGHT))

    score_text = SCORE_FONT.render(f"SCORE: {score}", 1, GRAY)
    WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, SCORE_HEIGHT + 80))

    pygame.display.update()
    pygame.time.delay(3000)


def main():
    bird = pygame.Rect(BIRD_X, 300, BIRD_WIDTH, BIRD_HEIGHT)
    score = 0

    pillars_up = []
    pillars_down = []
    
    clock = pygame.time.Clock()
    run = True
    pillar_timer = 0  # Timer to control when new pillars are created
    is_game_over = False

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == BIRD_HIT:
                is_game_over = True
            if event.type == GAME_OVER and is_game_over:
                game_over_display(score)
                main()  # Restart the game

        if not is_game_over:
            # Bird movement
            if bird.y + BIRD_HEIGHT < HEIGHT:
                bird.y += BIRD_VEL
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[space] and bird.y - BIRD_FLY > 0:
                bird.y -= BIRD_FLY

            # Pillar movement and creation
            pillar_timer += 1
            if pillar_timer > 90:
                pillar_up_height = random.randrange(100, 350)
                pillar_down_height = HEIGHT - pillar_up_height - PILLAR_GAP_HEIGHT
                pillar_up = pygame.Rect(WIDTH, 0, PILLAR_WIDTH, pillar_up_height)
                pillar_down = pygame.Rect(WIDTH, pillar_up_height + PILLAR_GAP_HEIGHT, PILLAR_WIDTH, pillar_down_height)
                pillars_up.append(pillar_up)
                pillars_down.append(pillar_down)
                pillar_timer = 0

            # Handle pillar movement and collision detection
            handle_crash(pillars_up, pillars_down, bird)

            # Increment score only when bird passes the center of the pillar
            for pillar_up in pillars_up:
                if pillar_up.x + PILLAR_WIDTH < bird.x:  # Bird has passed the pillar
                    score += 1
                    POINT_SOUND.play()
                    pillars_up.remove(pillar_up)  # Remove the pillar after passing
                    break  # Exit loop after scoring to prevent multiple increments in a single frame

            draw_window(bird, pillars_up, pillars_down, score)

        if bird.y + BIRD_HEIGHT >= HEIGHT or is_game_over:
            pygame.event.post(pygame.event.Event(GAME_OVER))

    pygame.quit()

if __name__ == "__main__":
    main()

