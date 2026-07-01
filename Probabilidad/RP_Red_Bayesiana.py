

# Implementa una red bayesiana simple para almacenar y consultar
# probabilidades condicionales entre eventos relacionados.

from collections import defaultdict        # Librería para manejar diccionarios con valores por defecto

class RedBayesiana:
    def __init__(self):
        # Diccionario anidado para guardar P(evento | dado_evento)
        self.probabilidades = defaultdict(dict)

    def agregar_probabilidad(self, evento, dado_evento, probabilidad):
        # Agrega una probabilidad condicional a la red
        self.probabilidades[evento][dado_evento] = probabilidad

    def calcular_probabilidad(self, evento, dado_evento):
        # Devuelve P(evento | dado_evento) si está definida
        return self.probabilidades[evento].get(dado_evento, "Probabilidad no definida en la red.")

    def mostrar_probabilidades(self):
        # Muestra todas las probabilidades registradas
        for evento, condicionadas in self.probabilidades.items():
            for dado_evento, probabilidad in condicionadas.items():
                print(f"P({evento} | {dado_evento}) = {probabilidad}")

# Crear instancia de la red bayesiana
red = RedBayesiana()

# Agregar probabilidades a la red
red.agregar_probabilidad('Emmanuel', 'Fernanda', 0.7)
red.agregar_probabilidad('Emiliano', 'Fernanda', 0.6)
red.agregar_probabilidad('Fernanda', 'Emiliano', 0.8)

# Consultar probabilidades específicas
prob_emmanuel_dado_fernanda = red.calcular_probabilidad('Emmanuel', 'Fernanda')
prob_emiliano_dado_fernanda = red.calcular_probabilidad('Emiliano', 'Fernanda')

# Mostrar los resultados
print("\nResultados de la Red Bayesiana:")
print(f"La probabilidad de que ocurra 'Emmanuel' dado que ocurrió 'Fernanda' es: {prob_emmanuel_dado_fernanda}")
print(f"La probabilidad de que ocurra 'Emiliano' dado que ocurrió 'Fernanda' es: {prob_emiliano_dado_fernanda}")

print("\nProbabilidades en la Red:")
red.mostrar_probabilidades()