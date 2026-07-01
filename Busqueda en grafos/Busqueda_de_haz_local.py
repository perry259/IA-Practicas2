# busqueda de haz local
# tambien llamada local beam search
# en lugar de seguir solo 1 estado como ascension de colinas
# seguimos varios estados al mismo tiempo
# tenemos k estados activos
# en cada paso vemos todos sus vecinos
# nos quedamos con los k mejores y repetimos
# esto intenta no quedarse atorado tan facil
# porque no estamos apostando todo a una sola opcion

def generar_siguientes(estados_actuales, vecinos):
    """
    estados_actuales: lista de estados donde estoy ahorita
    vecinos: diccionario con lista de vecinos por estado

    regresa una lista con:
    - todos los vecinos de todos los estados actuales
    - tambien incluye los estados actuales (para no perdernos si ya eran buenos)
    sin repetir
    """

    nuevo_conjunto = set()

    # agrego los estados actuales
    for e in estados_actuales:
        nuevo_conjunto.add(e)

    # agrego los vecinos de cada estado
    for e in estados_actuales:
        for v in vecinos.get(e, []):
            nuevo_conjunto.add(v)

    # regreso como lista
    return list(nuevo_conjunto)


def top_k(estados, valor, k):
    """
    estados: lista de posibles estados
    valor: funcion que da puntaje a cada estado
    k: cuantos estados quiero conservar

    regresa los k estados con mayor valor
    ordenados de mejor a peor
    """

    # ordeno por valor de mayor a menor
    ordenados = sorted(estados, key=lambda x: valor(x), reverse=True)

    # me quedo con los primeros k
    return ordenados[:k]


def haz_local(inicio_lista, vecinos, valor, k, iter_max):
    """
    inicio_lista: lista inicial de estados (por ejemplo [3, 4])
                  esto es importante: aqui ya empezamos con varios estados
    vecinos: diccionario que dice a donde puedo moverme desde cada estado
    valor: funcion que mide que tan bueno es un estado (mas grande = mejor)
    k: tamano del haz (cuantos estados mantengo vivos cada paso)
    iter_max: cuantas iteraciones maximo voy a hacer

    regresa:
    - mejor_estado (el estado con mayor valor al final)
    - historial (lista paso a paso de los estados activos en cada vuelta)
                 ejemplo: [[3,4], [5,6], [7,8], ...]
    """

    # estados actuales del haz
    actuales = inicio_lista[:]

    # historial guarda como fueron cambiando los k estados con el tiempo
    historial = [actuales[:]]

    for _ in range(iter_max):
        # genero todos los posibles siguientes estados
        candidatos = generar_siguientes(actuales, vecinos)

        # elijo los k mejores segun valor()
        actuales = top_k(candidatos, valor, k)

        # guardo para poder ver como fue avanzando
        historial.append(actuales[:])

    # el mejor estado final es el que tenga mas valor
    mejor_final = max(actuales, key=lambda x: valor(x))

    return mejor_final, historial

if __name__ == "__main__":
    # cada estado es un numero
    # vecinos dice a que numeros puedo saltar desde cada numero

    vecinos = {
        3: [4, 5, 6],
        4: [6, 7],
        5: [6, 8],
        6: [7, 8],
        7: [8, 9],
        8: [9, 10],
        9: [10],
        10: []
    }

    # la funcion valor mide que tan bueno es el estado
    # aqui usamos el mismo numero como valor
    # ejemplo: valor(8) = 8, valor(10) = 10
    def valor(x):
        return x

    # parametros:
    # inicio_lista = [3, 4]
    # k = 2  (solo mantenemos los 2 mejores estados en cada paso)
    # iter_max = 5 (cuantas rondas hacemos)
    mejor, historial = haz_local(
        inicio_lista=[3, 4],
        vecinos=vecinos,
        valor=valor,
        k=2,
        iter_max=5
    )

    print("mejor estado al final:", mejor)
    print("historial del haz en cada paso:")
    for paso, estados in enumerate(historial):
        print(" paso", paso, "=>", estados)

 # notas:
    # - k es el tamano del haz cuantos estados mantengo
    # - solo sigo a los k mejores cada vuelta
    # - historial guarda la lista de estados que quedaron en cada iteracion
    # funciones importantes:
    # generar_siguientes(...) junta todos los vecinos posibles
    # top_k(...) ordena por valor y se queda con los mejores