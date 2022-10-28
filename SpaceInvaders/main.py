import pygame, random
from os import path

pygame.font.init()
pygame.mixer.pre_init(8000, -16, 2, 32)
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DM Defender")
map_y = 0

# Load images

redShip = pygame.image.load(path.join('assets', 'pixel_ship_red_small.png'))
blueShip = pygame.image.load(path.join('assets', 'pixel_ship_blue_small.png'))
greenShip = pygame.image.load(path.join('assets', 'pixel_ship_green_small.png'))
bossShip = pygame.image.load(path.join('assets', 'masterhead.png'))

background = pygame.transform.scale(pygame.image.load(path.join('assets', 'background-black.png')).convert(),
                                    (WIDTH, HEIGHT))

laser_yellow = pygame.image.load(path.join('assets', 'pixel_laser_yellow.png'))
laserBlue = pygame.image.load(path.join('assets', 'dick_laser.png'))
laserYellow = pygame.image.load(path.join('assets', 'dick_laser.png'))
laserGreen = pygame.image.load(path.join('assets', 'dick_laser.png'))
laserRed = pygame.image.load(path.join('assets', 'dick_laser.png'))
# player
playerShip = pygame.image.load(path.join('assets', 'headship.png'))

# pygame.image.load(path.join('assets', 'pixel_ship_yellow.png'))

# Sound Effects
pews = pygame.mixer.Sound('assets/pewpew.wav')
expl1 = pygame.mixer.Sound('assets/explosion1.wav')
expl2 = pygame.mixer.Sound('assets/explosion2.wav')
expl3 = pygame.mixer.Sound('assets/explosion3.wav')
life_lost = pygame.mixer.Sound('assets/life_lost.wav')


class Music:
    def __init__(self, track):
        self.track = track
        self.track_list = {
            'default': 'assets/gameplay_default.wav',
            'menu': 'assets/menu_music.wav',
            'boss': 'assets/boss_music.wav',
            'loss': 'assets/loss.wav',
            'victory': 'assets/victory.wav'
        }

    def play(self, loops=-1):
        pygame.mixer.music.load(self.track_list[self.track])
        if self.track == 'default':
            pygame.mixer.music.set_volume(.5)
        pygame.mixer.music.play(loops=loops)

    @staticmethod
    def stop():
        pygame.mixer.music.stop()

    @staticmethod
    def fadeout(time):
        pygame.mixer.music.fadeout(time)


# music init
menu_music = Music('menu')
default_music = Music('default')
boss_music = Music('boss')
loss_music = Music('loss')
victory = Music('victory')


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (height >= self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 50

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.laser = []
        self.cooldown = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.laser:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cool_down()
        for laser in self.laser:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.laser.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.laser.remove(laser)

    def cool_down(self):
        if self.cooldown >= self.COOLDOWN:
            self.cooldown = 0
        elif self.cooldown > 0:
            self.cooldown += 1

    def shoot(self):
        if self.cooldown == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.laser.append(laser)
            self.cooldown = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Boss(Ship):
    def __init__(self, x, y, health=201):
        super().__init__(self, x, y)
        self.x = x
        self.y = y
        self.max_health = health
        self.health = health
        self.ship_img = bossShip
        self.laser_img = laserRed
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.left = False

    def move(self, vel, horvel):
        if self.y < 80:
            self.health = 201
            self.y += vel
        else:
            if self.x + horvel + self.get_width() < WIDTH and self.left == False:
                self.x += horvel
                if self.x + horvel + self.get_width() >= WIDTH-1:
                    self.left = True
                    self.y += vel + 15
            elif self.x - horvel > 0 and self.left == True:
                self.x -= horvel
                if self.x - horvel <= 0:
                    self.left = False
                    self.y += vel + 15

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def shoot(self):
        laser = Laser(self.x, self.y, self.laser_img)
        dual_laser = Laser(self.x - 20 + (self.get_width() - 100), self.y, self.laser_img)
        self.laser.extend([laser, dual_laser])

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (150, 50, 430, 20))
        pygame.draw.rect(window, (0, 255, 0), (150, 50, 430 * (self.health / self.max_health), 20))


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = playerShip
        self.laser_img = laser_yellow
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cool_down()
        for laser in self.laser:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.laser.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        random.choice([expl1, expl2, expl3]).play()
                        obj.health -= 10
                        if obj.health < 10:
                            objs.remove(obj)
                        self.laser.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (
        self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health),
        10))

    def shoot(self):
        if self.cooldown == 0:
            pews.play()
            laser = Laser(self.x, self.y, self.laser_img)
            self.laser.append(laser)
            self.cooldown = 1

    def move(self, vel):
        self.y += vel


class Enemy(Ship):
    COLOR_MAP = {
        'red': (redShip, laserRed),
        'green': (greenShip, laserGreen),
        'blue': (blueShip, laserBlue)
    }

    def __init__(self, x, y, color, health=10):
        super().__init__(x, y, health)
        self.health = health
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cooldown == 0:
            laser = Laser(self.x - 15, self.y, self.laser_img)
            self.laser.append(laser)
            self.cooldown = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None  # (x,y)


