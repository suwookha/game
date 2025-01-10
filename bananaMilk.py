import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 182, 193)
BROWN = (165, 42, 42)

# Fonts
FONT = pygame.font.Font(None, 36)
TITLE_FONT = pygame.font.Font(None, 72)

# Game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("유겸이의 우유 게임")

# Clock
clock = pygame.time.Clock()

# Game variables
straw_positions = []
player_score = 0
cucumber_count = 0
running = True

game_started = False

# Player attributes
player_x, player_y = WIDTH // 2, HEIGHT - 100
player_speed = 10

# Milk types and colors
MILK_TYPES = {
    "바나나": YELLOW,
    "딸기": PINK,
    "미수가루": BROWN,
    "오이": GREEN,
    "땅콩": RED,
    "시금치": GREEN,
}

class Milk:
    def __init__(self):
        self.type = random.choice(list(MILK_TYPES.keys()))
        self.color = MILK_TYPES[self.type]
        self.x = random.randint(0, WIDTH - 50)
        self.y = 0
        self.speed = random.randint(3, 7)

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 50, 50))
        pygame.draw.arc(screen, BLACK, (self.x, self.y, 50, 50), 0, 3.14, 2)
        pygame.draw.line(screen, BLACK, (self.x, self.y + 25), (self.x + 50, self.y + 25), 2)
        text = FONT.render(self.type[:1], True, BLACK)
        screen.blit(text, (self.x + 15, self.y + 10))

class Straw:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10

    def move(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x, self.y - 20), 3)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = WHITE

    def move(self, dx):
        self.x += dx
        self.x = max(0, min(WIDTH - 50, self.x))

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x + 25, self.y), 25)
        pygame.draw.line(screen, BLACK, (self.x + 25, self.y + 25), (self.x + 25, self.y + 75), 5)  # Body
        pygame.draw.line(screen, BLACK, (self.x + 25, self.y + 50), (self.x, self.y + 100), 5)  # Left leg
        pygame.draw.line(screen, BLACK, (self.x + 25, self.y + 50), (self.x + 50, self.y + 100), 5)  # Right leg
        pygame.draw.line(screen, BLACK, (self.x + 25, self.y + 40), (self.x, self.y + 50), 5)  # Left arm
        pygame.draw.line(screen, BLACK, (self.x + 25, self.y + 40), (self.x + 50, self.y + 50), 5)  # Right arm

# Game objects
player = Player(player_x, player_y)
milks = []
straws = []

# Start page
def show_start_screen():
    screen.fill(WHITE)
    title_text = TITLE_FONT.render("유겸이의 우유 게임", True, BLACK)
    instruction_text = FONT.render("Press SPACE to start", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

while running:
    if not game_started:
        show_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_started = True
        continue

    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                straws.append(Straw(player.x + 25, player.y))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-player_speed)
    if keys[pygame.K_RIGHT]:
        player.move(player_speed)

    # Spawn milks randomly
    if random.randint(1, 50) == 1:
        milks.append(Milk())

    # Move and draw milks
    for milk in milks[:]:
        milk.move()
        milk.draw()

        # Check if milk hits the bottom
        if milk.y > HEIGHT:
            milks.remove(milk)

    # Move and draw straws
    for straw in straws[:]:
        straw.move()
        straw.draw()

        # Check for collisions with milks
        for milk in milks[:]:
            if milk.x < straw.x < milk.x + 50 and milk.y < straw.y < milk.y + 50:
                if milk.type == "바나나":
                    player.color = YELLOW
                    player_score += 10
                elif milk.type == "미수가루":
                    player_score += 5
                elif milk.type == "시금치":
                    player_score += 5
                elif milk.type == "오이":
                    cucumber_count += 1
                    if cucumber_count == 3:
                        running = False
                milks.remove(milk)
                straws.remove(straw)
                break

        if straw.y < 0:
            straws.remove(straw)

    # Draw player
    player.draw()

    # Display score
    score_text = FONT.render(f"Score: {player_score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Check game over condition
    if cucumber_count >= 3:
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
