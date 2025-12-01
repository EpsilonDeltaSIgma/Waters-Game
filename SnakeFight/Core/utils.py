import pygame
import random
import hashlib
import csv
import sys
import os

# ---------------- BUTTON -----------------

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = (200, 200, 200)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 36)
        txt = font.render(self.text, True, (0,0,0))
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# ----------------- SNAKE NODES -----------------

class SnakeNode:
    def __init__(self, x, y, next=None):
        self.x = x
        self.y = y
        self.next = next


# ----------------- SNAKE NORMAL -----------------

class Snake:
    def __init__(self, init_x, init_y):
        head = SnakeNode(init_x, init_y)
        self.head = head
        self.tail = head
        self.length = 1

        self.dx = 1
        self.dy = 0

    def set_direction(self, dx, dy):
        # Evitar reversa
        if (dx == -self.dx and dx != 0) or (dy == -self.dy and dy != 0):
            return
        self.dx = dx
        self.dy = dy

    def move(self):
        new_x = self.head.x + self.dx
        new_y = self.head.y + self.dy

        new_head = SnakeNode(new_x, new_y, self.head)
        self.head = new_head
        self.length += 1

        self._remove_tail()

    def grow(self):
        new_x = self.head.x + self.dx
        new_y = self.head.y + self.dy
        new_head = SnakeNode(new_x, new_y, self.head)
        self.head = new_head
        self.length += 1

    def _remove_tail(self):
        if self.length <= 1:
            return

        cur = self.head
        while cur.next != self.tail:
            cur = cur.next

        cur.next = None
        self.tail = cur
        self.length -= 1

    def get_positions(self):
        result = []
        cur = self.head
        while cur:
            result.append((cur.x, cur.y))
            cur = cur.next
        return result

    def collides_with_self(self):
        hx, hy = self.head.x, self.head.y
        cur = self.head.next
        while cur:
            if cur.x == hx and cur.y == hy:
                return True
            cur = cur.next
        return False


# ----------------- IA: SERPIENTE AZUL -----------------

class SnakeAI(Snake):
    def __init__(self, x, y):
        super().__init__(x, y)

    def reset(self, x, y):
        super().__init__(x, y)


# ----------------- FOOD SYSTEM -----------------

class Food:
    def __init__(self, board_w, board_h, x=None, y=None):
        self.board_w = board_w
        self.board_h = board_h

        if x is not None and y is not None:
            self.x = x
            self.y = y
        else:
            self.respawn()

    def respawn(self, forbidden_positions=None):
        forbidden_positions = set(forbidden_positions or [])

        while True:
            nx = random.randint(0, self.board_w - 1)
            ny = random.randint(0, self.board_h - 1)
            if (nx, ny) not in forbidden_positions:
                self.x, self.y = nx, ny
                return

    def get_position(self):
        return (self.x, self.y)


class FoodManager:
    def __init__(self, board_w, board_h, count=1):
        self.board_w = board_w
        self.board_h = board_h
        self.count = count
        self.foods = []
        self.positions = set()

        for _ in range(count):
            f = Food(board_w, board_h)
            self.foods.append(f)
            self.positions.add(f.get_position())

    def respawn_one(self, index, forbidden_positions=None):
        old_pos = self.foods[index].get_position()
        if old_pos in self.positions:
            self.positions.remove(old_pos)

        self.foods[index].respawn(forbidden_positions)
        self.positions.add(self.foods[index].get_position())

    def get_positions(self):
        return [food.get_position() for food in self.foods]

    def remove_at(self, pos):
        for i, f in enumerate(self.foods):
            if f.get_position() == pos:
                self.respawn_one(i)
                return True
        return False


# ----------------- USERS / HASH SYSTEM -----------------

class UserRegistryCSV:
    def __init__(self, csv_path):
        """
        Inicializa el registro de usuarios.
        Soporta rutas empaquetadas con PyInstaller.
        """

        # Detectar si el programa está corriendo dentro de un .exe (PyInstaller)
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        # Ruta ABSOLUTA al archivo CSV
        self.csv_path = os.path.join(base_path, csv_path)

        self.users = []
        self.load_users()

    # ------------------------------------------------------

    def load_users(self):
        """
        Carga usuarios desde el archivo CSV en self.users.
        """

        try:
            with open(self.csv_path, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Convertir columnas numéricas
                    try:
                        row["ID"] = int(row["ID"])
                    except:
                        pass

                    try:
                        row["Nivel EXP"] = int(row.get("Nivel EXP", 0))
                    except:
                        row["Nivel EXP"] = 0

                    self.users.append(row)

        except FileNotFoundError:
            print(f"⚠ ERROR: No se encontró el archivo CSV: {self.csv_path}")
        except Exception as e:
            print("⚠ Error cargando usuarios:", e)

    # ------------------------------------------------------

    def generate_hash(self, password: str) -> int:
        """
        Devuelve hash entero (8 hex = 32 bits) basado en SHA-256.
        """
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return int(hashed[:8], 16)

    # ------------------------------------------------------

    def verify_user(self, username: str, password: str) -> bool:
        """
        Verifica si username + contraseña son correctos.
        """

        username = username.strip()
        password = password.strip()

        provided_hash = self.generate_hash(password)

        for user in self.users:
            if user["Nombre"].strip() == username:
                return str(user["ID"]).strip() == str(provided_hash)

        return False

    # ------------------------------------------------------

    def get_user_experience(self, username: str):
        """
        Regresa nivel de experiencia del usuario (si existe).
        """
        for user in self.users:
            if user["Nombre"].strip() == username:
                return user.get("Nivel EXP", 0)

        return None

    def get_user_experience(self, username: str):
        for user in self.users:
            if user["Nombre"] == username:
                return user["Nivel EXP"]
        return None
