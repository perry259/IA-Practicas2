# busqueda en grafos
# a veces el grafo tiene caminos que regresan a lugares ya visitados
# ejemplo: pasillo -> lab y lab -> pasillo
# eso puede hacer que des vueltas para siempre
# solucion:
# guardamos a que lugares ya fuimos (visitados)
# para no volver a meterlos otra vez
# Asi no repetimos lugares

from collections import deque  # deque = cola fifo (primero en entrar, primero en salir)

def busqueda_en_grafo(grafo, inicio):
    # recorre el grafo empezando en inicio
    # regresa el orden en el que visite los lugares
    # no repite lugares

    if inicio not in grafo:
        return []

    visitados = set([inicio])     # lugares donde ya estuve
    cola = deque([inicio])        # lugares pendientes por revisar
    orden = []                    # orden en que voy visitando

    while cola:
        actual = cola.popleft()   # saco el primero de la cola
        orden.append(actual)      # guardo que ya visite este lugar

        # reviso a donde puedo ir desde aqui
        for vecino in grafo.get(actual, []):
            if vecino not in visitados:
                visitados.add(vecino)   # marco ese lugar como ya visitado
                cola.append(vecino)     # lo meto al final de la cola

    return orden

def hay_camino(grafo, inicio, objetivo):
    # revisa si puedo llegar de inicio a objetivo
    # regresa True o False

    if inicio == objetivo:
        return True
    if inicio not in grafo:
        return False

    visitados = set([inicio])
    cola = deque([inicio])

    while cola:
        actual = cola.popleft()
        if actual == objetivo:
            return True

        for vecino in grafo.get(actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)

    return False

if __name__ == "__main__":
    # salon -> pasillo, patio
    # pasillo -> lab
    # lab -> pasillo, servidor   (aqui hay vuelta pasillo <-> lab)
    # patio -> cafeteria
    # cafeteria -> servidor
    # servidor -> (nada mas)
    grafo = {
        "salon": ["pasillo", "patio"],
        "pasillo": ["lab"],
        "patio": ["cafeteria"],
        "lab": ["pasillo", "servidor"],
        "cafeteria": ["servidor"],
        "servidor": []
    }

    print("orden de visita desde salon:", busqueda_en_grafo(grafo, "salon"))
    print("hay camino salon -> servidor?:", hay_camino(grafo, "salon", "servidor"))
    print("hay camino salon -> estacionamiento?:", hay_camino(grafo, "salon", "estacionamiento"))

    # visitados.add(x)  = marco que ya pase por x
    # cola.append(x)    = x se forma al final de la cola para revisarlo despues
    # cola.popleft()    = saco al primero en la cola (el siguiente a revisar)