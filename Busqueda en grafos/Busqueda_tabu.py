# busqueda tabu
# la busqueda tabu es parecida a ascension de colinas
# pero con memoria
# problema que tiene ascension de colinas:
# se puede quedar atorada en un punto
# guardamos una lista tabu (lugares recientes donde ya estuve)
# y no regreso a esos lugares por un rato
# esto ayuda a no repetir siempre lo mismo

def mejor_vecino_no_tabu(actual, vecinos, valor, tabu):
    # actual: estado actual
    # vecinos: diccionario con vecinos de cada estado
    # valor: funcion que da puntaje a cada estado
    # tabu: conjunto de estados que no debo usar ahorita
    # regresa el mejor vecino que no este en tabu
    # si no hay opcion valida regresa None

    candidato = None
    mejor_valor = None

    for v in vecinos.get(actual, []):
        if v in tabu:
            continue  # salto este vecino porque esta prohibido temporalmente

        val_v = valor(v)

        if candidato is None or val_v > mejor_valor:
            candidato = v
            mejor_valor = val_v

    return candidato  # puede ser None


def busqueda_tabu(inicio, vecinos, valor, tam_tabu, max_iter):
    # inicio: estado inicial
    # vecinos: conexiones posibles
    # valor: funcion que mide que tan bueno es un estado
    # tam_tabu: tamano maximo de la lista tabu
    # max_iter: numero maximo de pasos que voy a intentar
    # regresa (mejor_estado_encontrado, historial_de_estados)

    actual = inicio
    mejor_global = actual  # mejor estado que he visto en toda la busqueda
    historial = [actual]

    tabu = set([actual])   # estados prohibidos por ahora
    cola_tabu = [actual]   # para controlar quien sale cuando se llena

    for _ in range(max_iter):
        siguiente = mejor_vecino_no_tabu(actual, vecinos, valor, tabu)

        if siguiente is None:
            # no hay a donde moverme sin violar tabu
            break

        # me muevo
        actual = siguiente
        historial.append(actual)

        # actual entra a tabu
        tabu.add(actual)
        cola_tabu.append(actual)

        # si la lista tabu ya esta muy grande, saco el mas viejo
        if len(cola_tabu) > tam_tabu:
            viejo = cola_tabu.pop(0)
            if viejo in tabu:
                tabu.remove(viejo)

        # actualizo mejor_global si encontre algo mejor
        if valor(actual) > valor(mejor_global):
            mejor_global = actual

    return mejor_global, historial

if __name__ == "__main__":
    # cada numero puede saltar a otros numeros
    # valor(x) = x, entonces un numero mas grande es mejor

    vecinos = {
        3: [4, 5, 6],
        4: [5, 6],
        5: [4, 6, 7],
        6: [5, 7, 8],
        7: [6, 8, 9],
        8: [7, 9],
        9: [8]
    }

    def valor(x):
        return x

    # parametros:
    # inicio = 3
    # tam_tabu = 3  (cuantos estados mantengo marcados como tabu)
    # max_iter = 10 (cuantos pasos maximo intento moverme)
    mejor, pasos = busqueda_tabu(
        inicio=3,
        vecinos=vecinos,
        valor=valor,
        tam_tabu=3,
        max_iter=10
    )

    print("mejor estado encontrado:", mejor)
    print("pasos recorridos:", pasos)

    # - tabu = estados a los que no quiero regresar rapido
    # - esto evita dar vueltas entre los mismos dos o tres estados
    # - mejor_global guarda el mejor estado total que encontre