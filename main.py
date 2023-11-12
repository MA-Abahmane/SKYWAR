import os
import pygame
import random
import time, sys
from pygame import mixer

# object creation
pygame.init()
mixer.init()

# Window
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SKYWAR")

# Enemy ship assets
Garuka_ship = pygame.image.load(os.path.join("assets", "alien1.png"))
Tarantula_ship = pygame.image.load(os.path.join("assets", "alien2.png"))
Bit_ship = pygame.image.load(os.path.join("assets", "alien3.png"))

# Random Player Ship
Ghost = "Warcraft1.png"
blueBird = "Warcraft2.png"
FF_Falcon = "Warcraft3.png"

player = pygame.image.load(
    os.path.join("assets", (random.choice([Ghost, blueBird, FF_Falcon]))))

# Lasers
redLaser = pygame.image.load(os.path.join("assets", "blasterBlue.png"))
greenLaser = pygame.image.load(os.path.join("assets", "blasterRed.png"))
blueLaser = pygame.image.load(os.path.join("assets", "blasterBit.png"))

# missiles
m1 = "missile1.png"
m2 = "missile2.png"
missile = pygame.image.load(os.path.join("assets", (random.choice([m1, m2]))))

# Healt Box
healthBox = pygame.image.load(os.path.join("assets", "health.png"))

# Assault Box
saultX = "assaultX.png"
saultZ = "assaultZ.png"
assault = pygame.image.load(os.path.join("assets", "assault.png"))
newShot = pygame.image.load(os.path.join("assets", (random.choice([saultX, saultZ]))))


# Logo
logo = pygame.image.load(os.path.join("assets", "logo.png"))

# Backgrounds
BG_I = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "bg.png")), (WIDTH, HEIGHT))
BG_II = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "bg2.png")), (WIDTH, HEIGHT))

# pages
page_I   = "page_I.png"
page_II  = "page_II.png"
page_III = "page_III.png"




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

    def __init__(self, x, y, health = 100):
        # call __init__() from class player and allow us to defin it atributes
        super().__init__(x, y, health)
        self.ship_img = player
        self.shoot_img = missile
        # mask player to defind colision
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
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

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
        "Garuka": (Garuka_ship, redLaser),
        "Tarantula": (Tarantula_ship, greenLaser),
        "Bit": (Bit_ship, blueLaser)
                  }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        # Get ship from Dictionary
        self.ship_img, self.shoot_img = self.ENEMY_SHIPS[color]
        # Ship mask
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.shoot_img)
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


