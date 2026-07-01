# Implementa una red neuronal de una capa oculta para clasificación binaria,
# utilizando ReLU en la capa oculta y sigmoide en la capa de salida.
# Incluye entrenamiento con retropropagación y cálculo de pérdida MSE.

import numpy as np                            # Biblioteca para cálculos numéricos

# Función de activación ReLU
def relu(x):
    return np.maximum(0, x)

# Derivada de ReLU
def relu_derivada(x):
    return np.where(x > 0, 1, 0)

# Función sigmoide para salida
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivada de sigmoide
def sigmoid_derivada(x):
    s = sigmoid(x)
    return s * (1 - s)

class RedNeuronal:
    def __init__(self, input_size, hidden_size, output_size):
        # Inicializamos pesos pequeños y sesgos en cero
        self.w1 = np.random.rand(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.w2 = np.random.rand(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))

    def forward(self, X):
        # Propagación hacia adelante
        self.z1 = np.dot(X, self.w1) + self.b1
        self.a1 = relu(self.z1)
        self.z2 = np.dot(self.a1, self.w2) + self.b2
        self.a2 = sigmoid(self.z2)
        return self.a2

    def backward(self, X, y, output, lr=0.01):
        # Retropropagación y actualización de pesos
        error_output = output - y
        delta_output = error_output * sigmoid_derivada(self.z2)

        error_hidden = delta_output.dot(self.w2.T)
        delta_hidden = error_hidden * relu_derivada(self.z1)

        # Actualización de pesos y sesgos
        self.w2 -= self.a1.T.dot(delta_output) * lr
        self.b2 -= np.sum(delta_output, axis=0, keepdims=True) * lr
        self.w1 -= X.T.dot(delta_hidden) * lr
        self.b1 -= np.sum(delta_hidden, axis=0, keepdims=True) * lr

    def entrenar(self, X, y, epochs=1000, lr=0.01):
        for epoch in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output, lr)
            if epoch % 100 == 0:
                loss = np.mean(np.square(y - output))
                print(f'Epoch {epoch}, Loss: {loss}')

# Datos de ejemplo: XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# Inicialización y entrenamiento
red = RedNeuronal(input_size=2, hidden_size=2, output_size=1)
red.entrenar(X, y)

# Resultados después del entrenamiento
predicciones = red.forward(X)
print("\nPredicciones después del entrenamiento:")
print(predicciones)