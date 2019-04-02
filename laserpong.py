import pygame
import pygame.freetype
import random

pygame.init()

# Setting up window.
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Laser Pong")

# Globals
white = (255, 255, 255)
clock = pygame.time.Clock()
leftpos = [10, 320]
rightpos = [1190, 320]
done = False
font = pygame.freetype.Font('resources/fonts/digital-7.ttf', 80)

# Creating Classes

""" The background class is very straightforward, requiring an image file and a location. It places the image from the
top left corner. """


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


""" The button class allows for some more interesting features. It takes an image file, a pressed image file, for 
hovering or toggling. It also takes a location, as all things do. The hover method is very simple, allowing for hover
detection outside the method. If it's being hovered over, it switches images. If not, it uses it's default. The toggle
method uses a 0 or 1 variable to decide which image to display. It just switches every time it's called. """


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


""" Selectors are like togglable buttons with 3 different options. These are used in the ship selection and com 
difficulty choices. They take a selection number, 0, 1, or 2, and change their image based on that. Very simple. """


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


""" Images are just like backgrounds. Really, I didn't need to separate them. """


class Image(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


""" The player is one of the most dynamic classes. It takes a weapon choice, really the ship choice, and assigns values 
for bullet velocity, move speed, fire rate and damage. It also takes in the direction of the player and picks the 
appropriate side image for that. Lastly, it takes a location, which is the center of the screen as defined by a constant
in the globals section. The reason that it was separated was so that you can have different players on the right and the
left sides. It also has fire and update methods, the first of which handling weapon fire and cool down. The ship 
fire rates are in milliseconds, using that number as the delay in between shots. Every time a shot is fired, that time
is noted down as the most recent shot, and then if the delay is more than the time since the last shot, it shoots again.
The update method checks if it's health is 0, and changes to the exploded image if so. """


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
                                  self.velocity, self.damage, [self.rect.left + 40, self.rect.top + 40]))
            shot.play()

    def update(self):
        if self.health <= 0:
            self.image = pygame.image.load('resources/images/image_ship_exploded.png')


""" The bullet class takes an image file, a direction of travel (either 1 or -1) that gets multiplied by the velocity to
make it move left or right. It gets a target which it uses to check if hit boxes are overlapping, using the detect 
method. If so, it returns True.  """


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


""" The com class is almost identical to the player class, except with slight random variations based on the difficulty
selected by the user. It also has the fire and update methods, for the same reason as the players. One difference is
that it doesn't have a direction indicator, as it can only be on the right side. """


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
                                  self.velocity, self.damage, [self.rect.left + 40, self.rect.top + 40]))
            shot.play()

    def update(self):
        if self.health <= 0:
            self.image = pygame.image.load('resources/images/image_ship_exploded.png')


""" Creating Objects """

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
button_playagain = Button('resources/buttons/button_again.png', 'resources/buttons/button_again_hover.png', [416, 400])
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

# Setting starting variables.
scene = 0
gamemode = 0
game = 0
choice = 0
choice1 = 0
choice2 = 0
difficulty = 0
move_steps = 0
bullets = []
pause = 0

# Starting music (-1 makes it play forever).
pygame.mixer.music.play(-1)

