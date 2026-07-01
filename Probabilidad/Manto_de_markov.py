"""
el manto de markov (markov blanket) de un nodo x
es el conjunto minimo de nodos que necesito conocer
para poder razonar sobre x sin mirar toda la red completa
para que sirve:
- bajar el problema a solo las variables importantes
- hacer calculos mas rapidos en ia probabilistica
como se forma:
manto(x) = padres(x) + hijos(x) + copadres(x)
donde:
- padres(x): nodos que apuntan a x
- hijos(x): nodos a los que x apunta
- copadres(x): otros padres de los hijos de x
  (o sea, nodos que junto con x afectan al mismo hijo)
"""

# cada nodo tiene lista de padres y lista de hijos
red = {
    "a": { "padres": [],        "hijos": ["b"] },
    "b": { "padres": ["a","c"], "hijos": ["d"] },
    "c": { "padres": [],        "hijos": ["b"] },
    "d": { "padres": ["b"],     "hijos": [] }
}

def padres_de(nodo, red_local):
    """regresa los padres directos del nodo (causas de nodo)."""
    return red_local[nodo]["padres"]


def hijos_de(nodo, red_local):
    """regresa los hijos directos del nodo (efectos del nodo)."""
    return red_local[nodo]["hijos"]


def copadres_de(nodo, red_local):
    """
    regresa los otros padres de los hijos del nodo.
    estos tambien importan para predecir el nodo,
    porque explican en conjunto a los mismos hijos.
    """
    resultado = set()
    for h in hijos_de(nodo, red_local):
        for p in padres_de(h, red_local):
            if p != nodo:
                resultado.add(p)
    return list(resultado)


def manto_de_markov(nodo, red_local):
    """
    arma el manto de markov del nodo:
    padres + hijos + copadres (sin duplicados y sin el mismo nodo).
    este conjunto es toda la info relevante para ese nodo.
    """
    lista_padres = padres_de(nodo, red_local)
    lista_hijos = hijos_de(nodo, red_local)
    lista_copadres = copadres_de(nodo, red_local)

    conjunto = set(lista_padres + lista_hijos + lista_copadres)
    if nodo in conjunto:
        conjunto.remove(nodo)
    return list(conjunto)

print("manto de markov de b:", manto_de_markov("b", red))