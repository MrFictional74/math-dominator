import pygame
import sys
import os
import random


# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Square")

# Clock for framerate
clock = pygame.time.Clock()

# Load image
# If using an "assets" folder, update the path like: os.path.join("assets", "player.png")
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (50, 50))



# Colors
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)

# Rocket settings
square_size = 50
x, y = WIDTH // 2, HEIGHT // 2
speed = 5
lasers = []



#Laser setup
class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.width = 4
        self.height = 20

    def move(self):
        self.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def off_screen(self):
        return self.y < 0




# Starfield
stars = []
for _ in range(100):
    stars.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "speed": random.uniform(1, 4),
        "radius": random.randint(1, 2)
    })

def draw_stars():
    for star in stars:
        star["y"] += star["speed"]
        if star["y"] > HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)
            star["speed"] = random.uniform(1, 4)
        pygame.draw.circle(screen, (255, 255, 255), (int(star["x"]), int(star["y"])), star["radius"])









# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                laser_x = x + 25 - 2  # center of the rocket (50px wide)
                laser_y = y
                lasers.append(Laser(laser_x, laser_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed









    # Keep square in bounds
    x = max(0, min(WIDTH - square_size, x))
    y = max(0, min(HEIGHT - square_size, y))

    # Draw image instead of square
    screen.blit(player_img, (x, y))

    draw_stars()
    screen.blit(player_img, (x, y))

    for laser in lasers[:]:
        laser.move()
        laser.draw(screen)
        if laser.off_screen():
            lasers.remove(laser)

    # Update display and tick
    pygame.display.flip()
    clock.tick(60)

# Exit
pygame.quit()
sys.exit()
