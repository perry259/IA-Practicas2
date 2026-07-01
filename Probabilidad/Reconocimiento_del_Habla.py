# Este código simula un sistema básico de reconocimiento de palabras.
# El usuario puede seleccionar una palabra o dejar que se elija aleatoriamente.
# Luego, la palabra se interpreta según una lista predefinida.

import random
import time

# Lista de tuplas que mapea palabras habladas a su interpretación
palabras_habladas = [
    ("hola", "saludo"),
    ("adios", "despedida"),
    ("gracias", "agradecimiento"),
    ("perdon", "disculpa"),
    ("si", "afirmacion"),
    ("no", "negacion")
]

def reconocer_habla(entrada_habla):
    """
    Busca la interpretación de la palabra hablada en la lista de palabras_habladas.
    """
    print("\nReconociendo palabra...")
    time.sleep(1)  # Simulación de tiempo de procesamiento

    for palabra, interpretacion in palabras_habladas:
        if entrada_habla == palabra:
            print(f"Palabra '{entrada_habla}' reconocida como: {interpretacion}")
            return interpretacion
    print(f"Palabra '{entrada_habla}' no reconocida.")
    return "no reconocida"

def seleccionar_palabra():
    """
    Permite al usuario seleccionar una palabra de una lista o genera una aleatoriamente.
    """
    opciones = [palabra for palabra, _ in palabras_habladas]
    opciones.append("aleatoria")  # Opción para elegir aleatoriamente

    print("Selecciona una palabra o elige 'aleatoria' para que se seleccione una automáticamente:")
    for idx, opcion in enumerate(opciones, 1):
        print(f"{idx}. {opcion}")

    eleccion = input("Escribe el número de tu elección: ")

    if eleccion.isdigit() and 1 <= int(eleccion) <= len(opciones):
        if opciones[int(eleccion) - 1] == "aleatoria":
            palabra_hablada = random.choice(opciones[:-1])  # Excluimos 'aleatoria'
        else:
            palabra_hablada = opciones[int(eleccion) - 1]
    else:
        print("Elección no válida. Seleccionando una palabra aleatoria...")
        palabra_hablada = random.choice(opciones[:-1])  # Excluimos 'aleatoria'

    return palabra_hablada

# Interacción con el usuario
palabra_hablada = seleccionar_palabra()
print("Fernanda dijo:", palabra_hablada)

# Llamada a la función de reconocimiento de habla
resultado = reconocer_habla(palabra_hablada)
print("Interpretación final:", resultado)