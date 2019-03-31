import pygame
import pygame.freetype
import random

pygame.init()

# Setting up Window
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Laser Pong")

# Globals
black = (0, 0, 0)
white = (255, 255, 255)
gray = (115, 115, 115)
yellow = (255, 255, 0)
clock = pygame.time.Clock()


# Creating Classes
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Button(pygame.sprite.Sprite):
    def __init__(self, image_file, image_pressed, location):
        pygame.sprite.Sprite.__init__(self)
        self.toggled = 0
        self.image_file = pygame.image.load(image_file)
        self.image_pressed = pygame.image.load(image_pressed)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    # Adds hovering functionality to buttons
    def hover(self, mouseover):
        if mouseover == 1:
            self.image = self.image_pressed
        else:
            self.image = self.image_file

    # Adds toggle functionality to buttons
    def toggle(self):
        if self.toggled == 0:
            self.image = self.image_pressed
            self.toggled = 1
        else:
            self.image = self.image_file
            self.toggled = 0

    def reset(self):
        self.toggled = 0
        self.image = self.image_file

class Selector(pygame.sprite.Sprite):
    def __init__(self, image0, image1, image2, location):
        pygame.sprite.Sprite.__init__(self)
        self.image0 = pygame.image.load(image0)
        self.image1 = pygame.image.load(image1)
        self.image2 = pygame.image.load(image2)
        self.image = pygame.image.load(image0)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def selection(self, value):
        if value == 0:
            self.image = self.image0
        elif value == 1:
            self.image = self.image1
        else:
            self.image = self.image2


