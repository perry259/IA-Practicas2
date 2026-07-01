# Esta red neuronal simple con una capa oculta realiza propagación
# hacia adelante usando ReLU, sin entrenamiento (solo cálculo de salida).

import numpy as np

# Función de activación ReLU y su derivada
def relu(x):
    return np.maximum(0, x)

def derivada_relu(x):
    return np.where(x > 0, 1, 0)

# Clase para una neurona individual
class Neurona:
    def __init__(self, num_entradas):
        self.pesos = np.random.rand(num_entradas)    # Pesos aleatorios
        self.sesgo = np.random.rand()                # Sesgo aleatorio escalar

    def feedforward(self, entrada):
        return relu(np.dot(entrada, self.pesos) + self.sesgo)

# Clase para una capa de neuronas
class Capa:
    def __init__(self, num_neuronas, num_entradas):
        self.neuronas = [Neurona(num_entradas) for _ in range(num_neuronas)]

    def feedforward(self, entrada):
        return np.array([neurona.feedforward(entrada) for neurona in self.neuronas])

# Datos de entrada para XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])  # Salidas esperadas

# Inicialización de capas
capa_oculta = Capa(num_neuronas=2, num_entradas=2)
capa_salida = Capa(num_neuronas=1, num_entradas=2)

# Propagación hacia adelante
print("Resultados de la propagación hacia adelante:")
for entrada in X:
    salida_oculta = capa_oculta.feedforward(entrada)
    salida_final = capa_salida.feedforward(salida_oculta)
    print(f"Entrada: {entrada}, Salida final: {salida_final}")