import csv
import hashlib

def generate_hash(password: str) -> int:
    """Genera un hash entero desde un string usando SHA-256."""
    h = hashlib.sha256(password.encode()).hexdigest()
    return int(h[:8], 16)  # usamos solo 8 dígitos para obtener un int manejable

def generate_users_csv(filename):
    print("=== Generador de archivo CSV de jugadores ===")
    print("Cuando quieras terminar, deja el nombre vacío.\n")

    users = []

    while True:
        nombre = input("Nombre del jugador: ").strip()
        if nombre == "":
            break

        password = input("Contraseña del jugador: ").strip()
        nivel_exp = input("Nivel de experiencia (entero): ").strip()

        try:
            nivel_exp = int(nivel_exp)
        except ValueError:
            print("Nivel inválido. Pon un número entero.\n")
            continue

        hashed = generate_hash(password)

        users.append([nombre, hashed, nivel_exp])
        print(f"✔ Usuario '{nombre}' agregado con ID hash {hashed}\n")

    # Guardar CSV
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "ID", "Nivel EXP"])
        writer.writerows(users)

    print(f"\n=== Archivo '{filename}' generado correctamente ===")

if __name__ == "__main__":
    generate_users_csv("users.csv")  # cámbialo si quieres otra ruta
