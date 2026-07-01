"""
regla de la cadena
es una forma de calcular la probabilidad de que pasen 
varias cosas juntas al mismo tiempo.

ejemplo 
quiero saber la probabilidad de que pasen 3 cosas:
a, b y c.

la regla dice:
p(a, b, c) = p(a) * p(b | a) * p(c | a, b)
- primero preguntas: cual es la probabilidad de a ?
- luego: dado que paso a, cual es la prob de b ?
- luego: dado que ya pasaron a y b, cual es la prob de c ?
- multiplicas todo.

sirve para desarmar problemas grandes y complicados en pedacitos
que si podemos calcular.
esto se usa mucho en inteligencia artificial y estadistica
para models grandes donde hay muchas variables juntas.

vamos a crear una funcion que calcula p(a,b,c)
con esa formula, usando numeritos que le damos.
"""


def prob_conjunta(p_a, p_b_dado_a, p_c_dado_a_y_b):
    """
    esta funcion aplica:
    p(a, b, c) = p(a) * p(b | a) * p(c | a, b)

    parametros:
    p_a -> probabilidad de que pase a
    p_b_dado_a -> probabilidad de que pase b sabiendo que paso a
    p_c_dado_a_y_b -> probabilidad de que pase c sabiendo que ya pasaron a y b

    regresa:
    un numero entre 0 y 1 que representa p(a, b, c)
    """

    # multiplicamos todo segun la regla de la cadena
    resultado = p_a * p_b_dado_a * p_c_dado_a_y_b
    return resultado

# ahora usamos la funcion con ejemplos inventados
# supongamos:
# p(a) = 0.5   (50% chance de que pase a)
# p(b | a) = 0.4   (si a paso, b pasa con 40%)
# p(c | a, b) = 0.8 (si ya pasaron a y b, c pasa con 80%)

p_total = prob_conjunta(
    p_a = 0.5,
    p_b_dado_a = 0.4,
    p_c_dado_a_y_b = 0.8
)

print("probabilidad conjunta p(a, b, c) =", p_total)
print("en porcentaje eso es:", p_total * 100, "%")