# busqueda a*
# este algoritmo busca un camino con buen costo hasta el objetivo
# para decidir que nodo revisar usa esta formula:
# f(n) = g(n) + h(n)
# g(n) = costo real que llevo hasta n
# h(n) = cuanto creo que falta para llegar al objetivo (heuristica)
# siempre se escoge el nodo con f mas chico

import heapq  

def a_estrella(grafo_costos, heuristica, inicio, objetivo):
    # heuristica: estimacion de distancia al objetivo
    # inicio: nodo inicial
    # objetivo: nodo final
    # regresa (camino, costo_total) o (None, None) si no hay camino

    if inicio == objetivo:
        return [inicio], 0

    # costo real para llegar a cada nodo
    g = {inicio: 0}

    # cola de prioridad con tuplas (f, nodo, camino_hasta_nodo)
    abiertos = []
    f_inicio = g[inicio] + heuristica.get(inicio, float("inf"))
    heapq.heappush(abiertos, (f_inicio, inicio, [inicio]))

    visitados = set()

    while abiertos:
        f_actual, actual, camino = heapq.heappop(abiertos)

        # si ya llegamos al objetivo
        if actual == objetivo:
            return camino, g[actual]

        if actual in visitados:
            continue
        visitados.add(actual)

        # revisamos vecinos del nodo actual
        for vecino, costo_ir in grafo_costos.get(actual, {}).items():
            nuevo_g = g[actual] + costo_ir  # costo real si paso por aqui

            # si es primera vez que veo este vecino
            # o encontre una forma mas barata de llegar
            if (vecino not in g) or (nuevo_g < g[vecino]):
                g[vecino] = nuevo_g
                nuevo_camino = camino + [vecino]

                # f = g + h
                f_vecino = nuevo_g + heuristica.get(vecino, float("inf"))

                heapq.heappush(
                    abiertos,
                    (f_vecino, vecino, nuevo_camino)
                )

    # no hay forma de llegar
    return None, None

# nota ao*
# ao* se usa en grafos and-or (cuando hay pasos de tipo "tienes que hacer varias cosas a la vez")
# normalmente en este nivel solo se explica que ao* trabaja con and-or
# y no se suele pedir el codigo
# por eso abajo solo probamos a*


if __name__ == "__main__":
    # ejemplo con lugares y costo de moverse entre ellos

    grafo_costos = {
        "casa": {"tienda": 2, "parque": 5},
        "tienda": {"escuela": 2, "hospital": 5},
        "escuela": {"oficina": 4},
        "parque": {"hospital": 2},
        "hospital": {"oficina": 3},
        "oficina": {}
    }

    # heuristica: que tan cerca creo que esta cada nodo de "oficina"
    # mientras mas chico, mas cerca segun la estimacion
    heuristica = {
        "oficina": 0,
        "hospital": 2,
        "escuela": 3,
        "parque": 4,
        "tienda": 4,
        "casa": 6
    }

    camino, costo = a_estrella(grafo_costos, heuristica, "casa", "oficina")
    print("camino a* de casa a oficina:", camino)
    print("costo total:", costo)

    camino2, costo2 = a_estrella(grafo_costos, heuristica, "casa", "aeropuerto")
    print("camino a* de casa a aeropuerto:", camino2)
    print("costo total:", costo2)

    # g(n) = costo real
    # h(n) = estimacion
    # f(n) = g + h
    # a* elige el siguiente nodo con f mas chico