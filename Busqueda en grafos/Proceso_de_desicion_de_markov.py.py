# Mdp proceso de decision de markov
# un mdp describe una decision por pasos:
# - tengo un estado actual
# - elijo una accion
# - recibo una recompensa
# - paso a un nuevo estado (con cierta probabilidad)
# meta:
# elegir una politica (que accion tomar en cada estado)
# para maximizar la recompensa total esperada a largo plazo.
# esto es la base de cosas como iteracion de valores (27)
# e iteracion de politicas (28).
# diferencia importante:
# aqui metemos probabilidad en la transicion.
def iteracion_de_valores_mdp(estados, acciones_por_estado, transicion_prob, recompensa, descuento, pasos_max):
    """
    esta funcion hace iteracion de valores pero en version mdp
    con transiciones probabilisticas.

    estados:
        lista de estados, ej ["a","b","c"]

    acciones_por_estado:
        dict estado -> lista de acciones posibles
        ej:
        {
          "a": ["ir_b","ir_c"],
          "b": ["ir_c"],
          "c": []
        }

    transicion_prob(estado, accion):
        regresa una lista de (estado_siguiente, probabilidad)
        ej:
        transicion_prob("a","ir_b") -> [("b", 1.0)]
        transicion_prob("a","ir_c") -> [("c", 1.0)]
        en un mdp real puede ser algo como:
        [("b",0.7),("c",0.3)]

    recompensa(estado, accion):
        regresa la recompensa inmediata por hacer esa accion
        ej:
        recompensa("a","ir_b") -> 5

    descuento:
        numero entre 0 y 1
        que tanto me importa el futuro

    pasos_max:
        cuantas rondas de actualizacion hago

    regresa:
        diccionario con el valor de cada estado
    """

    # inicializamos todos los valores en 0
    valores = {e: 0 for e in estados}

    # repetimos actualizacion
    for _ in range(pasos_max):
        nuevos_valores = {}

        for estado in estados:
            acciones = acciones_por_estado[estado]

            if len(acciones) == 0:
                # estado terminal
                nuevos_valores[estado] = 0
            else:
                # para cada accion calculo su "q-valor" esperado
                # q = recompensa + descuento * valor futuro esperado
                # valor futuro esperado = suma(prob * valor(siguiente))
                estimaciones_acciones = []

                for acc in acciones:
                    r = recompensa(estado, acc)

                    # valor futuro esperado con esa accion
                    valor_futuro = 0
                    for (sig_estado, prob) in transicion_prob(estado, acc):
                        valor_futuro += prob * valores[sig_estado]

                    q_valor = r + descuento * valor_futuro
                    estimaciones_acciones.append(q_valor)

                # valor del estado = mejor accion
                nuevos_valores[estado] = max(estimaciones_acciones)

        valores = nuevos_valores

    return valores

def politica_optima_mdp(estados, acciones_por_estado, transicion_prob, recompensa, descuento, valores):
    """
    esta funcion dice cual es la mejor accion en cada estado
    usando los valores ya calculados.

    estados:
        lista de estados

    valores:
        dict con el valor de cada estado (salida de iteracion_de_valores_mdp)

    regresa:
        politica_optima: dict estado -> mejor accion
    """

    politica = {}

    for estado in estados:
        acciones = acciones_por_estado[estado]
        if len(acciones) == 0:
            politica[estado] = None
        else:
            mejor_accion = None
            mejor_q = None

            for acc in acciones:
                r = recompensa(estado, acc)

                # valor futuro esperado = suma(prob * valor(sig))
                valor_futuro = 0
                for (sig_estado, prob) in transicion_prob(estado, acc):
                    valor_futuro += prob * valores[sig_estado]

                q_valor = r + descuento * valor_futuro

                if (mejor_accion is None) or (q_valor > mejor_q):
                    mejor_accion = acc
                    mejor_q = q_valor

            politica[estado] = mejor_accion

    return politica

if __name__ == "__main__":
    # vamos a armar un mdp muy pequeño de ejemplo
    # estados:
    # a, b, c
    # acciones posibles:
    # desde a: puedo ir_b o ir_c
    # desde b: puedo ir_c
    # desde c: no hago nada (terminal)
    # recompensas:
    # a -> b : +5
    # a -> c : +10
    # b -> c : +2
    # c -> nada : 0
    # transicion_prob:
    # aqui lo hare casi determinista (prob 1.0),
    # pero lo escribo en formato probabilidades
    # porque asi es un mdp real.

    estados = ["a", "b", "c"]

    acciones_por_estado = {
        "a": ["ir_b", "ir_c"],
        "b": ["ir_c"],
        "c": []
    }

    def transicion_prob(estado, accion):
        # esta funcion regresa lista de (siguiente_estado, probabilidad)
        if estado == "a" and accion == "ir_b":
            return [("b", 1.0)]
        if estado == "a" and accion == "ir_c":
            return [("c", 1.0)]
        if estado == "b" and accion == "ir_c":
            return [("c", 1.0)]
        if estado == "c":
            return [("c", 1.0)]
        # si algo raro pasa, me quedo donde estoy
        return [(estado, 1.0)]

    def recompensa(estado, accion):
        if estado == "a" and accion == "ir_b":
            return 5
        if estado == "a" and accion == "ir_c":
            return 10
        if estado == "b" and accion == "ir_c":
            return 2
        return 0

    descuento = 0.9

    # 1) calculamos los valores de cada estado con iteracion de valores para mdp
    valores = iteracion_de_valores_mdp(
        estados,
        acciones_por_estado,
        transicion_prob,
        recompensa,
        descuento,
        pasos_max=10
    )

    print("valores estimados de cada estado (mdp):")
    for e in estados:
        print(" ", e, "->", valores[e])

    # 2) sacamos la politica optima: mejor accion en cada estado
    politica = politica_optima_mdp(
        estados,
        acciones_por_estado,
        transicion_prob,
        recompensa,
        descuento,
        valores
    )

    print("\npolitica optima segun el mdp:")
    for e in estados:
        print(" ", e, "->", politica[e])

    # - un mdp usa probabilidad en las transiciones
    # - el valor de un estado es: recompensa + descuento * valor futuro esperado
    # - la politica optima te dice que accion tomar en cada estado
    # - esto es la base de muchos metodos de control y de rl (aprendizaje por refuerzo)