# problemas de satisfaccion de restricciones (csp)
# en este tipo de problema tenemos varias cosas que decidir (variables)
# y cada decision tiene opciones (dominios)
# pero hay reglas que dicen que combinaciones si se permiten y cuales no
# sirve para hacer horarios, acomodar grupos, asignar salones, sudoku, etc
# por ejemplo:
# vamos a armar horario de examenes para 3 materias:
# mate, fisica, programacion
# reglas:
# - no quiero hacer 2 examenes el mismo dia porque es mucho
# - programacion no puede ser el lunes porque aun no estudio

def es_valida(asignacion, restricciones):
    """
    asignacion:
        lo que llevamos decidido hasta ahorita
        ejemplo:
        {
          "mate": "lunes",
          "fisica": "miercoles"
        }

    restricciones:
        lista de reglas. cada regla es una funcion
        cada regla regresa True si todo bien, False si rompe la regla

    regresa:
        True si todas las reglas se cumplen
        False si alguna regla se rompio
    """

    for regla in restricciones:
        if not regla(asignacion):
            return False
    return True


def resolver_csp(variables, dominios, restricciones, asignacion_actual=None):
    """
    variables:
        lista de cosas que hay que asignar
        en este caso son materias:
        ["mate", "fisica", "prog"]

    dominios:
        para cada materia, a que dia se puede poner
        ejemplo:
        {
          "mate": ["lunes", "miercoles"],
          "fisica": ["lunes", "miercoles"],
          "prog": ["lunes", "miercoles"]
        }

    restricciones:
        lista de funciones que revisan que las decisiones no choquen

    asignacion_actual:
        lo que ya tengo asignado hasta ahorita (diccionario)

    regresa:
        una asignacion completa valida
        o None si no hay forma de cumplir las reglas
    """

    if asignacion_actual is None:
        asignacion_actual = {}

    # si ya asigne todas las variables ya termine
    if len(asignacion_actual) == len(variables):
        return asignacion_actual

    # busco una variable que aun no tenga valor
    for var in variables:
        if var not in asignacion_actual:
            siguiente_var = var
            break

    # pruebo cada posible valor para esa variable
    for valor in dominios[siguiente_var]:
        nueva_asignacion = asignacion_actual.copy()
        nueva_asignacion[siguiente_var] = valor

        # si con este valor sigo respetando las reglas
        if es_valida(nueva_asignacion, restricciones):
            # sigo con las demas variables
            resultado = resolver_csp(
                variables,
                dominios,
                restricciones,
                nueva_asignacion
            )
            if resultado is not None:
                return resultado

    # si ningun valor funciono, regreso None
    return None

if __name__ == "__main__":
    # variables = las materias a las que les tengo que poner fecha de examen
    variables = ["mate", "fisica", "prog"]

    # dominios = que dias puedo usar para cada examen
    # en este caso solo dos dias posibles: lunes o miercoles
    dominios = {
        "mate": ["lunes", "miercoles"],
        "fisica": ["lunes", "miercoles"],
        "prog": ["lunes", "miercoles"]
    }

    # ahora escribimos las reglas del profe / de mi vida

    # regla 1:
    # no quiero dos examenes el mismo dia
    # o sea: si mate ya esta en lunes, fisica ya no puede ser lunes
    def regla_no_doble_mismo_dia(asignacion):
        # juntamos los dias que ya se usaron
        dias_usados = []
        for materia in asignacion:
            dias_usados.append(asignacion[materia])

        # si hay un dia repetido, esta mal
        # ejemplo: ["lunes","lunes"] -> rompe regla
        return len(dias_usados) == len(set(dias_usados))
        # truco rapido:
        # set(...) quita repetidos
        # si antes tenia 2 y ahora 1, entonces habia repetido

    # regla 2:
    # programacion NO puede ser lunes
    def regla_prog_no_lunes(asignacion):
        if "prog" in asignacion:
            return asignacion["prog"] != "lunes"
        return True  # si prog aun no tiene dia, no hay problema todavia

    restricciones = [regla_no_doble_mismo_dia, regla_prog_no_lunes]

    solucion = resolver_csp(variables, dominios, restricciones)

    print("horario de examenes:")
    print(solucion)

    # ejemplo de salida posible:
    # {'mate': 'lunes', 'fisica': 'miercoles', 'prog': 'miercoles'}
    # esto significa:
    # mate  -> lunes
    # fisica -> miercoles
    # prog   -> miercoles
    # revisa: no hay dos el mismo dia? fisica y prog si estan el mismo dia
    # entonces esa salida puede variar segun el orden
    # si te sale None significa que con estas reglas no se pudo hacer horario
    # - variables: lo que tengo que asignar
    # - dominios: opciones posibles para cada variable
    # - restricciones: reglas que deben cumplirse
    # - el buscador intenta llenarlo todo sin romper reglas