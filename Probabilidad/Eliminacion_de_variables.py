"""
eliminacion de variables es una tecnica para calcular
p(x | evidencia) en una red bayesiana
sin tener que probar todas las combinaciones posibles
sirve para hacer inferencia mas rapida.
la idea es ir "eliminando" variables que no nos importan
sumando sus probabilidades y quedandonos solo con lo necesario
"""
import itertools

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

def todas_asignaciones(vars_lista):
    """
    hace todas las combinaciones true/false de una lista de vars
    regresa diccionarios tipo {var: True/False}
    """
    for vals in itertools.product([True, False], repeat=len(vars_lista)):
        yield dict(zip(vars_lista, vals))

def hacer_factor(var, red_local):
    """
    convierte un nodo de la red en un factor
    un factor tiene:
    - lista de vars que usa
    - tabla con probs
    """
    padres = red_local[var]["padres"]
    vars_factor = [var] + padres
    tabla = {}

    for asign in todas_asignaciones(vars_factor):
        clave_padres = tuple(asign[p] for p in padres)
        p_true = red_local[var]["cpt"][clave_padres]
        p_val = p_true if asign[var] is True else (1 - p_true)
        fila = tuple(asign[v] for v in vars_factor)
        tabla[fila] = p_val

    return {
        "vars": vars_factor,
        "table": tabla
    }

def restringir_factor(factor, var, val):
    """
    mete evidencia al factor
    fija var = val y borra filas que no encajan
    """
    if var not in factor["vars"]:
        return factor

    idx = factor["vars"].index(var)
    nuevas_vars = [v for v in factor["vars"] if v != var]
    nueva_tabla = {}

    for fila, p in list(factor["table"].items()):
        if fila[idx] == val:
            fila_sin = tuple(v for i, v in enumerate(fila) if i != idx)
            nueva_tabla[fila_sin] = p

    return {
        "vars": nuevas_vars,
        "table": nueva_tabla
    }

def multiplicar_factores(f1, f2):
    """
    multiplica dos factores
    esto mezcla info probabilistica
    """
    vars1 = f1["vars"]
    vars2 = f2["vars"]
    nuevas_vars = list(dict.fromkeys(vars1 + vars2))
    nueva_tabla = {}

    for asign in todas_asignaciones(nuevas_vars):
        fila1 = tuple(asign[v] for v in vars1)
        fila2 = tuple(asign[v] for v in vars2)

        if fila1 in f1["table"] and fila2 in f2["table"]:
            fila_new = tuple(asign[v] for v in nuevas_vars)
            nueva_tabla[fila_new] = f1["table"][fila1] * f2["table"][fila2]

    return {
        "vars": nuevas_vars,
        "table": nueva_tabla
    }

def sumar_fuera(factor, var):
    """
    elimina una var del factor
    sumando sobre true y false de esa var
    (esto es literalmente "eliminar variable")
    """
    if var not in factor["vars"]:
        return factor

    idx = factor["vars"].index(var)
    nuevas_vars = [v for v in factor["vars"] if v != var]
    nueva_tabla = {}

    for fila, p in factor["table"].items():
        fila_sin = tuple(v for i, v in enumerate(fila) if i != idx)
        nueva_tabla[fila_sin] = nueva_tabla.get(fila_sin, 0.0) + p

    return {
        "vars": nuevas_vars,
        "table": nueva_tabla
    }

def normalizar_en_var(factor, var_obj):
    """
    convierte el factor final en una distribucion normalizada
    regresa {True: prob, False: prob} para var_obj
    """
    idx = factor["vars"].index(var_obj)
    dist = {True: 0.0, False: 0.0}

    for fila, p in factor["table"].items():
        val_var = fila[idx]
        dist[val_var] += p

    total = dist[True] + dist[False]
    if total != 0:
        dist[True] /= total
        dist[False] /= total

    return dist

def inferencia_eliminacion(query_var, evidencia, red_local):
    """
    calcula p(query_var | evidencia) usando eliminacion de variables

    pasos:
    1. convertir nodos a factores
    2. aplicar evidencia
    3. eliminar vars que no son ni query ni evidencia
    4. multiplicar todo
    5. normalizar
    """
    # 1: factores iniciales
    factores = [hacer_factor(v, red_local) for v in red_local.keys()]

    # 2: restringir por evidencia
    for ev_var, ev_val in evidencia.items():
        factores = [restringir_factor(f, ev_var, ev_val) for f in factores]

    # 3: elegir que vars eliminar
    todas = list(red_local.keys())
    ocultas = [v for v in todas if v != query_var and v not in evidencia]

    for var in ocultas:
        # tomamos factores que tengan esa var
        con_var = [f for f in factores if var in f["vars"]]
        sin_var = [f for f in factores if var not in f["vars"]]

        if len(con_var) == 0:
            factores = sin_var
            continue

        # multiplicamos todos los que la tienen
        comb = con_var[0]
        for f2 in con_var[1:]:
            comb = multiplicar_factores(comb, f2)

        # la eliminamos sumando
        reducido = sumar_fuera(comb, var)

        # guardamos de nuevo
        factores = sin_var + [reducido]

    # 4: multiplicar todo lo que queda
    final = factores[0]
    for f2 in factores[1:]:
        final = multiplicar_factores(final, f2)

    # 5: normalizar en la var que preguntamos
    return normalizar_en_var(final, query_var)

# llamada final para que imprima algo
# estamos preguntando prob de una variable dada otra observada
res = inferencia_eliminacion(
    query_var="fiebre",
    evidencia={"sudor": True},
    red_local=red
)

print("resultado inferencia con eliminacion de variables:")
print("fiebre=true  ->", round(res[True], 4))
print("fiebre=false ->", round(res[False], 4))