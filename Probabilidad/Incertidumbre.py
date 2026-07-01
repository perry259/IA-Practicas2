"""
incertidumbre es cuando no sabemos con seguridad que va a pasar.
en ia y en probabilidad casi nunca tenemos 100% de certeza,
solo tenemos creencias (probabilidades).
sirve para pensar en decisiones aunque no sepamos todo.
la idea es aceptar "no estoy seguro", medirlo,
y trabajar con eso en lugar de fingir que todo es fijo.
ejemplo:
- certeza: se que va a pasar
- incertidumbre: no se, pero puedo estimar que tan probable es cada cosa
aqui vamos a simular esa idea con codigo.
vamos a:
1. hacer "eventos" aleatorios
2. ver que no siempre sale lo mismo
3. medir mas o menos que tan incierto es
"""
import random

def evento_aleatorio():
    """
    esta funcion representa algo que no controlamos al 100%
    por ejemplo: que pase algo si hay cierto riesgo

    random.random() da un numero entre 0 y 1
    si el numero es menor que 0.3 decimos que "ocurre el evento"
    eso significa:
    prob del evento = 0.3 (30%)
    prob de que no pase = 0.7 (70%)

    notese: no estamos seguros si va a pasar o no en una vez,
    solo sabemos que tan probable es
    eso es incertidumbre
    """
    n = random.random()
    if n < 0.3:
        return True   # el evento paso
    else:
        return False  # el evento no paso

def medir_incertidumbre_intuitiva(intentos):
    """
    la idea aqui es repetir muchas veces el evento aleatorio
    y contar cuantas veces paso

    si el resultado cambia cada vez que corro el programa,
    eso me muestra que no todo es fijo, hay variacion

    esa variacion es la incertidumbre en accion
    """
    pasa = 0
    no_pasa = 0

    for _ in range(intentos):
        if evento_aleatorio():
            pasa += 1
        else:
            no_pasa += 1

    # calculamos frecuencia aproximada
    prob_aprox = pasa / intentos

    return {
        "veces_paso": pasa,
        "veces_no_paso": no_pasa,
        "prob_aprox_de_que_pase": prob_aprox
    }

# corremos la medicion
resultado = medir_incertidumbre_intuitiva(intentos=1000)

print("veces que el evento ocurrio     :", resultado["veces_paso"])
print("veces que no ocurrio            :", resultado["veces_no_paso"])
print("prob aproximada de que ocurra   :", round(resultado["prob_aprox_de_que_pase"], 3))

print("- no sabemos de antemano si el evento pasa o no en una prueba individual")
print("- solo sabemos una prob aproximada, ejemplo 0.3 ~ 30%")
print("- eso es manejar incertidumbre en vez de fingir que todo es seguro")