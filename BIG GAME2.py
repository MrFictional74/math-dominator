import pygame
import sys
import os
import random


# Initialize Pygame
pygame.init()

font = pygame.font.SysFont("SQR721KN.TTF", 36)  # None = default font, 36 = font size

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

player_rect = player_img.get_rect(topleft=(x, y))


lasers = []

targets = []
spawn_timer = 0
level = 1  # starts at level 1
health = 100


debris_list = []
debris_timer = 0


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


class TargetNumber:
    def __init__(self, level):
        self.font = pygame.font.SysFont(None, 36)
        self.x = random.randint(0, WIDTH - 40)
        self.y = -40
        self.speed = random.uniform(1, 2)

        # Determine if this target is a correct multiple (~30% chance)
        if random.random() < 0.3:
            self.value = level * random.randint(1, 10)
            self.is_correct = True
        else:
            if level == 1:
                # Can't avoid multiples of 1, so just fudge it
                self.value = random.randint(1, 100)
                self.is_correct = False
            else:
                # Generate a wrong number that is NOT a multiple
                attempts = 0
                while True:
                    n = random.randint(1, 100)
                    if n % level != 0:
                        self.value = n
                        self.is_correct = False
                        break
                    attempts += 1
                    if attempts > 100:  # emergency escape hatch
                        self.value = random.randint(1, 100)
                        self.is_correct = False
                        break

    def move(self):
        self.y += self.speed

    def draw(self, surface):
        text = self.font.render(str(self.value), True, (255, 255, 255))
        surface.blit(text, (self.x, self.y))

    def off_screen(self):
        return self.y > HEIGHT


class Debris:
    def __init__(self):
        self.image = pygame.image.load("rock.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # adjust as needed
        self.x = random.randint(0, WIDTH - 50)
        self.y = -50
        self.speed = random.uniform(2, 4)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.y > HEIGHT





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

    #level text
    level_text = font.render(f"Level: {level}", True, (43, 139, 247))
    display_text = font.render(f"Shoot only multiples of {level}", True, (43, 139, 247))
    screen.blit(level_text, (10, 10))  # Draw in top-left corner
    screen.blit(display_text, (10, 40))
    # Keep square in bounds
    x = max(0, min(WIDTH - square_size, x))
    y = max(0, min(HEIGHT - square_size, y))

    player_rect.topleft = (x, y)

    spawn_timer += 1
    if spawn_timer > 180:  # Adjust swan timer here
        targets.append(TargetNumber(level))
        spawn_timer = 0

    draw_stars()
    screen.blit(player_img, (x, y))



    for target in targets[:]:
        target.move()
        target.draw(screen)
        if target.off_screen():
            targets.remove(target)

    # Draw image instead of square
    screen.blit(player_img, (x, y))


    debris_timer += 1
    if debris_timer > 220:  # every 1.5 seconds-ish
        debris_list.append(Debris())
        debris_timer = 0

    for debris in debris_list[:]:
        debris.move()
        debris.draw(screen)
        if debris.off_screen():
            debris_list.remove(debris)
        elif player_rect.colliderect(debris.rect):
            print("HIT BY DEBRIS!")  # Replace this with health reduction
            debris_list.remove(debris)



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
