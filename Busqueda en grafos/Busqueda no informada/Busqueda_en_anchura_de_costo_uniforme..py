# busqueda de costo uniforme
# este algoritmo busca el camino mas barato desde inicio hasta objetivo
# barato = de menor costo total, no de menos pasos
# ejemplo:
# salon -> pasillo cuesta 2
# salon -> patio cuesta 6
# pasillo -> servidor cuesta 4
# patio -> servidor cuesta 1
# el algoritmo tiene que decidir que sale mas barato llegar a servidor

import heapq
# heapq es una cola de prioridad
# siempre nos da primero el camino mas barato hasta ahorita

def ucs_camino_mas_barato(grafo, inicio, objetivo):
    # si inicio ya es el objetivo, listo
    if inicio == objetivo:
        return [inicio], 0

    # si el inicio ni esta en el grafo, no puedo empezar
    if inicio not in grafo:
        return None, None

    # costo_hasta guarda el mejor costo conocido para cada lugar
    # al inicio, llegar a inicio cuesta 0
    costo_hasta = {inicio: 0}

    # padres guarda de donde llegue
    # ejemplo: para llegar a pasillo llegue desde salon
    padres = {inicio: None}

    # cola de prioridad
    # cada elemento es (costo_total_hasta_aqui, lugar_actual)
    cola = [(0, inicio)]

    while cola:
        # saco el lugar mas barato hasta ahorita
        costo_actual, actual = heapq.heappop(cola)

        # si ya llegue al objetivo, reconstruyo el camino y regreso
        if actual == objetivo:
            camino = [actual]
            paso = padres[actual]
            # voy caminando hacia atras: servidor <- pasillo <- salon
            while paso is not None:
                camino.append(paso)
                paso = padres[paso]
            camino.reverse()  # lo volteo: salon -> pasillo -> servidor
            return camino, costo_actual

        # reviso a donde puedo ir desde aqui
        # grafo[actual] es un diccionario con vecinos y su costo
        for vecino, costo_arista in grafo.get(actual, {}).items():
            # nuevo_costo = lo que ya me costo llegar aqui + lo que cuesta ir al vecino
            nuevo_costo = costo_actual + costo_arista

            # si el vecino no tiene costo guardado
            # o encontre una forma mas barata de llegar
            if (vecino not in costo_hasta) or (nuevo_costo < costo_hasta[vecino]):
                costo_hasta[vecino] = nuevo_costo
                padres[vecino] = actual
                # meto el vecino a la cola con su costo total hasta el
                heapq.heappush(cola, (nuevo_costo, vecino))

    # si nunca pude llegar al objetivo
    return None, None
# ejemplo muy corto para probar
if __name__ == "__main__":
    # grafo con costos
    # desde salon a pasillo cuesta 2
    # desde salon a patio cuesta 6
    # desde pasillo a servidor cuesta 4
    # desde patio a servidor cuesta 1
    grafo = {
        "salon": {"pasillo": 2, "patio": 6},
        "pasillo": {"servidor": 4},
        "patio": {"servidor": 1},
        "servidor": {}
    }
    # buscamos el camino mas barato para ir de salon a servidor
    camino, costo = ucs_camino_mas_barato(grafo, "salon", "servidor")

    print("camino mas barato de salon a servidor:", camino)
    print("costo total:", costo)

    # nota importante:
    # fijate que salon -> pasillo -> servidor cuesta 2 + 4 = 6
    # pero salon -> patio -> servidor cuesta 6 + 1 = 7
    # entonces el algoritmo elige salon -> pasillo -> servidor
    # porque 6 es mas barato que 7