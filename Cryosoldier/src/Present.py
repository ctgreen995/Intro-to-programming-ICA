import pygame
import random
import sys
from pygame import mixer
# Initialize the pygame module.
pygame.init()
# Title of the game window.
pygame.display.set_caption("Cryosoldier")
pygame.font.init()
myfont = pygame.font.SysFont('freesansbold. ttf', 80)
FPS = 60
CLOCK = pygame.time.Clock()
mixer.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
# Variables for button colours.
green = (0, 150, 0)
red = (250, 0, 0)
blue = (0, 0, 200)
# Function to play background music.
mixer.music.load('audio/background.wav')
effect = pygame.mixer.Sound('audio/explosion.wav')
effect.set_volume(0.3)

numbers_list = []
for i in range(0, 300, 20):
    numbers_list.append(i)


def play_music():
    mixer.music.play(-1)


# Take text content and font, returns text and text rectangle.
def text_objects(text, font):
    text_surface = font.render(text, True, blue)
    return text_surface, text_surface.get_rect()


# Function to create buttons, takes positions, could and colour when clicked.
def button(msg, x, y, w, h, colour, active_colour, action=None):
    global intro, game_over, running
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_colour, (x, y, w, h))
        if click[0] == 1 and action is not None:
            if action == "play":
                main()
            elif action == "quit":
                game_over = False
                intro = False
                running = False
                pygame.mixer.music.stop()

    else:
        pygame.draw.rect(screen, colour, (x, y, w, h))
    text_surf, text_rect = text_objects(msg, myfont)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)


