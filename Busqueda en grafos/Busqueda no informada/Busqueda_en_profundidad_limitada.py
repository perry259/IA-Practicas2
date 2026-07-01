# busqueda en profundidad limitada
# la busqueda en profundidad normal (dfs) se mete lo mas hondo que pueda
# problema: a veces se puede ir demasiado lejos y nunca parar
# la idea de profundidad limitada es ponerle un tope
# ejemplo: solo puedes bajar 2 niveles desde el inicio y ya
# si el objetivo esta muy lejos y el limite es chiquito, no lo va a encontrar
# si el limite es suficiente, si lo encuentra

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
    # grafo: conexiones entre lugares
    # actual: donde estoy ahorita
    # objetivo: a donde quiero llegar
    # limite: cuanta profundidad maxima puedo bajar
    # camino: el camino que llevo hasta ahorita
    
    # esta parte solo corre la primera vez para iniciar el camino
    if camino is None:
        camino = [actual]

    # si ya llegue al objetivo, regreso el camino
    if actual == objetivo:
        return camino

    # si ya me gaste todo el limite, ya no puedo bajar mas
    # entonces paro aqui y digo que por aqui no se llego
    if limite == 0:
        return None

    # si todavia tengo limite, intento avanzar con cada vecino
    for vecino in grafo.get(actual, []):
        if vecino in camino:
         continue
    
        # importante: le bajo 1 al limite
        resultado = dfs_limitada(
            grafo,
            vecino,
            objetivo,
            limite - 1,        # bajo un nivel de profundidad
            camino + [vecino]  # agrego el vecino al camino
        )

        # si encontre un camino valido, lo regreso
        if resultado is not None:
            return resultado

    # si ningun vecino funciono dentro del limite, regreso None
    return None

# ejemplo
if __name__ == "__main__":
    # salon va a pasillo y patio
    # pasillo va a lab
    # patio va a cafeteria
    # lab va a servidor
    # cafeteria va a servidor
    # servidor no va a otro lado
    
    grafo = cargar_grafo_csv(DATA_PATH, bidireccional=True)

    print("limite = 3 (Casa -> Cafeteria)")
    camino1 = dfs_limitada(grafo, "Casa", "Cafeteria", limite=3)
    print("  camino encontrado:", camino1)

    print("\nlimite = 6 (Casa -> Cafeteria)")
    camino2 = dfs_limitada(grafo, "Casa", "Cafeteria", limite=6)
    print("  camino encontrado:", camino2)

    print("\nlimite = 10 (Casa -> Estacionamiento)")
    camino3 = dfs_limitada(grafo, "Casa", "Estacionamiento", limite=10)
    print("  camino encontrado:", camino3)

    print("\nlimite = 10 (Casa -> Taller_CNC)")
    camino4 = dfs_limitada(grafo, "Casa", "Taller_CNC", limite=10)
    print("  camino encontrado:", camino4)