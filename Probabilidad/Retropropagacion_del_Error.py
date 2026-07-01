# Este código implementa una red neuronal simple de 2 capas para resolver el problema XOR
# utilizando la técnica de retropropagación del error.

import numpy as np

# Función de activación sigmoide
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivada de la función de activación sigmoide
def sigmoid_derivative(x):
    return x * (1 - x)

# Datos de entrada (XOR)
X = np.array([[0, 0],[0, 1],[1, 0],[1, 1]])

# Salidas esperadas
y = np.array([[0],[1],[1],[0]])

# Inicialización de pesos aleatorios
np.random.seed(42)
input_size = X.shape[1]
hidden_layer_size = 2
output_size = y.shape[1]

weights_input_hidden = np.random.rand(input_size, hidden_layer_size)
weights_hidden_output = np.random.rand(hidden_layer_size, output_size)

# Tasa de aprendizaje
learning_rate = 0.1

# Entrenamiento
for epoch in range(10000):
    # Forward pass
    hidden_input = np.dot(X, weights_input_hidden)
    hidden_output = sigmoid(hidden_input)

    output_input = np.dot(hidden_output, weights_hidden_output)
    predicted_output = sigmoid(output_input)

    # Error
    error = y - predicted_output

    # Backward pass
    d_output = error * sigmoid_derivative(predicted_output)
    error_hidden = d_output.dot(weights_hidden_output.T)
    d_hidden = error_hidden * sigmoid_derivative(hidden_output)

    # Actualización de pesos
    weights_hidden_output += hidden_output.T.dot(d_output) * learning_rate
    weights_input_hidden += X.T.dot(d_hidden) * learning_rate

print("Salidas de la red después del entrenamiento:")
print(predicted_output)