# Function to show the intro screen.
def play_intro():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    global intro
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        textsurface = myfont.render('Present Soldier', True, (0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(textsurface, (WIDTH - 710, 100))
        button("START", 100, 200, 200, 100, green, red, "play")
        button("QUIT", 700, 200, 200, 100, green, red, "quit")
        pygame.display.update()


def play_game_over():
    global game_over
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        textsurface = myfont.render('GAME OVER! YOUR SCORE: ' + str(player.score), True, (0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(textsurface, (WIDTH - 900, 100))
        button("PLAY AGAIN?", 10, 200, 400, 100, green, red, "play")
        button("QUIT", 700, 200, 200, 100, green, red, "quit")
        pygame.display.update()


def score_and_level(level):
    textsurface = myfont.render('SCORE: ' + str(player.score), True, (0, 0, 0))
    textsurface_2 = myfont.render("LEVEL: " + str(level), True, (0, 0, 0))
    screen.blit(textsurface, (WIDTH - 950, 25))
    screen.blit(textsurface_2, (WIDTH - 950, 70))


def draw_lives(surf, x, y, lives, img):
    for lives in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + -50 * lives
        img_rect.y = y
        surf.blit(img, img_rect)

# Set the background image.
background = pygame.image.load('images/whitehouse.jpg')
# Load all the images for assets.
player = pygame.image.load('images/tank.png')
player_life_image = pygame.transform.scale(player, (50, 50))
jet = pygame.image.load('images/jet-fighter.png')
jet_reversed = pygame.image.load('images/jet_reversed.png')
missile = pygame.image.load('images/missile.png')
enemy_missile = pygame.image.load('images/enemy_missile.png')


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = jet
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 10
        self.rect.y = random.randrange(150, 400)
        self.speedx = random.randrange(5, 8)
        self.rect.bottom = self.rect.bottom

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right <= 0:
            self.rect.left = 1000
            self.rect.y = random.randrange(150, 400)
            self.speedx = random.randrange(5, 8)

    def shoot(self, speed):
        bullet = Enemybullet(self.rect.x, self.rect.bottom, speed)
        all_sprites.add(bullet)
        enemy_bullet_sprites.add(bullet)


class EnemyReversed(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = jet_reversed
        self.rect = self.image.get_rect()
        self.rect.x = - 30
        self.rect.y = random.randrange(150, 400)
        self.speedx = random.randrange(5, 8)
        self.rect.bottom = self.rect.bottom

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left >= 1000:
            self.rect.right = -30
            self.rect.y = random.randrange(150, 400)
            self.speedx = random.randrange(5, 8)

    def shoot(self, speed):
        bullet = Enemybullet(self.rect.x, self.rect.bottom, speed)
        all_sprites.add(bullet)
        enemy_bullet_sprites.add(bullet)


class Enemybullet(pygame.sprite.Sprite):
    def __init__(self, enemy_x, enemy_bottom, speed):
        pygame.sprite.Sprite. __init__(self)
        self.image = enemy_missile
        self.rect = self.image.get_rect()
        self.rect.top = enemy_bottom - 30
        self.rect.x = enemy_x
        self.speedy = speed

    def update(self):
        self.rect.y += self.speedy


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.health = 10
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.score = 0

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = +5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self. rect.left < 0:
            self.rect.left = 0
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y, 100, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y, 100 - (5 * (10 - self.health)), 10))

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.y)
        all_sprites.add(bullet)
        player_bullet_sprites.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"images/exp{num}.png")
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

# Sprite groups
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
player_bullet_sprites = pygame.sprite.Group()
enemy_bullet_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
player_sprite.add(player)


# Game loop function.
def main():
    global running
    running = True
    for enemy in range(3):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemy_sprites.add(enemy)
    for enemy in range(3):
        enemy = EnemyReversed()
        all_sprites.add(enemy)
        enemy_sprites.add(enemy)
    # Init level at #1.
    level = 0
    player.lives = 3
    player.score = 0
    previous_time = pygame.time.get_ticks()
    while running:
        # If no music is playing, commence play music function.
        if pygame.mixer.music.get_busy() == False:
            play_music()
        # Set the fps at 60.
        CLOCK.tick(FPS)
        # Draw/Render
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        explosion_group.draw(screen)
        explosion_group.update()
        # Call function to print the current score and level to the screen.
        score_and_level(level)
        if player.score in numbers_list:
            # Advance the level +1.
            level += 1
            numbers_list.remove(player.score)
        # Randomise the enemy shooting.
        for enemy in enemy_sprites:
            if random.randrange(0, 4 * 60) == 1:
                # Set enemy bullet speed for the current level.
                speed = level + 1
                enemy.shoot(speed)
        # Show the remaining player lives at the top right of the screen.
        draw_lives(screen, WIDTH - 100, 5, player.lives,
                   player_life_image)
        # Check to see if the player bullets hit an enemy.
        enemy_hits = pygame.sprite.groupcollide(player_bullet_sprites, enemy_sprites, True, True)
        for hit in enemy_hits:
            # +1 score for each enemy destroyed.
            player.score += 1
            effect.play()
            # Play the explosion animation at each hit location.
            explosion = Explosion(hit.rect.x, hit.rect.y)
            explosion_group.add(explosion)
            # Spawn a new enemy, never from the same side twice.
            count = random.randrange(0, 2)
            if count % 2 == 0:
                new_enemy = EnemyReversed()
            else:
                new_enemy = Enemy()
            # Add the new enemy to the sprite groups.
            all_sprites.add(new_enemy)
            enemy_sprites.add(new_enemy)
        # Check to see if the enemy bullets hit a player.
        player_hits = pygame.sprite.groupcollide(enemy_bullet_sprites, player_sprite, True, False)
        for hit in player_hits:
            explosion = Explosion(hit.rect.x, hit.rect.y)
            explosion_group.add(explosion)
            player.health -= 5
            if player.health == -10:
                player.hide()
                player.lives -= 1
                player.health = 10
                if player.lives <= 0:
                    for enemy in enemy_sprites:
                        enemy.kill()
                    for bullet in enemy_bullet_sprites:
                        bullet.kill()
                    play_game_over()
        # Allow option to quit the game.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_time = pygame.time.get_ticks()
                    if current_time - previous_time > 250:
                        previous_time = current_time
                        player.shoot()
        pygame.display.update()
play_intro()