# Algoritmos geneticos
# un algoritmo genetico es una forma de buscar una buena solucion
# probando muchas posibles respuestas al mismo tiempo
# sirve cuando no sabemos la respuesta exacta, pero podemos medir
# si una respuesta es buena o mala con un puntaje
# por ejmplo:
# - tengo varias soluciones
# - me quedo con las mejores
# - las mezclo para crear soluciones nuevas
# - hago mutaciones chicas para no quedarme siempre en lo mismo
# - repito varias veces hasta que salga una solucion buena

import random

def crear_individuo(longitud):
    # crea una posible solucion
    # en este ejemplo una solucion es una lista de 0 y 1
    # ejemplo: [1, 0, 1, 1, 0]
    # longitud dice de cuantas posiciones es la lista
    individuo = []
    for _ in range(longitud):
        gen = random.randint(0, 1)  # 0 o 1 al azar
        individuo.append(gen)
    return individuo

def puntaje(individuo):
    # esta funcion dice que tan buena es una solucion
    # aqui definimos que "mas 1s = mejor"
    # ejemplo: [1,0,1,1,0] tiene 3 unos, su puntaje es 3
    return sum(individuo)

def seleccionar_padres(poblacion, cantidad):
    # poblacion: lista de individuos (varias soluciones)
    # cantidad: cuantos padres quiero elegir
    # aqui elegimos los mejores segun su puntaje
    poblacion_ordenada = sorted(
        poblacion,
        key=lambda ind: puntaje(ind),
        reverse=True  # mejor puntaje primero
    )
    return poblacion_ordenada[:cantidad]

def cruzar(padre1, padre2):
    # cruzar = combinar 2 soluciones para hacer una nueva
    # ejemplo:
    # padre1 = [1,0,1,1,0]
    # padre2 = [0,1,0,0,1]
    # el hijo se arma mitad de uno y mitad del otro
    # punto de corte = donde se parte
    # hijo = parte de padre1 + parte de padre2

    punto = random.randint(1, len(padre1) - 1)
    hijo = padre1[:punto] + padre2[punto:]
    return hijo

def mutar(individuo, prob_mutacion):
    # mutar = cambiar poquito la solucion al azar
    # esto ayuda a probar ideas nuevas
    # prob_mutacion es que tanto permites cambio
    # ejemplo 0.1 = 10% de cambiar cada posicion

    for i in range(len(individuo)):
        if random.random() < prob_mutacion:
            # si era 1 lo vuelvo 0
            # si era 0 lo vuelvo 1
            individuo[i] = 1 - individuo[i]
    return individuo

def algoritmo_genetico(
    tam_poblacion,
    longitud_individuo,
    generaciones,
    prob_mutacion,
    padres_a_tomar
):
    # esta es la funcion principal
    # tam_poblacion     = cuantas soluciones tengo al mismo tiempo
    # longitud_individuo = de cuantas posiciones es cada solucion
    # generaciones      = cuantas veces voy a mejorar
    # prob_mutacion     = que tanto dejo que cambie cada hijo
    # padres_a_tomar    = cuantos mejores uso como "padres"
    # regresa:
    # mejor_final       = la mejor solucion encontrada
    # puntaje(mejor_final) = su puntaje
    # historial_mejor   = mejores soluciones por cada generacion

    # 1) creo la poblacion inicial (todas aleatorias)
    poblacion = []
    for _ in range(tam_poblacion):
        poblacion.append(crear_individuo(longitud_individuo))

    historial_mejor = []

    # 2) repito el proceso varias generaciones
    for _ in range(generaciones):
        # escoger padres (los mejores)
        padres = seleccionar_padres(poblacion, padres_a_tomar)

        nueva_poblacion = []

        # copiamos directamente los padres (para no perder lo bueno)
        for p in padres:
            nueva_poblacion.append(p[:])  # [:] = copia

        # creamos hijos nuevos hasta llenar la poblacion
        while len(nueva_poblacion) < tam_poblacion:
            padre1 = random.choice(padres)
            padre2 = random.choice(padres)

            hijo = cruzar(padre1, padre2)
            hijo = mutar(hijo, prob_mutacion)

            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

        # guardamos el mejor de esta generacion para ver el progreso
        mejor = max(poblacion, key=lambda ind: puntaje(ind))
        historial_mejor.append((mejor[:], puntaje(mejor)))

    # al final nos quedamos con el mejor que haya salido
    mejor_final = max(poblacion, key=lambda ind: puntaje(ind))
    return mejor_final, puntaje(mejor_final), historial_mejor

if __name__ == "__main__":
    # aqui decimos como queremos correr el algoritmo genetico

    tam_poblacion = 6          # cuantas soluciones por ronda
    longitud_individuo = 5     # cuantos genes tiene cada solucion
    generaciones = 20          # cuantas rondas de mejora
    prob_mutacion = 0.1        # 0.1 = 10% de chance de cambiar cada gen
    padres_a_tomar = 2         # de cuantas soluciones "buenas" saco hijos

    mejor, score, historial = algoritmo_genetico(
        tam_poblacion,
        longitud_individuo,
        generaciones,
        prob_mutacion,
        padres_a_tomar
    )

    print("mejor solucion encontrada:", mejor)
    print("puntaje de esa solucion:", score)

    print("\nmejores por generacion:")
    for gen_idx, (ind, sc) in enumerate(historial):
        print(" gen", gen_idx, "->", ind, "puntaje:", sc)

    # crear_individuo()     hace una solucion aleatoria
    # puntaje()             mide que tan buena es una solucion
    # seleccionar_padres()  elige las mejores soluciones
    # cruzar()              mezcla dos soluciones para hacer una nueva
    # mutar()               cambia un poco la nueva solucion
    # algoritmo_genetico()  repite esto varias veces y se queda con lo mejor