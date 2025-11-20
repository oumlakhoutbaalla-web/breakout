# ===============================================
# BREAKOUT GAME – Fully Fixed & Super Fast Paddle
# Works on Python 3.13 + pygame 2.6.1
# ===============================================

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# === SETTINGS ===
WIDTH, HEIGHT = 800, 600
FPS = 60                                # ← THIS WAS MISSING!
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game – Fast & Fun!")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)

# Colors
WHITE = (255, 255, 255)
COLORS = [
    (255, 80, 80), (255, 160, 80), (255, 255, 80),
    (80, 255, 80), (80, 180, 255), (180, 80, 255)
]

# Paddle
class Paddle:
    def __init__(self):
        self.width = 130
        self.height = 15
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 50
        self.speed = 14                      # Fast and responsive!

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), border_radius=10)

# Ball
class Ball:
    def __init__(self):
        self.radius = 10
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vel_x = random.choice([-6, 6])
        self.vel_y = -6

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.vel_x *= -1
        if self.y <= self.radius:
            self.vel_y *= -1

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

# Brick
class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 70, 30)
        self.color = color

def create_bricks():
    bricks = []
    for row in range(6):
        for col in range(10):
            x = 65 + col * 74
            y = 100 + row * 40
            color = COLORS[row % len(COLORS)]
            bricks.append(Brick(x, y, color))
    return bricks

# Game objects
paddle = Paddle()
ball = Ball()
bricks = create_bricks()
score = 0
lives = 3
game_over = False
win = False

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                bricks = create_bricks()
                ball.reset()
                score = 0
                lives = 3
                game_over = False
                win = False

    if not game_over:
        paddle.move()
        ball.move()

        # Paddle collision
        if (ball.y + ball.radius >= paddle.y and
            paddle.x - 20 <= ball.x <= paddle.x + paddle.width + 20 and
            ball.vel_y > 0):
            ball.vel_y *= -1
            offset = (ball.x - (paddle.x + paddle.width / 2)) / (paddle.width / 2)
            ball.vel_x += offset * 5

        # Brick collision
        for brick in bricks[:]:
            if brick.rect.collidepoint(ball.x, ball.y):
                bricks.remove(brick)
                ball.vel_y *= -1
                score += 10
                break

        # Ball out
        if ball.y > HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                ball.reset()

        # Victory
        if len(bricks) == 0:
            game_over = True
            win = True

    # Draw
    screen.fill((10, 10, 30))
    paddle.draw()
    ball.draw()
    for brick in bricks:
        pygame.draw.rect(screen, brick.color, brick.rect, border_radius=8)

    info = font.render(f"Score: {score}   Lives: {lives}", True, WHITE)
    screen.blit(info, (20, 15))

    if game_over:
        msg = "YOU WIN! Press R" if win else "GAME OVER – Press R"
        color = (0, 255, 0) if win else (255, 50, 50)
        text = font.render(msg, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)          # ← Now FPS is defined → no more error!