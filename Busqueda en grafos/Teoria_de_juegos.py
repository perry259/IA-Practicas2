# Teoria de juegos: equilibrios y mecanismos
# en teoria de juegos hay varios jugadores.
# cada jugador escoge una accion/estrategia.
# lo que ganas depende de lo que haces tu y lo que hace el otro.
# equilibrio de nash:
# una combinacion de estrategias donde
# ningun jugador gana mas cambiando SOLO su propia estrategia.
# en este ejemplo vamos a usar dos jugadores:
# jugador a y jugador b
# cada uno puede elegir:
# - "cooperar"
# - "traicionar"
# definimos una tabla de pagos.
# pagos[a][b] -> (utilidad_de_A, utilidad_de_B)
# por ejemplo:
# pagos["cooperar"]["cooperar"] = ( -1, -1 )

def mejor_respuesta_para_a(eleccion_b, estrategias, pagos):
    """
    dado lo que hace b,
    regresa cual es la mejor respuesta de a.

    estrategias:
        lista de estrategias posibles, ej ["cooperar","traicionar"]

    pagos:
        pagos[a][b] = (utilidad_a, utilidad_b)
    """
    mejor = None
    mejor_utilidad = None

    for opcion_a in estrategias:
        utilidad_a, _ = pagos[opcion_a][eleccion_b]
        if (mejor is None) or (utilidad_a > mejor_utilidad):
            mejor = opcion_a
            mejor_utilidad = utilidad_a

    return mejor


def mejor_respuesta_para_b(eleccion_a, estrategias, pagos):
    """
    dado lo que hace a,
    regresa cual es la mejor respuesta de b.
    """
    mejor = None
    mejor_utilidad = None

    for opcion_b in estrategias:
        _, utilidad_b = pagos[eleccion_a][opcion_b]
        if (mejor is None) or (utilidad_b > mejor_utilidad):
            mejor = opcion_b
            mejor_utilidad = utilidad_b

    return mejor


def es_equilibrio_de_nash(a_juega, b_juega, estrategias, pagos):
    """
    checamos si (a_juega, b_juega) es equilibrio de nash.

    regla:
    - a_juega debe ser mejor respuesta a b_juega
    - b_juega debe ser mejor respuesta a a_juega
    """

    mejor_para_a = mejor_respuesta_para_a(b_juega, estrategias, pagos)
    mejor_para_b = mejor_respuesta_para_b(a_juega, estrategias, pagos)

    return (a_juega == mejor_para_a) and (b_juega == mejor_para_b)


if __name__ == "__main__":
    # estrategias posibles
    estrategias = ["cooperar", "traicionar"]

    # pagos:
    # pagos[a][b] = (utilidad_de_A, utilidad_de_B)

    # interpretacion de estas utilidades (ejemplo tipo dilema del prisionero):
    # - si los dos cooperan: ambos reciben -1 (poquito castigo)
    # - si a traiciona y b coopera:
    #     a queda en 0 (sale libre)
    #     b recibe -10 (le fue mal)
    # - si b traiciona y a coopera:
    #     b queda en 0
    #     a recibe -10
    # - si los dos traicionan:
    #     ambos reciben -5 (castigo medio)

    pagos = {
        "cooperar": {
            "cooperar":    (-1,  -1),
            "traicionar": (-10,   0)
        },
        "traicionar": {
            "cooperar":    (0,  -10),
            "traicionar": (-5,  -5)
        }
    }

    # probamos todas las combinaciones posibles
    for a_juega in estrategias:
        for b_juega in estrategias:
            # utilidad que obtiene cada uno
            util_a, util_b = pagos[a_juega][b_juega]

            # vemos si esto es equilibrio de nash
            equilibrio = es_equilibrio_de_nash(
                a_juega,
                b_juega,
                estrategias,
                pagos
            )

            print("a juega:", a_juega,
                  ", b juega:", b_juega,
                  "=> utilidad a:", util_a,
                  ", utilidad b:", util_b,
                  ", equilibrio_nash?:", equilibrio)

    # que vas a ver:
    # en el dilema del prisionero clasico,
    # la combinacion (traicionar, traicionar) termina siendo equilibrio de nash.
    # por que?
    # porque si uno trata de cambiar solo el/ella,
    # no mejora su utilidad.