# Este código implementa un modelo de lenguaje n-grama (bigramas)
# que aprende a predecir la próxima palabra en un texto dado un prefijo.

import numpy as np
from collections import defaultdict

class NGramLanguageModel:
    def __init__(self, n):
        self.n = n
        self.ngrams = defaultdict(lambda: defaultdict(int))
        self.vocab = set()

    def train(self, text):
        """Entrena el modelo con el texto dado."""
        tokens = text.lower().split()
        self.vocab.update(tokens)

        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i:i + self.n])
            prefix = ngram[:-1]
            self.ngrams[prefix][ngram[-1]] += 1

    def predict(self, prefix):
        """Predice la próxima palabra dada una secuencia de palabras."""
        prefix = tuple(prefix.lower().split())
        if len(prefix) != self.n - 1:
            raise ValueError(f"El prefijo debe tener {self.n - 1} palabras.")
        
        next_word_counts = self.ngrams[prefix]
        if not next_word_counts:
            return None  # No hay predicciones disponibles
        
        # Calculamos la probabilidad de cada palabra siguiente
        total_count = sum(next_word_counts.values())
        probabilities = {word: count / total_count for word, count in next_word_counts.items()}

        # Seleccionamos la palabra más probable
        predicted_word = max(probabilities, key=probabilities.get)
        return predicted_word, probabilities[predicted_word]

# Texto de ejemplo para entrenar el modelo
text_corpus = """
La inteligencia artificial es una rama de la informática.
La inteligencia artificial busca crear sistemas que imiten la inteligencia humana.
Los modelos de lenguaje son una parte importante de la inteligencia artificial.
"""

# Creamos un modelo n-grama de 2 (bigramas)
ngram_model = NGramLanguageModel(n=2)

# Entrenamos el modelo
ngram_model.train(text_corpus)

# Predicción de la próxima palabra
prefijo = "la"  # Prefijo de una palabra para bigramas
prediccion, probabilidad = ngram_model.predict(prefijo)

print(f"Predicción para '{prefijo}': {prediccion} (Probabilidad: {probabilidad:.4f})")