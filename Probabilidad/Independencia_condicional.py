"""
independencia condicional
es una idea importante en probabilidad e ia.

si yo ya se cierta informacion, a lo mejor otra informacion ya no cambia nada.
- variable lluvia (si llovio o no)
- variable trafico (si hay trafico o no)
- variable llegar_tarde (si llegas tarde a la escuela)
si yo ya se que hay trafico horrible, entonces saber si llovio ya no cambia mucho
mi creencia de "voy a llegar tarde". o sea, lluvia ya no agrega informacion extra.
eso es independencia condicional.
sirve para simplificar modelos. en ia esto baja el trabajo porque
no tenemos que revisar todas las combinaciones de todas las variables,
solo las que realmente afectan.
vamos a hacer una funcion que dice
"cual es la probabilidad de llegar tarde"
dependiendo de si hay trafico o no.
luego mostramos como el trafico manda todo.
"""
def prob_llegar_tarde(hay_trafico):
    """
    esta funcion regresa un numero entre 0 y 1
    que representa la probabilidad de llegar tarde.
    hay_trafico -> true o false
    true significa: si hay trafico
    false significa: no hay trafico
    en python true y false se escriben con mayuscula
    True / False
    pero eso es porque python lo exige asi.
    no es gramatica humana, es sintaxis del lenguaje.
    regresa (o sea "devuelve") un numero.
    ese numero lo podemos guardar o imprimir.
    """
    if hay_trafico:
        # si hay trafico, casi seguro llegas tarde
        return 0.9  # 90%
    else:
        # si no hay trafico, casi nunca llegas tarde
        return 0.1  # 10%


# ahora usamos la funcion y vemos los resultados
prob_con_trafico = prob_llegar_tarde(True)   # True = si hay trafico
prob_sin_trafico = prob_llegar_tarde(False)  # False = no hay trafico

print("prob de llegar tarde si hay trafico =", prob_con_trafico)
print("prob de llegar tarde si NO hay trafico =", prob_sin_trafico)