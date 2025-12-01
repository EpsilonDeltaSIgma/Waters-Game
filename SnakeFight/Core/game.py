import pygame
import time
from .utils import Snake, SnakeAI, FoodManager, Button, SnakeNode

CELL_SIZE = 35
GRID_W = 23
GRID_H = 12
TICK_RATE = 10

# ----- Direcciones -----
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


# ----- Helpers -----
def next_pos(pos, direction):
    x, y = pos
    dx, dy = direction
    return (x + dx, y + dy)


def is_safe(pos, snake_player, snake_ai):
    x, y = pos

    if x < 0 or x >= GRID_W or y < 0 or y >= GRID_H:
        return False

    if pos in snake_player.get_positions():
        return False

    if pos in snake_ai.get_positions():
        return False

    return True


# ----- Árbol Binario de Decisión -----
def ai_choose_direction(ai_snake, food_pos, snake_player):
    hx, hy = ai_snake.head.x, ai_snake.head.y
    fx, fy = food_pos

    dx = fx - hx
    dy = fy - hy

    # Capa 1: dirección ideal
    if abs(dx) >= abs(dy):
        primary = RIGHT if dx > 0 else LEFT
    else:
        primary = DOWN if dy > 0 else UP

    # Resto de direcciones
    directions = [primary] + [d for d in DIRECTIONS if d != primary]

    # Capa 2: seguridad
    for d in directions:
        if is_safe(next_pos((hx, hy), d), snake_player, ai_snake):
            return d

    return primary


# ----- Gráficos -----
def draw_grid(screen):
    for x in range(0, GRID_W * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, GRID_H * CELL_SIZE))
    for y in range(0, GRID_H * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (GRID_W * CELL_SIZE, y))


def draw_cell(screen, pos, color):
    x, y = pos
    pygame.draw.rect(
        screen,
        color,
        pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    )


# =================================================================
#                         LOOP PRINCIPAL
# =================================================================
def run_game(screen):

    punct = 0
    inicio = time.time()
    clock = pygame.time.Clock()

    snake = Snake(10, 10)
    ai     = SnakeAI(5, 5)

    foods = FoodManager(GRID_W, GRID_H, count=1)

    while True:
        ahora = time.time()
        Puntuacion = Button(150, 450, 200, 60, f"Puntuacion: {punct}")
        Tiempo     = Button(400, 450, 200, 60, f"Tiempo: {int(ahora-inicio)}")

        # ---- INPUT HUMANO ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.set_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    snake.set_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    snake.set_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction(1, 0)

        # ---- IA DECIDE ----
        food = foods.get_positions()[0]
        d = ai_choose_direction(ai, food, snake)
        ai.set_direction(d[0], d[1])

        # ---- MOVER ----
        snake.move()
        ai.move()

        # POSICIONES HEADS
        hx, hy   = snake.head.x, snake.head.y
        hx2, hy2 = ai.head.x, ai.head.y

        # ============================================================
        #                     COLISIONES HUMANO
        # ============================================================

        # Bordes
        if hx < 0 or hx >= GRID_W or hy < 0 or hy >= GRID_H:
            return "menu"

        # Consigo mismo
        if snake.collides_with_self():
            return "menu"

        # CONTRA IA (jugador muere)
        if (hx, hy) in ai.get_positions():
            print("Chocaste contra la IA.")
            return "menu"

        # ============================================================
        #                     COLISIONES IA
        # ============================================================

        # IA bordes
        if hx2 < 0 or hx2 >= GRID_W or hy2 < 0 or hy2 >= GRID_H:
            ai = SnakeAI(5, 5)

        # IA contra sí misma
        elif ai.collides_with_self():
            ai = SnakeAI(5, 5)

        # IA contra jugador (IA muere)
        elif (hx2, hy2) in snake.get_positions():
            ai = SnakeAI(5, 5)

        # ============================================================
        #                         COMER
        # ============================================================

        # Comer jugador
        if foods.remove_at((hx, hy)):
            snake.grow()
            punct += 1

        # Comer IA
        if foods.remove_at((hx2, hy2)):
            ai.grow()

        # ============================================================
        #                         RENDER
        # ============================================================
        screen.fill((20,20,20))
        draw_grid(screen)

        # Comida
        for fx, fy in foods.get_positions():
            draw_cell(screen, (fx, fy), (255,0,0))

        # Jugador verde
        for pos in snake.get_positions():
            draw_cell(screen, pos, (0,255,0))

        # IA azul
        for pos in ai.get_positions():
            draw_cell(screen, pos, (0,0,255))

        Puntuacion.draw(screen)
        Tiempo.draw(screen)

        pygame.display.flip()
        clock.tick(TICK_RATE)
