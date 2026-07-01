# busqueda local: minimos-conflictos
# este metodo empieza con una asignacion cualquiera (aunque este mal)
# y luego va arreglando las variables que causan conflicto
# cambiandolas al valor que cause menos conflictos.
# es rapido para problemas grandes tipo horarios, colores de mapa, etc.
# en vez de probar todo desde cero, solo voy corrigiendo lo que esta mal.
# esto es busqueda local, no recursion como antes.

import random

def contar_conflictos(asignacion, reglas):
    """
    asignacion:
        diccionario con valores actuales
        ejemplo: {"mate":"lunes","fisica":"lunes","prog":"miercoles"}

    reglas:
        lista de funciones que revisan si hay conflicto

    regresa:
        cuantas reglas se estan rompiendo
        numero mas alto = peor
    """
    conflictos = 0
    for regla in reglas:
        if not regla(asignacion):
            conflictos += 1
    return conflictos

def materias_en_conflicto(asignacion, reglas):
    """
    regresa una lista con las variables (materias)
    que estan causando conflictos ahorita

    idea:
    probamos quitar/alterar esa materia y vemos si baja el conflicto
    """
    malas = set()
    # reviso cada regla
    for regla in reglas:
        if not regla(asignacion):
            # si una regla esta mal, trato de adivinar cuales materias estan metidas
            # como este ejemplo es simple, vamos a marcar todas las materias
            # involucradas en la asignacion actual
            for materia in asignacion:
                malas.add(materia)

    return list(malas)

def mejor_valor_para(materia, asignacion, dominios, reglas):
    """
    esta funcion intenta todos los valores posibles de 'materia'
    y escoge el que deja MENOS conflictos

    materia:
        ej: "mate"

    asignacion:
        diccionario actual (se modificara temporalmente para probar)

    dominios:
        todas las opciones posibles de cada variable
        ej:
        {
          "mate":["lunes","miercoles","viernes"],
          "fisica":["lunes","miercoles","viernes"],
          "prog":["lunes","miercoles","viernes"]
        }

    reglas:
        lista de funciones que validan

    regresa:
        el mejor valor encontrado para esa materia
    """
    mejor_opcion = None
    mejor_conf = None

    for posible_valor in dominios[materia]:
        # probamos asignando este valor
        copia = asignacion.copy()
        copia[materia] = posible_valor

        # contamos conflictos con ese cambio
        conf = contar_conflictos(copia, reglas)

        if (mejor_opcion is None) or (conf < mejor_conf):
            mejor_opcion = posible_valor
            mejor_conf = conf

    return mejor_opcion

def minimos_conflictos(variables, dominios, reglas, intentos_max, pasos_max):
    """
    variables:
        lista de variables que quiero asignar (ej: ["mate","fisica","prog"])
    dominios:
        diccionario con los valores posibles para cada variable
    reglas:
        lista de funciones que regresan True si todo bien, False si hay conflicto
    intentos_max:
        cuantas veces voy a reiniciar si no encuentro solucion
    pasos_max:
        cuantas correcciones voy a intentar en un mismo intento

    regresa:
        (asignacion_valida, historial_pasos)
        asignacion_valida = diccionario solucion o None
        historial_pasos = lista con las asignaciones que se fueron probando
    """
    historial_pasos = []
    for _ in range(intentos_max):
        # paso 1: creo una asignacion inicial aleatoria
        asignacion = {}
        for var in variables:
            asignacion[var] = random.choice(dominios[var])

        # guardo esta asignacion inicial en historial
        historial_pasos.append(asignacion.copy())

        # paso 2: intento arreglarla paso por paso
        for _ in range(pasos_max):
            # si ya no hay conflictos, ya termine
            if contar_conflictos(asignacion, reglas) == 0:
                return asignacion, historial_pasos

            # veo cuales materias estan metiendo conflicto
            malas = materias_en_conflicto(asignacion, reglas)

            if not malas:
                # no detecto materias malas, lo tomo como solucion
                return asignacion, historial_pasos

            # elijo una materia con problema (al azar de las conflictivas)
            materia_a_arreglar = random.choice(malas)

            # busco el valor que deje menos conflicto para esa materia
            mejor_val = mejor_valor_para(
                materia_a_arreglar,
                asignacion,
                dominios,
                reglas
            )

            # aplico el cambio
            asignacion[materia_a_arreglar] = mejor_val

            # guardo estado despues del cambio
            historial_pasos.append(asignacion.copy())

        # si llegue aqui, no pude dejarlo sin conflicto en este intento
        # voy a reiniciar (otro intento con otra asignacion aleatoria)

    # si no salio solucion en ningun intento, regreso None
    return None, historial_pasos

if __name__ == "__main__":
    # vamos a usar el mismo tipo de ejemplo de examenes
    variables = ["mate", "fisica", "prog"]

    dominios = {
        "mate": ["lunes", "miercoles", "viernes"],
        "fisica": ["lunes", "miercoles", "viernes"],
        "prog": ["lunes", "miercoles", "viernes"]
    }

    # reglas:
    # 1) no quiero dos examenes el mismo dia
    def regla_no_mismo_dia(asignacion):
        # ejemplo asignacion:
        # {"mate":"lunes","fisica":"miercoles","prog":"lunes"}
        dias = list(asignacion.values())
        # si hay repetidos en dias, hay conflicto
        return len(dias) == len(set(dias))

    # 2) prog no puede ser lunes
    def regla_prog_no_lunes(asignacion):
        if "prog" in asignacion:
            return asignacion["prog"] != "lunes"
        return True

    reglas = [regla_no_mismo_dia, regla_prog_no_lunes]

    # corremos el algoritmo de minimos conflictos
    solucion, historial = minimos_conflictos(
        variables=variables,
        dominios=dominios,
        reglas=reglas,
        intentos_max=10,   # cuantas veces reinicio desde cero si no queda
        pasos_max=20       # cuantos cambios intento hacer por intento
    )

    print("solucion encontrada:", solucion)

    print("\nproceso (historial de asignaciones que se probaron):")
    for paso_idx, asign in enumerate(historial):
        print(" paso", paso_idx, "->", asign)
    # - empiezo con algo aleatorio aunque este mal
    # - busco que variable causa problemas
    # - cambio solo esa variable al valor que cause menos conflicto
    # - es busqueda local, no recursion.