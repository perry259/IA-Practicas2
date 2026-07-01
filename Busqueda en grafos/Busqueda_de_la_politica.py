# Busqueda de la politica
# en vez de aprender valores Q o valores de estados,
# intento buscar directamente cual politica (que accion tomar en cada estado)
# me da mas recompensa promedio.
# 1. tengo una politica actual (diccionario estado -> accion)
# 2. juego varias veces con esa politica y mido recompensa promedio
# 3. creo una version modificada de la politica (cambio una accion)
# 4. la pruebo
# 5. si la modificada es mejor, me quedo con esa

import random

def simular_con_politica(politica, transicion, recompensa_final, estado_inicial, episodios):
    """
    corre varios episodios usando una politica fija
    y regresa la recompensa promedio.

    politica:
        dict estado -> accion
        ejemplo:
        {
            "A": "a_B",
            "B": "b_C"
        }

    transicion(estado, accion):
        regresa el siguiente estado

    recompensa_final(estado):
        que gano al terminar en ese estado

    episodios:
        cuantas veces repetimos la simulacion

    regresa:
        promedio de recompensa
    """

    total = 0
    for _ in range(episodios):
        estado_actual = estado_inicial

        # caminamos hasta que ya no haya accion definida
        while estado_actual in politica:
            accion = politica[estado_actual]
            estado_actual = transicion(estado_actual, accion)

        # ya llegamos a estado final
        r = recompensa_final(estado_actual)
        total += r

    return total / episodios


def mutar_politica(politica, acciones_disponibles):
    """
    crea una copia de la politica pero cambia 1 decision al azar

    acciones_disponibles:
        diccionario:
        estado -> lista de acciones que se pueden tomar ahi
    """

    nueva = politica.copy()

    # elegimos un estado al azar para mutar
    estado_a_cambiar = random.choice(list(politica.keys()))

    # elegimos una accion posible diferente si se puede
    opciones = acciones_disponibles[estado_a_cambiar]
    if len(opciones) > 1:
        # elegimos una accion random cualquiera
        nueva[estado_a_cambiar] = random.choice(opciones)
    else:
        # si solo hay una accion posible, no cambia
        nueva[estado_a_cambiar] = opciones[0]

    return nueva


if __name__ == "__main__":
    # definimos un mini "mundo":
    # estados:
    # A -> B -> C
    # o A -> X  (X es otro final malo)
    # desde B puedo ir a C (bueno) o X (malo)
    # llegar a C da mucha recompensa
    # terminar en X da poca o mala recompensa

    def transicion(estado, accion):
        # reglas de movimiento:
        # desde A:
        #   "a_B" -> voy a B
        #   "a_X" -> voy directo a X (final malo)
        # desde B:
        #   "b_C" -> voy a C (final bueno)
        #   "b_X" -> voy a X (final malo)
        # C y X son estados finales

        if estado == "A" and accion == "a_B":
            return "B"
        if estado == "A" and accion == "a_X":
            return "X"
        if estado == "B" and accion == "b_C":
            return "C"
        if estado == "B" and accion == "b_X":
            return "X"

        # si ya estoy en final, me quedo ahi
        return estado

    def recompensa_final(estado_final):
        # C es bueno, X es malo
        if estado_final == "C":
            # recompensa alta
            # le metemos un poco de random para que no sea fijo
            return random.randint(8, 12)
        if estado_final == "X":
            # casi nada o castigo
            return random.randint(-2, 2)
        # si cae en otro raro, 0
        return 0

    # acciones posibles por estado (politica decide 1 por estado)
    acciones_disponibles = {
        "A": ["a_B", "a_X"],
        "B": ["b_C", "b_X"]
        # nota: C y X ya son finales, no tienen accion
    }

    # politica inicial (puede ser mala al inicio, da igual)
    politica_actual = {
        "A": "a_X",  # manda directo a X (malo)
        "B": "b_X"   # manda a X (malo)
    }

    print("politica inicial:", politica_actual)

    # medimos que tan buena es la politica inicial
    score_actual = simular_con_politica(
        politica_actual,
        transicion,
        recompensa_final,
        estado_inicial="A",
        episodios=20
    )

    print("score promedio politica inicial:", score_actual)

    # ahora intentamos mejorar la politica varias veces
    for intento in range(10):
        # creo una version modificada (mutada)
        politica_nueva = mutar_politica(politica_actual, acciones_disponibles)

        # la pruebo
        score_nuevo = simular_con_politica(
            politica_nueva,
            transicion,
            recompensa_final,
            estado_inicial="A",
            episodios=20
        )

        print("\nintento", intento)
        print("  politica candidata:", politica_nueva)
        print("  score promedio candidato:", score_nuevo)

        # si la nueva politica es mejor, me quedo con ella
        if score_nuevo > score_actual:
            politica_actual = politica_nueva
            score_actual = score_nuevo
            print("  -> mejora aceptada ✅")
        else:
            print("  -> no mejora")

    print("\npolitica final aprendida:", politica_actual)
    print("score promedio final:", score_actual)

    # - empiezo con una politica X (puede ser mala)
    # - la pruebo varias veces y saco score promedio
    # - hago una version cambiando una decision
    # - si la nueva politica es mejor, la adopto
    
    # esto es busqueda de la politica:
    # no estoy aprendiendo valores Q ni valor de estado
    # estoy buscando directamente la mejor politica (que hacer en cada estado)