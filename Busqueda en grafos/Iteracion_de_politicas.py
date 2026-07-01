# Iteracion de politicas
# una politica dice que accion tomar en cada estado.
# 1) evalua esa politica (que tan buena es si la sigo)
# 2) trata de mejorarla cambiando las acciones donde convenga
# repite hasta que la politica ya no cambia.
# sirve para encontrar una politica buena (que deberia hacer en cada estado)
# en problemas de decision por pasos (tipo mdp).

def evaluar_politica(estados, politica, acciones_por_estado, transicion, recompensa, descuento, pasos_eval):
    """
    esta funcion calcula el "valor" de cada estado
    si yo sigo la politica actual.

    estados:
        lista de estados, ej ["a","b","c"]

    politica:
        diccionario que dice que accion tomar en cada estado
        ej: {"a":"ir_b", "b":"ir_c", "c":None}

    acciones_por_estado:
        diccionario de acciones posibles por estado

    transicion(estado, accion):
        regresa a que estado voy si hago esa accion

    recompensa(estado, accion):
        regresa la recompensa inmediata de hacer esa accion

    descuento:
        que tanto me importa el futuro (0 a 1)

    pasos_eval:
        cuantas rondas de actualizacion hacemos para aproximar los valores

    regresa:
        diccionario valores[estado] con cuanto vale cada estado
        asumiendo que sigo la politica fija
    """

    # empezamos con 0 para todos
    valores = {e: 0 for e in estados}

    # repetimos varias veces para aproximar (esto es evaluacion iterativa)
    for _ in range(pasos_eval):
        nuevos_valores = {}

        for estado in estados:
            accion = politica[estado]

            if accion is None:
                # si no hay accion en este estado (estado terminal)
                nuevos_valores[estado] = 0
            else:
                siguiente = transicion(estado, accion)
                r = recompensa(estado, accion)
                # valor = recompensa + descuento * valor futuro segun la misma politica
                nuevos_valores[estado] = r + descuento * valores[siguiente]

        valores = nuevos_valores

    return valores


def mejorar_politica(estados, acciones_por_estado, transicion, recompensa, descuento, valores_actuales):
    """
    esta funcion intenta mejorar la politica:
    para cada estado, ve todas las acciones posibles
    y escoge la que tenga mejor score:
    score = recompensa + descuento * valor(futuro)

    estados:
        lista de estados

    acciones_por_estado:
        dict: estado -> lista de acciones validas

    valores_actuales:
        dict con el valor estimado de cada estado
        (esto viene de evaluar_politica)

    regresa:
        nueva_politica dict
    """

    nueva_politica = {}

    for estado in estados:
        acciones = acciones_por_estado[estado]

        if len(acciones) == 0:
            nueva_politica[estado] = None
        else:
            mejor_accion = None
            mejor_score = None

            for acc in acciones:
                siguiente = transicion(estado, acc)
                r = recompensa(estado, acc)
                score = r + descuento * valores_actuales[siguiente]

                if (mejor_accion is None) or (score > mejor_score):
                    mejor_accion = acc
                    mejor_score = score

            nueva_politica[estado] = mejor_accion

    return nueva_politica


def politicas_iguales(p1, p2):
    """
    checa si dos politicas son iguales (estado por estado)
    regresa True o False
    """
    for estado in p1:
        if p1[estado] != p2[estado]:
            return False
    return True


def iteracion_de_politicas(estados, acciones_por_estado, transicion, recompensa, descuento, pasos_eval, pasos_mejora):
    """
    estados:
        lista de estados, ej ["a","b","c"]

    acciones_por_estado:
        dict con las acciones posibles en cada estado

    transicion(estado, accion):
        a que estado pasas si haces esa accion

    recompensa(estado, accion):
        recompensa por esa accion

    descuento:
        cuanto valoras el futuro (0..1)

    pasos_eval:
        cuantas rondas usamos al evaluar la politica

    pasos_mejora:
        cuantas veces vamos a intentar mejorar la politica

    regresa:
        (politica_final, valores_finales)
    """

    # paso 0: politica inicial cualquiera
    # por ejemplo tomamos siempre la primera accion disponible en cada estado
    politica = {}
    for estado in estados:
        acciones = acciones_por_estado[estado]
        if len(acciones) == 0:
            politica[estado] = None
        else:
            politica[estado] = acciones[0]

    # mejoramos la politica varias veces
    for _ in range(pasos_mejora):
        # 1. evaluo la politica actual (cuanto vale cada estado si sigo esta politica)
        valores = evaluar_politica(
            estados,
            politica,
            acciones_por_estado,
            transicion,
            recompensa,
            descuento,
            pasos_eval
        )

        # 2. genero una politica nueva mas greedy con respecto a esos valores
        nueva_politica = mejorar_politica(
            estados,
            acciones_por_estado,
            transicion,
            recompensa,
            descuento,
            valores
        )

        # 3. si ya no cambio la politica, paro
        if politicas_iguales(politica, nueva_politica):
            return nueva_politica, valores

        politica = nueva_politica

    # si sali del for sin converger, regreso lo que tenga
    return politica, valores


if __name__ == "__main__":
    # vamos a usar el mismo mundo simple del ejercicio 27
    # estados:
    #   a -> puedo ir a b o ir a c
    #   b -> puedo ir a c
    #   c -> ya es final
    # recompensas:
    #   a -> b = +5
    #   a -> c = +10
    #   b -> c = +2
    #   c no da nada mas

    estados = ["a", "b", "c"]

    acciones_por_estado = {
        "a": ["ir_b", "ir_c"],
        "b": ["ir_c"],
        "c": []
    }

    def transicion(estado, accion):
        if estado == "a" and accion == "ir_b":
            return "b"
        if estado == "a" and accion == "ir_c":
            return "c"
        if estado == "b" and accion == "ir_c":
            return "c"
        if estado == "c":
            return "c"
        return estado

    def recompensa(estado, accion):
        if estado == "a" and accion == "ir_b":
            return 5
        if estado == "a" and accion == "ir_c":
            return 10
        if estado == "b" and accion == "ir_c":
            return 2
        return 0

    descuento = 0.9

    # pasos_eval:
    # cuantas rondas usamos para evaluar una politica fija
    # pasos_mejora:
    # cuantas veces dejamos que intente mejorar su politica
    politica_final, valores_finales = iteracion_de_politicas(
        estados,
        acciones_por_estado,
        transicion,
        recompensa,
        descuento,
        pasos_eval=10,
        pasos_mejora=10
    )

    print("politica final (mejor accion en cada estado):")
    for e in estados:
        print(" ", e, "->", politica_final[e])

    print("\nvalores finales estimados de cada estado:")
    for e in estados:
        print(" ", e, "->", valores_finales[e])

    # - la politica dice que accion tomar
    # - evaluo esa politica (cuanto vale seguirla)
    # - luego la mejoro
    # - repito hasta que ya no mejora