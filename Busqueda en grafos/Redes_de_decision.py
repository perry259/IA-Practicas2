# Redes de decision
# una red de decision mezcla 3 cosas:
# 1. decision (lo que yo elijo hacer)
# 2. azar / probabilidad (lo que puede pasar despues de mi decision)
# 3. utilidad (que tan bueno es el resultado final para mi)
# sirve para elegir la mejor accion cuando no hay certeza.
# la idea es: si hago X, pueden pasar varias cosas con distintas probabilidades,
# y cada cosa me da una utilidad diferente.
# entonces calculo la utilidad esperada de cada decision y escojo la mejor.

def utilidad_resultado(resultado):
    """
    resultado: string con el nombre del resultado
               ejemplo: "estudio_y_apruebo"

    regresa: numero que dice que tan bueno es ese resultado para mi

    nota: estos numeros los ponemos nosotros.
    no son fijos, dependen de la persona/problema.
    """

    tabla = {
        "estudio_y_apruebo": 100,      # estuve cansado pero pase, muy bien
        "estudio_y_repruebo": 20,      # me fue mal pero lo intente
        "no_estudio_y_apruebo": 60,    # pase de suerte
        "no_estudio_y_repruebo": -50   # me fue mal y ni le puse ganas
    }

    return tabla[resultado]


def utilidad_esperada_accion(accion, tabla_prob):
    """
    calcula la utilidad esperada de UNA accion (por ejemplo "estudiar")

    accion:
        "estudiar" o "no_estudiar"

    tabla_prob:
        diccionario con las probabilidades de cada resultado segun la accion
        formato:
        {
          "estudiar": [
            ("estudio_y_apruebo", 0.8),
            ("estudio_y_repruebo", 0.2)
          ],
          "no_estudiar": [
            ("no_estudio_y_apruebo", 0.3),
            ("no_estudio_y_repruebo", 0.7)
          ]
        }

    regresa:
        numero = utilidad esperada
    """

    total = 0

    # recorremos todos los resultados posibles de esa accion
    for resultado, prob in tabla_prob[accion]:
        u = utilidad_resultado(resultado)  # utilidad de ese resultado
        total += prob * u                  # probabilidad * utilidad

    return total

def mejor_decision(acciones, tabla_prob):
    """
    esta funcion calcula la utilidad esperada para cada accion posible,
    y escoge la mejor.

    acciones:
        lista de strings con acciones posibles
        ejemplo: ["estudiar", "no_estudiar"]

    tabla_prob:
        ver ejemplo del formato arriba
    """

    mejor_accion = None
    mejor_valor = None

    for acc in acciones:
        ue = utilidad_esperada_accion(acc, tabla_prob)
        print("utilidad esperada de", acc, "=", ue)

        # guardo la mejor
        if (mejor_accion is None) or (ue > mejor_valor):
            mejor_accion = acc
            mejor_valor = ue

    return mejor_accion, mejor_valor

if __name__ == "__main__":
    # este es nuestro mini problema tipo red de decision:
    # decision:
    # estudiar ? o no estudiar ?

    acciones = ["estudiar", "no_estudiar"]

    # azar / probabilidad:
    # que puede pasar segun lo que decida

    probabilidades = {
        "estudiar": [
            ("estudio_y_apruebo", 0.8),
            ("estudio_y_repruebo", 0.2)
        ],
        "no_estudiar": [
            ("no_estudio_y_apruebo", 0.3),
            ("no_estudio_y_repruebo", 0.7)
        ]
    }

    # utilidad final:
    # esta viene de utilidad_resultado(...)
    # y ya se usa dentro del calculo

    mejor, valor = mejor_decision(acciones, probabilidades)

    print("\nmejor decision segun la red de decision:", mejor)
    print("utilidad esperada de esa decision:", valor)

    # - red de decision es como un "diagrama mental" de:
    #   decido -> pasa algo con cierta prob -> obtengo cierta utilidad
    # - la mejor accion es la que tiene utilidad esperada mas alta