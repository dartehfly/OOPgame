import pygame
pygame.init()

window = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Laser Pong")

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.quit():
            done = True

pygame.quit()