# check if 2 objects colided
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
    laser_vel = 0.5

    lost = False
    lost_count = 0

    playerHealth_set = 50
    level_num = 7

    # Indexs
    player  = Player(300, 630)
    health  = Health(random.randrange(50, WIDTH - 100), (-100))
    assault = Assault(random.randrange(50, WIDTH - 100), (-100))


    clock = pygame.time.Clock()

    def redrawWin():
        #draw BG on the topleft corner
        WIN.blit(BG_I, (0, 0))

        # draw enemys
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
        if level >= level_num:
            assault.draw(WIN)



        # if lost is true
        if lost:

            defited_lable = lost_font.render(f"DEFEATED", 1, (255, 30, 30))

            lost_label1 = lost_font.render(f"Great game!", 1, (255, 60, 60))

            lost_label2 = lost_font.render(f"Let's go again!", 1,
                                           (255, 60, 60))
            lost_label3 = lost_font.render(f"Is that all you got?!", 1,
                                           (255, 60, 60))
            lost_label4 = lost_font.render(f"You seem disappointed", 1,
                                           (255, 60, 60))

            #hight_score = lost_font.render(f"Score: {level*3} Enemys defeated", 1,(0, 0, 255))

            # Place in the midle
            WIN.blit(defited_lable,
                     (WIDTH / 2 - defited_lable.get_width() / 2, 250))

            if (0 < level < 3):
                WIN.blit(lost_label4,
                         (WIDTH / 2 - lost_label4.get_width() / 2, 350))
            elif (2 < level < 5):
                WIN.blit(lost_label3,
                         (WIDTH / 2 - lost_label3.get_width() / 2, 350))
            elif (4 < level < 7):
                WIN.blit(lost_label2,
                         (WIDTH / 2 - lost_label2.get_width() / 2, 350))
            else:
                WIN.blit(lost_label1,
                         (WIDTH / 2 - lost_label1.get_width() / 2, 350))

        pygame.display.update()

    while run:
        # check 60f/s
        clock.tick(FPS)

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


        # if no enemies in map
        if len(enemies) == 0:
            level += 1
            wave_length += 3
            enemy_vel += 0.2
            laser_vel += 0.5

          # send enemys
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100),
                              random.randrange(-2500, -100),
                              random.choice(["Garuka", "Tarantula", "Bit"]))
                enemies.append(enemy)


        # Quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # keyboard input
        keys = pygame.key.get_pressed()
        # move UP
        if keys[pygame.K_UP] and player.y - player_mov > 0:
            player.y -= player_mov
        # move DOWN
        if keys[pygame.K_DOWN] and player.y + player_mov + player.get_height(
        ) < HEIGHT:
            player.y += player_mov
        # move LEFT
        if keys[pygame.K_LEFT] and player.x - player_mov > 0:
            player.x -= player_mov
        # move RIGHT
        if keys[pygame.K_RIGHT] and player.x + player_mov + player.get_width(
        ) < WIDTH:
            player.x += player_mov

        # shoot
        if keys[pygame.K_SPACE]:
            player.shoot()


        # Enemy movement
        for enemy in enemies[:]:  # copy enemy list
            enemy.move(enemy_vel)
            enemy.move_missile(laser_vel, player)
            # enemy shoot chance
            if random.randrange(0, 2 * 260) == 1:
                enemy.shoot()

            # if player hit enemy
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            # If enemy gets in base
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)


        # if player hit health box
        if collide(health, player):
            player.health = 100
            health = Health(2000, 30000)

        # if player hit assault box
        if collide(assault, player):
            player.shoot_img = newShot
            assault = Assault(2000, 30000)

        player.move_missile(-laser_vel, enemies)


        # health box drop speed
        if player.health <= playerHealth_set:
            health.move(0.4)

        # assault box drop speed
        if level >= level_num:
            assault.move(0.4)


def main_menu():
    label_font = pygame.font.SysFont("comicsans", 70)

    # Background
    WIN.blit(BG_II, (0, 0))
    # Logo print
    WIN.blit(logo, ((WIDTH / 2 - logo.get_width() /2) + 16, 30))
    # game message
    start_label = label_font.render("Press SPACE to start", 1, (200, 240, 255))
    WIN.blit(start_label, (WIDTH / 2 - start_label.get_width() / 2, 420))

    run = True
    flag = False

    while run:

        # after game posters
        if flag:
            WIN.blit(page, (0, 0))

        pygame.display.update()
        # start or quit game
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                run = False
            if keys[pygame.K_SPACE]:
                if (not flag):
                    # Loading Music File
                    mixer.music.load((os.path.join("music", "music.wav")))
                    # volume set
                    mixer.music.set_volume(0.1)
                    # play music
                    mixer.music.play(-1)

                ## Update playing music
                Rmusic = (random.choice(["music.mp3", "music2.mp3", "music3.mp3", "music4.mp3","music5.mp3", "music6.mp3", "music7.mp3", "music8.mp3", "music9.mp3"]))
                # fadeout main menu music
                mixer.music.fadeout(500)

                # get random music
                mixer.music.load((os.path.join("music", Rmusic)))
                # volume set
                mixer.music.set_volume(0.1)
                # play music
                mixer.music.play(-1)

                page = pygame.image.load(os.path.join("assets", (random.choice([page_I, page_II, page_III]))))
                flag = True
                # Start the game
                main()
    pygame.quit()

# Start game
main_menu()






