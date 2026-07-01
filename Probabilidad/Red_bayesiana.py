"""
red bayesiana
una red bayesiana es una forma de representar causas y efectos con probabilidad.
se dibuja como nodos (variables) conectados con flechas (quien causa a quien).
- fumar puede causar cancer
- cancer puede causar tos
entonces hay relacion entre fumar, cancer y tos
sirve para razonar cuando no tienes toda la informacion.
si una persona tiene tos, que tan probable es que tenga cancer?
y si sabes que fuma, cambia la cosa todavia mas.
idea clave:
no es logica dura tipo "si pasa x entonces forzosamente y".
es mas suave: "x hace mas probable y".
eso es lo interesante para inteligencia artificial.
vamos a simular una red bayesiana chiquita en python.
vamos a guardar:
- que nodos existen
- de quien depende cada nodo (o sea sus padres)
- algunas probabilidades inventadas
"""
# nodos de nuestra mini red
# en python una lista se pone con corchetes [ ]
nodos = ["fumar", "cancer", "tos"]
# "padres" significa: de que cosas depende esta variable
# ejemplo:
# cancer depende de fumar
# tos depende de fumar y de cancer
padres = {
    "fumar": [],              # fumar no depende de nadie mas en este mini ejemplo
    "cancer": ["fumar"],      # cancer depende de si la persona fuma
    "tos": ["fumar", "cancer"]  # tos depende de fumar y/o cancer
}
# ahora vamos a inventar tablas de probabilidad condicional super simples
# nota: en una red bayesiana real esto se guarda como tablas grandes con muchos casos
# aqui lo hacemos chiquito y didactico para que se entienda el concepto

# probabilidad de que una persona fume
# (esto seria p(fumar=true) )
p_fumar = 0.3  # 30% de prob que la persona fume, numero inventado para este ejemplo


# probabilidad de cancer dado fumar
# p(cancer=true | fumar=true) por ejemplo
def p_cancer_dado_fumar(fuma):
    """
    esta funcion regresa un numero entre 0 y 1 que representa
    que tan probable es que la persona tenga cancer
    dependiendo si fuma o no fuma
    
    fuma -> True si la persona fuma
            False si no fuma
    """
    if fuma:
        return 0.2   # si fuma, 20% prob de cancer (numero inventado)
    else:
        return 0.01  # si no fuma, 1% prob de cancer

# probabilidad de tos dado fumar y cancer
# p(tos=true | fumar, cancer)
def p_tos_dado_fumar_y_cancer(fuma, tiene_cancer):
   
    # casos:
    if tiene_cancer:
        return 0.9   # si tiene cancer, tos es muy probable
    elif fuma and not tiene_cancer:
        return 0.5   # fuma pero sin cancer: igual puede tener tos por irritacion
    else:
        return 0.1   # no fuma y no tiene cancer: tos rara vez

# ahora vamos a imprimir info de nuestra red
print("nodos de la red bayesiana:", nodos)
print("padres (de quien depende cada nodo):", padres)

print("\nejemplos de probabilidades:")
print("p(fumar=true) =", p_fumar)
print("p(cancer=true | fumar=true) =", p_cancer_dado_fumar(True))
print("p(cancer=true | fumar=false) =", p_cancer_dado_fumar(False))
print("p(tos=true | fuma=true, cancer=true) =", p_tos_dado_fumar_y_cancer(True, True))
print("p(tos=true | fuma=true, cancer=false) =", p_tos_dado_fumar_y_cancer(True, False))
print("p(tos=true | fuma=false, cancer=false) =", p_tos_dado_fumar_y_cancer(False, False))

"""
- nodos = ["fumar", "cancer", "tos"]
  esto es una lista. cada string es una variable que nos importa.
  cada una representa algo que puede ser verdadero o falso (enfermo, no enfermo, etc)
- padres = { ... }
  o sea, esas flechas de causa/efecto que normalmente se dibujan,
  aqui las estamos guardando en forma de texto.
- definimos funciones p_cancer_dado_fumar(...) y p_tos_dado_fumar_y_cancer(...)
  cada funcion es como una mini tabla de probabilidad condicional.
  te dice la probabilidad de una cosa, segun otras cosas.
  ejemplo: prob de tener tos depende si fumas y si tienes cancer.
- if ... elif ... else ...
  esto es una estructura condicional en python.
  if se ejecuta si la condicion es verdadera.
  elif es como "si no se cumplio lo de arriba, prueba esta otra condicion".
  else se ejecuta si ninguna de las anteriores se cumplio.
- print(...)
  estamos mostrando la informacion para que se vea claro en pantalla.
una red bayesiana es una forma organizada de guardar:
1) que variables existen
2) como se influyen entre si (quien depende de quien)
3) cuanta probabilidad tiene cada cosa dado sus causas
"""