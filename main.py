import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rain ")

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 80
PLAYER_VEL = 5

RAIN_WIDTH = 10
RAIN_HEIGHT = 20
RAIN_VEL = 3

FONT = pygame.font.SysFont("arial", 25)


def draw(player, elapsed_time, rains):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (55, 10))

    pygame.draw.rect(WIN, "black", player)

    for rain in rains:
        pygame.draw.rect(WIN, "lightblue", rain)

    pygame.display.update()


def main():
    run = True

    player = pygame.Rect(480, HEIGHT - 213,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    rain_add_increment = 3000
    rain_count = 0

    rains = []
    hit = False

    while run:
        rain_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if rain_count > rain_add_increment:
            for _ in range(3):
                rains_x = random.randint(0, WIDTH - RAIN_WIDTH)
                rain = pygame.Rect(rains_x, -RAIN_HEIGHT, RAIN_WIDTH, RAIN_HEIGHT)
                rains.append(rain)

            rain_add_increment = max(200, rain_add_increment - 50)
            rain_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_d] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for rain in rains[:]:
            rain.y += RAIN_VEL
            if rain.y > HEIGHT - 150:
                rains.remove(rain)
            elif rain.y + rain.height >= player.y and rain.colliderect(player):
                rains.remove(rain)
                hit = True
                break

        if hit:
            lost_text = FONT.render("GAME OVER!", 1, "white")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_width() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, rains)

    pygame.quit()


if __name__ == "__main__":
    main()
