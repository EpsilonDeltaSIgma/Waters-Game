#importamos funciones
import pygame
from Core.menu import run_menu
from Core.game import run_game
from Core.config import run_config
from .utils import Button


pygame.init()
screen = pygame.display.set_mode((800,600))

state = "menu"
running = True

while(running):

    if(state == "menu"):
        state = run_menu(screen)

    elif(state == "game"):
        state = run_game(screen)

    elif(state == "config"):
        state = run_config(screen)

    elif(state == "quit"):
        running = False


pygame.quit()



