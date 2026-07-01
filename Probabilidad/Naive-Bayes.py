# Este código implementa un clasificador Naïve Bayes sin librerías externas.
# Calcula probabilidades de cada clase, estima parámetros gaussianos
# y predice la clase de nuevas entradas basándose en las características.

import numpy as np
import pandas as pd

# Generamos un conjunto de datos de ejemplo
data = {
    'Característica1': [1.0, 2.0, 1.5, 1.2, 2.5, 1.8, 2.2, 1.0, 1.4, 2.0],
    'Característica2': [0.5, 1.5, 1.0, 0.7, 2.0, 1.5, 1.8, 0.6, 1.1, 1.4],
    'Clase': ['A', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B']
}

df = pd.DataFrame(data)

# Calcula la probabilidad a priori de cada clase
def calcular_probabilidades(df):
    probabilidades_clase = {}
    total_clases = len(df)
    for clase in df['Clase'].unique():
        probabilidades_clase[clase] = len(df[df['Clase'] == clase]) / total_clases
    return probabilidades_clase

# Calcula la media y desviación estándar de cada característica por clase
def calcular_parametros(df, clase):
    subset = df[df['Clase'] == clase]
    media = subset[['Característica1', 'Característica2']].mean()
    desviacion = subset[['Característica1', 'Característica2']].std()
    return media, desviacion

# Probabilidad usando distribución gaussiana
def probabilidad_gaussiana(x, media, desviacion):
    exponent = np.exp(-((x - media) ** 2) / (2 * desviacion ** 2))
    return (1 / (np.sqrt(2 * np.pi) * desviacion)) * exponent

# Predicción de clase para una entrada nueva
def predecir(df, entrada):
    probabilidades_clase = calcular_probabilidades(df)
    clases = df['Clase'].unique()
    probabilidades = {}

    for clase in clases:
        media, desviacion = calcular_parametros(df, clase)
        prob_total = probabilidades_clase[clase]

        for i in range(len(entrada)):
            prob_total *= probabilidad_gaussiana(entrada[i], media[i], desviacion[i])

        probabilidades[clase] = prob_total

    return max(probabilidades, key=probabilidades.get)

# Ejemplo de predicción
nueva_entrada = [1.5, 1.0]
clase_predicha = predecir(df, nueva_entrada)

print("La clase predicha para la entrada", nueva_entrada, "es:", clase_predicha)