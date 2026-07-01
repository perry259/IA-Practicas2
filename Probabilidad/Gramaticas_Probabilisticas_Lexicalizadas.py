# Este código genera oraciones usando una gramática probabilística
# lexicalizada, eligiendo producciones según sus probabilidades.
# La generación se hace de forma recursiva desde el símbolo 'S'.

import random

class LexicalizedPCFG:
    def __init__(self):
        # Gramática lexicalizada con probabilidades
        self.gramatica = {
            'S': [('NP VP', 1.0)],
            'NP': [('Det Noun', 0.7), ('Adj Noun', 0.3)],
            'VP': [('Verb NP', 1.0)],
            'Det': [('el', 0.5), ('la', 0.5)],
            'Adj': [('rápido', 0.6), ('lento', 0.4)],
            'Noun': [('perro', 0.4), ('gato', 0.4), ('pájaro', 0.2)],
            'Verb': [('corre', 0.7), ('salta', 0.3)],
        }

    def generar_oracion(self, simbolo='S'):
        if simbolo not in self.gramatica:
            return simbolo  # Es una hoja
        producciones = self.gramatica[simbolo]
        total_prob = sum(prob for _, prob in producciones)
        rand = random.uniform(0, total_prob)
        acumulado = 0
        for produccion, prob in producciones:
            acumulado += prob
            if rand <= acumulado:
                # Generar recursivamente cada símbolo de la producción
                return ' '.join(self.generar_oracion(s) for s in produccion.split())

# Crear instancia de la gramática lexicalizada
lexicalized_pcfg = LexicalizedPCFG()

# Generar y mostrar la oración
oracion_generada = lexicalized_pcfg.generar_oracion()
print("Oración generada:", oracion_generada)