"""
muestreo directo y muestreo por rechazo
en redes bayesianas a veces calcular p(x | evidencia) exacto es caro.
en lugar de hacer toda la matematica exacta,
podemos aproximar la probabilidad generando muchos casos falsos del mundo.
esto se llama muestreo (sampling).

tipos basicos:
1. muestreo directo (direct sampling / prior sampling)
   - generas valores para las variables siguiendo las probabilidades de la red
     (o sea vas "tirando dados" para cada nodo segun sus padres)
   - esto da muestras completas del sistema

2. muestreo por rechazo (rejection sampling)
   - generas muestras igual que arriba
   - pero descartas las que no cumplen la evidencia que ya sabemos
   - con las que quedan calculas la prob que quieres
esto sirve para aproximar p(x | evidencia) sin tener que hacer
enumeracion ni eliminacion de variables.
es util cuando la red es grande.
"""
import random

red = {
    "virus": {
        "padres": [],
        "cpt": { (): 0.1 }
    },
    "clima_frio": {
        "padres": [],
        "cpt": { (): 0.3 }
    },
    "fiebre": {
        "padres": ["virus", "clima_frio"],
        "cpt": {
            (True,  True ): 0.9,
            (True,  False): 0.8,
            (False, True ): 0.6,
            (False, False): 0.05
        }
    },
    "sudor": {
        "padres": ["fiebre"],
        "cpt": {
            (True,): 0.85,
            (False,): 0.1
        }
    }
}

# orden en el que vamos a samplear
# importante: los padres siempre van antes
orden_vars = ["virus", "clima_frio", "fiebre", "sudor"]

def prob_true_de_nodo(nodo, asignacion, red_local):
    """
    regresa p(nodo=true | padres) segun la red
    asignacion trae los valores ya elegidos de los padres
    """
    padres = red_local[nodo]["padres"]
    clave = tuple(asignacion[p] for p in padres)
    return red_local[nodo]["cpt"][clave]


def samplear_una_vez(red_local, orden):
    """
    hace una muestra completa del mundo
    vamos nodo por nodo en orden
    sacamos p(true) dado los padres
    tiramos un random y decidimos true o false
    """
    asignacion = {}
    for nodo in orden:
        p_true = prob_true_de_nodo(nodo, asignacion, red_local)
        asignacion[nodo] = (random.random() < p_true)
    return asignacion

def muestreo_directo(red_local, orden, n_muestras):
    """
    genera n_muestras usando samplear_una_vez
    regresa lista de asignaciones
    """
    datos = []
    for _ in range(n_muestras):
        datos.append(samplear_una_vez(red_local, orden))
    return datos

def cumple_evidencia(muestra, evidencia):
    """
    checa si la muestra respeta toda la evidencia
    ejemplo:
    si evidencia dice {"sudor": True}
    entonces la muestra tiene que tener sudor=True
    """
    for var, val in evidencia.items():
        if muestra[var] != val:
            return False
    return True


def muestreo_por_rechazo(red_local, orden, n_muestras, query_var, evidencia):
    """
    esto es muestreo por rechazo
    pasos:
    1. generamos muchas muestras completas
    2. nos quedamos solo con las que cumplen la evidencia
    3. contamos cuantas tienen query_var=true y cuantas false
    4. normalizamos
    regresa:
    diccionario {True: prob, False: prob}
    """
    cuenta_true = 0
    cuenta_false = 0

    for _ in range(n_muestras):
        m = samplear_una_vez(red_local, orden)

        # si no respeta la evidencia, la tiramos
        if not cumple_evidencia(m, evidencia):
            continue

        # si la respeta, la usamos
        if m[query_var] is True:
            cuenta_true += 1
        else:
            cuenta_false += 1

    total_validas = cuenta_true + cuenta_false
    if total_validas == 0:
        # si ninguna muestra paso la evidencia
        # (puede pasar si la evidencia es muy rara)
        return {True: 0.0, False: 0.0}

    p_true = cuenta_true / total_validas
    p_false = cuenta_false / total_validas

    return {True: p_true, False: p_false}

# ahora hacemos una consulta y mostramos resultado
# estamos usando muestreo por rechazo para aproximar p(fiebre | sudor=true)
resultado = muestreo_por_rechazo(
    red_local=red,
    orden=orden_vars,
    n_muestras=5000,        # entre mas grande mejor la aproximacion
    query_var="fiebre",
    evidencia={"sudor": True}
)

print("prob aproximada con muestreo por rechazo:")
print("fiebre=true  ->", round(resultado[True], 4))
print("fiebre=false ->", round(resultado[False], 4))