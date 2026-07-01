# Esta red neuronal simple con una capa oculta aprende la función XOR
# usando activación ReLU en la capa oculta y Sigmoid en la salida.

import numpy as np

# Función de activación ReLU y su derivada
def relu(x):
    return np.maximum(0, x)

def relu_derivada(x):
    return np.where(x > 0, 1, 0)

# Clase de la red neuronal
class RedNeuronal:
    def __init__(self, input_size, hidden_size, output_size):
        # Inicialización de pesos y sesgos
        self.w1 = np.random.rand(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.w2 = np.random.rand(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))

    def forward(self, X):
        self.z1 = np.dot(X, self.w1) + self.b1
        self.a1 = relu(self.z1)
        self.z2 = np.dot(self.a1, self.w2) + self.b2
        return self.sigmoid(self.z2)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def backward(self, X, y, output):
        # Gradientes
        output_error = output - y
        output_delta = output_error * output * (1 - output)
        hidden_error = output_delta.dot(self.w2.T)
        hidden_delta = hidden_error * relu_derivada(self.z1)

        # Actualización de pesos y sesgos
        self.w2 -= self.a1.T.dot(output_delta) * 0.01
        self.b2 -= np.sum(output_delta, axis=0, keepdims=True) * 0.01
        self.w1 -= X.T.dot(hidden_delta) * 0.01
        self.b1 -= np.sum(hidden_delta, axis=0, keepdims=True) * 0.01

    def entrenar(self, X, y, epochs=1000):
        for epoch in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output)
            if epoch % 100 == 0:
                loss = np.mean(np.square(y - output))
                print(f'Epoch {epoch}, Loss: {loss:.4f}')

# Datos de entrenamiento para XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# Inicializamos y entrenamos la red neuronal
red_neuronal = RedNeuronal(input_size=2, hidden_size=2, output_size=1)
red_neuronal.entrenar(X, y)

# Predicciones finales
predicciones = red_neuronal.forward(X)
print("Predicciones después del entrenamiento:")
print(predicciones)