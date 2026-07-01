# Parcialmente observable
# pomdp = mdp pero no sabes exactamente en que estado estas
# solo tienes una creencia (probabilidades sobre estados)
# ejemplo que vamos a usar:
# hay 2 estados posibles:
#   - "seguro"
#   - "peligro"
# tu no ves el estado directo
# tu solo crees algo como:
#   creencia["seguro"] = 0.7
#   creencia["peligro"] = 0.3
# puedes tomar acciones:
#   - "salir"
#   - "esperar"
#   - "observar" (preguntar / revisar)
# cada accion da cierta recompensa dependiendo
# de cual sea el estado real
# - calculo utilidad esperada de cada accion usando mi creencia
# - escojo la mejor
# - si observo, actualizo mi creencia


def utilidad_accion_en_estado(accion, estado_real):
    """
    esta funcion dice la utilidad inmediata de hacer una accion
    si el estado verdadero fuera X.

    accion:
        "salir", "esperar", "observar"
    estado_real:
        "seguro" o "peligro"

    nota: estos numeros son inventados como ejemplo de situacion de riesgo
    """

    # interpretacion:
    # - si sales y es seguro -> todo bien
    # - si sales y es peligro -> te va mal
    # - esperar es mas o menos ok pero no resuelve nada
    # - observar cuesta un poco (tiempo/energia) pero puede ayudarte despues

    tabla = {
        ("salir", "seguro"):  +10,
        ("salir", "peligro"): -20,
        ("esperar", "seguro"):  +1,
        ("esperar", "peligro"):  0,
        ("observar", "seguro"): -1,
        ("observar", "peligro"): -1,
    }

    return tabla[(accion, estado_real)]


def utilidad_esperada_de_accion(accion, creencia):
    """
    calcula la utilidad esperada de una accion usando la creencia actual

    creencia:
        dict con la prob de estar en cada estado
        ejemplo:
        {
            "seguro": 0.7,
            "peligro": 0.3
        }

    utilidad esperada = sum( prob(estado) * utilidad(accion, estado) )
    """

    total = 0.0
    for estado_real in creencia:
        prob = creencia[estado_real]
        u = utilidad_accion_en_estado(accion, estado_real)
        total += prob * u
    return total


def mejor_accion(creencia):
    """
    prueba todas las acciones validas y ve cual tiene mayor utilidad esperada
    usando la creencia actual.

    regresa:
        (accion_ganadora, utilidad_esperada)
    """

    acciones_posibles = ["salir", "esperar", "observar"]

    mejor_a = None
    mejor_u = None

    for accion in acciones_posibles:
        ue = utilidad_esperada_de_accion(accion, creencia)
        print("utilidad esperada de", accion, "=", ue)

        if (mejor_a is None) or (ue > mejor_u):
            mejor_a = accion
            mejor_u = ue

    return mejor_a, mejor_u


def actualizar_creencia(creencia_anterior, observacion, confiabilidad_sensor):
    """
    en un pomdp real, aqui entra bayes:
    nueva_creencia ∝ P(obs | estado) * creencia_anterior[estado]

    lo que hacemos aqui es una version muy simple:
    - observacion puede ser "parece_seguro" o "parece_peligro"
    - confiabilidad_sensor dice que tan confiable es esa observacion

    ejemplo:
    si observacion = "parece_seguro" y confiabilidad = 0.8
    eso significa:
        con 0.8 de prob la observacion acierta
        con 0.2 de prob se equivoca
    """

    # creencia inicial
    p_seguro = creencia_anterior["seguro"]
    p_peligro = creencia_anterior["peligro"]

    if observacion == "parece_seguro":
        # prob de ver "parece_seguro" dado que el estado es seguro
        like_seguro = confiabilidad_sensor        # acierta
        # prob de ver "parece_seguro" dado que el estado es peligro
        like_peligro = 1 - confiabilidad_sensor   # se equivoca
    else:
        # observacion == "parece_peligro"
        like_seguro = 1 - confiabilidad_sensor
        like_peligro = confiabilidad_sensor

    # bayes sin normalizar:
    # nueva_prob(estado) ~ like(estado) * prob_anterior(estado)

    nueva_seguro_sin_norm = like_seguro  * p_seguro
    nueva_peligro_sin_norm = like_peligro * p_peligro

    # normalizamos para que sumen 1
    total = nueva_seguro_sin_norm + nueva_peligro_sin_norm
    if total == 0:
        # caso raro: si total 0 (no deberia pasar con numeros validos)
        nueva_seguro = 0.5
        nueva_peligro = 0.5
    else:
        nueva_seguro = nueva_seguro_sin_norm / total
        nueva_peligro = nueva_peligro_sin_norm / total

    return {
        "seguro": nueva_seguro,
        "peligro": nueva_peligro
    }


if __name__ == "__main__":
    # paso 1: creencia inicial
    # creo que estoy en lugar seguro con 70%
    # y en peligro con 30%

    creencia = {
        "seguro": 0.7,
        "peligro": 0.3
    }

    print("creencia inicial:", creencia)

    # paso 2: con esta creencia inicial,
    # que accion es mejor?
    accion1, util1 = mejor_accion(creencia)

    print("\nmejor accion con creencia inicial:", accion1)
    print("utilidad esperada:", util1)

    # paso 3: supongamos que hago la accion "observar"
    # y lo que veo es "parece_peligro"
    # y mi sensor (miro, escucho, etc) es 80% confiable

    observacion = "parece_peligro"
    confiabilidad = 0.8

    nueva_creencia = actualizar_creencia(
        creencia,
        observacion,
        confiabilidad
    )

    print("\ncreencia despues de observar:", nueva_creencia)

    # paso 4: ahora con la nueva creencia,
    # que accion es mejor?
    accion2, util2 = mejor_accion(nueva_creencia)

    print("\nmejor accion despues de observar:", accion2)
    print("utilidad esperada:", util2)

    # - en pomdp no sabes exactamente el estado real
    # - en vez de estado real usas una creencia (probabilidades)
    # - puedes tomar acciones normales (salir / esperar)
    # - o acciones de informacion ("observar") para actualizar tu creencia
    # - decides basandote en tu creencia actual, no en el estado real