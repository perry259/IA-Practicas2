# busqueda de ascension de colinas
# siempre se mueve al vecino que este mejor que el estado actual
# "mejor" significa con mejor puntaje segun una funcion
# importante:
# - si ningun vecino es mejor, se detiene
# - se puede quedar atrapado en un punto que no es el mejor de todos
#   (eso se llama maximo local)

def mejor_vecino(estado_actual, vecinos, valor):
    # estado_actual: numero o estado donde estoy
    # vecinos: lista de posibles siguientes estados
    # valor: funcion que da un puntaje a cada estado (mientras mas alto mejor)
    # regresa el vecino que tiene mejor valor que el actual
    # si ningun vecino es mejor, regresa None

    valor_actual = valor(estado_actual)

    # buscamos el vecino con valor mas alto
    candidato = None
    mejor_valor = valor_actual

    for v in vecinos.get(estado_actual, []):
        val_v = valor(v)
        if val_v > mejor_valor:  # solo acepto si es mejor
            mejor_valor = val_v
            candidato = v

    return candidato  # puede ser None


def ascension_de_colinas(inicio, vecinos, valor):
    # inicio: estado inicial
    # vecinos: diccionario con lista de vecinos para cada estado
    # valor: funcion que mide que tan bueno es un estado
    # regresa (estado_final, historial)
    # historial es la lista de estados visitados en orden

    actual = inicio
    historial = [actual]

    while True:
        # intento mejorar
        siguiente = mejor_vecino(actual, vecinos, valor)

        # si no hay mejora posible, paro aqui
        if siguiente is None:
            return actual, historial

        # si si hay mejora, me muevo
        actual = siguiente
        historial.append(actual)


if __name__ == "__main__":
    # ejemplo:
    # cada "estado" es un numero
    # vecinos dice a que numeros puedo saltar desde cada numero
    # la funcion valor es simplemente "que tan alto es el numero"
    # o sea, mientras mas grande el numero, mejor

    vecinos = {
        1: [2, 3],
        2: [4, 5],
        3: [5, 6],
        4: [7],
        5: [7, 8],
        6: [8],
        7: [9],
        8: [9, 10],
        9: [],
        10: []
    }

    def valor(x):
        # aqui el valor es el mismo numero
        # ejemplo: valor(8) = 8, valor(10) = 10
        return x

    # empezamos en 1 y tratamos de ir subiendo
    final, pasos = ascension_de_colinas(1, vecinos, valor)

    print("estado final encontrado:", final)
    print("pasos que se siguieron:", pasos)

    # - siempre acepto solo un movimiento que mejore
    # - si ya no puedo mejorar, me detengo
    # - esto no garantiza el mejor valor global
    # - se puede quedar en un valor bueno pero no perfecto