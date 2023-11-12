import os
import pygame
import random
import time, sys
from pygame import mixer

pygame.init()
mixer.init()

# Set Window
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SKYWAR")

# Enemy ship assets
Garuka_ship = pygame.image.load(os.path.join("SKYWAR", "assets", "alien1.png"))
Tarantula_ship = pygame.image.load(os.path.join("SKYWAR", "assets", "alien2.png"))
Bit_ship = pygame.image.load(os.path.join("SKYWAR", "assets", "alien3.png"))

# Random Player Ship
Ghost = "Warcraft1.png"
blueBird = "Warcraft2.png"
FF_Falcon = "Warcraft3.png"
player = pygame.image.load(os.path.join("SKYWAR", "assets", (random.choice([Ghost, blueBird, FF_Falcon]))))

# Lasers
blueLaser = pygame.image.load(os.path.join("SKYWAR", "assets", "blasterBlue.png"))
redLaser = pygame.image.load(os.path.join("SKYWAR", "assets", "blasterRed.png"))
bitLaser = pygame.image.load(os.path.join("SKYWAR", "assets", "blasterBit.png"))

# missiles
m1 = "missile1.png"
m2 = "missile2.png"
missile = pygame.image.load(os.path.join("SKYWAR", "assets", (random.choice([m1, m2]))))

# Healt Box
healthBox = pygame.image.load(os.path.join("SKYWAR", "assets", "health.png"))

# Assault Box
saultX = "assaultX.png"
saultZ = "assaultZ.png"
# Load assault box
assault = pygame.image.load(os.path.join("SKYWAR", "assets", "assault.png"))
# Load assault missiles
newShot = pygame.image.load(os.path.join("SKYWAR", "assets", (random.choice([saultX, saultZ]))))

# Logo
logo = pygame.image.load(os.path.join("SKYWAR", "assets", "logo.png"))

# Backgrounds
BG_I = pygame.transform.scale(
    pygame.image.load(os.path.join("SKYWAR", "assets", "sky.png")), (WIDTH, HEIGHT))


# Game main page [1st page displayed]
GPage = pygame.image.load(os.path.join("SKYWAR", "assets", "GPage.png"))
# Game mission page [2st page displayed]
mission = pygame.image.load(os.path.join("SKYWAR", "assets", "mission.png"))

# pages
page_I   = "page_I.png"
page_II  = "page_II.png"
page_III = "page_III.png"


## SOUNDS
# set game shooting sounds (sound, volume)
missileS = ('SKYWAR/music/missileBlast.wav', 0.1)
missileS2 = ('SKYWAR/music/missileBlast2.wav', 0.15)
laserS = ('SKYWAR/music/laserBlast.wav', 0.1)
collisionS = ('SKYWAR/music/collision.wav', 0.15)
playerHitS = ('SKYWAR/music/playerHit.wav', 0.1)
enemyHitS = ('SKYWAR/music/enemyHit.wav', 0.25)
assaultS = ('SKYWAR/music/load.wav', 0.05)
healthS = ('SKYWAR/music/health.wav', 0.05)
WaveS = ('SKYWAR/music/wave.wav', 0.05)




## Laser class
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    # check for collision
    def collision(self, obj):
        return collide(self, obj)


## Ships class
class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.shoot_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_missile(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision (obj):
                obj.health -= 10
                # player get hiy by laser sound
                c = pygame.mixer.Sound(playerHitS[0])
                c.set_volume(playerHitS[1])
                c.play()
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.shoot_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


# player ship class
class Player(Ship):
    mslSound = missileS

    def __init__(self, x, y, health = 100):
        # call __init__() from class player and allow us to defin it atributes
        super().__init__(x, y, health)
        self.ship_img = player
        self.shoot_img = missile
        # mask player to define collision
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_missile(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        # missile hit enemy sound
                        c = pygame.mixer.Sound(enemyHitS[0])
                        c.set_volume(enemyHitS[1])
                        c.play()
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.shoot_img)
            # make a missile blast sound
            m = pygame.mixer.Sound(self.mslSound[0])
            m.set_volume(self.mslSound[1])
            m.play()
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10,
                          self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10,
                          self.ship_img.get_width() *
                          (self.health / self.max_health), 10))


