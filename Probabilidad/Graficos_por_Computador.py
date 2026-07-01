# Este código genera un gráfico de dispersión de datos aleatorios
# con colores y tamaños variables para cada punto.

import numpy as np
import matplotlib.pyplot as plt

# ======================= GENERACIÓN DE DATOS =======================

np.random.seed(0)
n = 100  # Número de puntos

x = np.random.rand(n) * 100  # Coordenadas X
y = np.random.rand(n) * 100  # Coordenadas Y
colores = np.random.rand(n)  # Colores aleatorios para cada punto
tamanos = np.random.rand(n) * 100  # Tamaños aleatorios para cada punto

# ======================= VISUALIZACIÓN ============================

plt.figure(figsize=(10, 6))
plt.scatter(x, y, c=colores, s=tamanos, alpha=0.5, cmap='viridis')

# Etiquetas y título
plt.title('Gráfico de Dispersión de Datos Aleatorios', fontsize=16)
plt.xlabel('Eje X', fontsize=14)
plt.ylabel('Eje Y', fontsize=14)
plt.grid(True)

plt.colorbar(label='Colores')
plt.show()