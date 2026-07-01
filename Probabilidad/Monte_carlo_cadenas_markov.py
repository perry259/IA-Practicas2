"""
monte carlo para cadenas de markov (mcmc)
mcmc es una forma de aproximar probabilidades cuando la red o el modelo es muy grande
en vez de calcular todo exacto, caminamos por valores posibles poco a poco
y contamos que tan seguido caemos en cada valor
sirve para aproximar p(x) o p(x | evidencia) cuando hacer las cuentas directo es muy caro
esto se usa un monton en ia bayesiana
1. tengo una distribucion objetivo (la prob que quiero aproximar)
2. hago una cadena de markov: o sea, voy saltando de un estado a otro
3. acepto o rechazo saltos segun que tan probable es el nuevo estado
4. al final cuento en que estados estuve mas tiempo
   eso me da las probabilidades aproximadas
"""

import random

# definimos una distribucion objetivo p(x) para una variable x con 3 posibles valores
# esto representa la prob deseada (puede venir de un modelo bayesiano grande)
# no tiene que estar normalizada (no tiene que sumar 1, eso lo aprende el muestreo)
objetivo = {
    "estado_a": 0.1,
    "estado_b": 0.4,
    "estado_c": 0.5
}

def prob_objetivo(estado):
    """
    regresa el peso del estado segun la distribucion objetivo
    si el estado es raro, su prob es chica
    si el estado es comun, su prob es grande
    """
    return objetivo[estado]

def proponer_estado(actual, todos):
    """
    propone un nuevo estado aleatorio
    en mcmc esto es como decir:
    intento saltar a otro lugar
    """
    candidatos = [s for s in todos if s != actual]
    return random.choice(candidatos)

def metropolis_hastings(iteraciones, estado_inicial):
    """
    este es el algoritmo mcmc basico tipo metropolis-hastings

    pasos por iteracion:
    1. tengo un estado actual
    2. propongo un estado nuevo
    3. calculo razon = p(nuevo)/p(actual)
    4. si razon >= 1 lo acepto
       si razon < 1 lo acepto con prob = razon
    5. guardo donde quede

    al final regreso el historial de estados visitados
    """
    estado_actual = estado_inicial
    historial = [estado_actual]

    todos_estados = list(objetivo.keys())

    for _ in range(iteraciones):
        candidato = proponer_estado(estado_actual, todos_estados)

        p_actual = prob_objetivo(estado_actual)
        p_candidato = prob_objetivo(candidato)

        # razon de aceptacion
        if p_actual == 0:
            acepto = True
        else:
            razon = p_candidato / p_actual
            # aceptacion probabilistica
            acepto = (random.random() < min(1.0, razon))

        if acepto:
            estado_actual = candidato

        historial.append(estado_actual)

    return historial

def estimar_distribucion(muestras):
    """
    cuenta cuantas veces aparecio cada estado
    y lo convierte en prob aproximada
    """
    conteo = {}
    for s in muestras:
        conteo[s] = conteo.get(s, 0) + 1

    total = len(muestras)
    aprox = {s: conteo[s] / total for s in conteo}
    return aprox

# corremos mcmc
muestras = metropolis_hastings(
    iteraciones=5000,
    estado_inicial="estado_a"
)

aprox = estimar_distribucion(muestras)

print("aprox de la distribucion con mcmc:")
for estado, p in aprox.items():
    print(estado, "->", round(p, 4))