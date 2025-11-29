import pygame
import random
import string
import math

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


class SnakeNode:
    def __init__(self, position, next = None):
        self.position = position
        self.next = next


class Snake:
    def __init__(self, init_x, init_y):
        head = SnakeNode(init_x, init_y)
        self.head = head
        self.tail = head
        self.length = 1

        self.dx = 1
        self.dy = 0

    def set_direction(self, dx, dy):   # Cambiar la dirección (evitando reversa ilegal)
        # Evita girar 180 grados
        if (dx == -self.dx and dx != 0) or (dy == -self.dy and dy != 0):
            return
        self.dx = dx
        self.dy = dy

    def move(self):   # Mover la serpiente: insertar nueva cabeza y borrar cola
        new_x = self.head.x + self.dx
        new_y = self.head.y + self.dy

        # Crear nueva cabeza
        new_head = SnakeNode(new_x, new_y)
        new_head.next = self.head
        self.head = new_head
        self.length += 1

        # Remover cola
        self._remove_tail()

    def grow(self):   # Comer: agregar cabeza sin borrar cola
        new_x = self.head.x + self.dx
        new_y = self.head.y + self.dy

        # Nueva cabeza sin borrar cola
        new_head = SnakeNode(new_x, new_y)
        new_head.next = self.head
        self.head = new_head
        self.length += 1

    def _remove_tail(self):   # Remover cola recorriendo la lista (O(n))
        if self.length == 1:
            return

        cur = self.head
        # Buscar penúltimo nodo
        while cur.next != self.tail:
            cur = cur.next

        cur.next = None
        self.tail = cur
        self.length -= 1

    def get_positions(self):   # Obtener lista de posiciones (útil para dibujar)
        positions = []
        cur = self.head
        while cur:
            positions.append((cur.x, cur.y))
            cur = cur.next
        return positions

    def collides_with_self(self):   # Detección de colisión consigo misma
        head_x, head_y = self.head.x, self.head.y
        cur = self.head.next
        while cur:
            if cur.x == head_x and cur.y == head_y:
                return True
            cur = cur.next
        return False


