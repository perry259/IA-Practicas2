# Exploracion vs explotacion
# - explotacion: elegir la accion que crees que es la mejor
# - exploracion: probar otra accion para aprender mas
# por que importa:
# si nunca exploras, nunca descubres una accion que podria ser mejor.
# si exploras demasiado, pierdes puntos probando cosas malas.
# normalmente hacemos algo tipo:
# con cierta probabilidad (prob_explorar) hago accion random (exploro)
# si no, hago la mejor accion conocida (explotacion).

import random

def elegir_accion(Q_estado, acciones, prob_explorar):
    """
    Q_estado:
        diccionario accion -> valor estimado
        ejemplo:
        {
            "accion1": 5.0,
            "accion2": 8.0
        }

    acciones:
        lista con las acciones posibles

    prob_explorar:
        numero entre 0 y 1
        ejemplo 0.3 = 30% del tiempo probamos algo random (explorar)

    regresa:
        (accion_elegida, modo)
        modo es "explorar" o "explotar"
    """

    # explorar (hacer algo random)
    if random.random() < prob_explorar:
        accion = random.choice(acciones)
        return accion, "explorar"

    # explotar (tomar la mejor accion conocida segun Q)
    mejor_accion = None
    mejor_valor = None
    for acc in acciones:
        q_val = Q_estado[acc]
        if (mejor_accion is None) or (q_val > mejor_valor):
            mejor_accion = acc
            mejor_valor = q_val

    return mejor_accion, "explotar"


if __name__ == "__main__":
    # tenemos un solo estado ficticio
    # y 2 acciones posibles
    acciones = ["ir_a_B", "ir_a_X"]

    # Q_estado guarda lo que creemos que vale cada accion
    # por ejemplo:
    # ir_a_B creemos que da 9.0 pts
    # ir_a_X creemos que da 4.5 pts
    Q_estado = {
        "ir_a_B": 9.0,
        "ir_a_X": 4.5
    }

    prob_explorar = 0.3  # 30% exploro, 70% exploto

    conteo_explorar = 0
    conteo_explotar = 0

    print("simulacion de decisiones:")
    for paso in range(20):
        accion_elegida, modo = elegir_accion(Q_estado, acciones, prob_explorar)

        if modo == "explorar":
            conteo_explorar += 1
        else:
            conteo_explotar += 1

        print(" paso", paso, "-> tome accion:", accion_elegida, "modo:", modo)

    print("\nresumen final:")
    print(" veces que explore (random):", conteo_explorar)
    print(" veces que explote (mejor conocida):", conteo_explotar)

    # - explorar = intentar cosas nuevas aunque no sean las mejores
    # - explotar = usar lo que ya crees que es mejor
    # - esto es basico en aprendizaje por refuerzo:
    #   necesitas las dos cosas