import pygame
import time
from .utils import Snake, FoodManager, Button

CELL_SIZE = 35
GRID_W = 23
GRID_H = 12
TICK_RATE = 10



def draw_grid(surface):
    for x in range(0, GRID_W * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(surface, (40, 40, 40), (x, 0), (x, GRID_H * CELL_SIZE))
    for y in range(0, GRID_H * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(surface, (40, 40, 40), (0, y), (GRID_W * CELL_SIZE, y))


def draw_cell(surface, pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)


def run_game(screen):
    punct = 0
    inicio_tiempo = time.time()
    
    clock = pygame.time.Clock()

    # Crear la serpiente
    snake = Snake(10, 10)

    # Comida
    foods = FoodManager(GRID_W, GRID_H, count=1)

    while True:
        ahora_tiempo = time.time()
        # INPUT de dirección
        Puntuacion = Button(150, 450, 200, 60, f"Puntuacion: {punct}")
        temporizador = Button(400, 450, 200, 60, f"Tiempo: {int(ahora_tiempo-inicio_tiempo)}")

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

        # Mover
        snake.move()

        # Colisiones con bordes
        hx, hy = snake.head.x, snake.head.y
        if hx < 0 or hx >= GRID_W or hy < 0 or hy >= GRID_H:
            print("Chocaste con la pared.")
            punct = 0
            return "menu"
        

        # Colisión consigo misma
        if snake.collides_with_self():
            print("Chocaste contigo mismo.")
            punct = 0
            return "menu"
            

        # Comer
        head_pos = (hx, hy)
        if foods.remove_at(head_pos):
            snake.grow()
            punct += 1

        # RENDER
        screen.fill((20, 20, 20))
        draw_grid(screen)

        # Dibujar comida
        for fx, fy in foods.get_positions():
            draw_cell(screen, (fx, fy), (255, 0, 0))

        # Dibujar serpiente
        for (sx, sy) in snake.get_positions():
            draw_cell(screen, (sx, sy), (0, 255, 0))
        
        Puntuacion.draw(screen)
        temporizador.draw(screen)

        pygame.display.flip()
        clock.tick(TICK_RATE)