class Food:
    """
    Representa un alimento en coordenadas de celda (x, y).
    board_w, board_h: dimensiones en celdas.
    """
    def __init__(self, board_w, board_h, x=None, y=None):
        self.board_w = board_w
        self.board_h = board_h
        if x is not None and y is not None:
            self.x = x
            self.y = y
        else:
            self.x = None
            self.y = None
            self.respawn()

    def respawn(self, forbidden_positions=None):
        """
        forbidden_positions: iterable o set de (x,y) que NO pueden usarse.
        Se intenta con retry si el tablero tiene muchas celdas libres.
        Si el tablero está casi lleno, se construye la lista de libres y se elige una.
        """
        if forbidden_positions is None:
            forbidden = set()
        else:
            forbidden = set(forbidden_positions)

        total_cells = self.board_w * self.board_h
        free_estimate = total_cells - len(forbidden)

        # Si quedan muchas posiciones libres: retry sampling (rápido)
        if free_estimate > total_cells * 0.3:
            # intentos limitados para evitar loop infinito en el peor caso
            for _ in range(200):
                nx = random.randint(0, self.board_w - 1)
                ny = random.randint(0, self.board_h - 1)
                if (nx, ny) not in forbidden:
                    self.x, self.y = nx, ny
                    return
        # Método seguro: construir la lista de posiciones libres y elegir una
        free_positions = [
            (x, y)
            for x in range(self.board_w)
            for y in range(self.board_h)
            if (x, y) not in forbidden
        ]
        if not free_positions:
            # No hay donde poner comida (tablero lleno). Marcar None para indicar esto.
            self.x = None
            self.y = None
            return
        self.x, self.y = random.choice(free_positions)

    def get_position(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"Food({self.x},{self.y})" if self.x is not None else "Food(None)"


class FoodManager:
    """
    Maneja varios alimentos en el tablero.
    Mantiene sets para búsquedas rápidas y evita solapamientos.
    """
    def __init__(self, board_w, board_h, count=1):
        self.board_w = board_w
        self.board_h = board_h
        self.foods = []
        self.positions = set()
        self.count = max(0, int(count))
        self._ensure_count()

    def _ensure_count(self):
        while len(self.foods) < self.count:
            f = Food(self.board_w, self.board_h)
            if (f.x, f.y) not in self.positions:
                self.foods.append(f)
                if f.x is not None:
                    self.positions.add((f.x, f.y))
            else:
                # si colisiona, intenta respawnear con posiciones prohibidas actuales
                f.respawn(forbidden_positions=self.positions)
                if f.x is not None:
                    self.foods.append(f)
                    self.positions.add((f.x, f.y))
                else:
                    break

    def respawn_one(self, index, forbidden_positions=None):
        if index < 0 or index >= len(self.foods):
            return
        # quitar la posición vieja
        pos_old = self.foods[index].get_position()
        if pos_old in self.positions:
            self.positions.discard(pos_old)

        # combinar posiciones prohibidas con las actuales (evitar solaparse)
        forbidden = set(self.positions)
        if forbidden_positions:
            forbidden.update(forbidden_positions)

        self.foods[index].respawn(forbidden_positions=forbidden)
        newpos = self.foods[index].get_position()
        if newpos is not None:
            self.positions.add(newpos)

    def respawn_all(self, forbidden_positions=None):
        forbidden = set(forbidden_positions) if forbidden_positions else set()
        # Reset y respawn cuidando no solaparse
        self.foods = []
        self.positions = set()
        for _ in range(self.count):
            f = Food(self.board_w, self.board_h)
            f.respawn(forbidden_positions=forbidden.union(self.positions))
            if f.x is None:
                break
            self.foods.append(f)
            self.positions.add((f.x, f.y))

    def get_positions(self):
        return [f.get_position() for f in self.foods if f.get_position() is not None]

    def remove_at(self, pos):
        """
        Remueve comida en pos (x,y) si existe y devuelve True; útil cuando una serpiente come.
        """
        for i, f in enumerate(self.foods):
            if f.get_position() == pos:
                self.positions.discard(pos)
                self.respawn_one(i)
                return True
        return False



class TreeNode:
    """
    Nodo abstracto de un árbol binario.
    value: cualquier dato (en tu caso, información del jugador)
    left, right: otros TreeNode o None
    """
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"TreeNode({self.value})"


class BinaryTree:
    """
    Árbol binario abstracto: no asume ordenamientos (no es BST a menos que lo extiendas).
    Sirve para representar emparejamientos arbitrarios, niveles, etc.
    """
    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root is None

    def set_root(self, value):
        """Define el nodo raíz del árbol."""
        self.root = TreeNode(value)
        return self.root

    def insert_left(self, parent: TreeNode, value):
        """
        Inserta un nuevo nodo como hijo izquierdo de 'parent'.
        """
        if parent.left is not None:
            raise ValueError("El hijo izquierdo ya existe.")
        parent.left = TreeNode(value)
        return parent.left

    def insert_right(self, parent: TreeNode, value):
        """
        Inserta un nuevo nodo como hijo derecho de 'parent'.
        """
        if parent.right is not None:
            raise ValueError("El hijo derecho ya existe.")
        parent.right = TreeNode(value)
        return parent.right

    # ------------------- Traversals -------------------

    def preorder(self, node=None, result=None):
        """
        Recorrido raíz-izquierda-derecha.
        """
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node:
            result.append(node.value)
            self.preorder(node.left, result)
            self.preorder(node.right, result)
        return result

    def inorder(self, node=None, result=None):
        """
        Recorrido izquierda-raíz-derecha.
        """
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node:
            self.inorder(node.left, result)
            result.append(node.value)
            self.inorder(node.right, result)
        return result

    def postorder(self, node=None, result=None):
        """
        Recorrido izquierda-derecha-raíz.
        """
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node:
            self.postorder(node.left, result)
            self.postorder(node.right, result)
            result.append(node.value)
        return result

    # ------------------- Nivel específico -------------------

    def find_level(self, level):
        """
        Retorna una lista con los valores de todos los nodos en el nivel 'level'.
        Nivel 0 = raíz.
        """
        if self.root is None:
            return []

        queue = [(self.root, 0)]
        result = []

        while queue:
            node, lvl = queue.pop(0)
            if lvl == level:
                result.append(node.value)
            if lvl > level:
                break
            if node.left:
                queue.append((node.left, lvl + 1))
            if node.right:
                queue.append((node.right, lvl + 1))
        return result

    # ------------------- Altura -------------------

    def height(self, node=None):
        """
        Retorna la altura del árbol.
        Altura = nivel máximo (número de niveles - 1).
        """
        if node is None:
            node = self.root
        if node is None:
            return -1
        return 1 + max(self.height(node.left), self.height(node.right))



def string_to_numbers(s: str):
    """
    Convierte un string a una lista de números,
    asignando a cada letra un número 'pseudo-aleatorio' consistente.

    - Misma letra → mismo número.
    - Diferentes letras → números distintos (alta probabilidad).
    - No es un mapeo trivial ni secuencial.
    """

    # Inicializamos generador con una semilla fija para consistencia.
    rng = random.Random(829347)  # semilla arbitraria

    # Creamos un mapeo aleatorio letra → número
    letters = string.ascii_lowercase
    assigned = {}

    # Mezclamos el alfabeto para romper patrones
    shuffled = list(letters)
    rng.shuffle(shuffled)

    # A cada letra le asignamos un número aleatorio grande
    for letter in shuffled:
        assigned[letter] = rng.randint(100, 9999)

    # Convertimos el string
    output = []
    for ch in s.lower():
        if ch in assigned:
            output.append(assigned[ch])
        else:
            # Para caracteres no alfabéticos asignamos -1 (o lo que prefieras)
            output.append(-1)

    return output


def sum_exp(values):
    """
    Recibe una lista de números y devuelve la suma de sus exponentiales.
    Es decir:  e^{v1} + e^{v2} + ... + e^{vn}
    """
    total = 0.0
    for x in values:
        total += math.exp(x)
    return total