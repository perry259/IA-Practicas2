# valor de la informacion
# valor de la informacion = cuanto mejora mi decision si primero consigo informacion extra
# (antes de actuar)
# me ayuda a saber si vale la pena "pagar por revisar / medir / preguntar" antes de decidir

# ejemplo
# quiero comprar un telefono usado
# puede salir bien o puede salir fallado
# puedo pagar una revision tecnica antes de comprarlo
# la pregunta es: ¿conviene pagar esa revision?

def utilidad_final(resultado):
    """
    resultado:
        string que representa que paso al final

    regresamos un numero que representa que tan bueno fue
    """

    # casos:
    # comp_compro_bien = compre y salio bueno
    # comp_compro_mal = compre y salio malo (perdi dinero)
    # comp_no_compro   = decidi no comprar (ni gano ni pierdo)
    # ojo: estos numeros son inventados solo para el ejemplo

    tabla = {
        "compro_bien": 80,     # hice una buena compra
        "compro_mal": -60,     # perdi dinero porque salio malo
        "no_compro": 0         # no gane nada pero tampoco perdi
    }
    return tabla[resultado]


def utilidad_esperada_sin_info(prob_bueno, prob_malo):
    """
    calcula la utilidad esperada si NO pido informacion extra.
    o sea, decido comprar o no comprar directo.

    prob_bueno:
        probabilidad de que el telefono este bien
    prob_malo:
        probabilidad de que el telefono este fallado

    regla que vamos a usar:
    - accion 1: comprar
        si compro:
            compro_bien con prob_bueno
            compro_mal con prob_malo
    - accion 2: no comprar
        siempre termino en "no_compro"
    """

    # utilidad esperada de comprar
    ue_comprar = (
        prob_bueno * utilidad_final("compro_bien") +
        prob_malo  * utilidad_final("compro_mal")
    )

    # utilidad esperada de no comprar
    ue_no_comprar = utilidad_final("no_compro")

    # elegimos lo mejor de esas dos
    if ue_comprar >= ue_no_comprar:
        mejor_accion = "comprar"
        mejor_utilidad = ue_comprar
    else:
        mejor_accion = "no_comprar"
        mejor_utilidad = ue_no_comprar

    return mejor_accion, mejor_utilidad


def utilidad_esperada_con_info(prob_bueno, prob_malo, costo_revision, calidad_revision):
    """
    ahora asumimos que SI pido informacion:
    pago una revision tecnica ANTES de decidir si comprar.

    costo_revision:
        cuanto "me cuesta" pedir la info (puede ser dinero, tiempo, etc)
        esto se resta de la utilidad final

    calidad_revision:
        que tan confiable es la revision (entre 0 y 1)
        ejemplo: 0.9 = el tecnico casi siempre dice la verdad

    mecanismo:
    - si la revision dice "esta bien", yo compro
    - si la revision dice "esta mal", yo no compro

    peeeeero:
    la revision se puede equivocar.
    calidad_revision = prob. de que el tecnico acierte
    """

    # probabilidad de que el tecnico diga "esta bien"
    # puede pasar por dos razones:
    # 1. el telefono realmente esta bien y el tecnico acierta
    # 2. el telefono esta mal pero el tecnico se equivoca
    prob_tecnico_dice_bien = (
        prob_bueno * calidad_revision +
        prob_malo  * (1 - calidad_revision)
    )

    # probabilidad de que el tecnico diga "esta mal"
    prob_tecnico_dice_mal = 1 - prob_tecnico_dice_bien

    # caso 1: el tecnico dice "esta bien" -> yo compro
    # pero que tan bueno me va en realidad si compro?
    # tengo que usar probabilidad condicionada

    # prob de que en verdad este bien dado que dijo "bien"
    if prob_tecnico_dice_bien > 0:
        prob_real_bien_si_dijo_bien = (
            prob_bueno * calidad_revision
        ) / prob_tecnico_dice_bien
    else:
        prob_real_bien_si_dijo_bien = 0

    # prob de que en verdad este malo dado que dijo "bien"
    if prob_tecnico_dice_bien > 0:
        prob_real_mal_si_dijo_bien = (
            prob_malo * (1 - calidad_revision)
        ) / prob_tecnico_dice_bien
    else:
        prob_real_mal_si_dijo_bien = 0

    ue_si_dijo_bien = (
        prob_real_bien_si_dijo_bien * utilidad_final("compro_bien") +
        prob_real_mal_si_dijo_bien * utilidad_final("compro_mal")
    )

    # caso 2: el tecnico dice "esta mal" -> no compro
    ue_si_dijo_mal = utilidad_final("no_compro")

    # ahora mezclamos los dos casos, pesados por las probs de que el tecnico diga bien/mal
    ue_total_con_info = (
        prob_tecnico_dice_bien * ue_si_dijo_bien +
        prob_tecnico_dice_mal * ue_si_dijo_mal
    )

    # restamos el costo de pedir la revision
    ue_total_con_info -= costo_revision

    return ue_total_con_info


if __name__ == "__main__":
    # supongamos esto:
    # prob_bueno = probabilidad de que el telefono este bien
    # prob_malo  = probabilidad de que este mal
    # (deben sumar 1)
    prob_bueno = 0.6
    prob_malo  = 0.4

    # primero calculamos la mejor decision SIN pedir info
    mejor_sin_info, utilidad_sin_info = utilidad_esperada_sin_info(
        prob_bueno,
        prob_malo
    )

    print("sin informacion extra:")
    print("  mejor decision directa:", mejor_sin_info)
    print("  utilidad esperada:", utilidad_sin_info)

    # ahora con informacion extra
    # costo_revision: pedir revision cuesta utilidad 5
    # calidad_revision: 0.9 = el tecnico acierta 90% de las veces
    costo_revision = 5
    calidad_revision = 0.9

    utilidad_con_info = utilidad_esperada_con_info(
        prob_bueno,
        prob_malo,
        costo_revision,
        calidad_revision
    )

    print("\ncon informacion (pagar revision):")
    print("  utilidad esperada despues de usar la info:", utilidad_con_info)

    # valor de la informacion:
    # que tanto me mejora pedir la info vs no pedirla
    valor_info = utilidad_con_info - utilidad_sin_info

    print("\nvalor de la informacion:", valor_info)
    # si valor_info > 0  -> conviene pedir la informacion (vale la pena pagar)
    # si valor_info <= 0 -> no conviene, es dinero/tiempo perdido
    # - la info tiene valor si cambia tu decision para mejor
    # - aqui calculamos utilidad esperada SIN info y LUEGO CON info
    # - la diferencia es el valor de la informacion