import pygame
import sys
from Core.menu import run_menu
from Core.game import run_game
from Core.config import run_config
from Core.utils import UserRegistryCSV
import sys, os

pygame.init()

FONT = pygame.font.Font(None, 36)

# Detectar ruta PyInstaller
if hasattr(sys, "_MEIPASS"):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

# *** IMPORTANTE ***
# Crear ventana ANTES de cargar imágenes
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Login - Snake en casa")

# CARGAR IMAGEN YA CON DISPLAY EXISTENTE
img_path = os.path.join(base_path, "Assets/Fonds/topS.png")
secret_default = pygame.image.load(img_path).convert_alpha()
secret_default = pygame.transform.scale(secret_default, (350, 250))

registry = UserRegistryCSV("Data/users.csv")


def draw_text(surface, text, pos, color=(255,255,255)):
    img = FONT.render(text, True, color)
    surface.blit(img, pos)


def login_screen():
    username = ""
    password = ""
    active_field = "user"

    # Cargar logo aquí también por seguridad
    img_path = os.path.join(base_path, "Assets/Fonds/topS.png")
    secret = pygame.image.load(img_path).convert_alpha()
    secret = pygame.transform.scale(secret, (350, 250))

    while True:
        screen.fill((20, 20, 20))

        pygame.draw.rect(screen, (50,50,50), (50, 90, 500, 30))
        pygame.draw.rect(screen, (50,50,50), (50, 190, 500, 30))

        draw_text(screen, "Nombre de usuario:", (50, 50))
        draw_text(screen, username, (55, 95))
        draw_text(screen, "Contraseña:", (50, 150))
        draw_text(screen, "*" * len(password), (55, 195))
        draw_text(screen, "Presiona ENTER para acceder", (50, 300), (180,180,180))

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
                    username = username.strip()
                    password = password.strip()
                    if registry.verify_user(username, password):
                        return username
                    else:
                        username = ""
                        password = ""
                        active_field = "user"
                        print("Acceso denegado")

        # Dibujar logo
        logo_x = (screen.get_width() - secret.get_width()) // 2
        screen.blit(secret, (logo_x, 350))

        pygame.display.flip()


# ==== LOGIN ====
user_logged = login_screen()
print("Acceso concedido:", user_logged)

# ==== MENU, GAME, CONFIG ====
state = "menu"
running = True

while running:
    if state == "menu":
        state = run_menu(screen)
    elif state == "game":
        state = run_game(screen)
    elif state == "config":
        state = run_config(screen)
    elif state == "quit":
        running = False

pygame.quit()
