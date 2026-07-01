# Este código implementa un filtro de partículas para estimar
# la posición de un objeto a partir de mediciones ruidosas y
# simulando su movimiento.

import numpy as np

class FiltradoParticulas:
    def __init__(self, n_particulas, rango, ruido_mov, ruido_medicion):
        self.n_particulas = n_particulas
        self.ruido_mov = ruido_mov
        self.ruido_medicion = ruido_medicion
        self.particulas = np.random.uniform(-rango, rango, n_particulas)

    def predecir(self, movimiento):
        # Actualiza la posición de cada partícula según el movimiento y el ruido
        self.particulas += movimiento + np.random.normal(0, self.ruido_mov, self.n_particulas)

    def actualizar(self, medicion):
        # Calcula pesos basados en la distancia de cada partícula a la medición
        pesos = (1 / (np.sqrt(2 * np.pi) * self.ruido_medicion)) * \
                np.exp(-0.5 * ((self.particulas - medicion) / self.ruido_medicion) ** 2)
        pesos /= np.sum(pesos)  # Normalización

        # Resampling de partículas basado en los pesos
        indices = np.random.choice(range(self.n_particulas), size=self.n_particulas, p=pesos)
        self.particulas = self.particulas[indices]

    def estimar(self):
        # Retorna el promedio de las partículas como estimación de posición
        return np.mean(self.particulas)

# Parámetros del filtro
n_particulas = 1000
rango = 10
ruido_mov = 1.0
ruido_medicion = 2.0
filtro = FiltradoParticulas(n_particulas, rango, ruido_mov, ruido_medicion)

# Simulación de movimiento y mediciones
movimientos = [1, 1, 1, 1, 1]
mediciones = [1.2, 2.8, 4.1, 5.9, 7.5]

print("Estimaciones con Filtrado de Partículas:")
for i, (movimiento, medicion) in enumerate(zip(movimientos, mediciones)):
    filtro.predecir(movimiento)
    filtro.actualizar(medicion)
    estimacion = filtro.estimar()
    print(f"Paso {i+1} -> Movimiento: {movimiento}, Medición: {medicion:.2f}, Estimación: {estimacion:.2f}")