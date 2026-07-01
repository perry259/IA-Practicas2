
# Este código implementa un traductor simple palabra por palabra
# usando un diccionario como base para la traducción estadística.

class TraductorEstadistico:
    def __init__(self):
        # Diccionario de traducción simple
        self.diccionario = {
            'hola': 'hello',
            'adios': 'goodbye',
            'gracias': 'thank you',
            'por favor': 'please',
            'si': 'yes',
            'no': 'no'
        }

    def traducir(self, frase):
        """Traduce una frase palabra por palabra usando el diccionario."""
        palabras = frase.split()  # Divide la frase en palabras
        traduccion = []

        for palabra in palabras:
            # Busca la traducción en el diccionario
            traduccion.append(self.diccionario.get(palabra.lower(), palabra))  # Si no hay traducción, mantiene la palabra

        return ' '.join(traduccion)  # Une las palabras traducidas en una frase


traductor = TraductorEstadistico()

frase_original = "hola gracias por favor"
frase_traducida = traductor.traducir(frase_original)

print("Frase original:", frase_original)
print("Frase traducida:", frase_traducida)
