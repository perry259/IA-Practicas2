# Este código grafica cuatro funciones de activación comúnmente usadas
# en redes neuronales: Sigmoid, Tanh, ReLU y Leaky ReLU.

import numpy as np
import matplotlib.pyplot as plt

# Rango de valores para la función
x = np.linspace(-10, 10, 100)

# Definición de funciones de activación
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

def relu(x):
    return np.maximum(0, x)

def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

# Calculamos las salidas para cada función
sigmoid_output = sigmoid(x)
tanh_output = tanh(x)
relu_output = relu(x)
leaky_relu_output = leaky_relu(x)

# Configuración de la figura para mostrar las gráficas
plt.figure(figsize=(12, 8))

# Gráfica de Sigmoid
plt.subplot(2, 2, 1)
plt.plot(x, sigmoid_output, color='blue', label='Sigmoid')
plt.title('Función Sigmoid')
plt.grid(True)
plt.legend()

# Gráfica de Tanh
plt.subplot(2, 2, 2)
plt.plot(x, tanh_output, color='orange', label='Tanh')
plt.title('Función Tanh')
plt.grid(True)
plt.legend()

# Gráfica de ReLU
plt.subplot(2, 2, 3)
plt.plot(x, relu_output, color='green', label='ReLU')
plt.title('Función ReLU')
plt.grid(True)
plt.legend()

# Gráfica de Leaky ReLU
plt.subplot(2, 2, 4)
plt.plot(x, leaky_relu_output, color='red', label='Leaky ReLU')
plt.title('Función Leaky ReLU')
plt.grid(True)
plt.legend()

# Ajuste de diseño y visualización
plt.tight_layout()
plt.show()