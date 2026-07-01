"""
distribucion de probabilidad
una distribucion de probabilidad es basicamente una lista donde dices:
para cada posible resultado, cual es su probabilidad.
si lanzas un dado justo (1,2,3,4,5,6) todos los numeros tienen la misma chance.
osea, cada numero tiene prob = 1/6 (aprox 0.1666...)
sirve para describir matematicamente el azar.
en inteligencia artificial usamos distribuciones para decirle al sistema
"estas son las opciones y esto tan probable es cada una".
tambien sirve para simular cosas.
vamos a crear una distribucion de probabilidad para un dado justo
y luego la vamos a imprimir en pantalla de manera entendible.
"""
# un diccionario en python se escribe con llaves { }
# formato: clave: valor
# aqui la "clave" va a ser el numero del dado (1..6)
# y el "valor" va a ser la probabilidad de que salga ese numero

distribucion_dado = {
    1: 1/6,
    2: 1/6,
    3: 1/6,
    4: 1/6,
    5: 1/6,
    6: 1/6
}

# ahora vamos a mostrar la distribucion
print("distribucion de probabilidad de un dado justo:\n")
# .items() sirve para recorrer el diccionario y obtener (clave, valor)
for cara, prob in distribucion_dado.items():
    # cara es el numero del dado (1..6)
    # prob es la probabilidad asignada a esa cara
    print("numero", cara, "=> prob =", prob, "equivale a", prob * 100, "%")

# comprobacion de que todo suma 1
suma_total = 0
for prob in distribucion_dado.values():  # .values() regresa solo los valores del diccionario
    suma_total += prob  # esto es lo mismo que suma_total = suma_total + prob

print("\nla suma de todas las probabilidades es:", suma_total)

# si la suma_total es 1.0 significa que nuestra distribucion esta bien armada
# si no sumara 1, entonces no seria una distribucion de probabilidad correcta