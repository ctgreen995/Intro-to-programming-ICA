import pygame
import random
import math

pygame.init()
# Title of the game window.
pygame.display.set_caption("Cryosoldier")

FPS = 60
CLOCK = pygame.time.Clock()

# Create the game window.
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the background image.
background = pygame.image.load('whitehouse2.jpg')
player = pygame.image.load('tank.png')
jet = pygame.image.load('jet-fighter.png')
jet_reversed = pygame.image.load('jet_reversed.png')
armybase = pygame.image.load('base.png')
medicalcentre = pygame.image.load('medical.png')
potus = pygame.image.load('potus.png')
missile = pygame.image.load('missile.png')

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = jet
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(300, 600)
        self.speedx = random.randrange(2,6)

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right <= 0:
            self.rect.left = 1000
            self.rect.y = random.randrange(200,700)


class Enemy_Reversed(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = jet_reversed
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(300, 600)
        self.speedx = random.randrange(2,6)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left >= 1000:
            self.rect.right = 0
            self.rect.y = random.randrange(200, 700)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = +5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self. rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.y)
        all_sprites.add(bullet)
        bullets.add(bullet)

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

# Sprite groups
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
bullets = pygame.sprite.Group()

for i in range(3):
    i = Enemy()
    all_sprites.add(i)
    enemy_sprites.add(i)

for i in range(3):
    e = Enemy_Reversed()
    all_sprites.add(e)
    enemy_sprites.add(e)

# Game loop

running = True
while running:
    CLOCK.tick(FPS)

    pygame.display.update()
    # Update
    all_sprites.update()

    # Draw/Render
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    if pygame.sprite.groupcollide(bullets, enemy_sprites, True, True):
        pass



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()




