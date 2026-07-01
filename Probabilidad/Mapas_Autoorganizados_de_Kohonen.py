# Este código implementa un mapa autoorganizado (SOM) de Kohonen
# para mapear y visualizar patrones de datos de entrada en un espacio 2D.

import numpy as np
import matplotlib.pyplot as plt

class KohonenMap:
    def __init__(self, input_dim, map_size, learning_rate=0.5, n_iterations=100):
        self.input_dim = input_dim
        self.map_size = map_size
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = np.random.rand(map_size[0], map_size[1], input_dim)  # Pesos iniciales

    def find_bmu(self, x):
        # Encuentra la Unidad de Mejor Coincidencia (BMU)
        bmu_idx = np.argmin(np.linalg.norm(self.weights - x, axis=2))
        return np.unravel_index(bmu_idx, self.map_size)

    def update_weights(self, x, bmu_idx, iteration):
        # Actualiza los pesos de la red
        lr = self.learning_rate * (1 - (iteration / self.n_iterations))
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                dist = np.linalg.norm(np.array([i, j]) - np.array(bmu_idx))
                if dist <= 1:  # Radio de vecindad
                    self.weights[i, j] += lr * (x - self.weights[i, j])

    def train(self, data):
        # Entrena el mapa con los datos
        for iteration in range(self.n_iterations):
            for x in data:
                bmu_idx = self.find_bmu(x)
                self.update_weights(x, bmu_idx, iteration)

    def plot_weights(self):
        # Visualiza los pesos aprendidos del mapa
        for dim in range(self.input_dim):
            plt.figure()
            plt.imshow(self.weights[:, :, dim], cmap='viridis')
            plt.colorbar()
            plt.title(f'Pesos del Mapa Autoorganizado - Dimensión {dim + 1}')
            plt.xlabel('Unidad de la Red (Eje X)')
            plt.ylabel('Unidad de la Red (Eje Y)')
            plt.show()

# Generar datos de ejemplo (2D)
n_samples = 100
data = np.random.rand(n_samples, 2)

# Crear y entrenar el mapa autoorganizado
som = KohonenMap(input_dim=2, map_size=(10, 10), learning_rate=0.5, n_iterations=100)
som.train(data)

# Visualizar los pesos aprendidos
som.plot_weights()