def main():
    default_music.play()
    run = True
    played = True
    FPS = 60
    level = 0
    lives = 3
    main_font = pygame.font.SysFont("Comicsans", 50)
    lost_font = pygame.font.SysFont("Comicsans", 60)
    win_font = pygame.font.SysFont("Comicsans", 60)
    sensei_font = pygame.font.SysFont("Comicsans", 30)

    playerVel = 5
    enemyVel = 2
    laser_velocity = 6

    enemies = []
    bosses = []
    waveLength = 0

    clock = pygame.time.Clock()

    boss_fight = False
    lost = False
    win = False
    lost_count = 0

    player = Player(300, 630)

    def redraw():
        # map scroll
        global map_y
        rel_y = map_y % background.get_rect().height
        WIN.blit(background, (0, rel_y - background.get_rect().height))
        if rel_y < HEIGHT:
            WIN.blit(background, (0, rel_y))
        map_y += 1

        # UI text
        lives_label = main_font.render(f"Lives: {lives}", 1, (0, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (0, 255, 255))
        boss_label = main_font.render(f"Level: {level}", 1, (255, 0, 0))
        sensei_label = sensei_font.render("SENSEI", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))

        if not boss_fight:
            WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
            for anemonies in enemies:
                anemonies.draw(WIN)
        else:
            WIN.blit(sensei_label, (320, 30))
            WIN.blit(boss_label, (WIDTH - boss_label.get_width() - 10, 10))
            for sensei in bosses:
                sensei.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("Too many fuccbois in the DMs", 1, (255, 0, 0))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        elif win:
            win_label = win_font.render("Competition Slain", 1, (0, 255, 0))
            WIN.blit(win_label, (WIDTH / 2 - win_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw()

        if player.health <= 0:
            if lives > 0:
                life_lost.play()
                player.health = 100
                lives -= 1

        if len(bosses) > 0:
            if bosses[0].health <= 11:
                win = True
                lost_count += 1

        if win:
            Music.stop()
            if lost_count > FPS * 4:
                run = False
            else:
                continue

        if lives <= 0:
            Music.stop()
            lost = True
            lost_count += 1

        if lost:
            Music.stop()
            loss_music.play(loops=1)
            if lost_count > FPS * 4:
                run = False
            else:
                continue

        if level == 5:
            boss_fight = True
            Music.stop()
            boss_music.play()
            level = 8055

        if len(enemies) == 0 and boss_fight == False:
            level += 1
            waveLength += 3
            for _ in range(waveLength):
                enemy = Enemy(random.randrange(100, WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(['red', 'blue', 'green']))
                enemies.append(enemy)
        elif len(bosses) == 0 and boss_fight == True:
            boss = Boss(300, -300)
            bosses.append(boss)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - playerVel > 0:  # left
            player.x -= playerVel
        if keys[pygame.K_d] and player.x + playerVel + player.get_width() < WIDTH:  # right
            player.x += playerVel
        if keys[pygame.K_w] and player.y - playerVel > 0:  # left
            player.y -= playerVel
        if keys[pygame.K_s] and player.y + playerVel + player.get_height() < HEIGHT:  # left
            player.y += playerVel
        if keys[pygame.K_SPACE]:
            player.shoot()

        if not boss_fight:
            for enemy in enemies[:]:
                enemy.move(enemyVel)
                enemy.move_lasers(laser_velocity, player)

                if random.randrange(0, 2 * 30) == 1:
                    enemy.shoot()

                if collide(enemy, player):
                    player.health -= 10
                    random.choice([expl1, expl2, expl3]).play()
                    enemies.remove(enemy)

                elif enemy.y + enemy.get_height() > HEIGHT:
                    lives -= 1
                    enemies.remove(enemy)

        elif boss_fight:
            for enemy in bosses:
                enemy.move(1, 4)
                enemy.move_lasers(laser_velocity, player)

                if random.randrange(0, 1 * 10) == 1:
                    enemy.shoot()

                if collide(enemy, player):
                    player.health -= 10
                    random.choice([expl1, expl2, expl3]).play()

                elif enemy.y + enemy.get_height() > HEIGHT:
                    lives = 0
                    bosses.remove(enemy)

        player.move_lasers(-laser_velocity, enemies)
        player.move_lasers(-laser_velocity, bosses)

    menu_music.play()


def main_menu():
    menu_music.play()
    game_title = pygame.font.SysFont('comicsans', 80)
    title_font = pygame.font.SysFont('comicsans', 45)
    run = True
    clock = pygame.time.Clock()
    while run:
        # background scroll
        clock.tick(60)
        global map_y
        rel_y = map_y % background.get_rect().height
        WIN.blit(background, (0, rel_y - background.get_rect().height))
        if rel_y < HEIGHT:
            WIN.blit(background, (0, rel_y))
        map_y += 1

        game_label = game_title.render("DM DEFENDER", 1, (153, 51, 255))
        title_label = title_font.render("Click to begin...", 1, (204, 153, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 375))
        WIN.blit(game_label, (WIDTH / 2 - game_label.get_width() / 2, 300))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Music.stop()
                default_music.play()
                main()
    quit()


main_menu()
