# Este código implementa los algoritmos hacia adelante y hacia atrás
# para un modelo oculto de Markov (HMM), calculando la probabilidad
# de una secuencia de observaciones dada la estructura del modelo.

import numpy as np

# Parámetros del modelo HMM
estados = ['Soleado', 'Lluvioso']
observaciones = ['Caminar', 'Comprar', 'Limpiar']
prob_inicial = np.array([0.6, 0.4])  # Probabilidades iniciales para cada estado

# Matriz de transición entre estados
matriz_transicion = np.array([
    [0.7, 0.3],  # Transiciones desde 'Soleado'
    [0.4, 0.6]   # Transiciones desde 'Lluvioso'
])

# Matriz de emisión (probabilidad de cada observación en cada estado)
matriz_emision = np.array([
    [0.1, 0.4, 0.5],  # Emisiones desde 'Soleado'
    [0.6, 0.3, 0.1]   # Emisiones desde 'Lluvioso'
])

# Secuencia de observaciones: 0->Caminar, 1->Comprar, 2->Limpiar
observacion_seq = [0, 1, 2]

# Algoritmo Hacia Adelante
def hacia_adelante(prob_inicial, matriz_transicion, matriz_emision, observacion_seq):
    alfa = np.zeros((len(observacion_seq), len(estados)))
    alfa[0, :] = prob_inicial * matriz_emision[:, observacion_seq[0]]
    
    for t in range(1, len(observacion_seq)):
        for j in range(len(estados)):
            alfa[t, j] = np.sum(alfa[t - 1] * matriz_transicion[:, j]) * matriz_emision[j, observacion_seq[t]]
    
    return alfa

# Algoritmo Hacia Atrás
def hacia_atras(matriz_transicion, matriz_emision, observacion_seq):
    beta = np.zeros((len(observacion_seq), len(estados)))
    beta[-1, :] = 1
    
    for t in range(len(observacion_seq) - 2, -1, -1):
        for i in range(len(estados)):
            beta[t, i] = np.sum(matriz_transicion[i, :] * matriz_emision[:, observacion_seq[t + 1]] * beta[t + 1])
    
    return beta

# Aplicación de los algoritmos hacia adelante y hacia atrás
alfa = hacia_adelante(prob_inicial, matriz_transicion, matriz_emision, observacion_seq)
beta = hacia_atras(matriz_transicion, matriz_emision, observacion_seq)

# Cálculo de la probabilidad de la secuencia de observaciones
probabilidad_observaciones = np.sum(alfa[-1, :])

# Mostrar resultados
print(f"Probabilidad de la secuencia de observaciones: {probabilidad_observaciones:.4f}")
print("Alfa (hacia adelante):")
print(alfa)
print("Beta (hacia atrás):")
print(beta)