# Teoria de la utilidad: funcion de utilidad
# la utilidad es un numero que dice que tan bueno es un resultado para mi.
# no siempre es dinero. puede ser comodidad, felicidad, seguridad, etc.
# si tengo varias opciones (acciones) y cada opcion puede tener diferentes resultados,
# puedo usar una funcion de utilidad para decidir cual opcion me conviene mas.
# - cada resultado posible tiene una utilidad (un puntaje)
# - cada resultado tiene una probabilidad de pasar
# - calculo la utilidad esperada de cada accion
# - escojo la accion con mayor utilidad esperada

def utilidad_resultado(resultado):
    """
    esta funcion asigna utilidad (puntaje) a cada resultado.

    resultado:
        string que describe que paso

    regresa:
        numero (entre mas alto mejor)

    ejemplo del escenario:
    estoy decidiendo si estudiar o no estudiar para un examen.

    posibles resultados:
    - "estudio_y_apruebo"
    - "estudio_y_repruebo"
    - "no_estudio_y_apruebo"
    - "no_estudio_y_repruebo"

    ojo:
    estos numeros los pone la persona.
    no son "reales", son personales.
    """
    tabla_utilidad = {
        "estudio_y_apruebo": 100,      # me siento bien, paso, valio la pena
        "estudio_y_repruebo": 20,      # me frustro pero al menos lo intente
        "no_estudio_y_apruebo": 60,    # tuve suerte, bien pero con culpa
        "no_estudio_y_repruebo": -50   # me fue mal y aparte ni estudie
    }

    return tabla_utilidad[resultado]

def utilidad_esperada(accion, probabilidades):
    """
    calcula la utilidad esperada de una accion.

    accion:
        string con el nombre de la accion
        ejemplo: "estudiar" o "no_estudiar"

    probabilidades:
        diccionario:
        - llave: accion
        - valor: lista de (resultado, probabilidad_de_ese_resultado_si_hago_esa_accion)

        ejemplo:
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
        numero = suma de (probabilidad * utilidad_de_resultado)
    """
    total = 0

    for resultado, prob in probabilidades[accion]:
        u = utilidad_resultado(resultado)
        total += prob * u

    return total


def elegir_mejor_accion(acciones, probabilidades):
    """
    calcula la utilidad esperada de cada accion
    y regresa la mejor.

    acciones:
        lista con acciones posibles
        ejemplo: ["estudiar", "no_estudiar"]

    probabilidades:
        ver formato en utilidad_esperada()
    """

    mejor_accion = None
    mejor_valor = None

    for acc in acciones:
        ue = utilidad_esperada(acc, probabilidades)

        # print opcional para ver calculo
        print("utilidad esperada de", acc, "=", ue)

        if (mejor_accion is None) or (ue > mejor_valor):
            mejor_accion = acc
            mejor_valor = ue

    return mejor_accion, mejor_valor

if __name__ == "__main__":
    # escenario:
    # decision: estudio o no estudio para el examen

    acciones_posibles = ["estudiar", "no_estudiar"]

    # probabilidades de cada resultado segun la accion que tomo
    # interpretacion:
    # si estudio:
    #   - prob 0.8 de pasar
    #   - prob 0.2 de reprobar
    # si no estudio:
    #   - prob 0.3 de pasar (tuve suerte)
    #   - prob 0.7 de reprobar

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

    # elegimos la mejor accion segun utilidad esperada
    accion, valor = elegir_mejor_accion(acciones_posibles, probabilidades)

    print("\nmejor decision segun mi utilidad:", accion)
    print("utilidad esperada de esa decision:", valor)

    # - utilidad = cuanto me importa un resultado
    # - probabilidad = que tan probable es ese resultado
    # - utilidad esperada = prob1*util1 + prob2*util2 + ...
    # - la mejor accion es la que tiene utilidad esperada mas alta