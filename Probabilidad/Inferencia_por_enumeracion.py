"""
inferencia por enumeracion
es una forma de calcular p(x | evidencia)
en una red bayesiana. la idea es recorrer (enumerar) todas las
combinaciones posibles de las variables que no sabemos,
multiplicar sus probabilidades, y sumar.
vamos a calcular p(x | evidencia)
probando todas las combinaciones posibles de las variables
esto se usa en redes bayesianas
"""
# cada nodo dice:
# - padres
# - cpt: p(nodo=true | padres)

red = {
    "virus": {
        "padres": [],
        "cpt": { (): 0.1 }  # p(virus=true)
    },
    "clima_frio": {
        "padres": [],
        "cpt": { (): 0.3 }  # p(clima_frio=true)
    },
    "fiebre": {
        "padres": ["virus", "clima_frio"],
        # p(fiebre=true | virus, clima_frio)
        "cpt": {
            (True,  True ): 0.9,
            (True,  False): 0.8,
            (False, True ): 0.6,
            (False, False): 0.05
        }
    },
    "sudor": {
        "padres": ["fiebre"],
        # p(sudor=true | fiebre)
        "cpt": {
            (True,): 0.85,
            (False,): 0.1
        }
    }
}
# orden de las variables para recorrer
orden_vars = ["virus", "clima_frio", "fiebre", "sudor"]

def prob_var_true(var, evidencia, red_local):
    """
    regresa p(var=true | padres)
    usando la cpt del nodo
    """
    padres = red_local[var]["padres"]
    clave = tuple(evidencia[p] for p in padres)
    return red_local[var]["cpt"][clave]

def prob_de_var(var, val, evidencia, red_local):
    """
    regresa p(var = val | padres)
    si val es false = 1 - p(true)
    """
    p_true = prob_var_true(var, evidencia, red_local)
    return p_true if val is True else (1 - p_true)

def enumerar_todo(vars_restantes, evidencia, red_local):
    """
    prob conjunta total dada la evidencia
    si una var no tiene valor asignado,
    probamos true y false y sumamos
    """
    if len(vars_restantes) == 0:
        return 1.0

    v = vars_restantes[0]
    resto = vars_restantes[1:]

    if v in evidencia:
        p = prob_de_var(v, evidencia[v], evidencia, red_local)
        return p * enumerar_todo(resto, evidencia, red_local)
    else:
        total = 0.0
        for val in [True, False]:
            nueva_evid = evidencia.copy()
            nueva_evid[v] = val
            p = prob_de_var(v, val, nueva_evid, red_local)
            total += p * enumerar_todo(resto, nueva_evid, red_local)
        return total

def normalizar(dist):
    """
    hace que los valores sumen 1
    """
    s = sum(dist.values())
    return {k: v / s for k, v in dist.items()}

def preguntar(var_objetivo, evidencia, red_local, orden):
    """
    calcula p(var_objetivo | evidencia)
    regresa {True: prob, False: prob}
    """
    dist = {}
    for val in [True, False]:
        evid_tmp = evidencia.copy()
        evid_tmp[var_objetivo] = val
        dist[val] = enumerar_todo(orden, evid_tmp, red_local)
    return normalizar(dist)

# preguntamos prob de fiebre sabiendo que hay sudor
resultado = preguntar(
    "fiebre",
    {"sudor": True},
    red,
    orden_vars
)

print("prob de fiebre dado sudor=true:")
print("fiebre=true  ->", round(resultado[True], 4))
print("fiebre=false ->", round(resultado[False], 4))