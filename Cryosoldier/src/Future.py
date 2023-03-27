import pygame
import sys
import random

pygame.init()
pygame.mixer.init()
game_time = pygame.time.Clock()

# Game window variables
WIDTH, HEIGHT = 1500, 600
game_display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Cryosoldier")

# Colours
cryo_colour = (159, 192, 226)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Variables for player and enemy movement speed
MAX_VELOCITY = 4
up_down = (8, -8)

# Image and audio
background = pygame.image.load("images/Space_background.png")
intro_font = pygame.font.SysFont("freesansbold. ttf", 80)
score_font = pygame.font.SysFont("freesansbold. ttf", 20)
game_over_font = pygame.font.SysFont("freesansbold. ttf", 80)
final_score_font = pygame.font.SysFont("freesansbold. ttf", 50)
play_again_font = pygame.font.SysFont("freesansbold. ttf", 50)
quit_font = pygame.font.SysFont("freesansbold. ttf", 50)
pygame.mixer.music.load("audio/space_audio.wav")
explosion_audio = pygame.mixer.Sound("audio/explosion.wav")
player_laser_audio = pygame.mixer.Sound("audio/laser.wav")
enemy_laser_audio = pygame.mixer.Sound("audio/enemy_laser.wav")
asteroid_images = ["images/Asteroid_1.png",
                   "images/Asteroid_2.png",
                   "images/Asteroid_3.png"]

# Sprite groups
asteroid_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_lasers = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_lasers = pygame.sprite.Group()

# Enemy firing timer
enemy_shot_start = pygame.time.get_ticks()

# Show intro function, shows intro for 3 seconds
def intro():
    start = pygame.time.get_ticks()

    show_intro = True
    while show_intro:
        timer = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        text_surface = intro_font.render("Future Soldier", True,
                                         cryo_colour)
        game_display.blit(background, (0, 0))
        game_display.blit(text_surface, (WIDTH - 950, HEIGHT - 340))
        pygame.display.update()
        if timer - start > 3000:
            show_intro = False
            start = timer


# Shows game over screen following main game
def game_over(score):
    show_game_over = True
    while show_game_over:
        events = pygame.event.get()
        key_press = pygame.key.get_pressed()
        game_over_surface = game_over_font.render("GAME OVER!", True,
                                                  cryo_colour)
        score_surface = \
            final_score_font.render("Final Score: " + str(score),
                                    True, cryo_colour)
        quit_surface = quit_font.render("Quit", True, red)
        play_surface = play_again_font.render("Play", True, green)
        game_display.blit(background, (0, 0))
        game_display.blit(game_over_surface, (WIDTH - 950, HEIGHT - 440))
        game_display.blit(score_surface, (WIDTH - 890, HEIGHT - 340))
        pygame.draw.rect(game_display, cryo_colour,
                         (WIDTH - 710, HEIGHT - 240, 73, 35))
        pygame.draw.rect(game_display, cryo_colour,
                         (WIDTH - 910, HEIGHT - 240, 73, 35))
        game_display.blit(quit_surface, (WIDTH - 710, HEIGHT - 240))
        game_display.blit(play_surface, (WIDTH - 910, HEIGHT - 240))
        mouse = pygame.mouse.get_pos()
        pygame.display.update()
        # if quit or escape quits game
        for i in events:
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # If user presses button plays or goes back to text based game
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH - 910 <= mouse[0] <= WIDTH - 837 and \
                        HEIGHT - 240 <= mouse[1] <= HEIGHT - 205:
                    player.lives = 5
                    player.score = 0
                    player.rect.center = (player.rect.width, HEIGHT / 2)
                    main()
                elif WIDTH - 710 <= mouse[0] <= WIDTH - 637 and \
                        HEIGHT - 240 <= mouse[1] <= HEIGHT - 205:
                    pygame.mixer.music.stop()
                    show_game_over = False


# Asteroid class
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.choice = random.choice(asteroid_images)
        self.image = pygame.image.load(self.choice)
        self.rect = self.image.get_rect()
        self.rect.center = (1600, random.randint(30, 530))
        self.velocity = 0

    # Moves asteroids at game speed and deletes them when they leave screen
    def update(self, asteroid, game_speed, asteroids):
        self.velocity = game_speed
        self.rect.x -= self.velocity
        if self.rect.x == 0:
            self.velocity = self.velocity * 2
        if self.rect.x < -64:
            asteroids.remove(asteroid)

    # Draws to screen
    def draw(self):
        game_display.blit(self.image, self.rect)


