# Este código implementa un sistema de recuperación de documentos,
# que permite buscar documentos que contengan todas las palabras
# de una consulta dada.

import numpy as np

class DocumentRetrieval:
    def __init__(self):
        # Base de datos de documentos (puede ampliarse)
        self.documentos = {
            1: "El perro juega en el parque.",
            2: "El gato duerme en la casa.",
            3: "Los pájaros cantan en la mañana.",
            4: "El perro y el gato son amigos.",
            5: "Los niños juegan en el parque."
        }

    def buscar(self, consulta):
        """Busca documentos que contienen todas las palabras de la consulta."""
        consulta_palabras = consulta.lower().split()
        resultados = []

        for id_doc, doc in self.documentos.items():
            if all(palabra in doc.lower() for palabra in consulta_palabras):
                resultados.append(id_doc)

        return resultados


# Crear una instancia del sistema de recuperación
sistema_recuperacion = DocumentRetrieval()

# Definir consulta
consulta = "perro parque"

# Realizar búsqueda
resultados = sistema_recuperacion.buscar(consulta)

# Mostrar resultados
print("Documentos encontrados para la consulta:", consulta)
for doc_id in resultados:
    print(f"Documento {doc_id}: {sistema_recuperacion.documentos[doc_id]}")