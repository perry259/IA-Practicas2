# Iteracion de valores
# calculamos que tan bueno es estar en cada estado
# suponiendo que vamos a actuar de forma inteligente.
# esto se usa en planeacion y aprendizaje por refuerzo.
# nos dice "cuanto voy a ganar si estoy en este estado y luego juego bien".
# valor(estado) = recompensa_inmediata + descuento * mejor_valor_de_los_estados_siguientes
# en este ejemplo:
# tenemos 3 estados: a, b, c
# en cada estado puedo tomar acciones que me llevan a otro estado y me dan una recompensa.
# iteracion de valores va actualizando los valores hasta que ya casi no cambian.

def iteracion_de_valores(estados, acciones_por_estado, transicion, recompensa, descuento, pasos_max):
    """
    estados:
        lista de estados, ejemplo ["a","b","c"]

    acciones_por_estado:
        diccionario que dice que acciones puedo hacer en cada estado
        ejemplo:
        {
          "a": ["ir_b", "ir_c"],
          "b": ["ir_c"],
          "c": []
        }

    transicion(estado, accion):
        funcion que dice a que estado voy si hago esa accion
        ejemplo: transicion("a","ir_b") -> "b"

    recompensa(estado, accion):
        funcion que regresa la recompensa inmediata de hacer esa accion
        ejemplo: recompensa("a","ir_b") -> 5

    descuento:
        numero entre 0 y 1
        dice que tanto me importa el futuro
        0.9 significa que me importa mucho el futuro
        0.0 significa que solo me importa lo inmediato

    pasos_max:
        cuantas veces actualizo los valores

    regresa:
        diccionario con el valor final aproximado de cada estado
    """
    # paso 1: inicializamos todos los valores en 0
    valores = {e: 0 for e in estados}

    # paso 2: repetimos actualizacion varias veces
    for _ in range(pasos_max):
        nuevos_valores = {}

        # calculo el nuevo valor para cada estado
        for estado in estados:
            acciones = acciones_por_estado[estado]

            if len(acciones) == 0:
                # si no hay acciones posibles, valor queda en 0 directo
                nuevos_valores[estado] = 0
            else:
                # evaluo cada accion posible
                estimaciones = []

                for acc in acciones:
                    siguiente = transicion(estado, acc)
                    r = recompensa(estado, acc)
                    # formula:
                    # valor estimado = recompensa inmediata + descuento * valor futuro
                    estimado = r + descuento * valores[siguiente]
                    estimaciones.append(estimado)

                # elijo la mejor accion (max)
                nuevos_valores[estado] = max(estimaciones)

        # actualizo
        valores = nuevos_valores

    return valores

def politica_greedy(estados, acciones_por_estado, transicion, recompensa, valores, descuento):
    """
    esta funcion saca la mejor accion para cada estado
    usando los valores ya calculados.

    para cada estado:
    elegimos la accion que da
    recompensa + descuento * valor(futuro)
    mas grande.
    """
    politica = {}

    for estado in estados:
        acciones = acciones_por_estado[estado]
        if len(acciones) == 0:
            politica[estado] = None
        else:
            mejor_accion = None
            mejor_score = None

            for acc in acciones:
                siguiente = transicion(estado, acc)
                r = recompensa(estado, acc)
                score = r + descuento * valores[siguiente]

                if (mejor_accion is None) or (score > mejor_score):
                    mejor_accion = acc
                    mejor_score = score

            politica[estado] = mejor_accion

    return politica

if __name__ == "__main__":
    # vamos a armar un mini mundo de 3 estados
    # estados:
    #  a -> b o c
    #  b -> c
    #  c -> c (ya es final, como "meta")
    # recompensas:
    #  ir de a a b = +5
    #  ir de a a c = +10
    #  ir de b a c = +2
    #  en c ya no hay accion, recompensa 0

    estados = ["a", "b", "c"]

    acciones_por_estado = {
        "a": ["ir_b", "ir_c"],
        "b": ["ir_c"],
        "c": []  # c no hace nada mas
    }

    def transicion(estado, accion):
        if estado == "a" and accion == "ir_b":
            return "b"
        if estado == "a" and accion == "ir_c":
            return "c"
        if estado == "b" and accion == "ir_c":
            return "c"
        if estado == "c":
            return "c"  # quedarse en c
        # fallback
        return estado

    def recompensa(estado, accion):
        if estado == "a" and accion == "ir_b":
            return 5
        if estado == "a" and accion == "ir_c":
            return 10
        if estado == "b" and accion == "ir_c":
            return 2
        # en c ya no ganas mas
        return 0

    descuento = 0.9  # me importa el futuro bastante
    pasos_max = 10   # cuantas rondas de actualizacion hago

    valores_finales = iteracion_de_valores(
        estados,
        acciones_por_estado,
        transicion,
        recompensa,
        descuento,
        pasos_max
    )

    print("valores estimados de cada estado:")
    for e in estados:
        print(" ", e, "->", valores_finales[e])

    # ahora, con esos valores, podemos decir
    # "cual accion es mejor en cada estado?"
    poli = politica_greedy(
        estados,
        acciones_por_estado,
        transicion,
        recompensa,
        valores_finales,
        descuento
    )

    print("\npolitica recomendada (mejor accion en cada estado):")
    for e in estados:
        print(" ", e, "->", poli[e])
    # - iteracion de valores calcula que tan bueno es cada estado
    # - lo hace pensando en que siempre escoges la mejor accion
    # - ya con esos valores puedes sacar una politica (que accion tomar en cada estado)