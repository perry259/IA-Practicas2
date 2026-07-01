# propagacion de restricciones
# se van eliminando valores que ya no pueden funcionar
# de los dominios de las variables, usando las reglas.
# esto limpia el problema antes (o durante) la busqueda.
# asi evitamos probar valores que ya sabemos que van a fallar.
# en este ejemplo hacemos algo tipo ac-3:
# si una variable x tiene un valor que nunca puede combinar con ningun valor valido de otra variable y,
# entonces quitamos ese valor de x.

from collections import deque 

def compatibles(var_x, val_x, var_y, dominio_y, restriccion_binaria):
    """
    checa si val_x (un valor de var_x) es compatible con algun valor
    de var_y segun la restriccion_binaria.

    var_x: nombre de variable x (ej: "a")
    val_x: valor que estoy probando para x (ej: "rojo")
    var_y: nombre de variable y (ej: "b")
    dominio_y: lista de valores posibles de y (ej: ["rojo","verde"])
    restriccion_binaria: funcion que dice si x,y cumplen o no

    regresa True si existe al menos un valor en dominio_y que sirva
    regresa False si val_x ya no sirve con ningun valor de var_y
    """

    for val_y in dominio_y:
        # reviso si (x = val_x, y = val_y) respeta la restriccion
        if restriccion_binaria(var_x, val_x, var_y, val_y):
            return True
    return False


def revisar_arco(var_x, var_y, dominios, restriccion_binaria):
    """
    intenta limpiar el dominio de var_x usando var_y.

    si un valor de var_x no es compatible con NINGUN valor de var_y,
    entonces ese valor se elimina del dominio de var_x.

    regresa:
    - True si se elimino al menos un valor de var_x
    - False si no se cambio nada
    """

    dominio_x = dominios[var_x]
    dominio_y = dominios[var_y]

    # guardamos aqui los valores que se tienen que quitar de x
    quitar = []

    for val_x in dominio_x:
        if not compatibles(var_x, val_x, var_y, dominio_y, restriccion_binaria):
            # este valor de x ya no tiene forma de combinar con y
            quitar.append(val_x)

    # si hay que quitar valores, los quitamos
    if quitar:
        for v in quitar:
            dominio_x.remove(v)
        return True  # hubo cambio

    return False  # no hubo cambio


def ac3(variables, dominios, vecinos, restriccion_binaria):
    """
    ac3 = algoritmo de consistencia de arcos

    variables:
        lista de variables, ejemplo ["a","b","c"]

    dominios:
        diccionario con opciones posibles de cada variable
        ejemplo:
        {
          "a": ["rojo","verde"],
          "b": ["rojo","verde"],
          "c": ["rojo","verde"]
        }

    vecinos:
        para cada variable, con quien tiene restriccion directa
        ejemplo:
        {
          "a": ["b"],
          "b": ["a","c"],
          "c": ["b"]
        }

    restriccion_binaria:
        funcion que recibe (var1, val1, var2, val2)
        y regresa True si esa combinacion se permite

    regresa:
        True si los dominios quedaron consistentes
        False si algun dominio se quedo vacio (o sea imposible)
    """

    # metemos todos los pares (x,y) a la cola
    cola = deque()
    for x in variables:
        for y in vecinos[x]:
            cola.append((x, y))

    # procesamos hasta que la cola quede vacia
    while cola:
        x, y = cola.popleft()

        # intentamos limpiar el dominio de x usando y
        cambio = revisar_arco(x, y, dominios, restriccion_binaria)

        if cambio:
            # si cambie el dominio de x, puede afectar a sus otros vecinos
            if len(dominios[x]) == 0:
                # si un dominio queda vacio, ya no hay solucion
                return False

            for z in vecinos[x]:
                if z != y:
                    cola.append((z, x))

    return True


if __name__ == "__main__":
    # ejemplo:
    # vamos a colorear 3 zonas: a, b, c
    # colores posibles: rojo, verde
    # reglas:
    # a y b no pueden tener el mismo color
    # b y c no pueden tener el mismo color
    # (a y c pueden repetir color, no hay restriccion directa)

    variables = ["a", "b", "c"]

    dominios = {
        "a": ["rojo", "verde"],
        "b": ["rojo", "verde"],
        "c": ["rojo", "verde"]
    }

    # vecinos dice cuales variables afectan a cuales
    # a choca con b
    # b choca con a y con c
    # c choca con b
    vecinos = {
        "a": ["b"],
        "b": ["a", "c"],
        "c": ["b"]
    }
    # restriccion_binaria:
    # esta funcion define la regla entre dos variables conectadas
    # aqui la regla es:
    # si estan conectadas, deben tener color diferente
    # si no estan conectadas directamente, no importa
    def restriccion_binaria(x, val_x, y, val_y):
        # si x y y son vecinos, no pueden tener el mismo color
        if (x == "a" and y == "b") or (x == "b" and y == "a"):
            return val_x != val_y
        if (x == "b" and y == "c") or (x == "c" and y == "b"):
            return val_x != val_y
        # si no hay restriccion directa entre x e y, esta ok
        return True

    # corremos ac3
    consistente = ac3(variables, dominios, vecinos, restriccion_binaria)

    print("es consistente?:", consistente)
    print("dominios despues de ac3:")
    for var in variables:
        print(" ", var, "->", dominios[var])

    # que significa esto:
    # - si en algun punto un dominio queda vacio, consistente = False
    # - si no, ac3 reduce listas quitando valores imposibles
    # - despues de esto, ya puedo intentar asignar valores con menos prueba y error
    # - propagacion de restricciones intenta limpiar dominios antes
    # - ac3 revisa pares (x,y) y quita valores que no tienen soporte
    # - si un dominio se queda vacio, ya no hay solucion posible