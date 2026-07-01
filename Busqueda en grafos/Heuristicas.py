# heuristicas
# en las busquedas informadas usamos una "pista" para decidir a donde movernos
# esa pista se llama heuristica
# una heuristica es un numero que dice
# que tan cerca creo que estoy del objetivo
# mientras mas chico el numero, mejor (mas cerca segun mi estimacion)
# esto no garantiza el mejor camino
# pero ayuda a elegir primero los lugares que "se ven prometedores"

def mejor_vecino_por_heuristica(grafo, heuristica, actual):
    # esta funcion mira a que lugares puedo ir desde actual
    # y elige el vecino con la heuristica mas baja (o sea el mas "cercano")
    # grafo: conexiones normales
    # heuristica: diccionario con el valor estimado para cada lugar
    # actual: donde estoy ahorita

    vecinos = grafo.get(actual, [])

    if not vecinos:
        return None  # si no hay a donde ir

    # ordeno los vecinos por su heuristica
    # min(...) me da el vecino que tenga heuristica mas baja
    # uso key= para decirle con que comparar
    mejor = min(vecinos, key=lambda v: heuristica.get(v, float("inf")))

    return mejor

def camino_greedy(grafo, heuristica, inicio, objetivo):
    # esta funcion trata de llegar al objetivo
    # siempre moviendose al vecino con mejor heuristica
    # esto es de como la heuristica guia
    # no es a* ni es garantia de mejor camino
    # esto se parece mas a busqueda voraz (greedy), que lo veremos mas adelante

    actual = inicio
    camino = [actual]
    visitados = set([actual])

    while actual != objetivo:
        siguiente = mejor_vecino_por_heuristica(grafo, heuristica, actual)

        if siguiente is None:
            # ya no hay a donde ir
            return camino, False

        if siguiente in visitados:
            # me estoy quedando atorada dando vueltas
            return camino, False

        camino.append(siguiente)
        visitados.add(siguiente)
        actual = siguiente

    # si sali del ciclo es porque llegue al objetivo
    return camino, True

if __name__ == "__main__":
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

    # heuristica:
    # numero que dice que tan cerca creo que estoy del servidor
    # entre mas chico el numero, segun yo estoy mas cerca del servidor
    # ejemplo:
    # servidor tiene heuristica 0 (porque ya estoy ahi)
    # cafeteria tiene 1 (porque cafeteria llega directo a servidor)
    # cosas mas lejos tienen numeros mas grandes
    heuristica = {
        "servidor": 0,
        "cafeteria": 1,
        "lab": 1,
        "biblioteca": 2,
        "pasillo": 2,
        "patio": 2,
        "salon": 3
    }

    # probamos movernos desde salon hasta servidor
    camino, exito = camino_greedy(grafo, heuristica, "salon", "servidor")

    print("camino propuesto usando heuristica (salon -> servidor):", camino)
    print("llegamos al objetivo?:", exito)

    # notas:
    # heuristica["cafeteria"] = 1
    # eso se lee como: segun mi estimacion cafeteria esta cerca del servidor
    # min(lista, key=algo) elige el elemento de la lista que tiene el key mas chico
    # lista.append(x) mete x al final de la lista
    # conjunto.add(x) mete x a un set (set = lugares ya visitados)