# busqueda de vuelta atras
# este algoritmo intenta construir una solucion paso a paso.
# si en algun punto poner un valor rompe una regla,
# entonces regresa (da vuelta atras / backtrack) y prueba otra opcion.
# se usa para resolver csp probando combinaciones sin quedarse con las que ya sabemos que no sirven.

# nota:
# la base es igual que el csp anterior, pero aqui explicamos claro el paso de "me regreso".

def es_valida(asignacion, restricciones):
    # checa que la asignacion actual no rompa ninguna regla
    for regla in restricciones:
        if not regla(asignacion):
            return False
    return True


def backtracking(variables, dominios, restricciones, asignacion_actual=None):
    """
    variables:
        lista de variables que quiero asignar
        ejemplo: ["mate","fisica","prog"]

    dominios:
        para cada variable, que valores puede tomar
        ejemplo:
        {
          "mate": ["lunes","miercoles"],
          "fisica": ["lunes","miercoles"],
          "prog": ["lunes","miercoles"]
        }

    restricciones:
        lista de reglas (funciones) que dicen si lo que llevo esta bien

    asignacion_actual:
        diccionario con las decisiones que ya hice hasta el momento

    regresa:
        una asignacion completa valida
        o None si no hay forma
    """

    if asignacion_actual is None:
        asignacion_actual = {}

    # si ya asigne todas las variables, ya termine
    if len(asignacion_actual) == len(variables):
        return asignacion_actual

    # elijo la siguiente variable sin asignar
    for var in variables:
        if var not in asignacion_actual:
            var_pendiente = var
            break

    # intento cada valor posible para esa variable
    for valor in dominios[var_pendiente]:
        # propongo asignar esa variable = ese valor
        nueva_asignacion = asignacion_actual.copy()
        nueva_asignacion[var_pendiente] = valor

        # checo si sigue valido
        if es_valida(nueva_asignacion, restricciones):
            # intento seguir con lo demas
            resultado = backtracking(
                variables,
                dominios,
                restricciones,
                nueva_asignacion
            )

            # si eso funciono, lo regreso
            if resultado is not None:
                return resultado

        # si NO funciono:
        # aqui es donde entra "vuelta atras"
        # basicamente, probamos otra opcion del dominio
        # (esto pasa automaticamente en el for, no hay que hacer nada extra)

    # si ningun valor funciono para esta variable, no hay solucion por este camino
    return None

if __name__ == "__main__":
    # vamos a usar el mismo tipo de ejemplo del horario de examenes,
    # porque es facil de entender
    # quiero asignar dia de examen a cada materia
    variables = ["mate", "fisica", "prog"]
    # los dias posibles
    dominios = {
        "mate": ["lunes", "miercoles"],
        "fisica": ["lunes", "miercoles"],
        "prog": ["lunes", "miercoles"]
    }

    # reglas del horario
    # regla 1: no quiero 2 examenes el mismo dia
    def regla_no_mismo_dia(asignacion):
        dias_usados = []
        for materia in asignacion:
            dias_usados.append(asignacion[materia])
        # si hay repetidos ya esta mal
        # truco: len(lista) == len(set(lista)) significa "no hay repetidos"
        return len(dias_usados) == len(set(dias_usados))

    # regla 2: prog no puede ser lunes
    def regla_prog_no_lunes(asignacion):
        if "prog" in asignacion:
            return asignacion["prog"] != "lunes"
        return True

    restricciones = [regla_no_mismo_dia, regla_prog_no_lunes]

    solucion = backtracking(variables, dominios, restricciones)

    print("solucion con vuelta atras:", solucion)
    # que esta pasando en backtracking paso a paso:
    # 1. intenta dar dia a mate
    # 2. luego da dia a fisica
    # 3. luego da dia a prog
    # 4. si poner prog rompe una regla, regresa y cambia una decision anterior
    
    # eso es la diferencia importante:
    # no sigue adelante con algo que ya esta mal,
    # sino que se regresa a la ultima decision y prueba otra opcion.
    # - backtracking = busqueda con retroceso cuando una opcion rompe reglas
    # - en cada paso intento asignar algo
    # - si se rompe una regla, deshago y pruebo otra opcion