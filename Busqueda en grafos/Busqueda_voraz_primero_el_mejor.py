# busqueda voraz primero el mejor
# tambien se llama greedy best first search
# siempre trato de ir al lugar que "se ve mas cerca" del objetivo
# uso solo la heuristica (una estimacion de que tan cerca estoy)
# no me importa el costo real del camino, solo lo prometedor
# ventaja: es rapida
# desventaja: puede elegir un camino que parece bueno al inicio
# pero no es el mejor de verdad

import heapq  # cola de prioridad

def busqueda_voraz(grafo, heuristica, inicio, objetivo):
    # grafo: conexiones entre lugares
    # heuristica: que tan cerca esta cada lugar del objetivo (numero mas chico = mejor)
    # inicio: desde donde empiezo
    # objetivo: a donde quiero llegar

    if inicio == objetivo:
        return [inicio]

    # abiertos = lugares que vamos a revisar
    # cada elemento en la cola es (h, nodo, camino_hasta_ahora)
    abiertos = []
    heapq.heappush(
        abiertos,
        (heuristica.get(inicio, float("inf")), inicio, [inicio])
    )

    visitados = set([inicio])  # para no repetir lugares

    while abiertos:
        # saco el nodo que tiene la heuristica mas baja
        _, actual, camino = heapq.heappop(abiertos)

        # si ya llegue al objetivo termino
        if actual == objetivo:
            return camino

        # reviso a donde puedo ir desde aqui
        for vecino in grafo.get(actual, []):
            if vecino not in visitados:
                visitados.add(vecino)

                nuevo_camino = camino + [vecino]

                # meto al vecino usando su heuristica como prioridad
                heapq.heappush(
                    abiertos,
                    (heuristica.get(vecino, float("inf")), vecino, nuevo_camino)
                )

    # si nunca llegue
    return None

if __name__ == "__main__":
    # conexiones del mapa
    # salon -> pasillo, patio
    # pasillo -> lab, biblioteca
    # patio -> cafeteria
    # lab -> servidor
    # biblioteca -> cafeteria
    # cafeteria -> servidor
    # servidor -> (nada)
    grafo = {
        "salon": ["pasillo", "patio"],
        "pasillo": ["lab", "biblioteca"],
        "patio": ["cafeteria"],
        "lab": ["servidor"],
        "biblioteca": ["cafeteria"],
        "cafeteria": ["servidor"],
        "servidor": []
    }
    # heuristica = "que tan cerca creo que estoy del servidor"
    # numero chico = siento que estoy mas cerca
    # el objetivo (servidor) vale 0
    heuristica = {
        "servidor": 0,
        "cafeteria": 1,
        "lab": 1,
        "biblioteca": 2,
        "pasillo": 2,
        "patio": 2,
        "salon": 3
    }

    camino1 = busqueda_voraz(grafo, heuristica, "salon", "servidor")
    print("camino voraz de salon a servidor:", camino1)

    camino2 = busqueda_voraz(grafo, heuristica, "salon", "estacionamiento")
    print("camino voraz de salon a estacionamiento:", camino2)

    # - siempre elige el siguiente lugar con heuristica mas baja
    # - ignora el costo real del camino
    # - es rapida pero no siempre da la mejor ruta