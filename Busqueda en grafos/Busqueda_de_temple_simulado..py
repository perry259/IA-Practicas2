# busqueda de temple simulado
# este busca un buen estado (una buena solucion)
# diferencia contra ascension de colinas:
# - ascension de colinas solo se mueve si encuentra algo mejor
# - temple simulado a veces acepta algo peor a corto plazo
# para que sirve aceptar algo peor?
# - para no quedarse atorado en un punto que no es el mejor
# como decide si acepta algo peor:
# - usa una "temperatura" (temp)
# - al inicio la temperatura es alta, entonces se permite cambiar
# - la temperatura va bajando, y despues ya casi no acepta cosas malas
# - cada estado es un numero
# - valor(x) = que tan bueno es x (numero mas grande = mejor)
# - vecinos[x] = lista de estados a los que me puedo mover desde x
#   import random  -> para elegir vecinos al azar
#   import math    -> para calcular la probabilidad de aceptar un peor estado

import random
import math

def elegir_vecino_aleatorio(actual, vecinos):
    """
    actual: estado actual
    vecinos: con lista de vecinos para cada estado
             ejemplo:
             vecinos = {
                 3: [4, 5, 6],
                 4: [5, 7],
                 5: [6]
             }

    regresa un vecino aleatorio de la lista vecinos[actual]
    si no hay vecinos, regresa None
    """

    opciones = vecinos.get(actual, [])
    if not opciones:
        return None
    return random.choice(opciones)  # random.choice elige 1 elemento al azar

def temple_simulado(inicio, vecinos, valor, temp_inicial, factor_enfriar, iter_max):
    """
    inicio: estado inicial (por ejemplo 3)
    vecinos: con las conexiones posibles
    valor: funcion que regresa el puntaje de un estado (mas alto = mejor)
    temp_inicial: temperatura inicial (por ejemplo 10.0)
    factor_enfriar: de cuanto baja la temperatura en cada paso (ej 0.9)
    iter_max: cuantas iteraciones maximo voy a intentar

    esta funcion regresa:
    - mejor_estado_global: el mejor estado que vi en toda la busqueda
    - historial: lista con los estados que fui tomando en orden

    como trabaja temple_simulado paso a paso:
    1. empiezo en "actual"
    2. cada paso elijo un vecino al azar
    3. si el vecino es mejor, me muevo
    4. si el vecino es peor:
         a veces acepto moverme igual
         depende de la temperatura actual
    5. bajo la temperatura
    """

    actual = inicio
    mejor_estado_global = actual
    historial = [actual]

    temp = temp_inicial  # temperatura actual

    for _ in range(iter_max):
        vecino = elegir_vecino_aleatorio(actual, vecinos)
        if vecino is None:
            # no me puedo mover a ningun lado
            break

        valor_actual = valor(actual)
        valor_vecino = valor(vecino)

        # si el vecino es mejor, me muevo directo
        if valor_vecino > valor_actual:
            actual = vecino
        else:
            # el vecino es peor
            # calculamos si aun asi lo aceptamos
            # diff = que tan peor es
            diff = valor_vecino - valor_actual  # esto va a ser negativo

            # prob = probabilidad de aceptar el movimiento peor
            # math.exp(x) = e^x
            # mientras temp sea grande, esta prob puede ser alta
            # cuando temp baja, ya casi no acepta cosas peores
            prob = math.exp(diff / temp) if temp > 0 else 0

            # random.random() da un numero entre 0.0 y 1.0
            # si prob es mas grande que ese numero aleatorio, aceptamos movernos
            if random.random() < prob:
                actual = vecino
                # si no pasa el if, me quedo igual en "actual"

        # guardo el estado actual en historial
        historial.append(actual)

        # actualizo el mejor estado global si encontre algo mejor
        if valor(actual) > valor(mejor_estado_global):
            mejor_estado_global = actual

        # bajo la temperatura
        temp = temp * factor_enfriar
        # ejemplo: si temp era 10 y factor_enfriar es 0.9
        # siguiente temp = 9
        # luego 8.1
        # luego 7.29
        # etc

        # si la temperatura ya es muy baja, no tiene caso seguir
        if temp <= 0.0001:
            break

    return mejor_estado_global, historial

if __name__ == "__main__":
    # vecinos dice a donde puedo ir desde cada estado
    # en este ejemplo cada estado es un numero
    vecinos = {
        3: [4, 5, 6],
        4: [5, 7],
        5: [6, 7],
        6: [7, 8],
        7: [8, 9],
        8: [9, 10],
        9: [10],
        10: []
    }

    # esta funcion le da un valor a cada estado
    # aqui simplemente el valor es el mismo numero
    # ejemplo: valor(8) = 8, valor(10) = 10
    def valor(x):
        return x

    mejor, pasos = temple_simulado(
        inicio=3,
        vecinos=vecinos,
        valor=valor,
        temp_inicial=10.0,   # temperatura alta al inicio
        factor_enfriar=0.9,  # que tan rapido baja la temperatura
        iter_max=50          # cuantas iteraciones maximo
    )

    print("mejor estado encontrado:", mejor)
    print("historial de estados visitados:", pasos)

    # - temp_inicial: mientras sea alta, el algoritmo se permite probar cosas peores
    # - factor_enfriar: numero entre 0 y 1, controla que tan rapido baja temp
    # - math.exp(diff / temp): calcula la probabilidad de aceptar un movimiento peor
    # - random.random(): numero aleatorio para decidir si acepto ese movimiento