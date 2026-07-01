# Salto atras dirigido por conflictos
# es parecido a backtracking, pero mas listo.
# si una eleccion causa un problema, no solo me regreso 1 paso,
# salto directo hasta la variable que causo el conflicto.
# por eso se llama salto atras.
# hace la busqueda mas rapida porque no pierdo tiempo revisando cosas
# que no tienen la culpa del error.

def revisar_reglas(asignacion):
    """
    esta funcion revisa si lo que llevo asignado rompe alguna regla.
    si todo esta bien regresa (True, None)
    si hay problema regresa (False, info_del_conflicto)

    reglas que estamos usando en este ejemplo:
    1) no puedo tener dos examenes el mismo dia
    2) prog no puede ser lunes
    """

    # regla 1: no dos examenes el mismo dia
    # si mate = lunes y fisica = lunes -> conflicto
    for materia1 in asignacion:
        for materia2 in asignacion:
            if materia1 != materia2 and asignacion[materia1] == asignacion[materia2]:
                # conflicto porque misma fecha
                # regreso ("same_day", materia2) para saber con quien choco
                return False, ("same_day", materia2)

    # regla 2: prog no puede ser lunes
    if "prog" in asignacion and asignacion["prog"] == "lunes":
        return False, ("prog_lunes", None)

    # si llegue aqui no hay problema
    return True, None

def salto_atras_conflictos(variables, dominios):
    """
    esta funcion controla todo el proceso.
    variables: lista de variables que quiero asignar
               ejemplo: ["mate", "fisica", "prog"]
    dominios: diccionario con los valores posibles de cada variable
              ejemplo:
              {
                "mate": ["lunes","miercoles","viernes"],
                "fisica": ["lunes","miercoles","viernes"],
                "prog": ["lunes","miercoles","viernes"]
              }

    regresa:
    (solucion_dict, historial_debug)
    solucion_dict es una asignacion valida o None
    historial_debug es solo para imprimir el proceso
    """
    # mapeo de variable -> posicion en la lista
    # esto me sirve para saber a que nivel debo saltar
    indice_variable = {var: i for i, var in enumerate(variables)}

    historial_debug = []  # solo para entender que hizo el algoritmo

    def intentar(index, asignacion_actual):
        """
        index:
            en que variable voy (por posicion en la lista variables)
        asignacion_actual:
            diccionario con lo que llevo asignado hasta ahorita

        regresa:
        (solucion, saltar_a)
        solucion: dict con la solucion final si ya la encontre, o None
        saltar_a: a que index debo regresar si esto truena
                  ejemplo: 0, 1, etc
                  o None si no tengo que saltar mas
        """

        # si ya asigne todas las variables, ya termine bien
        if index == len(variables):
            return asignacion_actual.copy(), None

        var_actual = variables[index]

        mejor_salto = None  # a donde deberia saltar si nada sirve para esta variable

        # probamos cada valor posible para esta variable
        for valor in dominios[var_actual]:
            asignacion_actual[var_actual] = valor

            ok, conflicto = revisar_reglas(asignacion_actual)

            historial_debug.append(
                f"probando {var_actual} = {valor} -> {'ok' if ok else 'conflicto'}"
            )

            if ok:
                # si no hay conflicto, intento asignar la siguiente variable
                solucion, salto = intentar(index + 1, asignacion_actual)

                if solucion is not None:
                    return solucion, None  # ya encontre solucion final

                # si no hubo solucion mas adelante
                # y salto me dice que debo regresar mas atras que yo,
                # guardo ese salto
                if salto is not None and (mejor_salto is None or salto < mejor_salto):
                    mejor_salto = salto

            else:
                # hubo conflicto inmediato con este valor
                tipo_conflicto, data_extra = conflicto

                if tipo_conflicto == "same_day":
                    # choque porque dos materias quedaron el mismo dia
                    # conflictiva = la otra materia con la que choque
                    conflictiva = data_extra
                    # saco el index de esa materia conflictiva
                    salto_conflicto = indice_variable.get(conflictiva, index - 1)
                elif tipo_conflicto == "prog_lunes":
                    # conflicto directo con prog = lunes
                    salto_conflicto = indice_variable["prog"]
                else:
                    # fallback (no deberia pasar en este ejemplo)
                    salto_conflicto = index - 1

                # guardo el mejor (o sea, el mas chico)
                if mejor_salto is None or salto_conflicto < mejor_salto:
                    mejor_salto = salto_conflicto

            # seguimos probando otros valores de la misma variable
            # (no hacemos return todavia, porque quiza otro valor si funciona)

        # si ningun valor funciono para esta variable
        # entonces quitamos esta variable de la asignacion
        # y regresamos None + el indice donde deberiamos brincar para atras
        del asignacion_actual[var_actual]

        # mejor_salto me dice hasta donde debo saltar
        return None, mejor_salto

    solucion_final, _ = intentar(0, {})

    return solucion_final, historial_debug

if __name__ == "__main__":
    # ejemplo:
    # queremos asignar dias de examen para 3 materias
    # variables:
    variables = ["mate", "fisica", "prog"]

    # dominios:
    # ahora cada materia puede ser lunes, miercoles o viernes
    # esto deja chance de que no se empalmen
    dominios = {
        "mate": ["lunes", "miercoles", "viernes"],
        "fisica": ["lunes", "miercoles", "viernes"],
        "prog": ["lunes", "miercoles", "viernes"]
    }

    # reglas otra vez (las revisa revisar_reglas):
    # 1) no quiero dos examenes el mismo dia
    # 2) prog no puede ser lunes

    solucion, debug = salto_atras_conflictos(variables, dominios)

    print("solucion encontrada:", solucion)
    print("\npasos que intento el algoritmo:")
    for linea in debug:
        print(" ", linea)

    # - backtracking normal: regresa solo 1 nivel
    # - salto atras dirigido por conflictos:
    #   cuando hay un problema, salta directo a la variable que causo el problema
    #   esto ahorra revisar cosas que no tienen la culpa