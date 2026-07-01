# Aprendizaje por refuerzo pasivo
# - el agente ya tiene una politica fija (ya sabe que accion tomar en cada estado)
# - el agente NO trata de cambiar la politica todavia
# - solo observa episodios y aprende "que tan bueno es cada estado"
# en otras palabras:
# aprende los valores de los estados, pero no decide mejor aun.
# este ejemplo:
# tenemos 3 estados: "A", "B", "C"
# "C" es un estado final con recompensa +10
# politica fija:
# A -> ir_a_B
# B -> ir_a_C
# C -> nada (ya termino)
# vamos a simular episodios de A -> B -> C
# y usar promedio para estimar el valor de cada estado

import random

def simular_episodio(politica, transicion, recompensa, estado_inicial):
    """
    corre un episodio siguiendo la politica fija,
    hasta llegar a un estado final.

    regresa una lista con (estado, retorno_desde_ahi)

    ejemplo del retorno:
    si el episodio fue A -> B -> C
    y en C ganas +10
    entonces:
        retorno en C = 10
        retorno en B = 10 (porque desde B llegaste a 10)
        retorno en A = 10 (porque desde A llegaste a 10)
    """

    estado_actual = estado_inicial
    recorrido = []  # guardaremos los estados visitados en orden

    while True:
        recorrido.append(estado_actual)

        # si ya no hay accion en este estado, paramos episodio
        if politica.get(estado_actual) is None:
            break

        # accion a tomar segun la politica fija
        accion = politica[estado_actual]

        # siguiente estado segun el modelo transicion
        estado_siguiente = transicion(estado_actual, accion)

        estado_actual = estado_siguiente

    # ya terminamos. el ultimo estado (ej: "C") tiene recompensa
    r_final = recompensa(estado_actual)

    # ahora calculamos el retorno para cada estado del episodio
    # en este ejemplo, toda la ganancia ocurre al final,
    # asi que todos los estados reciben la misma recompensa final.
    retorno_por_estado = []
    for est in recorrido:
        retorno_por_estado.append((est, r_final))

    return retorno_por_estado


def aprender_valores_pasivo(episodios, politica, transicion, recompensa, estado_inicial):
    """
    corre varios episodios siguiendo la politica fija
    y aprende el valor promedio de cada estado.

    episodios:
        cuantas veces repetimos la experiencia

    regresa:
        diccionario valores_estimados[estado] = promedio de retorno
    """

    # guardaremos todas las muestras de retorno que vimos por estado
    retornos = {}  # estado -> lista de retornos vistos
    for _ in range(episodios):
        datos_ep = simular_episodio(politica, transicion, recompensa, estado_inicial)

        # datos_ep es lista de (estado, retorno)
        for (estado, ret) in datos_ep:
            if estado not in retornos:
                retornos[estado] = []
            retornos[estado].append(ret)

    # calculamos promedio de retorno por estado
    valores_estimados = {}
    for estado in retornos:
        lista = retornos[estado]
        prom = sum(lista) / len(lista)
        valores_estimados[estado] = prom

    return valores_estimados


if __name__ == "__main__":
    # definimos los estados
    estados = ["A", "B", "C"]

    # politica fija (no la vamos a cambiar en el modo pasivo)
    # esta politica siempre avanza hacia C
    politica = {
        "A": "ir_a_B",
        "B": "ir_a_C",
        "C": None  # ya termino
    }

    # modelo de transicion
    # aqui lo hacemos determinista para mantenerlo simple
    def transicion(estado, accion):
        if estado == "A" and accion == "ir_a_B":
            return "B"
        if estado == "B" and accion == "ir_a_C":
            return "C"
        # si algo raro pasa, nos quedamos donde estamos
        return estado

    # recompensa: solo el estado final C da puntos
    def recompensa(estado):
        if estado == "C":
            # para que no sea siempre igual,
            # metemos un poco de variacion random,
            # simulando que a veces el final fue mejor o peor
            # por ejemplo entre 8 y 12
            return random.randint(8, 12)
        else:
            return 0

    # ahora aprendemos valores corriendo muchos episodios
    valores = aprender_valores_pasivo(
        episodios=20,              # cuantas experiencias juntamos
        politica=politica,         # politica fija
        transicion=transicion,     # como nos movemos
        recompensa=recompensa,     # que ganamos al final
        estado_inicial="A"         # siempre empezamos desde A
    )

    print("valores aprendidos (estimacion de que tan bueno es cada estado):")
    for estado in valores:
        print(" ", estado, "->", valores[estado])

    # que significa esto:
    # - valor(A) es que tan bueno es empezar en A si sigo esta politica
    # - valor(B) es que tan bueno es estar en B si sigo esta politica
    # - valor(C) es lo que gano al terminar
    #
    # esto es "aprendizaje por refuerzo PASIVO":
    # NO estoy cambiando lo que hago,
    # solo estoy aprendiendo cuanta recompensa espero obtener desde cada estado.