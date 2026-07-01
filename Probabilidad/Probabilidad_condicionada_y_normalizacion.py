"""
probabilidad condicionada y normalizacion
cual es la probabilidad de que el ruido en la casa sea un gato,
sabiendo que la ventana esta cerrada?
normalizacion.
normalizar es ajustar los numeros para que todo sume 1 (o sea 100%).
esto se hace mucho en ia porque a veces primero calculamos valores "crudos"
y luego los acomodamos para que sean probabilidades validas.
sirve para actualizar lo que creemos cuando tenemos nueva evidencia.
"""
# paso 1: probabilidades iniciales sin usar evidencia extra
# vamos a inventar una situacion tipo:
# escucho un ruido en la noche
# podria ser "gato" o "viento"

p_gato = 0.6    # antes de saber nada mas, creo que es gato con 60%
p_viento = 0.4  # creo que es viento con 40%

# estas 2 ya suman 1 (0.6 + 0.4 = 1.0) asi que son una distribucion valida
# paso 2: ahora aparece nueva informacion (evidencia)
# por ejemplo: "la ventana esta cerrada"

p_gato_dado_ventana = 0.9   # ahora creo que si la ventana esta cerrada es muy probable que sea el gato
p_viento_dado_ventana = 0.2 # viento casi no puede entrar, pero igual le dejo un 0.2 por si vibro algo

# estos numeros todavia NO son probabilidades limpias
# por que? porque 0.9 + 0.2 = 1.1 (eso es mas de 1)

# paso 3: normalizacion
suma_cruda = p_gato_dado_ventana + p_viento_dado_ventana

# dividimos cada valor entre la suma total
p_gato_normalizado = p_gato_dado_ventana / suma_cruda
p_viento_normalizado = p_viento_dado_ventana / suma_cruda

print("prob(gato | ventana cerrada) normalizada =", p_gato_normalizado)
print("prob(viento | ventana cerrada) normalizada =", p_viento_normalizado)

"""
- p_gato y p_viento:
  estas son las probabilidades "a lo bruto" sin evidencia nueva.
  es como lo que yo creo antes de revisar nada mas.
- p_gato_dado_ventana y p_viento_dado_ventana:
  el nombre "dado_ventana" significa "dado que la ventana esta cerrada".
  en palabras: ya tengo evidencia extra. estoy actualizando mis creencias.
- suma_cruda:
  sumo los valores nuevos (0.9 y 0.2) aunque no sumen 1.
  esto es como decir: estos son mis instintos despues de la pista nueva.
- normalizacion:
  hago cada valor / suma_cruda
  asi logro que ahora las nuevas probabilidades SI sumen 1 exacto.
  eso ya me da una distribucion valida.
probabilidad condicionada = probabilidad con contexto

normalizar = ajustar los numeros para que tengan sentido como probabilidades reales
"""

# extra: mostramos los valores en porcentaje nomas para que se vea bonito
print("gato con ventana cerrada (porcentaje) =", p_gato_normalizado * 100, "%")
print("viento con ventana cerrada (porcentaje) =", p_viento_normalizado * 100, "%")