
# Calcula y grafica la probabilidad de obtener cierto número de caras
# al lanzar una moneda varias veces, usando la distribución binomial.

import numpy as np                       # Biblioteca para cálculos numéricos y arreglos
import matplotlib.pyplot as plt          # Para crear gráficos
from scipy.stats import binom            # Importa la distribución binomial

n_lanzamientos = 10                      # Número total de lanzamientos
probabilidad_exito = 0.5                 # Probabilidad de obtener cara en un lanzamiento

x = np.arange(0, n_lanzamientos + 1)     # Posibles resultados: 0, 1, 2, ..., 10 caras
probabilidades = binom.pmf(x, n_lanzamientos, probabilidad_exito)
# Calcula la probabilidad de obtener exactamente k caras para cada valor en x

plt.figure(figsize=(10, 6))              # Crea la figura del gráfico con tamaño 10x6

plt.stem(x, probabilidades, basefmt=" ", use_line_collection=True)
# Dibuja el gráfico de tallos mostrando las probabilidades

plt.xlabel("Número de éxitos (caras)")    # Etiqueta eje X
plt.ylabel("Probabilidad")                # Etiqueta eje Y
plt.title("Distribución Binomial: Caras en lanzamientos de moneda")
plt.grid(True)                            # Activa la cuadrícula
plt.show()                                # Muestra la gráfica