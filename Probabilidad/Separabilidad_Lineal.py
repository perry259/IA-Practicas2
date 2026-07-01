import numpy as np
import matplotlib.pyplot as plt

# Generar datos de ejemplo: puntos separables linealmente
np.random.seed(0)
n_samples = 100
X1 = np.random.randn(n_samples, 2) + np.array([1, 1])   # Clase 1
X2 = np.random.randn(n_samples, 2) + np.array([-1, -1]) # Clase 0
X = np.vstack((X1, X2))                                  # Unir las clases
Y = np.array([1] * n_samples + [0] * n_samples)          # Etiquetas de clase

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
    for i in range(len(Y)):
        linear_output = np.dot(X_biased[i], weights)
        predicted = step_function(linear_output)
        # Actualización de pesos
        update = learning_rate * (Y[i] - predicted)
        weights += update * X_biased[i]

# Visualización de los resultados
plt.figure(figsize=(8, 6))
plt.scatter(X[Y == 0][:, 0], X[Y == 0][:, 1], color='red', label='Clase 0')
plt.scatter(X[Y == 1][:, 0], X[Y == 1][:, 1], color='blue', label='Clase 1')

# Línea de decisión
x_values = np.linspace(-3, 3, 100)
y_values = -(weights[0] + weights[1] * x_values) / weights[2]
plt.plot(x_values, y_values, color='green', label='Línea de Decisión')

plt.title('Separabilidad Lineal: Perceptrón')
plt.xlabel('Característica 1')
plt.ylabel('Característica 2')
plt.legend()
plt.grid(True)
plt.xlim(-3, 3)
plt.ylim(-3, 3)
plt.axhline(0, color='black', lw=0.5, ls='--')
plt.axvline(0, color='black', lw=0.5, ls='--')
plt.show()