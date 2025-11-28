import pygame
import utils  # variables y clases

def run_menu(screen):
    clock = pygame.time.Clock()

    # Instanciar el botón correctamente
    button_play = Button(100, 100, 200, 60, "Jugar")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.is_clicked(event.pos):
                    print("¡Botón Jugar presionado!")

        # Orden correcto del draw
        screen.fill((20, 20, 20))
        button_play.draw(screen)

        pygame.display.flip()
        clock.tick(60)
