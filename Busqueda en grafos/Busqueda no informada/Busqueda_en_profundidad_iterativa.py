# busqueda en profundidad Iterativa
# esta busqueda es como una version mas lista de la profundidad limitada
# 1 primero intento con limite 1
# 2 si no lo encuentro, intento con limite 2
# 3 si no, intento con limite 3
# y asi voy subiendo el limite poco a poco
# esto sirve porque
# - no me voy super profundo desde el inicio (eso puede ser infinito)
# - pero tarde o temprano llego al objetivo si es alcanzable

import csv
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "data" / "rutas.csv"

def cargar_grafo_csv(ruta_csv: Path, bidireccional: bool = True):
    grafo = {}
    with ruta_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            o = row["origen"].strip()
            d = row["destino"].strip()
            grafo.setdefault(o, []).append(d)
            grafo.setdefault(d, [])
            if bidireccional:
                grafo.setdefault(d, []).append(o)
    return grafo

def dfs_limitada(grafo, actual, objetivo, limite, camino=None):
    # esta funcion es igual que en el tema anterior (profundidad limitada)
    # intenta llegar al objetivo sin pasar el limite

    if camino is None:
        camino = [actual]  # camino que llevo hasta ahorita

    # si ya llegue al objetivo, regreso el camino
    if actual == objetivo:
        return camino

    # si ya no me queda profundidad permitida, paro aqui
    if limite == 0:
        return None

    # pruebo cada vecino desde el lugar actual
    for vecino in grafo.get(actual, []):
        if vecino in camino:
            continue
        # llamada recursiva bajando el limite
        resultado = dfs_limitada(
            grafo,
            vecino,
            objetivo,
            limite - 1,        # bajo uno al limite
            camino + [vecino]  # agrego el vecino al camino
        )

        # si encontre camino valido lo regreso
        if resultado is not None:
            return resultado

    # si ninguno funciono, regreso none
    return None

def profundidad_iterativa(grafo, inicio, objetivo, limite_max):
    # esta funcion hace la parte "iterativa"
    # intenta encontrar camino con limite 1
    # luego con limite 2
    # luego con limite 3
    # y sigue asi hasta limite_max
    # si lo encuentra antes de llegar al limite max, se detiene

    for limite in range(1, limite_max + 1):
        # intento con este limite
        camino = dfs_limitada(grafo, inicio, objetivo, limite)

        # si si encontro camino, ya lo regresamos
        if camino is not None:
            return camino, limite

    # si acabe todos los limites y nunca encontre nada
    return None, None

# ejemplo rapido
if __name__ == "__main__":
    # salon -> pasillo, patio
    # pasillo -> lab
    # patio -> cafeteria
    # lab -> servidor
    # cafeteria -> servidor
    # servidor -> (nada)
    
    grafo = cargar_grafo_csv(DATA_PATH, bidireccional=True)

    camino, limite_usado = profundidad_iterativa(
        grafo,
        "Casa",
        "Cafeteria",
        limite_max=15
    )

    print("camino de Casa a Cafeteria:", camino)
    print("limite que se necesito:", limite_usado)

    camino2, limite2 = profundidad_iterativa(
        grafo,
        "Casa",
        "Taller_CNC",
        limite_max=15
    )   

    print("\ncamino de Casa a Taller_CNC:", camino2)
    print("limite que se intento:", limite2)