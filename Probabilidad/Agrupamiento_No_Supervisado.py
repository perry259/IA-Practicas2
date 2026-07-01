# Este código genera datos sintéticos y aplica el algoritmo K-means
# para realizar agrupamiento no supervisado. Se visualizan los puntos
# originales y los clusters con sus respectivos centros.

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

# Generación de datos sintéticos
n_samples = 300
n_features = 2
n_clusters = 4
X, _ = make_blobs(n_samples=n_samples, centers=n_clusters, cluster_std=0.60, random_state=42)

# Visualización de los datos generados
plt.scatter(X[:, 0], X[:, 1], s=30, alpha=0.5)
plt.title("Datos Generados para Agrupamiento")
plt.xlabel("Característica 1")
plt.ylabel("Característica 2")
plt.grid(True)
plt.show()

# Aplicación de K-means
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(X)
labels = kmeans.labels_
centros = kmeans.cluster_centers_

# Visualización de los resultados del agrupamiento
plt.scatter(X[:, 0], X[:, 1], c=labels, s=30, cmap='viridis', alpha=0.5)
plt.scatter(centros[:, 0], centros[:, 1], c='red', s=200, marker='X', label='Centros de Clusters')
plt.title("Resultado del Agrupamiento K-means")
plt.xlabel("Característica 1")
plt.ylabel("Característica 2")
plt.legend()
plt.grid(True)
plt.show()

# Mostrar los centros de los clusters
print("Centros de los clusters (K-means):")
print(centros)