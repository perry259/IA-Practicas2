# Este código implementa el algoritmo de Viterbi para un HMM,
# permitiendo encontrar la secuencia de estados más probable
# dada una secuencia de observaciones.

import numpy as np

# Parámetros del modelo HMM
estados = ['Soleado', 'Lluvioso']
observaciones = ['Caminar', 'Comprar', 'Limpiar']
prob_inicial = np.array([0.6, 0.4])

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

# Algoritmo de Viterbi
def viterbi(prob_inicial, matriz_transicion, matriz_emision, observacion_seq):
    n_estados = len(estados)
    n_observaciones = len(observacion_seq)
    T1 = np.zeros((n_estados, n_observaciones))
    T2 = np.zeros((n_estados, n_observaciones), dtype=int)
    
    # Inicialización
    T1[:, 0] = prob_inicial * matriz_emision[:, observacion_seq[0]]
    
    # Iteración
    for t in range(1, n_observaciones):
        for j in range(n_estados):
            prob_tran = T1[:, t-1] * matriz_transicion[:, j]
            T1[j, t] = np.max(prob_tran) * matriz_emision[j, observacion_seq[t]]
            T2[j, t] = np.argmax(prob_tran)
    
    # Reconstrucción del camino más probable
    camino_optimo = np.zeros(n_observaciones, dtype=int)
    camino_optimo[-1] = np.argmax(T1[:, -1])
    for t in range(n_observaciones - 2, -1, -1):
        camino_optimo[t] = T2[camino_optimo[t+1], t+1]
    
    camino_estado = [estados[i] for i in camino_optimo]
    return camino_estado

# Aplicación del algoritmo de Viterbi
camino_optimo = viterbi(prob_inicial, matriz_transicion, matriz_emision, observacion_seq)

# Mostrar resultados
print("Secuencia de observaciones:", [observaciones[i] for i in observacion_seq])
print("Camino de estados más probable:", camino_optimo)
