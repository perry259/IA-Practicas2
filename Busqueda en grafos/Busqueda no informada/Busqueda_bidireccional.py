# Busqueda bidireccional
# en lugar de buscar solo desde inicio hacia objetivo
# buscamos desde los dos lados al mismo tiempo
# lado inicio -> avanza normal
# lado objetivo -> avanza al reves
# si se encuentran, ya hay camino

from collections import deque  # cola fifo para explorar por niveles

def reconstruir_camino(padres_inicio, padres_objetivo, punto):
    # arma el camino final cuando ya sabemos
    # en que punto se encontraron las dos busquedas

    # camino desde inicio hasta el punto
    parte_a = [punto]
    n = padres_inicio[punto]
    while n is not None:
        parte_a.append(n)
        n = padres_inicio[n]
    parte_a.reverse()  # ahora empieza en inicio

    # camino desde el punto hasta el objetivo
    parte_b = []
    n = padres_objetivo[punto]
    while n is not None:
        parte_b.append(n)
        n = padres_objetivo[n]

    # junto las dos partes
    return parte_a + parte_b

def busqueda_bidireccional(grafo, inicio, objetivo):
    # caso facil
    if inicio == objetivo:
        return [inicio]

    # si inicio u objetivo no existen en el grafo
    if inicio not in grafo or objetivo not in grafo:
        return None

    # visitados desde inicio
    visit_i = {inicio}
    # visitados desde objetivo
    visit_o = {objetivo}

    # colas de cada lado
    cola_i = deque([inicio])
    cola_o = deque([objetivo])

    # padres para reconstruir
    padres_i = {inicio: None}
    padres_o = {objetivo: None}

    # repetimos mientras haya nodos en ambas colas
    while cola_i and cola_o:

        # paso desde el lado inicio
        actual_i = cola_i.popleft()

        for vecino in grafo.get(actual_i, []):
            if vecino not in visit_i:
                visit_i.add(vecino)
                padres_i[vecino] = actual_i
                cola_i.append(vecino)

                # si este vecino ya fue visto desde el lado objetivo
                # las dos busquedas se encontraron
                if vecino in visit_o:
                    return reconstruir_camino(padres_i, padres_o, vecino)

        # paso desde el lado objetivo
        actual_o = cola_o.popleft()

        # aqui vamos "al reves"
        # buscamos nodos que puedan llegar a actual_o
        for nodo, vecinos in grafo.items():
            if actual_o in vecinos:
                if nodo not in visit_o:
                    visit_o.add(nodo)
                    padres_o[nodo] = actual_o
                    cola_o.append(nodo)

                    # si este nodo ya fue visto desde inicio
                    # las dos mitades se encontraron
                    if nodo in visit_i:
                        return reconstruir_camino(padres_i, padres_o, nodo)

    # si nunca se encontraron
    return None

if __name__ == "__main__":
    # conexiones ejemplo
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

    camino = busqueda_bidireccional(grafo, "salon", "servidor")
    print("camino salon -> servidor:", camino)

    camino2 = busqueda_bidireccional(grafo, "salon", "estacionamiento")
    print("camino salon -> estacionamiento:", camino2)