class Image(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Player(pygame.sprite.Sprite):
    def __init__(self, weapon, direction, location):
        pygame.sprite.Sprite.__init__(self)
        self.weapon = weapon
        self.direction = direction
        if self.weapon == 0:
            if direction == 1:
                self.image = pygame.image.load('resources/players/player_ship1.png')
            else:
                self.image = pygame.image.load('resources/players/player_ship1_right.png')
            self.velocity = 28
            self.movespeed = 10
            self.firerate = 500
            self.damage = 12
        elif self.weapon == 1:
            if direction == 1:
                self.image = pygame.image.load('resources/players/player_ship2.png')
            else:
                self.image = pygame.image.load('resources/players/player_ship2_right.png')
            self.velocity = 20
            self.movespeed = 6
            self.firerate = 200
            self.damage = 4
        else:
            if direction == 1:
                self.image = pygame.image.load('resources/players/player_ship3.png')
            else:
                self.image = pygame.image.load('resources/players/player_ship3_right.png')
            self.velocity = 120
            self.movespeed = 4
            self.firerate = 1200
            self.damage = 25
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.health = 100
        self.lastshot = pygame.time.get_ticks()


    def fire(self, target):
        time = pygame.time.get_ticks()
        if time - self.lastshot >= self.firerate:
            self.lastshot = time
            bullets.append(Bullet('resources/images/image_laser.png', self.direction, target,
                                  player.velocity, self.damage, [self.rect.left + 40, self.rect.top + 40]))
            shot.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image_file, direction, target, velocity, damage, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.velocity = velocity*direction
        self.damage = damage
        self.target = target

    def detect(self, target):
        return self.rect.colliderect(target.rect)


class Com(pygame.sprite.Sprite):
    def __init__(self, diffvalue, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/players/com_ship.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.health = 100
        self.lastshot = pygame.time.get_ticks()
        if diffvalue == 0:
            self.movespeed = 3
            self.velocity = random.randint(8, 18)
            self.firerate = random.randint(600, 900)
            self.damage = random.randint(3, 12)
        elif diffvalue == 1:
            self.movespeed = 6
            self.velocity = random.randint(15, 30)
            self.firerate = random.randint(300, 700)
            self.damage = random.randint(9, 21)
        else:
            self.movespeed = 8
            self.velocity = random.randint(25, 50)
            self.firerate = random.randint(100, 500)
            self.damage = random.randint(15, 30)

    def fire(self):
        time = pygame.time.get_ticks()
        if time - self.lastshot >= self.firerate:
            self.lastshot = time
            bullets.append(Bullet('resources/images/image_laser.png', -1, player,
                                  player.velocity, self.damage, [self.rect.left + 40, self.rect.top + 40]))
            shot.play()

# Sounds
music = pygame.mixer.music.load('resources/sounds/music.mp3')
button = pygame.mixer.Sound('resources/sounds/button.wav')
shot = pygame.mixer.Sound('resources/sounds/shot.wav')

# Backgrounds
bg_menu = Background('resources/backgrounds/bg_menu.png', [0, 0])
bg_game = Background('resources/backgrounds/bg_game.png', [0, 0])

# Buttons
button_start = Button('resources/buttons/button_start.png', 'resources/buttons/button_start_hover.png', [545, 590])
button_players = Button('resources/buttons/button_players_1.png', 'resources/buttons/button_players_2.png', [46, 40])
button_play = Button('resources/buttons/button_play.png', 'resources/buttons/button_play_hover.png', [1020, 40])
button_playagain = Button('resources/buttons/button_playagain.png', 'resources/buttons/button_playagain_hover.png', [416, 400])
button_quit = Button('resources/buttons/button_quit.png', 'resources/buttons/button_quit_hover.png', [655, 400])

# Images
image_title = Image('resources/images/image_title.png', [0, 0])
image_gameover = Image('resources/images/image_gameover.png', [0, 0])
image_singleplayer_menu = Image('resources/images/image_singleplayer_menu.png', [0, 0])
image_multiplayer_menu = Image('resources/images/image_multiplayer_menu.png', [0, 0])
image_menu_selectbuttons = Image('resources/images/image_menu_selectbuttons.png', [155, 206])
image_menu_selectbuttons1 = Image('resources/images/image_menu_selectbuttons.png', [55, 206])
image_menu_selectbuttons2 = Image('resources/images/image_menu_selectbuttons.png', [658, 206])

# Selectors
com_diff = Selector(
    'resources/images/image_com_easy.png',
    'resources/images/image_com_medium.png',
    'resources/images/image_com_hard.png',
    [945, 350])
selector = Selector(
    'resources/selectors/selector_ship1.png',
    'resources/selectors/selector_ship2.png',
    'resources/selectors/selector_ship3.png',
    [155, 206])
selector1 = Selector(
    'resources/selectors/selector_ship1.png',
    'resources/selectors/selector_ship2.png',
    'resources/selectors/selector_ship3.png',
    [55, 206])
selector2 = Selector(
    'resources/selectors/selector_ship1.png',
    'resources/selectors/selector_ship2.png',
    'resources/selectors/selector_ship3.png',
    [658, 206])

# Setting Starting Variables
done = False
font = pygame.freetype.Font('resources/fonts/digital-7.ttf', 80)
scene = 0
leftpos = [10, 320]
rightpos = [1190, 320]

gamemode = 0
game = 0
choice = 0
choice1 = 0
choice2 = 0
difficulty = 0
move_steps = 0
bullets = []
pause = 0

# Starting Menu Music
pygame.mixer.music.play(-1)

while not done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()

    if scene == 0:

        # Checking for Button Hover
        if 545 < mouse[0] < 735 and 590 < mouse[1] < 654:
            hovering = 1
            if pressed[0] == 1:
                scene = 1
                button.play()
        else:
            hovering = 0

        # Base Fill
        window.fill(white)

        # Loading Static Images
        window.blit(bg_menu.image, bg_menu.rect)
        window.blit(image_title.image, image_title.rect)

        # Loading Dynamic Images
        button_start.hover(hovering)
        window.blit(button_start.image, button_start.rect)

    if scene == 1:

        # Player Number Selection Button Clicking
        if 46 < mouse[0] < 276 and 40 < mouse[1] < 104:

            if pressed[0] == 1:

                button.play()

                if gamemode == 1:

                    gamemode = 0
                    button_players.toggle()

        elif 306 < mouse[0] < 536 and 40 < mouse[1] < 104:

            if pressed[0] == 1:

                button.play()

                if gamemode == 0:

                    gamemode = 1
                    button_players.toggle()

        # Base Fill
        window.fill(white)

        # One Player
        if gamemode == 0:

            # Loading Static Images
            window.blit(bg_menu.image, bg_menu.rect)
            window.blit(image_menu_selectbuttons.image, image_menu_selectbuttons.rect)
            window.blit(image_singleplayer_menu.image, image_singleplayer_menu.rect)

            # Checking for Play Button Press
            if 1020 < mouse[0] < 1250 and 40 < mouse[1] < 104:

                hovering = 1

                if pressed[0] == 1:
                    scene = 2
                    button.play()

            else:

                hovering = 0

            # Weapon Selection
            if 215 < mouse[0] < 237 and 308 < mouse[1] < 348:
                if pressed[0] == 1 and choice > 0:
                    choice -= 1

            if 647 < mouse[0] < 668 and 308 < mouse[1] < 348:
                if pressed[0] == 1 and choice < 2:
                    choice += 1

            # Com Difficulty Selection
            if 967 < mouse[0] < 1171 and 350 < mouse[1] < 415:
                if pressed[0] == 1:
                    difficulty = 0
            if 967 < mouse[0] < 1171 and 430 < mouse[1] < 495:
                if pressed[0] == 1:
                    difficulty = 1
            if 967 < mouse[0] < 1171 and 510 < mouse[1] < 575:
                if pressed[0] == 1:
                    difficulty = 2

            # Loading Dynamic Images
            com_diff.selection(difficulty)
            window.blit(com_diff.image, com_diff.rect)
            selector.selection(choice)
            window.blit(selector.image, selector.rect)
            button_play.hover(hovering)
            window.blit(button_play.image, button_play.rect)

        player = Player(choice, 1, leftpos)
        com = Com(difficulty, rightpos)

        # Two Player
        if gamemode == 1:

            # Loading Static Images
            window.blit(bg_menu.image, bg_menu.rect)
            window.blit(image_multiplayer_menu.image, image_multiplayer_menu.rect)
            window.blit(image_menu_selectbuttons1.image, image_menu_selectbuttons1.rect)
            window.blit(image_menu_selectbuttons2.image, image_menu_selectbuttons2.rect)

            # Checking for Play Button Press
            if 1020 < mouse[0] < 1250 and 40 < mouse[1] < 104:

                hovering = 1

                if pressed[0] == 1:
                    scene = 3
                    button.play()

            else:

                hovering = 0

            # Making Weapon Choices

            # Player 1

            if 114 < mouse[0] < 137 and 308 < mouse[1] < 348:
                if pressed[0] == 1 and choice1 > 0:
                    choice1 -= 1

            if 547 < mouse[0] < 565 and 308 < mouse[1] < 348:
                if pressed[0] == 1 and choice1 < 2:
                    choice1 += 1

            # Player 2

            if 716 < mouse[0] < 739 and 308 < mouse[1] < 348:
                if pressed[0] == 1 and choice2 > 0:
                    choice2 -= 1

            if 1150 < mouse[0] < 1169 and 308 < mouse[1] < 348:
                if pressed[0] == 1 and choice2 < 2:
                    choice2 += 1

            # Loading Dynamic Images
            button_play.hover(hovering)
            window.blit(button_play.image, button_play.rect)
            selector1.selection(choice1)
            window.blit(selector1.image, selector1.rect)
            selector2.selection(choice2)
            window.blit(selector2.image, selector2.rect)

        # Player Selection Button
        window.blit(button_players.image, button_players.rect)

        player_left = Player(choice1, 1, leftpos)
        player_right = Player(choice2, -1, rightpos)

    if scene == 2:

        # Loading Static Images
        window.blit(bg_game.image, bg_game.rect)

        # Loading Dynamic Images
        font.render_to(window, (40, 40), str(player.health), white)
        font.render_to(window, (1160, 40), str(com.health), white)

        for bullet in bullets:
            if 40 < bullet.rect.left < 1240:
                bullet.rect.left += bullet.velocity
                if game == 0:
                    if bullet.detect(bullet.target):
                        bullet.target.health -= bullet.damage
                        bullets.pop(bullets.index(bullet))
                window.blit(bullet.image, bullet.rect)
            else:
                bullets.pop(bullets.index(bullet))

        if game == 0:

            # Player Movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player.rect.top -= player.movespeed
            if keys[pygame.K_DOWN]:
                player.rect.top += player.movespeed
            if player.rect.top <= 40:
                player.rect.top += player.movespeed
            elif player.rect.top >= 600:
                player.rect.top -= player.movespeed

            if keys[pygame.K_SPACE]:
                player.fire(com)

            com.fire()

            # Com AI
            if com.rect.top <= 40:
                move_steps = 20
            elif com.rect.top >= 600:
                move_steps = -20

            if move_steps > 1:
                move_steps -= 1
                com.rect.top += com.movespeed
            elif move_steps < 1:
                move_steps += 1
                com.rect.top -= com.movespeed
            else:
                move_steps = random.randint(-30, 30)

            if player.health <= 0:
                player.health = 0
                game = 1
            elif com.health <= 0:
                com.health = 0
                game = 1

        else:

            pause += 1

            if pause == 100:
                scene = 4

        # Draw Characters
        window.blit(player.image, player.rect)
        window.blit(com.image, com.rect)

    if scene == 3:

        # Loading Static Images
        window.blit(bg_game.image, bg_game.rect)

        # Loading Dynamic Images
        font.render_to(window, (40, 40), str(player_left.health), white)
        font.render_to(window, (1160, 40), str(player_right.health), white)

        for bullet in bullets:
            if -30 < bullet.rect.left < 1250:
                bullet.rect.left += bullet.velocity
                if game == 0:
                    if bullet.detect(bullet.target):
                        bullet.target.health -= bullet.damage
                        bullets.pop(bullets.index(bullet))
                window.blit(bullet.image, bullet.rect)
            else:
                bullets.pop(bullets.index(bullet))

        if game == 0:

            # Player 1 Buttons
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player_left.rect.top -= player_left.movespeed
            if keys[pygame.K_s]:
                player_left.rect.top += player_left.movespeed

            if player_left.rect.top <= 40:
                player_left.rect.top += player_left.movespeed
            elif player_left.rect.top >= 600:
                player_left.rect.top -= player_left.movespeed

            if keys[pygame.K_SPACE]:
                player_left.fire(player_right)

            # Player 2 Buttons
            if keys[pygame.K_UP]:
                player_right.rect.top -= player_right.movespeed
            if keys[pygame.K_DOWN]:
                player_right.rect.top += player_right.movespeed

            if player_right.rect.top <= 40:
                player_right.rect.top += player_right.movespeed
            elif player_right.rect.top >= 600:
                player_right.rect.top -= player_right.movespeed

            if keys[pygame.K_RETURN]:
                player_right.fire(player_left)

            if player_left.health <= 0:
                player_left.health = 0
                game = 1
            elif player_right.health <= 0:
                player_right.health = 0
                game = 1

        else:

            pause += 1

            if pause == 100:
                scene = 4

        # Draw Characters
        window.blit(player_left.image, player_left.rect)
        window.blit(player_right.image, player_right.rect)

    if scene == 4:

        # Loading Static Images
        window.blit(bg_menu.image, bg_menu.rect)
        window.blit(image_gameover.image, image_gameover.rect)

        # Checking for Play Again Button Press
        if 416 < mouse[0] < 625 and 400 < mouse[1] < 464:

            hovering1 = 1

            if pressed[0] == 1:

                scene = 1
                gamemode = 0
                game = 0
                choice = 0
                choice1 = 0
                choice2 = 0
                difficulty = 0
                move_steps = 0
                bullets = []
                pause = 0
                button_players.reset()
                button.play()

        else:

            hovering1 = 0

        # Checking for Quit Button Press
        if 655 < mouse[0] < 864 and 400 < mouse[1] < 464:

            hovering2 = 1

            if pressed[0] == 1:
                pygame.quit()
                button.play()

        else:

            hovering2 = 0

        # Loading Dynamic Images
        button_playagain.hover(hovering1)
        window.blit(button_playagain.image, button_playagain.rect)

        button_quit.hover(hovering2)
        window.blit(button_quit.image, button_quit.rect)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
