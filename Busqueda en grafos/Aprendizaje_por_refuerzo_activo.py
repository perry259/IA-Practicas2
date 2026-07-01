# Aprendizaje por refuerzo activo
# ahora el agente ya no solo observa.
# ahora el agente intenta APRENDER que accion tomar
# vamos a usar una mini tabla Q:
# Q[estado][accion] = que tan buena creemos que es esa accion en ese estado
# 1. estamos en un estado
# 2. elegimos una accion
# 3. vamos al siguiente estado y vemos la recompensa final
# 4. actualizamos Q
# al final, sacamos la "politica aprendida":
# para cada estado, cual accion tiene Q mas alto


import random


def elegir_accion(Q, estado, acciones_disponibles, prob_explorar):
    """
    elegimos una accion en este estado.

    prob_explorar:
        chance de probar algo random (explorar)
        esto evita que el agente siempre repita lo mismo sin probar otras cosas

    si no exploramos, elegimos la mejor accion segun Q.
    """

    # exploracion aleatoria
    if random.random() < prob_explorar:
        return random.choice(acciones_disponibles[estado])

    # explotacion (usar lo que ya creo que es mejor)
    mejor_accion = None
    mejor_valor = None

    for accion in acciones_disponibles[estado]:
        valor_q = Q[estado][accion]
        if (mejor_accion is None) or (valor_q > mejor_valor):
            mejor_accion = accion
            mejor_valor = valor_q

    return mejor_accion


def correr_un_episodio(Q, acciones_disponibles, transicion, recompensa_final, estado_inicial, prob_explorar, tasa_aprendizaje):
    """
    corre un episodio completo hasta el estado final.

    actualiza la Q en el proceso.

    Q:
        tabla Q[estado][accion] = valor estimado

    tasa_aprendizaje:
        que tanto ajustamos Q basado en lo que vimos (entre 0 y 1)

    prob_explorar:
        probabilidad de tomar una accion al azar (explorar)
    """

    estado_actual = estado_inicial
    historial = []  # guardamos (estado, accion) que tomamos

    # caminamos hasta llegar al estado final
    while True:
        # si este estado ya es final (sin acciones), paramos
        if len(acciones_disponibles[estado_actual]) == 0:
            break

        # elegimos accion (a veces probamos random)
        accion = elegir_accion(Q, estado_actual, acciones_disponibles, prob_explorar)

        # guardo la accion tomada en este estado
        historial.append((estado_actual, accion))

        # nos movemos al siguiente estado
        estado_siguiente = transicion(estado_actual, accion)

        # avanzamos
        estado_actual = estado_siguiente

    # ya terminamos episodio, estamos en estado_final
    r = recompensa_final(estado_actual)

    # ahora actualizamos Q hacia atras
    # a todas las (estado, accion) del episodio les subimos su valor hacia la recompensa final r
    for (estado_visitado, accion_tomada) in historial:
        valor_anterior = Q[estado_visitado][accion_tomada]

        # update tipo promedio movible:
        # nuevo_valor = viejo_valor + tasa * (recompensa_observada - viejo_valor)
        Q[estado_visitado][accion_tomada] = valor_anterior + tasa_aprendizaje * (r - valor_anterior)

    # regresamos la recompensa que se obtuvo en este episodio, por si queremos ver
    return r


def politica_aprendida(Q, acciones_disponibles):
    """
    con la Q aprendida, sacamos la mejor accion por estado
    """

    politica = {}

    for estado in acciones_disponibles:
        if len(acciones_disponibles[estado]) == 0:
            politica[estado] = None
        else:
            mejor_accion = None
            mejor_valor = None
            for accion in acciones_disponibles[estado]:
                q_val = Q[estado][accion]
                if (mejor_accion is None) or (q_val > mejor_valor):
                    mejor_accion = accion
                    mejor_valor = q_val
            politica[estado] = mejor_accion

    return politica


if __name__ == "__main__":
    # usamos el mismo mapa simple de antes:
    # A -> B -> C
    # C es final y da recompensa positiva

    estados = ["A", "B", "C"]

    acciones_disponibles = {
        "A": ["ir_a_B"],
        "B": ["ir_a_C"],
        "C": []  # en C ya se acaba
    }

    def transicion(estado, accion):
        if estado == "A" and accion == "ir_a_B":
            return "B"
        if estado == "B" and accion == "ir_a_C":
            return "C"
        return estado

    def recompensa_final(estado):
        # igual que antes, C da una recompensa entre 8 y 12
        if estado == "C":
            return random.randint(8, 12)
        return 0

    # inicializamos Q con puros 0
    Q = {}
    for estado in acciones_disponibles:
        Q[estado] = {}
        for accion in acciones_disponibles[estado]:
            Q[estado][accion] = 0.0

    # parametros del "agente"
    prob_explorar = 0.3      # 30% de las veces prueba algo random
    tasa_aprendizaje = 0.5   # que tan rapido ajusta lo que cree

    # corremos varios episodios para que el agente aprenda
    recompensas_obtenidas = []
    for _ in range(20):
        r_ep = correr_un_episodio(
            Q,
            acciones_disponibles,
            transicion,
            recompensa_final,
            estado_inicial="A",
            prob_explorar=prob_explorar,
            tasa_aprendizaje=tasa_aprendizaje
        )
        recompensas_obtenidas.append(r_ep)

    # mostramos la Q aprendida
    print("tabla Q aprendida (que tan buena es cada accion en cada estado):")
    for estado in Q:
        for accion in Q[estado]:
            print(" ", estado, ",", accion, "->", Q[estado][accion])

    # sacamos la politica final segun lo que aprendio
    poli = politica_aprendida(Q, acciones_disponibles)

    print("\npolitica aprendida (mejor accion por estado):")
    for estado in poli:
        print(" ", estado, "->", poli[estado])

    print("\nrecompensas vistas en cada episodio:", recompensas_obtenidas)

    # que significa esto:
    # - el agente probo, recibio recompensa y ajusto Q
    # - ya no es pasivo, ahora "aprende que hacer"
    # - esto ya es refuerzo activo basico