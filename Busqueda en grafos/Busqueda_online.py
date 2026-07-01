# busqueda online
# este tipo de busqueda no conoce todo el grafo al inicio.
# por ejemplo: el agente solo conoce donde esta y que vecinos tiene.
# cuando se mueve a otro lugar, descubre mas vecinos y los guarda.
# sirve como un mapa es desconocido y lo vas explorando al momento.

def paso_online(actual, mundo_real, memoria_local, visitados):
    """
    actual:
        donde estoy ahorita

    mundo_real:
        este si es el grafo completo con todas las conexiones
        pero ojo: el agente NO lo ve todo de golpe
        solo ve los vecinos del lugar donde esta

    memoria_local:
        lo que el agente ha aprendido hasta ahora
        ejemplo:
        {
          "A": ["B","C"],
          "B": ["D"]
        }
        significa: ya se que de A puedo ir a B y C, y de B puedo ir a D

    visitados:
        lugares donde ya estuve, para no regresar mil veces

    regresa:
        lista de vecinos nuevos (lugares a donde puedo ir despues)
    """
    # obtener vecinos REALES del lugar actual
    vecinos_reales = mundo_real.get(actual, [])

    # guardar esta info en memoria_local
    memoria_local[actual] = vecinos_reales[:]

    # filtro los que no he visitado todavia
    opciones = []
    for v in vecinos_reales:
        if v not in visitados:
            opciones.append(v)

    return opciones

def busqueda_online(inicio, objetivo, mundo_real, max_pasos):
    """
    inicio:
        nodo inicial
    objetivo:
        a donde queremos llegar
    mundo_real:
        grafo real del mundo (todas las conexiones)
        este grafo lo tiene el profe / el programa
        pero el "agente" lo va aprendiendo poquito a poco
    max_pasos:
        limite para no quedarnos en un ciclo eterno

    regresa:
        camino_recorrido: los lugares por donde paso el agente
        memoria_local: lo que el agente aprendio del mundo
    """

    actual = inicio
    camino_recorrido = [actual]

    # memoria_local empieza vacia
    memoria_local = {}

    # visitados guarda donde ya estuve
    visitados = set([actual])

    for _ in range(max_pasos):
        # si ya llegue al objetivo paro
        if actual == objetivo:
            return camino_recorrido, memoria_local, True

        # pregunto: desde aqui donde me puedo mover?
        opciones = paso_online(actual, mundo_real, memoria_local, visitados)

        if not opciones:
            # ya no hay a donde ir que no haya visto
            # me quedo atorado
            return camino_recorrido, memoria_local, False

        # estrategia simple:
        # me muevo al primer vecino que no he visitado
        siguiente = opciones[0]

        # actualizo todo
        actual = siguiente
        visitados.add(actual)
        camino_recorrido.append(actual)

    # si llegue al limite de pasos y no encontre el objetivo
    return camino_recorrido, memoria_local, False

if __name__ == "__main__":
    # mundo_real es el mapa verdadero
    # este grafo SI lo conoce el programa
    # pero el agente lo va aprendiendo poco a poco con paso_online()
    # ejemplo tipo mapa de cuartos conectados
    # A -> B, C
    # B -> D
    # C -> D, E
    # D -> F
    # E -> F
    # F -> (nada)
    mundo_real = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D", "E"],
        "D": ["F"],
        "E": ["F"],
        "F": []
    }

    # queremos ir de A a F sin conocer el mapa completo desde el inicio
    camino, memoria, exito = busqueda_online(
        inicio="A",
        objetivo="F",
        mundo_real=mundo_real,
        max_pasos=10
    )

    print("camino recorrido paso a paso:", camino)
    print("el agente aprendio esto del mundo:")
    for lugar, vecs in memoria.items():
        print(" ", lugar, "->", vecs)
    print("llego al objetivo?:", exito)

    # - memoria_local guarda lo que el agente ha descubierto
    # - paso_online descubre vecinos del nodo actual
    # - no planeamos todo desde el inicio, decidimos paso por paso