# Enemy ship
class Enemy(Ship):
    ENEMY_SHIPS = {
        "Garuka": (Garuka_ship, blueLaser),
        "Tarantula": (Tarantula_ship, redLaser),
        "Bit": (Bit_ship, bitLaser)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.name = color
        # Get ship from Dictionary
        self.ship_img, self.shoot_img = self.ENEMY_SHIPS[color]
        # Ship mask
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.shoot_img)
            if (not laser.off_screen(HEIGHT)):
                # make a laser blast sound
                l = pygame.mixer.Sound(laserS[0])
                l.set_volume(laserS[1])
                l.play()
            self.lasers.append(laser)
            self.cool_down_counter = 2


# Health Box
class Health():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Get health box picture
        self.health_img = healthBox
        # health box mask
        self.mask = pygame.mask.from_surface(self.health_img)

    def draw(self, window):
        window.blit(self.health_img, (self.x, self.y))

    def move(self, vel):
        self.y += vel


# Assault Box
class Assault():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Get health box picture
        self.assault_img = assault
        # health box mask
        self.mask = pygame.mask.from_surface(self.assault_img)

    def move(self, vel):
        self.y += vel

    def draw(self, window):
        window.blit(self.assault_img, (self.x, self.y))



# check if 2 objects collided
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return (obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None)



## main ##
def main():

    run = True
    FPS = 60
    level = 0
    lives = 5

    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 3
    enemy_vel = 0.5

    player_mov = 5
    laser_vel = 1

    lost = False
    lost_count = 0

    # drops set
    playerHealth_set = 50
    assault_lvl = 1
    drop_speed = 0.7


    # Indexes
    player  = Player(300, 630)
    health  = Health(random.randrange(50, WIDTH - 100), (-100))
    assault = Assault(random.randrange(50, WIDTH - 100), (-100))


    clock = pygame.time.Clock()

    def redrawWin():

        # draw enemies
        for enemy in enemies:
            enemy.draw(WIN)

        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (30, 100, 200))
        wave_label = main_font.render(f"Wave: {level}", 1, (245, 250, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(wave_label, (WIDTH - wave_label.get_width() - 10, 10))


        # draw player
        player.draw(WIN)

        #  draw health box when needed
        if player.health <= playerHealth_set:
            health.draw(WIN)

        #  drop an assault box
        if level >= assault_lvl:
            assault.draw(WIN)


        # if lost is true
        if lost:
            defited_lable = lost_font.render(f"DEFEATED", 1, (220, 20, 60))
            lost_label1 = lost_font.render(f"Great game!", 1, (220, 20, 60))
            lost_label2 = lost_font.render(f"Let's go again!", 1, (220, 20, 60))
            lost_label3 = lost_font.render(f"Is that all?!", 1, (220, 20, 60))
            lost_label4 = lost_font.render(f"You seem disappointed", 1, (220, 20, 60))

            #hight_score = lost_font.render(f"Score: {level*3} Enemys defeated", 1,(0, 0, 255))

            # Place in the midle
            WIN.blit(defited_lable,
                     (WIDTH / 2 - defited_lable.get_width() / 2, 250))

            if (0 < level < 4):
                WIN.blit(lost_label4,
                         (WIDTH / 2 - lost_label4.get_width() / 2, 350))
            elif (3 < level < 6):
                WIN.blit(lost_label3,
                         (WIDTH / 2 - lost_label3.get_width() / 2, 350))
            elif (5 < level < 9):
                WIN.blit(lost_label2,
                         (WIDTH / 2 - lost_label2.get_width() / 2, 350))
            else:
                WIN.blit(lost_label1,
                         (WIDTH / 2 - lost_label1.get_width() / 2, 350))

        pygame.display.update()


    i = 0
    while run:
        # main game loop
        # Check 60/s for input
        clock.tick(FPS)

        ## Draw moving Background
        WIN.fill((0, 0, 0))
        # Draw background
        WIN.blit(BG_I, (0, i))
        # Draw next background
        WIN.blit(BG_I, (0, -HEIGHT + i))

        # Draw the next background when the top is reached
        if (i == HEIGHT):
            WIN.blit(BG_I, (0, -HEIGHT + i))
            i = 0
        i += 1

        redrawWin()

        # if lost
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        ## WAVE SET
        # if no enemies in map
        if len(enemies) == 0:
            level += 1
            wave_length += 2
            enemy_vel += 0.3
            laser_vel += 0.3
            # Blow the alert horn
            c = pygame.mixer.Sound(WaveS[0])
            c.set_volume(WaveS[1])
            c.play()

          # send enemies
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100),
                              random.randrange(-2500, -100),
                              random.choice(["Garuka", "Tarantula", "Bit"]))
                enemies.append(enemy)


        # Quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


        ## keyboard input
        keys = pygame.key.get_pressed()

        # Pause/play music
        if keys[pygame.K_p]:
                mixer.music.pause()
        if keys[pygame.K_o]:
                mixer.music.unpause()

        # move UP
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y - player_mov > 0:
            player.y -= player_mov
        # move DOWN
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y + player_mov + player.get_height(
        ) < HEIGHT:
            player.y += player_mov
        # move LEFT
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x - player_mov > 0:
            player.x -= player_mov
        # move RIGHT
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + player_mov + player.get_width(
        ) < WIDTH:
            player.x += player_mov

        # shoot missile
        if keys[pygame.K_SPACE]:
            player.shoot()


        ## SET ENEMIES
        # =>Enemy movement
        for enemy in enemies[:]:  # copy enemy list
            # Tarantula will be 20% faster
            if (enemy.name == 'Tarantula'):
                enemy.move(enemy_vel + (enemy_vel * 0.2))
            else:
                enemy.move(enemy_vel)

            # Garukas laser will be twice as fast
            if (enemy.name == 'Garuka'):
                enemy.move_missile(laser_vel * 2, player)
            # Tarantula laser stabilization
            elif (enemy.name == 'Tarantula'):
                enemy.move_missile(laser_vel + (laser_vel * 0.2), player)
            else:
                enemy.move_missile(laser_vel, player)

            # => enemy shoot chance
            if random.randrange(0, 2 * 160) == 1:
                enemy.shoot()

            # If player hit enemy (Ships collision)
            if collide(enemy, player):
                # make a collision sound
                c = pygame.mixer.Sound(collisionS[0])
                c.set_volume(collisionS[1])
                c.play()
                player.health -= 10
                enemies.remove(enemy)

            # If enemy gets in base
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)


        # laser shoot up
        player.move_missile(-laser_vel, enemies)

        ## DROPS
        # if player hit health box
        if collide(health, player):
            # Health sound affect
            a = pygame.mixer.Sound(healthS[0])
            a.set_volume(healthS[1])
            a.play()
            player.health = 100
            health = Health(2000, 30000)

        # if player hit assault box
        if collide(assault, player):
            # assault gear up sound affect
            h = pygame.mixer.Sound(assaultS[0])
            h.set_volume(assaultS[1])
            h.play()
            player.shoot_img = newShot
            player.mslSound = missileS2
            assault = Assault(2000, 30000)


        # health box drop speed
        if player.health <= playerHealth_set:
            health.move(drop_speed)

        # assault box drop speed
        if level >= assault_lvl:
            assault.move(drop_speed)



