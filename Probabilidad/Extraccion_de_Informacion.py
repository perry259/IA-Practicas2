# Este código implementa la extracción de información de un texto,
# específicamente nombres y fechas utilizando expresiones regulares.

import re

class ExtraccionInformacion:
    def __init__(self, texto):
        self.texto = texto

    def extraer_nombres(self):
        """Extrae nombres en formato 'Nombre Apellido'."""
        patron = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
        nombres = re.findall(patron, self.texto)
        return list(set(nombres))  # Nombres únicos

    def extraer_fechas(self):
        """Extrae fechas en formato dd/mm/yyyy o dd-mm-yyyy."""
        patron = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b'
        fechas = re.findall(patron, self.texto)
        return list(set(fechas))  # Fechas únicas



texto = """
El cumpleaños de Juan Pérez es el 12/03/1995. 
La reunión con María González será el 15-04-2023.
José López no puede asistir el 12/03/2023.
"""

# Crear instancia de extracción
extraccion = ExtraccionInformacion(texto)

# Extraer nombres y fechas
nombres_extraidos = extraccion.extraer_nombres()
fechas_extraidas = extraccion.extraer_fechas()

# Mostrar resultados
print("Nombres extraídos:", nombres_extraidos)
print("Fechas extraídas:", fechas_extraidas)