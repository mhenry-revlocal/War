import pygame
import sys
from framework.gamecontroller import GameController
from framework.utilities import wrapline
        
pygame.init()
pygame.mixer.init()

display_width = 500
display_height = 500

game_display = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
game_display.fill([0, 255, 0])
game_title = 'War'
pygame.display.set_caption(game_title)
pygame.display.set_icon(pygame.image.load('images/Cards/cardJoker.png'))
clock = pygame.time.Clock()

quit = False
game_controller = GameController(display_width, display_height)
game_controller.sprites = []

while not quit:
    events = pygame.event.get()
    enter_clicked = False
    for event in events:
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                enter_clicked = True
    
    game_controller.act(events)
    
    for sprite in game_controller.sprites:
        sprite.act(display_height, display_width, game_controller, events)
    for sprite in game_controller.sprites:
        sprite.draw(game_display, display_height, display_width, game_controller)
    game_controller.draw(game_display, display_height, display_width)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
    