# Laser firing class
class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, direction, laser_colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 5)).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.colour = laser_colour
        self.mask = pygame.mask.from_surface(self.image)

    # MOves the lasers when fired, deletes them when they leave the screen
    def update(self, game_speed):
        pygame.draw.rect(game_display, pygame.Color(self.colour), self.rect)
        if self.direction == "right":
            self.rect.x += game_speed + 8
        else:
            self.rect.x -= game_speed + 8
        if self.rect.x < 0:
            self.kill()
        elif self.rect.x > 1600:
            self.kill()

# Player class
class Human(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/battleship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width, HEIGHT / 2)
        self.score = 0
        self.respawn = 0
        self.dead = 0
        self.lives = 5
        self.player_enemy = False
        self.keys_on = True

    # Takes key presses and moves player within boundaries of screen
    def update(self, key):
        if key[pygame.K_UP] and self.rect.y > 0 and self.keys_on:
            self.rect.y -= MAX_VELOCITY
        if key[pygame.K_DOWN] and self.rect.y < (HEIGHT - 64) and self.keys_on:
            self.rect.y += MAX_VELOCITY
        if key[pygame.K_LEFT] and self.rect.x > 0 and self.keys_on:
            self.rect.x -= MAX_VELOCITY
        if key[pygame.K_RIGHT] and self.rect.x < (WIDTH - 64) and self.keys_on:
            self.rect.x += MAX_VELOCITY

    # Handles player collisions
    def player_collide(self, hit_timer):

        player_asteroid = \
            pygame.sprite.spritecollide(player, asteroid_group, True,

                                        pygame.sprite.collide_mask)
        self.player_enemy = \
            pygame.sprite.spritecollide(player, enemy_group, True,
                                        pygame.sprite.collide_mask)
        player_hit = \
            pygame.sprite.spritecollide(player, enemy_lasers, True,
                                        pygame.sprite.collide_mask)

        # Make player invulnerable for short period, plays explosion audio
        # and explosion image
        self.dead = self.respawn > 0
        if self.dead:
            pygame.mixer.Sound.play(explosion_audio)
            self.image = pygame.image.load("images/explosion.png")
            game_display.blit(self.image, self.rect)
            self.keys_on = False
            self.respawn -= hit_timer
        if self.respawn < 0:
            self.respawn = 0
            self.keys_on = True

        # If player hit remove life, make invulnerable by setting respawn time
        if not self.dead and player_asteroid or self.player_enemy or player_hit:
            if self.respawn <= 0:
                self.lives -= 1
            self.respawn = 1500

        # If not hit player image is battleship
        elif not self.dead:
            self.image = pygame.image.load("images/battleship.png")
            game_display.blit(self.image, self.rect)

        # Player lasers hitting asteroid absorbs lasers
        if pygame.sprite.groupcollide(player_lasers, asteroid_group,
                                      True, False):
            pass

    # Player shoot function, plays player laser audio and adds laser to
    # player_laser group
    def shoot(self, events):
        for i in events:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE and not self.dead:
                    pygame.mixer.Sound.play(player_laser_audio, loops=0)
                    player_lasers.add(Laser(self.rect.midright, "right", "blue"))


# Enemy class
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/space-ship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (1600, random.randint(30, 530))
        self.velocity = 0
        self.dodge = random.choice(up_down)
        self.splat = 0
        self.dead = 0
        self.start = enemy_shot_start

    # Moves enemies and deletes when leave screen
    def update(self, game_speed, enemies):
        self.velocity = game_speed
        self.rect.x -= self.velocity + 1

        if self.rect.x == 0:
            self.rect.x -= self.velocity * 2
        if self.rect.x < -64:
            self.kill()
            enemies.remove(self)

    # Enemy collisions
    def enemy_collide(self, kill_timer, enemies):
        collide_asteroid = \
            pygame.sprite.groupcollide(enemy_group, asteroid_group,
                                       True, True, pygame.sprite.collide_mask)
        # If enemy collides asteroid move enemy around asteroid
        if collide_asteroid:
            self.rect.x += self.velocity
            self.rect.y += self.dodge
        # If enemy hits boundary, reverse enemy
        if self.rect.y < 0:
            self.dodge = self.velocity + 1
        elif self.rect.y > 530:
            self.dodge = -self.velocity + 1

        # Enemy laser hits asteroid gets absorbed
        if pygame.sprite.groupcollide(enemy_lasers, asteroid_group, True,
                                      False):
            pass

        enemy_hit = \
            pygame.sprite.groupcollide(enemy_group, player_lasers, True, True,
                                       pygame.sprite.collide_mask)
        # Delays deleting enemy for short period
        self.dead = self.splat > 0
        if self.dead:
            self.splat -= kill_timer
        # If player collides with enemy, remove enemy immediately
        if self.splat == 2 or player.player_enemy:
            self.kill()
            enemies.remove(self)
        elif self.splat < 0:
            self.splat = 0

        # If enemy hit, show and play explosion audio, player score +=1
        if not self.dead:
            if enemy_hit:
                pygame.mixer.Sound.play(explosion_audio)
                self.image = pygame.image.load("images/explosion.png")
                player.score += 1
                self.splat = 10
        # Enemies absorb enemy lasers
        if pygame.sprite.groupcollide(enemy_group, enemy_lasers, False, True,
                                      pygame.sprite.collide_mask):
            pass

    # Enemy firing function, plays enemy laser audio and adds laser to
    # enemy_lasers group
    def enemy_shoot(self, shot_timer):
        if shot_timer - self.start > random.randint(3000, 4000) and not self.dead:
            pygame.mixer.Sound.play(enemy_laser_audio)
            enemy_lasers.add(Laser(self.rect.topleft, "left", "red"))
            enemy_lasers.add(Laser(self.rect.bottomleft, "left", "red"))
            self.start = shot_timer

    # Draw enemy to screen
    def draw(self):
        game_display.blit(self.image, self.rect)


