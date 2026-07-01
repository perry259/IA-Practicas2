# comprobacion hacia delante
# cuando asigno una variable, reviso de inmediato si las demas variables
# todavia tienen opciones validas o ya se quedaron sin opciones.
# esto ayuda a detectar rapido caminos que no van a funcionar.
# asi no seguimos probando algo que ya esta muerto.
# diferencia vs backtracking normal:
# backtracking se da cuenta mas tarde.
# comprobacion hacia delante (forward checking) lo revisa antes de seguir.

def es_valida(asignacion, restricciones):
    """
    asignacion:
        diccionario con lo que llevo asignado hasta ahorita
        ejemplo:
        {"mate": "lunes", "fisica": "miercoles"}

    restricciones:
        lista de reglas. cada regla es una funcion que regresa True o False

    regresa:
        True si ninguna regla se rompe
        False si alguna regla se rompio
    """
    for regla in restricciones:
        if not regla(asignacion):
            return False
    return True


def dominio_filtrado(variable_objetivo, asignacion_parcial, dominios, restricciones):
    """
    esta funcion mira una variable que todavia no he asignado,
    y revisa cuales valores todavia son posibles para esa variable.

    variable_objetivo:
        por ejemplo "fisica"

    asignacion_parcial:
        lo que ya tengo decidido (ej: {"mate": "miercoles"})

    dominios:
        diccionario con las opciones posibles para cada variable

    restricciones:
        lista de reglas

    regresa:
        lista con los valores que todavia sirven para esa variable
        si regresa [], significa que esa variable se quedo sin opciones
    """

    valores_validos = []

    for posible_valor in dominios[variable_objetivo]:
        prueba = asignacion_parcial.copy()
        prueba[variable_objetivo] = posible_valor

        if es_valida(prueba, restricciones):
            valores_validos.append(posible_valor)

    return valores_validos


def forward_checking(variables, dominios, restricciones, asignacion_actual=None):
    """
    variables:
        lista de variables que tengo que asignar
        ejemplo: ["mate", "fisica", "prog"]

    dominios:
        opciones posibles para cada variable
        ejemplo:
        {
          "mate": ["lunes","miercoles"],
          "fisica": ["lunes","miercoles"],
          "prog": ["lunes","miercoles"]
        }

    restricciones:
        lista de reglas (funciones)

    asignacion_actual:
        diccionario con lo que llevo hasta ahorita

    regresa:
        asignacion completa valida (diccionario)
        o None si no hay solucion
    """

    if asignacion_actual is None:
        asignacion_actual = {}

    # debug: muestro como vamos hasta ahorita
    print("intentando con asignacion_actual:", asignacion_actual)

    # si ya asigne todas las variables, ya termine
    if len(asignacion_actual) == len(variables):
        return asignacion_actual

    # agarro una variable que aun no tenga valor
    for var in variables:
        if var not in asignacion_actual:
            var_pendiente = var
            break

    # pruebo cada valor posible para esa variable
    for valor in dominios[var_pendiente]:
        nueva_asig = asignacion_actual.copy()
        nueva_asig[var_pendiente] = valor

        print(" probando", var_pendiente, "=", valor)
        # paso 1: checar si ya rompi una regla
        if not es_valida(nueva_asig, restricciones):
            print("  rompe una regla, salto este valor")
            continue

        # paso 2: comprobacion hacia delante
        # reviso TODAS las variables que faltan
        # y veo si todavia les queda al menos una opcion posible
        consistente = True

        for otra_var in variables:
            if otra_var not in nueva_asig:
                # veo que opciones le quedan a esa otra variable
                dominio_restante = dominio_filtrado(
                    otra_var,
                    nueva_asig,
                    dominios,
                    restricciones
                )

                print("   dominio restante para", otra_var, "->", dominio_restante)

                # si ya no le queda ninguna opcion a esa variable,
                # significa que esta decision mata el futuro
                if len(dominio_restante) == 0:
                    print("   esta decision deja sin opciones a", otra_var, "descartando")
                    consistente = False
                    break

        if not consistente:
            # intento con otro valor
            continue

        # si llegamos aqui:
        # - no he roto reglas
        # - nadie se quedo sin opciones
        # entonces sigo asignando el resto
        resultado = forward_checking(
            variables,
            dominios,
            restricciones,
            nueva_asig
        )

        if resultado is not None:
            return resultado

    # si ningun valor funciono para esta variable
    return None

if __name__ == "__main__":
    # ejemplo: armar horario de examenes

    # variables = materias
    variables = ["mate", "fisica", "prog"]

    # dominios = dias posibles
    dominios = {
        "mate": ["lunes", "miercoles"],
        "fisica": ["lunes", "miercoles"],
        "prog": ["lunes", "miercoles"]
    }

    # regla 1:
    # no quiero dos examenes el mismo dia
    def regla_no_mismo_dia(asignacion):
        dias = []
        for materia in asignacion:
            dias.append(asignacion[materia])
        # check rapido:
        # si hay repetidos en dias, ya esta mal
        return len(dias) == len(set(dias))

    # regla 2:
    # prog no puede ser lunes
    def regla_prog_no_lunes(asignacion):
        if "prog" in asignacion:
            return asignacion["prog"] != "lunes"
        return True

    restricciones = [regla_no_mismo_dia, regla_prog_no_lunes]
    # corremos la busqueda
    solucion = forward_checking(variables, dominios, restricciones)

    print("\nsolucion con comprobacion hacia delante:", solucion)
    print("listo")
    # - forward checking revisa el futuro antes de seguir
    # - si alguna variable se queda sin opciones, cancela ese camino luego luego
    # - por eso a veces es mas rapido que backtracking puro