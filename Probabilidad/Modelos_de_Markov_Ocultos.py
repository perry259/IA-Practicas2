# Este código calcula la probabilidad de una secuencia de observaciones
# dada un modelo oculto de Markov con estados, probabilidades de transición,
# probabilidades de emisión y probabilidades iniciales.

# Probabilidades de transición entre estados ocultos
probabilidades_transicion = {
    'Fernanda': {'Fernanda': 0.6, 'Emmanuel': 0.3, 'Emiliano': 0.1},
    'Emmanuel': {'Fernanda': 0.2, 'Emmanuel': 0.5, 'Emiliano': 0.3},
    'Emiliano': {'Fernanda': 0.1, 'Emmanuel': 0.4, 'Emiliano': 0.5}
}

# Probabilidades de emisión para cada estado oculto
probabilidades_emision = {
    'Fernanda': {'si': 0.7, 'no': 0.3},
    'Emmanuel': {'si': 0.4, 'no': 0.6},
    'Emiliano': {'si': 0.8, 'no': 0.2}
}

# Probabilidades iniciales para cada estado oculto
probabilidades_iniciales = {'Fernanda': 0.5, 'Emmanuel': 0.3, 'Emiliano': 0.2}

# Secuencia de observaciones
secuencia_observaciones = ['si', 'no', 'si']

# Función que calcula la probabilidad de la secuencia usando algoritmo hacia adelante
def calcular_probabilidad(secuencia_observaciones):
    # Inicialización: probabilidades al primer tiempo
    prob_actuales = {estado: probabilidades_iniciales[estado] * probabilidades_emision[estado][secuencia_observaciones[0]]
                     for estado in probabilidades_iniciales}

    # Iteración sobre cada observación siguiente
    for obs in secuencia_observaciones[1:]:
        prob_siguientes = {}
        for estado in probabilidades_transicion:
            # Probabilidad total de estar en 'estado' dado las observaciones previas
            prob_siguientes[estado] = sum(
                prob_actuales[estado_anterior] * probabilidades_transicion[estado_anterior][estado]
                for estado_anterior in probabilidades_transicion
            ) * probabilidades_emision[estado][obs]

        prob_actuales = prob_siguientes

    # Suma de probabilidades de todos los estados para obtener la probabilidad total
    return sum(prob_actuales.values())

# Cálculo de la probabilidad de la secuencia
probabilidad_resultado = calcular_probabilidad(secuencia_observaciones)

print("Probabilidad de la secuencia de observaciones:", probabilidad_resultado)