def main_menu():
    """ Get to know the game (Info page) """
    run = True
    count = False

    WIN.blit(mission, (0, 0))

    while run:
        # posters
        if count:
            WIN.blit(page, (0, 0))

        pygame.display.update()
        # start or quit game
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                run = False
            # Pause/play music
            if keys[pygame.K_o]:
                    mixer.music.pause()
            if keys[pygame.K_p]:
                    mixer.music.unpause()

            # Let's play
            if keys[pygame.K_SPACE]:
                if (not count):
                    # fadeout main menu music
                    mixer.music.fadeout(500)
                    # Loading Music File
                    mixer.music.load((os.path.join("SKYWAR", "music", "Gmusic.wav")))
                    # volume set
                    mixer.music.set_volume(0.1)
                    # play music
                    mixer.music.play(-1)

                page = pygame.image.load(os.path.join("SKYWAR", "assets", (random.choice([page_I, page_II, page_III]))))
                count = True
                # Start the game
                main()

    pygame.quit()


def Play():
    """ Let the game begin [Main Page] """
    run = True

    WIN.blit(GPage, (0, 0))
    #Loading Music File
    mixer.music.load((os.path.join("SKYWAR", "music", "DBZ_GohansAnger.wav")))
    #volume set
    mixer.music.set_volume(0.1)
    #play music
    mixer.music.play()

    while run:

        pygame.display.update()
        for event in pygame.event.get():
            # save keys pressed in a list
            keys = pygame.key.get_pressed()
            # Quit game
            if event.type == pygame.QUIT:
                run = False
            # Pause/play music
            if keys[pygame.K_o]:
                    mixer.music.pause()
            if keys[pygame.K_p]:
                    mixer.music.unpause()
            # Play
            if keys[pygame.K_SPACE]:
                main_menu()

# RUN SKYWAR
Play()