player = Human()
def main():
    # Background positions
    bg1_x = 0
    bg2_x = background.get_width()

    # How often asteroids and enemies spawn in beginning
    asteroid_spawner = 6000
    enemy_spawner = 5000

    # Game speed in beginning
    game_speed = 1

    asteroids = []
    enemies = []

    # Empties sprite groups for if play again selected
    asteroid_group.empty()
    player_group.empty()
    player_lasers.empty()
    enemy_group.empty()
    enemy_lasers.empty()

    # Start timers
    start = pygame.time.get_ticks()
    asteroid_start = pygame.time.get_ticks()
    enemy_start = pygame.time.get_ticks()

    run = True
    while run:
        events = pygame.event.get()
        key_press = pygame.key.get_pressed()
        game_timer = pygame.time.get_ticks()

        asteroid = Rock()
        enemy = Alien()

        # Asteroid spawn timer and function calls
        asteroid_timer = pygame.time.get_ticks()
        if asteroid_timer - asteroid_start > asteroid_spawner:
            asteroids.append(asteroid)
            asteroid_start = asteroid_timer
        for asteroid in asteroids:
            asteroid_group.add(asteroid)
            asteroid.draw()
            asteroid.update(asteroid, game_speed, asteroids)

        # Player variables and function calls
        player_hit_timer = game_time.tick()
        player.update(key_press)
        player.shoot(events)
        player.player_collide(player_hit_timer)
        player_lasers.draw(game_display)
        player_lasers.update(game_speed)

        # Enemy spawn timer and function calls
        enemy_timer = pygame.time.get_ticks()
        enemy_hit_timer = game_time.tick()
        enemy_shot_timer = pygame.time.get_ticks()
        if enemy_timer - enemy_start > enemy_spawner:
            enemies.append(enemy)
            enemy_start = enemy_timer
        for enemy in enemies:
            enemy_group.add(enemy)
            enemy.draw()
            enemy.update(game_speed, enemies)
            enemy.enemy_collide(enemy_hit_timer, enemies)
            enemy.enemy_shoot(enemy_shot_timer)
        enemy_lasers.draw(game_display)
        enemy_lasers.update(game_speed)

        pygame.display.update()

        # Game display
        game_display.blit(background, (bg1_x, 0))
        game_display.blit(background, (bg2_x, 0))
        # Move background to simulate sidescroll
        bg1_x -= game_speed
        bg2_x -= game_speed
        if bg1_x < background.get_width() * -1:
            bg1_x = background.get_width()
        if bg2_x < background.get_width() * -1:
            bg2_x = background.get_width()
        # Show score and lives
        score_surface = score_font.render("Score: " + str(player.score), True,
                                          (159, 192, 226))
        game_display.blit(score_surface, (WIDTH - 100, 20))
        spacing = 30
        for i in range(0, player.lives):
            game_display.blit(pygame.image.load("images/hospital.png"),
                              ((WIDTH / 2) + spacing, 20))
            spacing += 20

        # Increase game speed to simulate difficulty
        if game_timer - start > 10000:
            game_speed = game_speed + 1
            if enemy_spawner > 500:
                enemy_spawner = enemy_spawner - 500
            if asteroid_spawner > 500:
                asteroid_spawner = asteroid_spawner - 100
            start = game_timer

        # If user quits, loses all lives or presses escape, exit game loop
        for i in events:
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if player.lives == 0:
            run = False


pygame.mixer.music.play(loops=-1)
intro()
main()
game_over(player.score)
