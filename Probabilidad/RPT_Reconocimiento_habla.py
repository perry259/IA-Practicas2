# Simula un sistema simple de reconocimiento de habla que asocia
# palabras habladas con su interpretación correspondiente.

import random                               # Para elegir palabras al azar
import time                                 # Para simular el tiempo de procesamiento

# Lista de tuplas que mapea palabras habladas con su significado
palabras_habladas = [
    ("hola", "saludo"),
    ("adios", "despedida"),
    ("gracias", "agradecimiento"),
    ("perdon", "disculpa"),
    ("si", "afirmacion"),
    ("no", "negacion")
]

def reconocer_habla(entrada_habla):
    # Busca la interpretación de la palabra ingresada en la lista
    print("\nReconociendo palabra...")
    time.sleep(1)  # Simula el procesamiento

    for palabra, interpretacion in palabras_habladas:
        if entrada_habla == palabra:
            print(f"Palabra '{entrada_habla}' reconocida como: {interpretacion}")
            return interpretacion

    # Si no se encuentra coincidencia
    print(f"Palabra '{entrada_habla}' no reconocida.")
    return "no reconocida"

def seleccionar_palabra():
    # Permite al usuario elegir una palabra o generar una aleatoria
    opciones = [palabra for palabra, _ in palabras_habladas]
    opciones.append("aleatoria")

    print("Selecciona una palabra o elige 'aleatoria' para que se seleccione una automáticamente:")
    for idx, opcion in enumerate(opciones, 1):
        print(f"{idx}. {opcion}")

    eleccion = input("Escribe el número de tu elección: ")

    # Validación de la entrada del usuario
    if eleccion.isdigit() and 1 <= int(eleccion) <= len(opciones):
        if opciones[int(eleccion) - 1] == "aleatoria":
            palabra_hablada = random.choice(opciones[:-1])  # Excluye “aleatoria”
        else:
            palabra_hablada = opciones[int(eleccion) - 1]
    else:
        print("Elección no válida. Seleccionando una palabra aleatoria...")
        palabra_hablada = random.choice(opciones[:-1])

    return palabra_hablada

# Interacción principal con el usuario
palabra_hablada = seleccionar_palabra()
print("Fernanda dijo:", palabra_hablada)

# Reconocimiento de la palabra seleccionada
resultado = reconocer_habla(palabra_hablada)
print("Interpretación final:", resultado)
