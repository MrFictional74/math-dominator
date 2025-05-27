import pygame
import sys
import os
import random


# Initialize Pygame
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("bg_music.wav")
pygame.mixer.music.set_volume(0.5)  # optional volume control (0.0 to 1.0)
pygame.mixer.music.play(-1)  # -1 means loop forever


font = pygame.font.SysFont("SQR721KN.TTF", 36)  # None = default font, 36 = font size

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplication Dominator by MrFictional")


backgrounds = {}
for i in range(2, 11):
    img = pygame.image.load(f"bg{i}.bmp").convert()
    img = pygame.transform.scale(img, (WIDTH, 800))  # scale to match screen width
    backgrounds[i] = img




# Clock for framerate
clock = pygame.time.Clock()

#Stating initial variables
level = 2  # starts at level 1
health = 100
p_score = 0

bg_y = 0
bg_scroll_speed = 0.3  # nice and subtle






# Load images/assets
# If using an "assets" folder, update the path like: os.path.join("assets", "player.png")
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (50, 50))
boom_img = pygame.image.load("boom.png").convert_alpha()
boom_img = pygame.transform.scale(boom_img, (50, 50))
startup_img = pygame.image.load("title_screen.bmp").convert()
startup_img = pygame.transform.scale(startup_img, (WIDTH, HEIGHT))
game_over_img = pygame.image.load("game_over.png").convert()
game_over_img = pygame.transform.scale(game_over_img, (WIDTH, HEIGHT))



#sounds
laser_sound = pygame.mixer.Sound("laser.mp3")
laser_sound.set_volume(0.6)  # 0.0 to 1.0
hit_correct_sound = pygame.mixer.Sound("hit_correct.wav")
hit_wrong_sound = pygame.mixer.Sound("hit_wrong.mp3")
destroy_sound = pygame.mixer.Sound("destroy.wav")
level_sound = pygame.mixer.Sound("level.wav")




#volumes
laser_sound.set_volume(0.6)  # 0.0 to 1.0
hit_correct_sound.set_volume(0.5)
hit_wrong_sound.set_volume(0.5)
destroy_sound.set_volume(0.5)
level_sound.set_volume(0.5)

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
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y -= self.speed
        self.y -= self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def off_screen(self):
        return self.y < 0


class TargetNumber:
    def __init__(self, level):
        self.font = pygame.font.SysFont(None, 48)
        self.x = random.randint(0, WIDTH - 40)
        self.y = -40
        self.speed = random.uniform(1, 2)

        # 60% chance it's a correct multiple
        max_value = level * 10
        if random.random() < 0.6:
            possible_multiples = [i for i in range(level, max_value + 1, level)]
            self.value = random.choice(possible_multiples)
            self.is_correct = True
        else:
            attempts = 0
            while True:
                n = random.randint(1, max_value)
                if n % level != 0:
                    self.value = n
                    self.is_correct = False
                    break
                attempts += 1
                if attempts > 100:  # safety hatch
                    self.value = n
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
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.x = random.randint(0, WIDTH - 50)
        self.y = -50
        self.speed = random.uniform(2, 5)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.hit = False
        self.boom_timer = 0

    def move(self):
        if not self.hit:
            self.y += self.speed
            self.rect.topleft = (self.x, self.y)
        else:
            self.boom_timer += 1  # count how long boom is shown

    def draw(self, surface):
        if self.hit:
            surface.blit(boom_img, (self.x, self.y))
        else:
            surface.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.y > HEIGHT

    def is_done(self):
        return self.hit and self.boom_timer > 10  # Adjust frames of explosion






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




#STARTUP SCREEN
def show_startup_screen():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

        screen.blit(startup_img, (0, 0))
        pygame.display.flip()




#Game Over Screen
def show_game_over_screen(final_score):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    return "restart"
                elif event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))  # black background

        # Always draw the image or fallback background first
        if 'game_over_img' in globals():
            screen.blit(game_over_img, (0, 0))
        else:
            screen.fill((0, 0, 0))  # fallback if no image

        # Now draw text on top
        font = pygame.font.SysFont(None, 64)


        small_font = pygame.font.SysFont(None, 36)
        restart_msg = small_font.render(f" {final_score}", True, (200, 200, 200))
        screen.blit(restart_msg, (WIDTH // 2 - restart_msg.get_width() // 2, HEIGHT // 2 + 20))




        pygame.display.flip()



show_startup_screen()












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
                laser_sound.play()



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


    if health <= 0:
        print("GAME OVER")
        running = False






    # Keep square in bounds
    x = max(0, min(WIDTH - square_size, x))
    y = max(0, min(HEIGHT - square_size, y))

    player_rect.topleft = (x, y)

    spawn_timer += 1
    if spawn_timer > 260:  # Adjust swan timer here
        targets.append(TargetNumber(level))
        spawn_timer = 0

    # Get current background image for level (fallback to black if missing)
    bg_img = backgrounds.get(level)
    if bg_img:
        screen.blit(bg_img, (0, bg_y))
        screen.blit(bg_img, (0, bg_y - 800))  # the one *above* the first
    else:
        screen.fill((0, 0, 0))

    draw_stars()
    screen.blit(player_img, (x, y))

    # ALL GAME TEXT HERE
    level_text = font.render(f"Level: {level}", True, (43, 139, 247))
    display_text = font.render(f"SCORE: {p_score}", True, (43, 139, 247))
    screen.blit(level_text, (10, 10))  # Draw in top-left corner
    screen.blit(display_text, (10, 40))

    health_text = font.render(f"Health: {health}", True, (255, 100, 100))
    screen.blit(health_text, (10, 70))




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

        elif debris.hit and debris.is_done():
            debris_list.remove(debris)

        elif player_rect.colliderect(debris.rect) and not debris.hit:
            debris.hit = True
            health -= 50
            destroy_sound.play()

    for laser in lasers[:]:
        laser.move()
        laser.draw(screen)
        if laser.off_screen():
            lasers.remove(laser)

    for laser in lasers[:]:
        for target in targets[:]:
            # Make a rect for the target
            target_rect = pygame.Rect(target.x, target.y, 70, 70)  # Adjust if needed

            if laser.rect.colliderect(target_rect):
                if target.is_correct:
                    p_score += 50
                    hit_correct_sound.play()
                else:
                    health -= 5
                    hit_wrong_sound.play()

                lasers.remove(laser)
                targets.remove(target)
                break  # break inner loop so we don't reuse the same laser

    # Check for level up
    if p_score >= level * 100:
        level += 1
        level_sound.play()

    bg_y += bg_scroll_speed
    if bg_y >= 800:
        bg_y = 0

    # Update display and tick
    pygame.display.flip()
    clock.tick(60)

    if health <= 0:
        result = show_game_over_screen(p_score)
        if result == "restart":
            level = 2
            p_score = 0
            health = 100
            lasers.clear()
            targets.clear()
            debris_list.clear()
            bg_y = 0
            continue

# Exit
pygame.quit()
sys.exit()
