"""
regla de bayes
la regla de bayes es una forma de actualizar lo que creemos
cuando recibimos nueva informacion.
una prueba medica sale positiva.
pregunta: que tan probable es que de verdad estes enfermo?
sirve para no paniquear solo porque una prueba dio positivo.
tambien se usa en ia para que una maquina ajuste sus creencias
cada vez que ve evidencia nueva.
"""
def prob_bayes(prior_enfermo, sens_prueba, falso_positivo):
    """
    esta funcion aplica la formula de bayes
    prior_enfermo:
        esto es la probabilidad a priori de estar enfermo
        antes de hacerte la prueba
        ejemplo: si la enfermedad es rara, puede ser 0.01 = 1%
    sens_prueba:
        sensibilidad de la prueba
        probabilidad de que la prueba salga positiva
        si SI estas enfermo
        (esto se llama p(positivo | enfermo))
    falso_positivo:
        probabilidad de que la prueba salga positiva
        aunque NO estes enfermo
        (esto se llama p(positivo | sano))
        tambien se llama tasa de falso positivo
    la probabilidad de estar enfermo dado que la prueba salio positiva
    o sea p(enfermo | positivo)
    formula usada (escrita en texto):
    p(a | b) = [ p(b | a) * p(a) ] / [ p(b | a)*p(a) + p(b | no a)*p(no a) ]
    a  = estas enfermo
    b  = prueba positiva
    p(a) = prior_enfermo
    p(no a) = 1 - prior_enfermo
    p(b | a) = sens_prueba
    p(b | no a) = falso_positivo
    """
    p_a = prior_enfermo              # p(a)
    p_no_a = 1 - p_a                 # p(no a)

    p_b_dado_a = sens_prueba         # p(b | a)
    p_b_dado_no_a = falso_positivo   # p(b | no a)

    # numerador = p(b | a) * p(a)
    numerador = p_b_dado_a * p_a

    # denominador = p(b | a)*p(a) + p(b | no a)*p(no a)
    denominador = (p_b_dado_a * p_a) + (p_b_dado_no_a * p_no_a)

    # el resultado final es numerador / denominador
    return numerador / denominador

# ahora vamos a usar nuestra funcion con numeros de ejemplo
# ej:
# - la enfermedad es rara: solo 1% de la gente la tiene -> 0.01
# - si estas enfermo, la prueba detecta positivo el 90% -> 0.90
# - si NO estas enfermo, aun asi da positivo falso un 5% -> 0.05

resultado = prob_bayes(
    prior_enfermo = 0.01,
    sens_prueba = 0.90,
    falso_positivo = 0.05
)
print("probabilidad real de estar enfermo si tu prueba salio positiva =", resultado)
print("en porcentaje eso es:", resultado * 100, "%")

"""
si el resultado sale bajo, significa:
aunque tu prueba dio positivo, aun asi es poco probable que estes enfermo,
porque la enfermedad es super rara en general.
esto es contra intuitivo pero es real.
por eso bayes es tan importante:
te da una evaluacion mas fria y menos dramatica.
"""