# q-learning
# q-learning aprende que accion tomar en cada estado
# sin que le des una politica fija.
# guarda una tabla Q:
# Q[estado][accion] = valor esperado de hacer esa accion en ese estado
# formula de actualizacion:
# Q(s,a) = Q(s,a) + alpha * ( recompensa + gamma * max_a' Q(siguiente, a') - Q(s,a) )
# donde:
# - s es el estado actual
# - a es la accion que tomaste
# - recompensa es lo que ganaste en ese paso
# - siguiente es el nuevo estado
# - gamma es cuanto valoras el futuro
# - alpha es que tanto corriges lo que creias

import random

def elegir_accion(Q, estado, acciones_disponibles, prob_explorar):
    """
    elegimos una accion en este estado usando e-greedy:
    - con cierta prob. exploramos (random)
    - si no, elegimos la mejor accion segun Q
    """

    # si este estado no tiene acciones (estado final), regresamos None
    if len(acciones_disponibles[estado]) == 0:
        return None

    # explorar (accion random)
    if random.random() < prob_explorar:
        return random.choice(acciones_disponibles[estado])

    # explotar (mejor accion conocida)
    mejor_accion = None
    mejor_valor = None

    for accion in acciones_disponibles[estado]:
        valor_q = Q[estado][accion]
        if (mejor_accion is None) or (valor_q > mejor_valor):
            mejor_accion = accion
            mejor_valor = valor_q

    return mejor_accion


def max_q(Q, estado, acciones_disponibles):
    """
    regresa el maximo Q(estado, accion) sobre todas las acciones posibles en ese estado.
    si no hay acciones (estado final), regresa 0.
    """
    if len(acciones_disponibles[estado]) == 0:
        return 0.0

    mejor = None
    for accion in acciones_disponibles[estado]:
        valor = Q[estado][accion]
        if (mejor is None) or (valor > mejor):
            mejor = valor
    return mejor


def correr_q_learning(
    estados,
    acciones_disponibles,
    transicion,
    recompensa_step,
    estado_inicial,
    alpha,          # tasa de aprendizaje
    gamma,          # descuento futuro
    prob_explorar,  # probabilidad de accion random
    episodios_max
):
    """
    entrena Q-learning por varios episodios

    recompensa_step:
        funcion que dice la recompensa inmediata al hacer esa accion
        (nota: a diferencia de antes, aqui vamos a dar recompensa en el paso
         no solo al final, pero igual la podemos hacer simple)

    regresa:
        la tabla Q aprendida
    """

    # inicializamos Q en 0s
    Q = {}
    for estado in estados:
        Q[estado] = {}
        for accion in acciones_disponibles[estado]:
            Q[estado][accion] = 0.0

    # corremos muchos episodios de entrenamiento
    for _ in range(episodios_max):
        estado_actual = estado_inicial

        # seguimos hasta llegar a estado final (sin acciones)
        while True:
            accion = elegir_accion(Q, estado_actual, acciones_disponibles, prob_explorar)

            if accion is None:
                # ya estamos en estado terminal
                break

            # nos movemos
            estado_siguiente = transicion(estado_actual, accion)

            # recompensa inmediata de hacer esa accion
            r = recompensa_step(estado_actual, accion, estado_siguiente)

            # mejor valor futuro desde el estado siguiente
            mejor_futuro = max_q(Q, estado_siguiente, acciones_disponibles)

            # valor actual de Q(s,a)
            valor_viejo = Q[estado_actual][accion]

            # aplicamos la formula de q-learning
            # nuevo = viejo + alpha * (r + gamma*mejor_futuro - viejo)
            Q[estado_actual][accion] = valor_viejo + alpha * (
                r + gamma * mejor_futuro - valor_viejo
            )

            # actualizamos el estado actual
            estado_actual = estado_siguiente

    return Q


def politica_desde_Q(Q, acciones_disponibles):
    """
    saca la mejor accion por estado viendo los Q aprendidos
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
    # mundo simple:
    # A -> B -> C
    # en A puedes ir a B
    # en B puedes ir a C
    # C es final

    estados = ["A", "B", "C"]

    acciones_disponibles = {
        "A": ["ir_a_B"],
        "B": ["ir_a_C"],
        "C": []  # final
    }

    def transicion(estado, accion):
        if estado == "A" and accion == "ir_a_B":
            return "B"
        if estado == "B" and accion == "ir_a_C":
            return "C"
        return estado

    def recompensa_step(estado, accion, estado_siguiente):
        # aqui hago algo sencillo:
        # solo doy recompensa grande cuando llego a C
        if estado_siguiente == "C":
            # metemos un poco de variacion para que aprenda promedio
            return random.randint(8, 12)
        else:
            return 0

    alpha = 0.5          # tasa de aprendizaje
    gamma = 0.9          # descuento futuro (me importa el futuro)
    prob_explorar = 0.3  # 30% de las veces exploro
    episodios_max = 30   # cuantas veces entreno

    Q_aprendido = correr_q_learning(
        estados,
        acciones_disponibles,
        transicion,
        recompensa_step,
        estado_inicial="A",
        alpha=alpha,
        gamma=gamma,
        prob_explorar=prob_explorar,
        episodios_max=episodios_max
    )

    print("tabla Q aprendida:")
    for estado in Q_aprendido:
        for accion in Q_aprendido[estado]:
            print(" ", estado, ",", accion, "->", Q_aprendido[estado][accion])

    poli = politica_desde_Q(Q_aprendido, acciones_disponibles)

    print("\npolitica sugerida (mejor accion por estado):")
    for estado in poli:
        print(" ", estado, "->", poli[estado])

    # - q-learning ajusta la tabla Q durante la experiencia
    # - despues de entrenar, para cada estado elegimos la accion con Q mas alto
    # - eso es la politica aprendida