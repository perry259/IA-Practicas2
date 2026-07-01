# Red bayesiana dinamica
# una red bayesiana dinamica (dbn) modela como cambian las cosas con el tiempo.
# ejemplo: clima_hoy -> clima_manana

# en vez de solo decir "cual es el clima ahorita",
# tambien decimos "cual creo que sera el clima manana"
# usando probabilidades de cambio.

# en este ejemplo:
# estados posibles = "soleado" o "lluvia"

# lo que vamos a hacer:
# 1. tenemos una creencia de como esta el clima HOY
# 2. tenemos una tabla que dice como pasa de hoy a mañana
# 3. calculamos la creencia de MAÑANA

def prob_manana(creencia_hoy, transicion):
    """
    calcula la creencia de mañana usando:
    creencia_hoy:
        diccionario con prob actual de cada estado hoy
        por ejemplo:
        {
            "soleado": 0.6,
            "lluvia": 0.4
        }

    transicion:
        dice como cambia cada estado de hoy a mañana
        ejemplo:
        {
            "soleado": {"soleado": 0.8, "lluvia": 0.2},
            "lluvia":  {"soleado": 0.3, "lluvia": 0.7}
        }

        se lee asi:
        si hoy esta soleado:
            mañana 80% sigue soleado
            mañana 20% llueve
        si hoy llueve:
            mañana 30% sale el sol
            mañana 70% sigue lloviendo

    regresa:
        nueva creencia (diccionario) para mañana
    """
    # formula:
    # P(manana=soleado) =
    #    P(hoy=soleado) * P(soleado->soleado)
    #  + P(hoy=lluvia)  * P(lluvia->soleado)

    p_hoy_soleado = creencia_hoy["soleado"]
    p_hoy_lluvia = creencia_hoy["lluvia"]

    p_manana_soleado = (
        p_hoy_soleado * transicion["soleado"]["soleado"] +
        p_hoy_lluvia  * transicion["lluvia"]["soleado"]
    )

    p_manana_lluvia = (
        p_hoy_soleado * transicion["soleado"]["lluvia"] +
        p_hoy_lluvia  * transicion["lluvia"]["lluvia"]
    )

    return {
        "soleado": p_manana_soleado,
        "lluvia": p_manana_lluvia
    }


if __name__ == "__main__":
    # creencia de hoy:
    # creo que hoy esta soleado con 0.6
    # y lloviendo con 0.4
    creencia_hoy = {
        "soleado": 0.6,
        "lluvia": 0.4
    }

    # tabla de transicion clima_hoy -> clima_manana
    transicion = {
        "soleado": {"soleado": 0.8, "lluvia": 0.2},
        "lluvia":  {"soleado": 0.3, "lluvia": 0.7}
    }

    print("creencia hoy:", creencia_hoy)

    # calculamos creencia de mañana usando la red bayesiana dinamica
    creencia_manana = prob_manana(creencia_hoy, transicion)

    print("creencia mañana:", creencia_manana)

    # como leer el resultado:
    # - creencia_manana["soleado"] = prob de que mañana este soleado
    # - creencia_manana["lluvia"]  = prob de que mañana llueva
    # recordar
    # la red bayesiana dinamica modela el paso t -> t+1
    # y actualiza la creencia con las probabilidades de transicion