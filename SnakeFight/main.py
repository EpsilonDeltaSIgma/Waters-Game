#importamos funciones
import pygame
import sys
from Core.menu import run_menu
from Core.game import run_game
from Core.config import run_config
from Core.utils import UserRegistryCSV


pygame.init()


FONT = pygame.font.Font(None, 36)
SCREEN = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Login - Snake en casa")


def draw_text(surface, text, pos, color=(255,255,255)):
    img = FONT.render(text, True, color)
    surface.blit(img, pos)

def login_screen():
    username = ""
    password = ""
    active_field = None  # "user" or "pass"

    while True:
        SCREEN.fill((20, 20, 20))

        draw_text(SCREEN, "Nombre de usuario:", (50, 50))
        draw_text(SCREEN, username, (50, 90))

        draw_text(SCREEN, "Contraseña:", (50, 150))
        draw_text(SCREEN, "*" * len(password), (50, 190))

        draw_text(SCREEN, "Presiona ENTER para acceder", (50, 300), (180,180,180))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 50 <= x <= 550 and 90 <= y <= 120:
                    active_field = "user"
                elif 50 <= x <= 550 and 190 <= y <= 220:
                    active_field = "pass"

            if event.type == pygame.KEYDOWN:
                if active_field == "user":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

                elif active_field == "pass":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

                if event.key == pygame.K_RETURN:
                    if registry.verify_user(username, password):
                        return username  # Login exitoso
                    else:
                        password = ""
                        username = ""
                        active_field = None
                        print("Acceso denegado")  # o texto en pantalla

        pygame.display.flip()


registry = UserRegistryCSV("players.csv")

username = login_screen()
if username is None:
    print("Cerrando el juego")
    pygame.quit()
    sys.exit()
print(f"Bienvenido, {username}!")


screen = pygame.display.set_mode((800,600))

registry = UserRegistryCSV("Data/users.csv")
print(registry.generate_hash("contraseña123"))

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