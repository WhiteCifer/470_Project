import pygame
from Controller import GameController

pygame.init()
controller = GameController()

# main game loop
while controller.window.running:
    controller.handle_input()
    controller.view.update_display()
    # other game loop code here

