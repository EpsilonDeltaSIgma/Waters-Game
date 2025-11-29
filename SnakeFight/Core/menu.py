import pygame
from .utils import Button  # variables y clases

def run_menu(screen):
    clock = pygame.time.Clock()

    # Instanciar el botón correctamente
    button_play = Button(100, 100, 200, 60, "Jugar")
    button_play2 = Button(100, 300, 200, 100, "Configurar")


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.is_clicked(event.pos):
                    return "game"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play2.is_clicked(event.pos):
                    print("¡Botón Configurar presionado!")

        # Orden correcto del draw
        screen.fill((20, 20, 20))
        button_play.draw(screen)
        button_play2.draw(screen)

        pygame.display.flip()
        clock.tick(60)