while not done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

    # Gets the state of the mouse and it's location that will be all throughout the program.
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

            # Checking for Play Button hovering and press
            if 1020 < mouse[0] < 1250 and 40 < mouse[1] < 104:

                hovering = 1

                if pressed[0] == 1:
                    scene = 2
                    button.play()

            else:

                hovering = 0

            # Weapon Selection Menu
            # Left arrow
            if 215 < mouse[0] < 237 and 308 < mouse[1] < 348:
                if pressed[0] == 1 and choice > 0:
                    choice -= 1
            # Right arrow
            if 647 < mouse[0] < 668 and 308 < mouse[1] < 348:
                if pressed[0] == 1 and choice < 2:
                    choice += 1

            # Com Difficulty Selection
            # Easy button
            if 967 < mouse[0] < 1171 and 350 < mouse[1] < 415:
                if pressed[0] == 1:
                    difficulty = 0
            # Medium button
            if 967 < mouse[0] < 1171 and 430 < mouse[1] < 495:
                if pressed[0] == 1:
                    difficulty = 1
            # Hard button
            if 967 < mouse[0] < 1171 and 510 < mouse[1] < 575:
                if pressed[0] == 1:
                    difficulty = 2

            # Loading Dynamic Images
            com_diff.selection(difficulty)  # Update difficulty button
            window.blit(com_diff.image, com_diff.rect)
            selector.selection(choice)  # Update weapon selector
            window.blit(selector.image, selector.rect)
            button_play.hover(hovering)  # Update play button if hovering
            window.blit(button_play.image, button_play.rect)

        # Create player and com based on weapon and difficulty choices.
        player = Player(choice, 1, leftpos)
        com = Com(difficulty, rightpos)

        # Two Player
        if gamemode == 1:

            # Loading Static Images
            window.blit(bg_menu.image, bg_menu.rect)
            window.blit(image_multiplayer_menu.image, image_multiplayer_menu.rect)
            window.blit(image_menu_selectbuttons1.image, image_menu_selectbuttons1.rect)
            window.blit(image_menu_selectbuttons2.image, image_menu_selectbuttons2.rect)

            # Checking for Play Button hovering and press
            if 1020 < mouse[0] < 1250 and 40 < mouse[1] < 104:

                hovering = 1

                if pressed[0] == 1:
                    scene = 3
                    button.play()

            else:

                hovering = 0

            # Making Weapon Choices

            # Player 1

            # Checking if player 1 left selector arrow is pressed.
            if 114 < mouse[0] < 137 and 308 < mouse[1] < 348:
                if pressed[0] == 1 and choice1 > 0:
                    choice1 -= 1

            # Checking if player 1 right selector arrow is pressed.
            if 547 < mouse[0] < 565 and 308 < mouse[1] < 348:
                if pressed[0] == 1 and choice1 < 2:
                    choice1 += 1

            # Player 2

            # Checking if player 2 left selector arrow is pressed.
            if 716 < mouse[0] < 739 and 308 < mouse[1] < 348:
                if pressed[0] == 1 and choice2 > 0:
                    choice2 -= 1
            # Checking if player 2 right selector arrow is pressed.
            if 1150 < mouse[0] < 1169 and 308 < mouse[1] < 348:
                if pressed[0] == 1 and choice2 < 2:
                    choice2 += 1

            # Loading Dynamic Images (Play button, both ship selectors)
            button_play.hover(hovering)
            window.blit(button_play.image, button_play.rect)

            selector1.selection(choice1)
            window.blit(selector1.image, selector1.rect)

            selector2.selection(choice2)
            window.blit(selector2.image, selector2.rect)

        # Render Player Number Selection Button.
        window.blit(button_players.image, button_players.rect)

        # Create left and right players based on weapon choice.
        player_left = Player(choice1, 1, leftpos)
        player_right = Player(choice2, -1, rightpos)

    """ Scene 2 is the game in single player vs. a com of their selected difficulty. """
    if scene == 2:

        # Loading Static Images (Background).
        window.blit(bg_game.image, bg_game.rect)

        # Loading Dynamic Images (Health).
        font.render_to(window, (40, 40), str(player.health), white)
        font.render_to(window, (1160, 40), str(com.health), white)

        # Updates and moves each bullet in the list.
        for bullet in bullets:

            # Ensures that bullets are within the screen, if not, deletes them.
            if -30 < bullet.rect.left < 1250:

                # Allows for dynamic bullet velocity, and still moves bullet even if the game is over.
                bullet.rect.left += bullet.velocity

                # Makes bullets only do damage while the game is still going (excluding pause at the end).
                if game == 0:

                    # Calls on bullet.detect method, checks if it's hit box is colliding with target's.
                    if bullet.detect(bullet.target):
                        bullet.target.health -= bullet.damage

                        # Deletes bullet after it hits the target.
                        bullets.pop(bullets.index(bullet))

                # Excluded from if statement  so that it's still drawn even if it doesn't do damage.
                window.blit(bullet.image, bullet.rect)

            else:

                # Deletes bullet if not on screen.
                bullets.pop(bullets.index(bullet))

        """ All player controls are within an if statement that ends when a player reaches 0 health. This makes it so 
        that when a player loses, there is time for their ship to explode and for bullets to continue moving off the 
        screen. Just allows things that have already started to continue, removes player controls. """
        if game == 0:

            # Checks which keys are pressed, makes a list.
            keys = pygame.key.get_pressed()

            # Player Movement Keys.
            if keys[pygame.K_UP]:
                # .movespeed is used to move all characters, and allows for variable movespeed depending on ship choice.
                player.rect.top -= player.movespeed
            if keys[pygame.K_DOWN]:
                player.rect.top += player.movespeed

            # Bumps the player back down if they try to move above 40 pixels from the top.
            if player.rect.top <= 40:
                player.rect.top += player.movespeed

            # Just like the last, but for the bottom.
            elif player.rect.top >= 600:
                player.rect.top -= player.movespeed

            if keys[pygame.K_SPACE]:
                player.fire(com)

            # Com tries to fire every frame, .fire() method applies it's timed cool down.
            com.fire()

            """ Computer opponent movement. I originally did just random movement, but found that since it was picking 
            a random direction every frame, it was extremely stutter-y and didn't move much. I switched to a 'steps' 
            system, picking a number of steps when it reaches 0 and keeps moving in that direction for a while. """

            # If it reaches the top, move 20 steps down.
            if com.rect.top <= 40:
                move_steps = 20

            # If it reaches the bottom, move 20 steps up.
            elif com.rect.top >= 600:
                move_steps = -20

            # If positive steps, remove a step and move down by it's move speed.
            if move_steps > 1:
                move_steps -= 1
                com.rect.top += com.movespeed
            # If negative steps, add a step and move up by it's move speed.
            elif move_steps < 1:
                move_steps += 1
                com.rect.top -= com.movespeed
            # If it runs out of steps, generate more.
            else:
                move_steps = random.randint(-30, 30)

            # Ends game if either player reaches 0 health, also makes sure health can't go negative.
            if player.health <= 0:
                player.health = 0
                game = 1
            elif com.health <= 0:
                com.health = 0
                game = 1

        else:

            # If the game is no longer running, starts counting up frames. Gives time to see the explosion and allows
            # bullets to go off the end of the screen. Players can't move or shoot.
            pause += 1

            # After 100 frames of pausing, go to the game over screen.
            if pause == 100:
                scene = 4

        # Update Characters (only for explosion if 0 health left).
        player.update()
        com.update()

        # Render Characters.
        window.blit(player.image, player.rect)
        window.blit(com.image, com.rect)

    """ Scene 3 is the game in multi player against a real-life opponent. """
    if scene == 3:

        # Rendering Static Images (Background).
        window.blit(bg_game.image, bg_game.rect)

        # Rendering Dynamic Images (Health).
        font.render_to(window, (40, 40), str(player_left.health), white)
        font.render_to(window, (1160, 40), str(player_right.health), white)

        # Updates and moves each bullet in the list.
        for bullet in bullets:

            # Ensures that bullets are within the screen, if not, deletes them.
            if -30 < bullet.rect.left < 1250:

                # Allows for dynamic bullet velocity, and still moves bullet even if the game is over.
                bullet.rect.left += bullet.velocity

                # Makes bullets only do damage while the game is still going (excluding pause at the end).
                if game == 0:

                    # Calls on bullet.detect method, checks if it's hit box is colliding with target's.
                    if bullet.detect(bullet.target):
                        bullet.target.health -= bullet.damage

                        # Deletes bullet after it hits the target.
                        bullets.pop(bullets.index(bullet))

                # Excluded from if statement  so that it's still drawn even if it doesn't do damage.
                window.blit(bullet.image, bullet.rect)

            else:

                # Deletes bullet if not on screen.
                bullets.pop(bullets.index(bullet))

        """ All player controls are within an if statement that ends when a player reaches 0 health. This makes it so 
        that when a player loses, there is time for their ship to explode and for bullets to continue moving off the 
        screen. Just allows things that have already started to continue, removes player controls. """
        if game == 0:

            # Checks which keys are pressed, makes a list.
            keys = pygame.key.get_pressed()

            # Player 1 Movement Keys
            if keys[pygame.K_w]:
                player_left.rect.top -= player_left.movespeed

            if keys[pygame.K_s]:
                player_left.rect.top += player_left.movespeed

            # Bumps the player back down if they try to move above 40 pixels from the top.
            if player_left.rect.top <= 40:
                player_left.rect.top += player_left.movespeed

            # Just like the last, but for the bottom.
            elif player_left.rect.top >= 600:
                player_left.rect.top -= player_left.movespeed

            # Left player fire button, sets bullet target as player_right.
            if keys[pygame.K_SPACE]:
                player_left.fire(player_right)

            # Player 2 Movement Keys
            if keys[pygame.K_UP]:
                player_right.rect.top -= player_right.movespeed

            if keys[pygame.K_DOWN]:
                player_right.rect.top += player_right.movespeed

            # Bumps the player back down if they try to move above 40 pixels from the top.
            if player_right.rect.top <= 40:
                player_right.rect.top += player_right.movespeed

            # Just like the last, but for the bottom.
            elif player_right.rect.top >= 600:
                player_right.rect.top -= player_right.movespeed

            # Right player fire button, sets bullet target as player_left.
            if keys[pygame.K_RETURN]:
                player_right.fire(player_left)

            # Ends game if either player reaches 0 health, also makes sure health can't go negative.
            if player_left.health <= 0:
                player_left.health = 0
                game = 1
            elif player_right.health <= 0:
                player_right.health = 0
                game = 1

        else:

            # If the game is no longer running, starts counting up frames. Gives time to see the explosion and allows
            # bullets to go off the end of the screen. Players can't move or shoot.
            pause += 1

            # After 100 frames of pausing, go to the game over screen.
            if pause == 100:
                scene = 4

        # Update Characters (only for explosion if 0 health left).
        player_left.update()
        player_right.update()

        # Rendering Characters
        window.blit(player_left.image, player_left.rect)
        window.blit(player_right.image, player_right.rect)

    """ Scene 4 is the game over scene, allowing for playing again or quitting. """
    if scene == 4:

        # Rendering Static Images (Background, Game Over Text)
        window.blit(bg_menu.image, bg_menu.rect)
        window.blit(image_gameover.image, image_gameover.rect)

        # Checking for Play Again Button hovering and press
        if 416 < mouse[0] < 625 and 400 < mouse[1] < 464:

            hovering1 = 1

            # If left click is pressed, do stuff and play the sound.
            if pressed[0] == 1:

                # Resets game and selection screen options before the user sees them again.
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

                # Needed a special reset method for this toggleable button as it could be in either state.
                button_players.reset()

                # Plays button sound.
                button.play()

        else:

            hovering1 = 0

        # Checking for Quit Button hovering and press
        if 655 < mouse[0] < 864 and 400 < mouse[1] < 464:

            hovering2 = 1

            # If left click is pressed, do stuff and play the sound.
            if pressed[0] == 1:
                pygame.quit()
                button.play()

        else:

            hovering2 = 0

        # Tell Play Again button to update if hovering, then draw
        button_playagain.hover(hovering1)
        window.blit(button_playagain.image, button_playagain.rect)

        # Tell Quit button to update if hovering, then draw
        button_quit.hover(hovering2)
        window.blit(button_quit.image, button_quit.rect)

    # Update screen, 60fps
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
