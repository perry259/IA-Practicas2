
import random

class PCFG:
    def __init__(self):
        # Definir las producciones con probabilidades
        # Formato: 'NoTerminal': [(Produccion, Probabilidad), ...]
        self.producciones = {
            'S': [(['NP', 'VP'], 0.9), (['VP'], 0.1)],
            'NP': [(['Det', 'N'], 1.0)],
            'VP': [(['V', 'NP'], 0.5), (['V'], 0.5)],
            'Det': [(['el'], 0.5), (['la'], 0.5)],
            'N': [(['gato'], 0.5), (['perro'], 0.5)],
            'V': [(['come'], 0.5), (['ve'], 0.5)]
        }

    def generar_oracion(self, simbolo='S'):
        if simbolo not in self.producciones:
            return simbolo  # Terminal
        producciones = self.producciones[simbolo]
        # Elegir una producción basada en probabilidades
        reglas, probs = zip(*producciones)
        seleccion = random.choices(reglas, weights=probs, k=1)[0]
        # Generar recursivamente la oración
        return ' '.join(self.generar_oracion(s) for s in seleccion)

# Crear instancia de la gramática
pcfg = PCFG()

# Generar una oración
oracion_generada = pcfg.generar_oracion()
print("Oración generada:", oracion_generada)
