
# Implementa una red neuronal simple con una capa oculta,
# que aprende la función XOR mediante el uso de la función ReLU
# y entrenamiento por retropropagación.

import numpy as np                            # Biblioteca para cálculos numéricos

# Función de activación ReLU
def relu(x):
    return np.maximum(0, x)

# Derivada de la función ReLU
def relu_derivada(x):
    return np.where(x > 0, 1, 0)

class RedNeuronal:
    def __init__(self, input_size, hidden_size, output_size):
        # Inicialización de pesos y sesgos con valores pequeños
        self.w1 = np.random.rand(input_size, hidden_size) * 0.01   # Pesos entrada → oculta
        self.b1 = np.zeros((1, hidden_size))                       # Sesgo capa oculta
        self.w2 = np.random.rand(hidden_size, output_size) * 0.01  # Pesos oculta → salida
        self.b2 = np.zeros((1, output_size))                       # Sesgo capa de salida

    def forward(self, X):
        # Propagación hacia adelante (feedforward)
        self.z1 = np.dot(X, self.w1) + self.b1                     # Suma ponderada capa oculta
        self.a1 = relu(self.z1)                                    # Aplicación de ReLU
        self.z2 = np.dot(self.a1, self.w2) + self.b2               # Suma ponderada capa salida
        return self.sigmoid(self.z2)                               # Activación sigmoide final

    def sigmoid(self, x):
        # Función sigmoide para salida entre 0 y 1
        return 1 / (1 + np.exp(-x))

    def backward(self, X, y, output):
        # Calcula los gradientes y actualiza pesos y sesgos
        output_error = output - y                                  # Error en salida
        output_delta = output_error * output * (1 - output)        # Gradiente salida

        hidden_error = output_delta.dot(self.w2.T)                 # Error en capa oculta
        hidden_delta = hidden_error * relu_derivada(self.z1)       # Gradiente capa oculta

        # Actualización de parámetros con tasa de aprendizaje de 0.01
        self.w2 -= self.a1.T.dot(output_delta) * 0.01
        self.b2 -= np.sum(output_delta, axis=0, keepdims=True) * 0.01
        self.w1 -= X.T.dot(hidden_delta) * 0.01
        self.b1 -= np.sum(hidden_delta, axis=0, keepdims=True) * 0.01

    def entrenar(self, X, y, epochs=1000):
        # Entrena la red durante varias iteraciones (epochs)
        for epoch in range(epochs):
            output = self.forward(X)                               # Propagación hacia adelante
            self.backward(X, y, output)                            # Retropropagación
            if epoch % 100 == 0:                                   # Muestra el error cada 100 epochs
                loss = np.mean(np.square(y - output))
                print(f'Epoch {epoch}, Loss: {loss}')

# Datos de ejemplo: tabla XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])                    # Entradas
y = np.array([[0], [1], [1], [0]])                                # Salidas esperadas

# Creación y entrenamiento de la red neuronal
red_neuronal = RedNeuronal(input_size=2, hidden_size=2, output_size=1)
red_neuronal.entrenar(X, y)

# Prueba del modelo entrenado
predicciones = red_neuronal.forward(X)
print("\nPredicciones después del entrenamiento:")
print(predicciones)