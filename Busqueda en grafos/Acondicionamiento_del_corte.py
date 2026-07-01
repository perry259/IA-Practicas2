# acondicionamiento del corte
# en algunos problemas con muchas restricciones, hay variables que conectan
# o chocan con muchas otras. esas variables son las que complican todo.
# la idea es: asigno primero esas variables "problematicas" con todos sus valores posibles,
# y luego resuelvo el resto normalmente.
# esto rompe el problema grande en problemas mas faciles.
# basicamente es: pruebo opciones para las variables dificiles,
# y cada opcion genera un subproblema mas sencillo.

def es_valida(asignacion, reglas):
    """
    revisa si las reglas se cumplen con la asignacion actual
    regresa True o False
    """
    for r in reglas:
        if not r(asignacion):
            return False
    return True


def backtracking_simple(variables, dominios, reglas, asignacion_actual=None):
    """
    este es un backtracking normal, sin cosas raras.
    lo usamos despues de fijar las variables del corte.

    variables:
        lista de variables que faltan por asignar
    dominios:
        valores posibles para cada variable
    reglas:
        lista de funciones que validan la asignacion

    asignacion_actual:
        lo que ya llevo asignado

    regresa:
        diccionario solucion completa o None si no se pudo
    """

    if asignacion_actual is None:
        asignacion_actual = {}

    # si ya asigne todas las variables, reviso si cumple reglas finales
    if len(asignacion_actual) == len(variables):
        if es_valida(asignacion_actual, reglas):
            return asignacion_actual.copy()
        else:
            return None

    # busco una variable que todavia no tenga valor
    for v in variables:
        if v not in asignacion_actual:
            var_pendiente = v
            break

    # intento cada valor posible para esa variable
    for valor in dominios[var_pendiente]:
        nueva = asignacion_actual.copy()
        nueva[var_pendiente] = valor

        if es_valida(nueva, reglas):
            resultado = backtracking_simple(
                variables,
                dominios,
                reglas,
                nueva
            )
            if resultado is not None:
                return resultado

    # si ningun valor sirvio
    return None


def generar_asignaciones_cutset(cutset_vars, dominios, reglas, base=None):
    """
    genera todas las posibles asignaciones para las variables del "cutset"
    (el conjunto que quiero fijar primero)

    cutset_vars:
        lista de variables del corte (las conflictivas)
        ejemplo: ["mate"]

    dominios:
        diccionario con lista de valores posibles por variable

    reglas:
        lista de reglas que deben cumplirse

    base:
        asignacion que ya llevo hecha de estas mismas variables

    regresa:
        lista de asignaciones posibles (todas las combinaciones validas)
        ejemplo:
        [
          {"mate": "lunes"},
          {"mate": "miercoles"}
        ]
    """
    if base is None:
        base = {}

    # si ya asigne todas las variables del cutset, regreso esta combinacion
    if len(base) == len(cutset_vars):
        # valido que cumpla las reglas
        if es_valida(base, reglas):
            return [base.copy()]
        else:
            return []

    # si aun faltan variables del cutset
    idx = len(base)
    var_actual = cutset_vars[idx]

    posibles = []
    for valor in dominios[var_actual]:
        nueva = base.copy()
        nueva[var_actual] = valor

        # checo si sigue valido hasta ahora
        if es_valida(nueva, reglas):
            siguientes = generar_asignaciones_cutset(
                cutset_vars,
                dominios,
                reglas,
                nueva
            )
            posibles.extend(siguientes)

    return posibles

def acondicionamiento_del_corte(variables, dominios, reglas, cutset_vars):
    """
    variables:
        todas las variables del problema
        ejemplo: ["mate","fisica","prog"]

    dominios:
        valores posibles de cada variable
        ejemplo:
        {
          "mate":["lunes","miercoles","viernes"],
          "fisica":["lunes","miercoles","viernes"],
          "prog":["lunes","miercoles","viernes"]
        }

    reglas:
        lista de funciones que regresan True/False

    cutset_vars:
        lista de variables que voy a fijar primero
        ejemplo:
        ["mate"]
        idea: estas son las variables "conflictivas"

    regresa:
        una solucion valida completa o None si no hay
    """

    # 1. genero todas las posibles asignaciones validas
    #    de las variables del corte (cutset)
    opciones_cutset = generar_asignaciones_cutset(
        cutset_vars,
        dominios,
        reglas
        # base None
    )

    # 2. por cada opcion del cutset, resuelvo el resto con backtracking normal
    for asign_cutset in opciones_cutset:
        # variables que faltan despues del cutset
        restantes = [v for v in variables if v not in asign_cutset]

        # empiezo con lo que ya fije en el cutset
        solucion_restante = backtracking_simple(
            restantes,
            dominios,
            reglas,
            asign_cutset.copy()
        )

        if solucion_restante is not None:
            return solucion_restante  # encontramos solucion completa

    # si ninguna opcion del cutset funciono, no hay solucion
    return None

if __name__ == "__main__":
    # ejemplo: horario de examenes otra vez
    # variables = materias
    variables = ["mate", "fisica", "prog"]

    # dominios = dias posibles para cada materia
    dominios = {
        "mate": ["lunes", "miercoles", "viernes"],
        "fisica": ["lunes", "miercoles", "viernes"],
        "prog": ["lunes", "miercoles", "viernes"]
    }

    # reglas:
    # 1) no quiero dos examenes el mismo dia
    def regla_no_mismo_dia(asignacion):
        # ejemplo asignacion: {"mate":"miercoles","fisica":"miercoles"}
        dias = list(asignacion.values())
        # si hay valores repetidos en dias, es conflicto
        return len(dias) == len(set(dias))

    # 2) prog no puede ser lunes
    def regla_prog_no_lunes(asignacion):
        if "prog" in asignacion:
            return asignacion["prog"] != "lunes"
        return True

    reglas = [regla_no_mismo_dia, regla_prog_no_lunes]
    # ahora, que es cutset_vars?
    # idea: escogemos una o varias variables "duras" (las que causan mas problemas)
    # y las fijamos primero probando sus valores.
    # por ejemplo, vamos a fijar primero "mate".
    cutset_vars = ["mate"]

    solucion = acondicionamiento_del_corte(
        variables=variables,
        dominios=dominios,
        reglas=reglas,
        cutset_vars=cutset_vars
    )

    print("solucion con acondicionamiento del corte:", solucion)
    # - escogemos algunas variables criticas (cutset_vars)
    # - probamos todas las opciones validas de esas variables primero
    # - luego resolvemos el resto normal
    # - esto reduce la dificultad del problema grande