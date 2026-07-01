# busqueda en anchura (bfs)
# busqueda en anchura sirve para encontrar un camino corto
# desde un punto inicio hasta un punto objetivo
# lo hace revisando primero los lugares que estan cerca (1 paso),
# luego los que estan a 2 pasos, luego 3 pasos, etc.
# esto sirve por ejemplo para ver como llegar rapido de un salon a un servidor pasando por pasillo, lab, etc

from collections import deque
# importamos deque
# deque es una cola (fifo: first in first out)
# piensa en una fila normal: el primero que llega es el primero que sale
# bfs usa esa idea de fila para decidir que lugar visitar despues
# def se usa para crear una función en python.
# una función es un bloque de código con un nombre, 
# que hace algo y que puedes volver a usar sin repetir todo,
#alguna tienen parametros(a,b,c) y otras no()
import csv
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "data" / "rutas.csv"

def cargar_grafo_csv(ruta_csv, bidireccional=True):
    grafo = {}
    with ruta_csv.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
          o = row["origen"].strip()
          d = row["destino"].strip()
          grafo.setdefault(o, []).append(d)
          grafo.setdefault(d, [])
          if bidireccional:
              grafo.setdefault(d, []).append(o)
    return grafo

def bfs_camino_mas_corto(grafo, inicio, objetivo):
    """
    esta funcion busca el camino mas corto en numero de pasos
    desde inicio hasta objetivo usando busqueda en anchura

    grafo: es un diccionario que dice a donde puedo ir desde cada lugar
    ejemplo:
        "salon": ["pasillo", "patio"]
        significa: desde salon puedo ir a pasillo o a patio

    regresa:
    - una lista con el camino paso a paso
      por ejemplo ['salon', 'pasillo', 'lab']
    - o None si no hay forma de llegar
    """
    # si ya estoy en el lugar que quiero, ya acabe
    if inicio == objetivo:
        return [inicio]

    # si el inicio ni existe en el grafo, no puedo ni empezar
    if inicio not in grafo:
        return None

    # visitados: lugares que ya vimos
    # esto es para no repetir el mismo lugar una y otra vez
    visitados = {inicio}

    # cola: lugares que faltan por explorar (fila fifo)
    # al inicio solo tengo el punto de inicio
    cola = deque([inicio])

    # padres: aqui guardo de donde vengo
    # ejemplo mental: para llegar a lab llegue desde pasillo
    # esto luego me deja reconstruir el camino final
    padres = {inicio: None}

    # mientras aun haya lugares pendientes en la cola
    while cola:
        # saco el siguiente lugar a revisar
        actual = cola.popleft()

        # veo a cuales lugares puedo ir desde el lugar actual
        for vecino in grafo.get(actual, []):
            # si todavia no he visitado ese vecino
            if vecino not in visitados:
                # lo marco como visitado
                visitados.add(vecino)

                # guardo quien me llevo hasta ese vecino
                padres[vecino] = actual

                # si el vecino es justo el objetivo, ya encontre ruta
                if vecino == objetivo:
                    # armo el camino empezando desde el objetivo
                    camino = [vecino]
                    paso = padres[vecino]

                    # voy caminando hacia atras
                    # ejemplo: servidor <- cafeteria <- patio <- salon
                    while paso is not None:
                        camino.append(paso)
                        paso = padres[paso]

                    # el camino ahorita esta al reves
                    # lo volteo para que quede de inicio a objetivo
                    camino.reverse()
                    return camino

                # si aun no llegue al objetivo
                # meto este vecino a la cola para revisarlo luego
                cola.append(vecino)

    # si se vacio la cola y nunca llegue al objetivo
    # entonces no hay camino posible
    return None

def bfs_orden_visita(grafo, inicio):
    """
    esta funcion regresa el orden en el que bfs va visitando lugares
    esto ayuda a ver como bfs explora por niveles
    ejemplo de salida:
    ['salon', 'pasillo', 'patio', 'lab', 'biblioteca', 'cafeteria', 'servidor']
    """

    # si el inicio no esta en el grafo regreso lista vacia
    if inicio not in grafo:
        return []

    # marco el inicio como visitado
    visitados = {inicio}

    # creo la cola con el inicio
    cola = deque([inicio])

    # esta lista guarda el orden en el que se ven los lugares
    orden = [inicio]

    # mientras la cola no este vacia
    while cola:
        # saco el siguiente lugar a revisar
        actual = cola.popleft()

        # veo a donde puedo ir desde este lugar
        for vecino in grafo.get(actual, []):
            # si ese vecino no se ha visto todavia
            if vecino not in visitados:
                # lo marco como visitado
                visitados.add(vecino)

                # lo paso a la cola para luego explorar sus vecinos
                cola.append(vecino)

                # tambien lo agrego a la lista orden
                orden.append(vecino)

    # regreso el orden en el que bfs recorrio todo
    return orden


# bloque principal
if __name__ == "__main__":
    # este es nuestro grafo de ejemplo
    # desde salon puedo ir a pasillo y patio
    # desde pasillo puedo ir a lab y biblioteca
    # desde patio puedo ir a cafeteria
    # desde lab puedo ir a servidor
    # desde biblioteca puedo ir a cafeteria
    # desde cafeteria puedo ir a servidor
    # servidor ya no lleva a ningun lado
   
    grafo = cargar_grafo_csv(DATA_PATH, bidireccional=True)
   
    print("grafo de ejemplo (lugar -> a donde puedo ir):")
    for lugar, vecinos in grafo.items():
        print(" ", lugar, "->", vecinos)

    print("\norden de visita empezando en Casa:")
    print(bfs_orden_visita(grafo, "Casa"))

    print("\ncamino mas corto de Casa a Cafeteria:")
    print(bfs_camino_mas_corto(grafo, "Casa", "Cafeteria"))

    print("\ncamino mas corto de Casa a Estacionamiento:")
    print(bfs_camino_mas_corto(grafo, "Casa", "Estacionamiento"))

    # nota rapida:
    # si sale None significa que no hay forma de llegar