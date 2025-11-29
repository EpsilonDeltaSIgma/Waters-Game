import pygame
from . import utils  # Variables y clases


def run_config(screen):
    clock = pygame.time.Clock() #FPS

    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
        screen.fill((20, 20, 20))
        pygame.display.flip() #actualiza frame
        clock.tick(60)