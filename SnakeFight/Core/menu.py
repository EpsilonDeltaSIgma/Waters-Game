import pygame
import sys
from .utils import Button


def draw_gradient_background(surface, top_color, bottom_color):
    width, height = surface.get_size()
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))


def draw_button(surface, text, rect, font, hover=False):
    """
    Dibuja un botón; recibe la fuente en el argumento `font`.
    """
    x, y, w, h = rect
    color_idle = (40, 120, 255)
    color_hover = (80, 180, 255)

    color = color_hover if hover else color_idle

    # fondo del botón
    pygame.draw.rect(surface, color, rect, border_radius=18)
    # borde brillante
    pygame.draw.rect(surface, (200, 240, 255), rect, 3, border_radius=18)

    # label usando la fuente pasada
    label = font.render(text, True, (230, 240, 255))
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))
    surface.blit(label, label_rect)


def run_menu(screen):

    # Inicializamos fuentes AQUÍ (después de pygame.init())
    TITLE_FONT = pygame.font.Font(None, 80)
    BUTTON_FONT = pygame.font.Font(None, 40)

    # Intento cargar logo (cambia la ruta/nombre si es distinto)
    try:
        logo = pygame.image.load("assets/fonds/Logo.png").convert_alpha()
        logo = pygame.transform.scale(logo, (350, 250))
    except Exception as e:
        logo = None
        print("⚠ No se pudo cargar assets/fonds/logo.png:", e)

    clock = pygame.time.Clock()

    # Botones (posiciones)
    play_rect  = pygame.Rect(80, 380, 260, 70)   # izquierda
    cfg_rect   = pygame.Rect(460, 380, 260, 70)  # derecha
    quit_rect  = pygame.Rect(260, 500, 280, 70)  # centro abajo

    while True:
        mouse_pos = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        # Fondo futurista azul
        draw_gradient_background(screen, (10,15,40), (0,60,140))

        # Logo/título en la parte superior
        if logo:
            # Centrar el logo arriba
            logo_x = (screen.get_width() - logo.get_width()) // 2
            screen.blit(logo, (logo_x, 40))

        # Título futurista debajo del logo
        title_surf = TITLE_FONT.render("SNAKE FIGHT", True, (200,220,255))
        title_rect = title_surf.get_rect(center=(screen.get_width()//2, 320))
        screen.blit(title_surf, title_rect)

        # Hover detection
        hover_play = play_rect.collidepoint(mouse_pos)
        hover_cfg = cfg_rect.collidepoint(mouse_pos)
        hover_quit = quit_rect.collidepoint(mouse_pos)

        # Dibujar botones PASANDO la fuente
        draw_button(screen, "Jugar", play_rect, font=BUTTON_FONT, hover=hover_play)
        draw_button(screen, "Configuración", cfg_rect, font=BUTTON_FONT, hover=hover_cfg)
        draw_button(screen, "Salir", quit_rect, font=BUTTON_FONT, hover=hover_quit)

        # Click handling
        if click:
            if hover_play:
                return "game"
            if hover_cfg:
                return "config"
            if hover_quit:
                return "quit"

        pygame.display.update()
        clock.tick(60)