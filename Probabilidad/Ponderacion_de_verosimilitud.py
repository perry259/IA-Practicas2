"""
ponderacion de verosimilitud (likelihood weighting)
esta tecnica sirve para aproximar p(x | evidencia)
en una red bayesiana usando muestreo (sampling)

1. las variables que NO son evidencia se samplean normal
2. las variables que SI son evidencia se fijan al valor dado
   y multiplicamos el peso por p(evidencia | padres)
3. juntamos muchos samples con sus pesos
4. usamos eso para estimar p(query | evidencia)
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
# orden topologico (padres antes que hijos)
orden_vars = ["virus", "clima_frio", "fiebre", "sudor"]

def prob_true_de_nodo(nodo, asignacion, red_local):
    """
    regresa p(nodo=true | padres)
    usando la cpt del nodo
    """
    padres = red_local[nodo]["padres"]
    clave = tuple(asignacion[p] for p in padres)
    return red_local[nodo]["cpt"][clave]

def samplear_lw(red_local, orden, evidencia):
    """
    hace una muestra con ponderacion de verosimilitud
    asignacion = valores de todas las vars
    peso = que tan consistente es esta muestra con la evidencia

    pasos:
    - si la var es evidencia:
        no se samplea, se fija al valor dado
        y el peso se multiplica por p(var = ese valor | padres)
    - si la var NO es evidencia:
        se samplea normal (random segun su prob condicional)
    """
    asignacion = {}
    peso = 1.0

    for nodo in orden:
        p_true = prob_true_de_nodo(nodo, asignacion, red_local)

        if nodo in evidencia:
            # fijamos el valor observado
            valor_obs = evidencia[nodo]
            asignacion[nodo] = valor_obs

            # actualizamos peso segun que tan probable era ese valor
            if valor_obs is True:
                peso *= p_true
            else:
                peso *= (1 - p_true)
        else:
            # no es evidencia, sample normal
            asignacion[nodo] = (random.random() < p_true)

    return asignacion, peso

def lw_inferencia(query_var, evidencia, red_local, orden, n_muestras):
    """
    estima p(query_var | evidencia) con ponderacion de verosimilitud
    hacemos muchas muestras,
    cada muestra tiene un peso,
    y sumamos los pesos a true y false por separado
    """
    peso_true = 0.0
    peso_false = 0.0

    for _ in range(n_muestras):
        asignacion, w = samplear_lw(red_local, orden, evidencia)

        if asignacion[query_var] is True:
            peso_true += w
        else:
            peso_false += w

    total = peso_true + peso_false
    if total == 0:
        return {True: 0.0, False: 0.0}

    return {
        True: peso_true / total,
        False: peso_false / total
    }

# llamada final para que imprima algo
# estamos aproximando p(fiebre | sudor=true)
res = lw_inferencia(
    query_var="fiebre",
    evidencia={"sudor": True},
    red_local=red,
    orden=orden_vars,
    n_muestras=5000
)

print("prob aprox con ponderacion de verosimilitud:")
print("fiebre=true  ->", round(res[True], 4))
print("fiebre=false ->", round(res[False], 4))