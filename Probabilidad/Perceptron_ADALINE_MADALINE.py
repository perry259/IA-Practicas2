# Este código implementa un perceptrón simple para clasificar dos clases
# en un conjunto de datos 2D y visualiza la línea de decisión.

import numpy as np
import matplotlib.pyplot as plt

# Generar datos de ejemplo: dos clases (0 y 1)
np.random.seed(0)
n_samples = 100
X = np.random.randn(n_samples, 2)  # 100 puntos en 2D
Y = np.array([1 if x[0] + x[1] > 0 else 0 for x in X])  # Clase 1 si x1 + x2 > 0, clase 0 de lo contrario

# Agregar un sesgo a los datos
X_biased = np.c_[np.ones((X.shape[0], 1)), X]  # Columna de 1s para el término de sesgo

# Parámetros del Perceptrón
learning_rate = 0.1
n_iterations = 1000

# Inicializar los pesos aleatoriamente
weights = np.random.randn(X_biased.shape[1])

# Función de activación (step function)
def step_function(x):
    return 1 if x >= 0 else 0

# Entrenamiento del Perceptrón
for _ in range(n_iterations):
    for i in range(n_samples):
        # Salida lineal
        linear_output = np.dot(X_biased[i], weights)
        predicted = step_function(linear_output)
        # Actualización de pesos
        update = learning_rate * (Y[i] - predicted)
        weights += update * X_biased[i]

# Visualización de los resultados
plt.figure(figsize=(8, 6))
plt.scatter(X[Y == 0][:, 0], X[Y == 0][:, 1], color='red', label='Clase 0')
plt.scatter(X[Y == 1][:, 0], X[Y == 1][:, 1], color='blue', label='Clase 1')

# Graficar la línea de decisión
x_values = np.linspace(-3, 3, 100)
y_values = -(weights[0] + weights[1] * x_values) / weights[2]
plt.plot(x_values, y_values, color='green', label='Línea de Decisión')

plt.title('Perceptrón: Clasificación de dos clases')
plt.xlabel('Característica 1')
plt.ylabel('Característica 2')
plt.legend()
plt.grid(True)
plt.show()