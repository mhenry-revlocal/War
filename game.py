import pygame
import sys
from framework.gamecontroller import GameController
        
pygame.init()
pygame.mixer.init()

display_width = 500
display_height = 500

game_display = pygame.display.set_mode((display_width, display_height))
game_display.fill([0, 255, 0])

game_title = 'War'
pygame.display.set_caption(game_title)

pygame.display.set_icon(pygame.image.load('images/Cards/cardJoker.png'))

clock = pygame.time.Clock()

game_controller = GameController(game_display, display_width, display_height)

while not game_controller.quit:
    game_controller.act()
    game_controller.draw()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
    
