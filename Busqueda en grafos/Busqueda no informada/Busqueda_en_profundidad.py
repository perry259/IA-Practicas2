# busqueda en profundidad (dfs)
# busqueda en profundidad intenta ir lo mas lejos posible por un camino
# o sea baja, baja, baja hasta que ya no puede
# si no llego al objetivo, se regresa y prueba otro camino
# diferencia con busqueda en anchura (bfs):
# bfs explora lugares por niveles (lo mas cerca primero)
# dfs se mete directo por un camino hasta el fondo

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

def dfs_camino(grafo, inicio, objetivo, visitados=None, camino=None):
    # inicio: donde empiezo
    # objetivo: a donde quiero llegar
    # esta funcion regresa un camino (lista) desde inicio hasta objetivo
    # o regresa None si no existe camino
    # nota: esta version usa recursion
    # recursion significa que la funcion se llama a si misma
    # este if es solo para la primera llamada
    # aqui iniciamos las estructuras
    if visitados is None:
        visitados = set()   # conjunto de lugares ya visitados
    if camino is None:
        camino = [inicio]   # lista con el camino que llevo hasta ahorita

    # marcamos el nodo actual (inicio) como visitado
    visitados.add(inicio)

    # si ya estoy en el objetivo, ya termine
    # regreso el camino actual
    if inicio == objetivo:
        return camino

    # si no he llegado todavia
    # veo a donde puedo ir desde este lugar
    for vecino in grafo.get(inicio, []):
        # si ese vecino no se ha visitado aun
        if vecino not in visitados:
            # intento seguir por ese vecino
            # llamada recursiva:
            # copiamos el camino actual y le agregamos el vecino
            resultado = dfs_camino(
                grafo,
                vecino,
                objetivo,
                visitados,
                camino + [vecino]
            )

            # si resultado no es None
            # significa que desde ese vecino si pude llegar al objetivo
            if resultado is not None:
                return resultado

    # si probe todos los vecinos y ninguno llego al objetivo
    # regreso None para decir "por aqui no hubo camino"
    return None

# ejemplo
if __name__ == "__main__":
    # desde salon puedo ir a pasillo y patio
    # desde pasillo puedo ir a lab
    # desde patio puedo ir a cafeteria
    # desde lab puedo ir a servidor
    # cafeteria tambien puede ir a servidor
    # servidor ya no lleva a otro lado

    grafo = cargar_grafo_csv(DATA_PATH, bidireccional=True)

    resultado = dfs_camino(grafo, "Casa", "Cafeteria")
    print("camino encontrado con dfs (Casa a Cafeteria):", resultado)

    resultado2 = dfs_camino(grafo, "Casa", "Estacionamiento")
    print("camino de Casa a Estacionamiento:", resultado2)

    resultado3 = dfs_camino(grafo, "Casa", "Taller_CNC")
    print("camino de Casa a Taller_CNC:", resultado3)
    # dfs se mete en un camino hasta el fondo
    # si no sirve, se regresa y prueba otro
    # dfs no promete el camino mas corto