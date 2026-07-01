"""
probabilidad a priori
tambien se dice prior es lo que tu crees antes de ver nueva informacion.
tengo una moneda normal, antes de lanzarla creo que cara = 0.5 (50%).
todavia no la lance, solo estoy diciendo lo que pienso antes de mirar evidencia.
esto se usa mucho en inteligencia artificial porque muchas veces la maquina tiene que
"asumir" algo inicial antes de observar datos reales. es como su punto de inicio.
vamos a calcular la probabilidad de sacar un dulce rojo de una bolsa,
basado solo en cuantas piezas hay de cada color. osea, nuestra creencia inicial.
"""
# supongamos que tengo una bolsa con dulces
# hay 3 dulces rojos y 1 dulce azul
rojos = 3
azules = 1
# total de dulces en la bolsa
total = rojos + azules  # esto es suma normal, 3 + 1 = 4
# formula de probabilidad clasica:
# probabilidad = casos favorables / casos totales
prob_rojo_apriori = rojos / total   # probabilidad a priori de sacar rojo
prob_azul_apriori = azules / total  # probabilidad a priori de sacar azul

print("prob a priori de sacar dulce rojo =", prob_rojo_apriori)
print("prob a priori de sacar dulce azul =", prob_azul_apriori)

"""
rojos = 3, azules = 1
  estas variables guardan cantidades. en python una variable es como una cajita con un valor.

 total = rojos + azules
  sumamos para saber cuantas piezas hay en total en la bolsa.

-prob_rojo_apriori = rojos / total
  el simbolo / es division. esto nos da un numero entre 0 y 1.
  ejemplo: si da 0.75 eso es 75%

print(...)
  print sirve para mostrar cosas en pantalla cuando ejecutes el programa.

a priori = antes de ver lo que realmente salio
todavia no metimos la mano a la bolsa, solo estamos calculando que tan probable seria
cada color con la info que tenemos al inicio
"""

# si quieres ver el porcentaje bonito en %
print("rojo en porcentaje =", prob_rojo_apriori * 100, "%")
print("azul en porcentaje =", prob_azul_apriori * 100, "%")