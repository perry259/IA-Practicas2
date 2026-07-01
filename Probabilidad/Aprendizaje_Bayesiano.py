# Este código implementa un clasificador Naïve Bayes usando un conjunto de datos de ejemplo.
# Se divide el conjunto en entrenamiento y prueba, se entrena el modelo, 
# se hacen predicciones y se calcula la precisión del clasificador.

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# Generamos un conjunto de datos de ejemplo
data = {
    'Característica1': [1.0, 2.0, 1.5, 1.2, 2.5, 1.8, 2.2, 1.0, 1.4, 2.0],
    'Característica2': [0.5, 1.5, 1.0, 0.7, 2.0, 1.5, 1.8, 0.6, 1.1, 1.4],
    'Clase': ['A', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B']
}

# Convertimos el conjunto de datos en un DataFrame de pandas
df = pd.DataFrame(data)

# Separamos las características y la clase
X = df[['Característica1', 'Característica2']]
y = df['Clase']

# Dividimos el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creamos el clasificador Naïve Bayes
modelo = GaussianNB()

# Entrenamos el modelo
modelo.fit(X_train, y_train)

# Realizamos predicciones sobre el conjunto de prueba
y_pred = modelo.predict(X_test)

# Calculamos la precisión del modelo
precision = accuracy_score(y_test, y_pred)

print("Predicciones del modelo:", y_pred)
print("Precisión del modelo:", precision)