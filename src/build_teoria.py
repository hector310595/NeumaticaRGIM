"""Sesión 1 (teoría, 2 h): Representación neumática.  Uso: python3 src/build_teoria.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pptx_utils import (DGREEN, GREEN, GTINT, INK, MUTED, NAVY, ORANGE, RED, ROOT, TINT,  # noqa: E402
                        WHITE, Deck, box, caption, card, circle_num, image, table, text)
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402

OUT = os.path.join(ROOT, "sesion1_teoria", "RGIM_S1_Representacion_Neumatica_Teoria.pptx")

d = Deck("Representación neumática · RGIM")

# ------------------------------------------------------------------ apertura
d.cover()
d.title_slide("Representación neumática",
              "Representación Gráfica para Ingeniería Mecatrónica\nSesión teórica · 2 h",
              notes="Bienvenida. Esta semana es la única dedicada a neumática: hoy aprendemos a LEER y "
                    "DIBUJAR esquemas neumáticos (norma ISO 1219); en la práctica dirigida los "
                    "construiremos y simularemos en FluidSim. El foco es la representación, no el "
                    "dimensionamiento.")

s = d.content("Al terminar la semana podrás…",
              notes="(3 min) Dejar claro el alcance. Lo que NO veremos (y sí se ve en cursos de "
                    "automatización): cálculo de consumo de aire, dimensionamiento de válvulas, "
                    "electroneumática, PLC, Karnaugh/Grafcet.")
items = [
    ("1", "Leer un esquema", "Reconocer los símbolos ISO 1219 de cilindros, válvulas y accesorios."),
    ("2", "Dibujar un circuito", "Representarlo en posición de reposo, por niveles y con la "
                                 "nomenclatura correcta."),
    ("3", "Describir una secuencia", "Con notación A+ B+ … y con el diagrama espacio-fase."),
    ("4", "Resolver un enunciado", "Del texto al circuito en FluidSim, detectando y resolviendo "
                                   "señales bloqueadas (cascada)."),
]
for i, (n, h, b) in enumerate(items):
    y = 1.6 + i * 1.08
    circle_num(s, 0.8, y + 0.08, 0.62, n)
    text(s, 1.65, y, 5.2, 0.45, [h], size=19, bold=True, color=NAVY)
    text(s, 1.65, y + 0.45, 5.6, 0.6, [b], size=14, color=MUTED)
box(s, 7.6, 1.6, 5.1, 4.3, fill=TINT)
text(s, 7.85, 1.75, 4.7, 0.45, ["Agenda de hoy (120 min)"], size=18, bold=True, color=NAVY)
agenda = [("10'", "¿Por qué neumática? Cadena de energía"),
          ("30'", "Símbolos ISO 1219"),
          ("30'", "Circuitos básicos: mando, velocidad, lógica"),
          ("40'", "Secuencias, señales bloqueadas y cascada"),
          ("10'", "Metodología y cierre")]
for i, (t, a) in enumerate(agenda):
    y = 2.35 + i * 0.68
    text(s, 7.85, y, 0.8, 0.5, [t], size=16, bold=True, color=DGREEN)
    text(s, 8.65, y, 3.9, 0.6, [a], size=15, color=INK)

s = d.content("¿Por qué neumática en mecatrónica?",
              notes="(4 min) Contexto rápido. Mencionar ejemplos: pinzas de robots, prensas de "
                    "estampado, puertas de bus, clasificadores en fajas (como el ejercicio de la "
                    "práctica). Idea clave de KU Leuven: el aire comprimido es CARO (fugas) y "
                    "PELIGROSO (energía almacenada) – por eso se dibuja y se verifica con cuidado.")
card(s, 0.6, 1.6, 3.9, 3.25, "Ventajas", [
    "Movimientos lineales rápidos y simples",
    "Aire disponible y limpio; escape a la atmósfera",
    "Seguro en ambientes explosivos",
    "Tolera sobrecargas (el cilindro se detiene)"], fill=GTINT, head_color=DGREEN)
card(s, 4.72, 1.6, 3.9, 3.25, "Limitaciones", [
    "Aire compresible: difícil posicionar en puntos intermedios",
    "Fuerzas moderadas (≈ 6 bar)",
    "Ruido en escapes",
    "Energía cara: las fugas cuestan"], fill=TINT)
card(s, 8.85, 1.6, 3.9, 3.25, "Dónde lo verás", [
    "Pinzas y garras de robots",
    "Prensas, estampado y doblado",
    "Clasificadores en fajas transportadoras",
    "Puertas automáticas"], fill=TINT)
box(s, 0.6, 5.05, 12.15, 0.9, fill=TINT)
text(s, 0.85, 5.1, 11.7, 0.8, [[("El aire comprimido es caro y peligroso: ", {"bold": True, "color": RED}),
                                ("por eso el circuito se dibuja y se simula antes de montarlo.", {})]],
     size=17, anchor=MSO_ANCHOR.MIDDLE)

s = d.content("La cadena de energía neumática",
              notes="(4 min) Recorrer de izquierda a derecha. En los esquemas de FluidSim NO "
                    "dibujamos toda la red: cada puerto 1 lleva un símbolo de fuente (círculo con "
                    "triángulo) que representa la alimentación ya tratada por la unidad de "
                    "mantenimiento.")
steps = [("Compresor", "genera aire a presión"),
         ("Unidad de mantenimiento", "filtra, regula y (lubrica)"),
         ("Válvulas", "deciden a dónde va el aire"),
         ("Actuadores", "convierten la presión en movimiento")]
for i, (h, b) in enumerate(steps):
    x = 0.6 + i * 3.08
    box(s, x, 1.65, 2.75, 1.45, fill=TINT if i % 2 else GTINT)
    text(s, x + 0.15, 1.75, 2.45, 0.5, [h], size=16, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    text(s, x + 0.15, 2.3, 2.45, 0.7, [b], size=13, color=MUTED, align=PP_ALIGN.CENTER)
    if i < 3:
        text(s, x + 2.72, 2.05, 0.4, 0.5, ["→"], size=24, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
image(s, "sym_unidad", 0.8, 3.55, 4.6, 1.8)
caption(s, 0.8, 5.4, 4.6, "Fuente + unidad de mantenimiento (símbolo simplificado)")
image(s, "sym_fuente", 5.9, 3.55, 1.6, 1.4)
caption(s, 5.6, 5.0, 2.2, "Fuente de aire\n(en cada puerto 1)")
image(s, "sym_escape", 8.2, 3.55, 1.6, 1.4)
caption(s, 7.9, 5.0, 2.2, "Escape a la\natmósfera")
box(s, 10.1, 3.55, 2.65, 2.25, fill=GTINT)
text(s, 10.25, 3.65, 2.4, 2.1, [[("Convención FluidSim: ", {"bold": True, "color": DGREEN}),
                                 ("no se dibuja la tubería de alimentación; cada válvula lleva su "
                                  "fuente.", {})]], size=13)

# ------------------------------------------------------------- 1 · símbolos
d.section("1", "Símbolos ISO 1219", "Actuadores, válvulas, accionamientos y accesorios",
          notes="Bloque de 30 min. Mensaje: un símbolo describe la FUNCIÓN, no la construcción.")

s = d.content("Actuadores lineales: cilindros",
              notes="(4 min) Simple efecto: el aire empuja en un sentido y el resorte retorna; un "
                    "solo puerto. Doble efecto: dos puertos, el aire mueve en ambos sentidos – es el "
                    "que usaremos en casi todos los ejercicios. Convención: cilindros horizontales, "
                    "dibujados RETRAÍDOS (posición de reposo).")
image(s, "sym_cil_se", 0.7, 1.7, 5.6, 2.2)
text(s, 0.8, 3.95, 5.4, 0.45, ["Cilindro de simple efecto"], size=18, bold=True, color=NAVY)
text(s, 0.8, 4.45, 5.4, 1.5, ["Un puerto de trabajo", "Retorno por resorte",
                               "Fuerza útil solo en un sentido"], size=14, bullets=True)
image(s, "sym_cil_de", 6.9, 1.7, 5.6, 2.2)
text(s, 7.0, 3.95, 5.4, 0.45, ["Cilindro de doble efecto"], size=18, bold=True, color=NAVY)
text(s, 7.0, 4.45, 5.6, 1.5, ["Dos puertos: cámara posterior y lado vástago",
                               "Avance (A+) y retroceso (A−) con aire",
                               "Se nombran A, B, C…; sus finales de carrera a0, a1, b0…"],
     size=14, bullets=True)

s = d.content("Cómo se lee una válvula distribuidora",
              notes="(6 min) Explicar con calma: cada cuadro es una posición estable; las flechas "
                    "indican el paso de aire, la T es un puerto bloqueado. Los puertos (líneas "
                    "externas) se dibujan SOLO en el cuadro de reposo. Para 'ver' la otra posición "
                    "imaginar que el cuadro se desliza hasta quedar bajo los puertos. Pedir a los "
                    "alumnos que digan qué pasa con 4 y 2 al pilotar 14.")
image(s, "anatomia_valvula", 0.6, 1.5, 12.1, 4.55)

s = d.content("Nomenclatura: vías / posiciones y numeración",
              notes="(5 min) 3/2 = 3 vías (puertos de trabajo) y 2 posiciones. Recalcar 3/2 NC "
                    "(normalmente cerrada) como 'válvula de señal' típica y 5/2 como válvula de "
                    "potencia de cilindros de doble efecto. La 4/2 del enunciado de la cuchara es "
                    "funcionalmente igual a una 5/2 con los escapes unidos. El número del pilotaje "
                    "dice qué une: 14 → une 1 con 4; 12 → une 1 con 2.")
table(s, 0.6, 1.6, 5.6, [
    ["Puerto", "Función"],
    ["1", "Alimentación (presión)"],
    ["2, 4", "Utilización (salidas)"],
    ["3, 5", "Escape"],
    ["12", "Pilotaje que conecta 1 → 2"],
    ["14", "Pilotaje que conecta 1 → 4"],
], [1.3, 4.3], size=15, row_h=0.5)
text(s, 0.6, 4.85, 5.6, 1.1, [[("X/Y", {"bold": True, "color": NAVY}),
                               (" = número de vías / número de posiciones", {})],
                              [("ISO 5599: ", {"bold": True, "color": NAVY}),
                               ("la numeración es la misma en FluidSim", {})]], size=15)
image(s, "sym_32_boton", 6.6, 1.55, 3.0, 1.8)
caption(s, 6.6, 3.35, 3.0, "3/2 NC, pulsador / resorte")
image(s, "sym_52_boton", 9.7, 1.55, 3.0, 1.8)
caption(s, 9.7, 3.35, 3.0, "5/2, pulsador / resorte")
image(s, "sym_42_biestable", 6.6, 3.85, 3.0, 1.8)
caption(s, 6.6, 5.65, 3.0, "4/2, piloto / piloto")
image(s, "sym_52_biestable", 9.7, 3.85, 3.0, 1.8)
caption(s, 9.7, 5.65, 3.0, "5/2, piloto / piloto")

s = d.content("Accionamientos: ¿quién mueve la válvula?",
              notes="(5 min) Manuales (pulsador, palanca, pedal), mecánicos (rodillo; rodillo "
                    "escamoteable que solo actúa en un sentido; resorte) y neumáticos (pilotaje). "
                    "El rodillo es el 'final de carrera' neumático: se dibuja en la válvula y su "
                    "nombre (a1) se pone también como marca sobre el vástago del cilindro.")
acts = [("act_button", "Pulsador"), ("act_lever", "Palanca"), ("act_pedal", "Pedal"),
        ("act_roller", "Rodillo\n(final de carrera)"), ("act_roller1", "Rodillo escamoteable\n(un sentido)"),
        ("act_spring", "Resorte\n(retorno)"), ("act_pilot", "Pilotaje\nneumático")]
groups = [("Manual", 0, 3, TINT), ("Mecánico", 3, 6, GTINT), ("Neumático", 6, 7, TINT)]
cw = 1.68
for gname, a, b, fill in groups:
    x = 0.6 + a * cw + (0.12 if a else 0) + (0.12 if a >= 6 else 0)
    box(s, x, 1.6, (b - a) * cw - 0.05, 3.9, fill=fill)
    text(s, x, 1.68, (b - a) * cw, 0.4, [gname], size=15, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    for k in range(a, b):
        xx = 0.6 + k * cw + (0.12 if a else 0) + (0.12 if a >= 6 else 0)
        image(s, acts[k][0], xx + 0.12, 2.2, cw - 0.3, 1.6)
        caption(s, xx, 3.95, cw, acts[k][1], size=12, color=INK)
text(s, 0.6, 5.6, 12.1, 0.45, [[("Regla: ", {"bold": True, "color": DGREEN}),
                                ("el accionamiento dibujado a un lado lleva a la válvula al cuadro "
                                 "de ese lado.", {})]], size=15)

s = d.content("Monoestable vs. biestable (memoria)",
              notes="(4 min) Clave para los ejercicios: la válvula biestable 'recuerda' la última "
                    "orden aunque la señal desaparezca. Por eso basta un PULSO en 14 para que el "
                    "cilindro salga y quede afuera. Pregunta: ¿qué pasa si llegan señales a 12 y 14 "
                    "al mismo tiempo? → la válvula no cambia: esa es la semilla de las 'señales "
                    "bloqueadas'.")
image(s, "sym_52_pilot_resorte", 0.7, 1.6, 5.4, 2.6)
text(s, 0.8, 4.25, 5.4, 0.45, ["Monoestable (piloto / resorte)"], size=18, bold=True, color=NAVY)
text(s, 0.8, 4.75, 5.6, 1.3, ["Vuelve sola al reposo al quitar la señal",
                               "Necesita señal mantenida mientras dure el movimiento"],
     size=14, bullets=True)
image(s, "sym_52_biestable", 6.9, 1.6, 5.4, 2.6)
text(s, 7.0, 4.25, 5.6, 0.45, ["Biestable (piloto / piloto)"], size=18, bold=True, color=DGREEN)
text(s, 7.0, 4.75, 5.6, 1.3, ["Mantiene la última posición: es una MEMORIA",
                               "Basta un pulso en 14 (A+) o en 12 (A−)"],
     size=14, bullets=True)

s = d.content("Elementos de regulación y lógica",
              notes="(4 min) Reguladora unidireccional = estrangulación + antirretorno en paralelo: "
                    "regula en un sentido y deja paso libre en el otro. Selectora (O, 'shuttle'): "
                    "sale aire si llega por cualquiera de las dos entradas. Simultaneidad (Y): solo "
                    "sale aire si llega por las dos. Alternativa a la Y: poner dos válvulas en serie.")
for i, (img, h, b) in enumerate([
        ("sym_reguladora", "Reguladora unidireccional", "Estrangula en un sentido; paso libre en el "
                                                        "otro (antirretorno)."),
        ("sym_or", "Válvula selectora · O", "Salida 2 activa si hay señal en una U otra entrada."),
        ("sym_and", "Simultaneidad · Y", "Salida 2 activa solo si hay señal en AMBAS entradas.")]):
    x = 0.6 + i * 4.1
    box(s, x, 1.6, 3.85, 4.3, fill=TINT)
    image(s, img, x + 0.4, 1.8, 3.05, 2.1)
    text(s, x + 0.2, 4.05, 3.45, 0.45, [h], size=17, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    text(s, x + 0.2, 4.55, 3.45, 1.2, [b], size=14, color=INK, align=PP_ALIGN.CENTER)

# ------------------------------------------------------ 2 · circuitos básicos
d.section("2", "Circuitos básicos", "Mando directo e indirecto, velocidad, lógica y finales de carrera",
          notes="Bloque de 30 min. Cada circuito de este bloque es una 'pieza' que reaparece en los "
                "ejercicios de la práctica.")

s = d.content("Reglas para dibujar un esquema",
              notes="(5 min) Estas reglas son las que se evaluarán en la práctica. Los esquemas se "
                    "leen de abajo (señales) hacia arriba (actuadores), igual que fluye la "
                    "información.")
rules = [("Por niveles", "Actuadores arriba → válvulas de potencia → elementos de señal abajo."),
         ("Posición de reposo", "Todo se dibuja en reposo: cilindros retraídos, pulsadores sin "
                                "pulsar. Un final de carrera pisado en reposo (a0) se dibuja accionado."),
         ("Nombres", "Cilindros A, B, C; válvula de potencia VA; finales de carrera a0 / a1 "
                     "(marcados sobre el vástago)."),
         ("Líneas", "Continuas = trabajo (potencia). Discontinuas = pilotaje / señal. Punto = "
                    "unión; cruce sin punto = no hay unión."),
         ("Sin cruces innecesarios", "Ordena las válvulas de señal según la secuencia, de izquierda "
                                     "a derecha.")]
for i, (h, b) in enumerate(rules):
    y = 1.55 + i * 0.9
    circle_num(s, 0.65, y + 0.05, 0.5, str(i + 1), size=14)
    text(s, 1.35, y, 3.2, 0.8, [h], size=17, bold=True, color=NAVY)
    text(s, 4.3, y, 8.45, 0.85, [b], size=16, color=INK)

s = d.content("Mando directo",
              notes="(4 min) La válvula accionada por el operario alimenta directamente al cilindro. "
                    "Sencillo, pero: el operario debe estar junto al cilindro, la válvula debe ser "
                    "grande (caudal de potencia) y al soltar el pulsador el cilindro regresa. "
                    "Pregunta: ¿qué pasa si suelto S1 a mitad de carrera?")
image(s, "t_mando_directo_se", 0.6, 1.5, 5.7, 3.7)
caption(s, 0.6, 5.25, 5.7, "Simple efecto + 3/2 NC con pulsador", size=13, color=INK)
image(s, "t_mando_directo_de", 6.8, 1.5, 5.9, 3.7)
caption(s, 6.8, 5.25, 5.9, "Doble efecto + 5/2 con pulsador y resorte", size=13, color=INK)

s = d.content("Mando indirecto y memoria",
              notes="(5 min) Separar potencia y señal: la válvula de potencia VA (5/2 biestable) "
                    "está junto al cilindro; las válvulas de señal (pequeñas) pueden estar lejos — "
                    "justo lo que piden los enunciados ('el operador controla a distancia', "
                    "'pulsador alejado de la zona de doblado'). Un pulso en S1 extiende y el "
                    "cilindro se queda afuera hasta un pulso en S2.")
image(s, "t_mando_indirecto_memoria", 0.6, 1.5, 6.4, 4.55)
card(s, 7.3, 1.6, 5.4, 4.3, "¿Por qué indirecto?", [
    "Las válvulas de señal son pequeñas y pueden estar lejos (mando a distancia)",
    "La válvula de potencia va cerca del cilindro",
    "Con 5/2 biestable: un pulso basta (memoria)",
    "Las líneas de señal se dibujan discontinuas"])

s = d.content("Regulación de velocidad",
              notes="(5 min) En neumática se regula estrangulando el ESCAPE (meter-out): el aire "
                    "atrapado en la cámara que se vacía hace de 'colchón' y el movimiento es "
                    "estable. Estrangular la entrada produce movimiento a saltos (stick-slip). Para "
                    "regular la salida del vástago se coloca la reguladora en el lado vástago, con "
                    "el antirretorno dejando pasar libre HACIA el cilindro.")
image(s, "t_regulacion_velocidad", 0.6, 1.5, 8.4, 4.55)
card(s, 9.25, 1.6, 3.45, 4.3, "Regla práctica", [
    "Regular el ESCAPE (meter-out)",
    "Reguladora en la línea por la que SALE el aire del movimiento a frenar",
    "Antirretorno: paso libre hacia el cilindro"], size=14, fill=GTINT, head_color=DGREEN)

s = d.content("Funciones lógicas: O e Y",
              notes="(5 min) O: dos lugares para dar la misma orden (puerta del garaje: interior "
                    "O exterior; prensa: pedal O pulsador). Y: seguridad a dos manos, o 'solo arranca "
                    "si el ciclo terminó' (S Y a0 Y b0 …). La Y también se logra poniendo válvulas "
                    "en serie: la salida de una alimenta el puerto 1 de la siguiente.")
image(s, "t_logica_or", 0.6, 1.5, 5.1, 4.1)
caption(s, 0.6, 5.6, 5.1, "O: S1 o S2 mueven el cilindro", size=13, color=INK)
image(s, "t_logica_and", 6.0, 1.5, 5.1, 4.1)
caption(s, 6.0, 5.6, 5.1, "Y: se necesitan S1 y S2", size=13, color=INK)
box(s, 11.25, 1.6, 1.5, 4.3, fill=GTINT)
text(s, 11.32, 1.7, 1.36, 4.1, [[("Y en serie", {"bold": True, "color": DGREEN})],
                                 "Salida 2 de una válvula → entrada 1 de la siguiente"],
     size=12, align=PP_ALIGN.CENTER)

s = d.content("Final de carrera: retorno automático",
              notes="(4 min) S1 da la orden A+; cuando el vástago llega al final pisa el rodillo a1, "
                    "que pilota 12 y el cilindro regresa (A−). Es el esqueleto del ejercicio de la "
                    "cuchara. Preguntar: ¿qué pasa si el operario MANTIENE presionado S1 cuando el "
                    "vástago llega a a1? → la válvula recibe 14 y 12 a la vez y no retrocede. "
                    "Gancho para el bloque 3.")
image(s, "t_semiautomatico", 0.6, 1.5, 7.2, 4.55)
box(s, 8.1, 1.6, 4.6, 2.3, fill=TINT)
text(s, 8.3, 1.7, 4.3, 2.1, [[("Ciclo: ", {"bold": True, "color": NAVY}), ("S1 → A+ → a1 → A−", {})],
                             "El rodillo a1 se dibuja abajo, en la zona de señales, y su nombre "
                             "se marca sobre el vástago."], size=15)
box(s, 8.1, 4.1, 4.6, 1.8, fill=GTINT)
text(s, 8.3, 4.2, 4.3, 1.6, [[("Pregunta: ", {"bold": True, "color": RED}),
                              ("¿qué ocurre si mantengo S1 pulsado cuando el vástago llega a a1?", {})]],
     size=15)

# --------------------------------------------------------------- 3 · secuencias
d.section("3", "Secuencias y método cascada", "Notación, diagrama espacio-fase y señales bloqueadas",
          notes="Bloque de 40 min. Es el corazón de lo que piden los enunciados de la práctica 11.")

s = d.content("Notación y diagrama espacio-fase",
              notes="(6 min) A+ = sale el vástago de A; A− = entra. Paréntesis = movimientos "
                    "simultáneos: (A− B−). El diagrama espacio-fase dibuja cada cilindro entre 0 "
                    "(retraído) y 1 (extendido) a lo largo de las fases; arriba se anota qué señal "
                    "dispara cada fase. Abajo: cuándo está activo cada final de carrera. Construirlo "
                    "en la pizarra junto con los alumnos.")
image(s, "fase_ABAB", 0.6, 1.5, 7.4, 4.55)
card(s, 8.3, 1.6, 4.4, 4.3, "Cómo leerlo", [
    "Cada fase = un paso de la secuencia",
    "Línea inclinada = cilindro en movimiento",
    "Flecha arriba = señal que dispara la fase",
    "Barras abajo = final de carrera activo",
    "Regla: el final de un movimiento dispara el siguiente"])

s = d.content("Del diagrama al circuito: A+ B+ A− B−",
              notes="(5 min) Cada señal del diagrama se convierte en una válvula de rodillo que "
                    "pilota la válvula del siguiente movimiento: S·b0 → 14 de VA; a1 → 14 de VB; "
                    "b1 → 12 de VA; a0 → 12 de VB. b0 y a0 están pisados en reposo: se dibujan "
                    "accionados. La serie b0 → S es una Y: solo arranca si B está en casa. En esta "
                    "secuencia NO hay señales bloqueadas, por eso no necesitamos nada más.")
image(s, "t_secuencia_ABAB", 0.6, 1.5, 8.0, 4.55)
table(s, 8.9, 1.7, 3.8, [["Fase", "Orden", "Señal"],
                         ["1", "A+", "S · b0"], ["2", "B+", "a1"], ["3", "A−", "b1"], ["4", "B−", "a0"]],
      [0.9, 1.1, 1.8], size=15, row_h=0.5)
text(s, 8.9, 4.4, 3.8, 1.5, ["S en serie con b0 = arranque solo si el ciclo anterior terminó."],
     size=14, color=MUTED)

s = d.content("El problema: señales bloqueadas",
              notes="(6 min) Cambiando el orden a A+ B+ B− A− aparece el problema: en la fase 3 "
                    "queremos B− (señal b1) pero a1 sigue pisado mandando B+ → la válvula VB recibe "
                    "12 y 14 a la vez y no cambia. Lo mismo en la fase 1 con b0 (mando A−) mientras "
                    "pedimos A+. Una señal está 'bloqueada' (o 'permanente') cuando sigue activa "
                    "cuando hay que dar la orden contraria. Cómo detectarlo: en el diagrama, una "
                    "barra de sensor que sigue activa cuando el mismo cilindro debe invertir.")
image(s, "fase_ABBA_bloqueo", 0.6, 1.5, 7.8, 4.55)
card(s, 8.7, 1.6, 4.0, 4.3, "A+ B+ B− A−", [
    "Fase 3: b1 pide B−, pero a1 sigue pidiendo B+",
    "Fase 1: S pide A+, pero b0 sigue pidiendo A−",
    "La válvula biestable recibe 12 y 14 a la vez → no conmuta"], size=15, fill=GTINT,
     head_color=RED)

s = d.content("¿Cómo se eliminan las señales bloqueadas?",
              notes="(4 min) Tres caminos (KU Leuven los presenta todos). En este curso usamos el "
                    "rodillo escamoteable para casos sencillos y el método cascada como método "
                    "sistemático. Temporizadores y electroneumática/PLC se ven en cursos de "
                    "automatización.")
table(s, 0.6, 1.6, 12.1, [
    ["Solución", "Idea", "A favor", "En contra"],
    ["Rodillo escamoteable", "El final de carrera da solo un pulso, en un sentido",
     "Pocos componentes", "No confirma la posición; poco robusto"],
    ["Método cascada", "Dividir la secuencia en grupos; solo un grupo tiene aire",
     "Sistemático, seguro", "Más válvulas; cambios de grupo"],
    ["Temporizadores / PLC", "La lógica corta la señal (electrónica)",
     "Flexible", "Fuera del alcance de esta semana"],
], [2.6, 4.0, 2.4, 3.1], size=14, row_h=0.75)
box(s, 0.6, 4.95, 12.1, 0.95, fill=GTINT)
text(s, 0.8, 5.05, 11.7, 0.8, [[("En la práctica usaremos el ", {}), ("método cascada", {"bold": True,
                                                                                    "color": DGREEN}),
                                 (": siempre funciona y se dibuja paso a paso.", {})]], size=16,
     anchor=MSO_ANCHOR.MIDDLE)

s = d.content("Método cascada: receta",
              notes="(8 min) Hacerlo con A+ B+ B− A− en la pizarra. 1) Escribir la secuencia y "
                    "cortar cada vez que una letra se repetiría: A+ B+ | B− A−. 2) N.º de grupos = "
                    "2 → 1 válvula selectora de grupo VG (5/2 biestable). 3) Cada grupo es una línea "
                    "de alimentación; solo una tiene presión. 4) El PRIMER movimiento de cada grupo "
                    "sale directo de su línea. 5) Los demás los dispara el final de carrera del "
                    "movimiento anterior, alimentado por la línea del grupo. 6) El ÚLTIMO final de "
                    "carrera de un grupo conmuta VG al siguiente grupo. 7) El arranque S va en serie "
                    "en la última línea (la que está activa en reposo).")
recipe = ["Escribe la secuencia y córtala en grupos donde ninguna letra se repita",
          "N.º de válvulas selectoras = n.º de grupos − 1 (2 grupos → 1 VG 5/2 biestable)",
          "Cada grupo es una línea de alimentación; en cada instante solo una tiene aire",
          "El primer movimiento de cada grupo se pilota directo desde su línea",
          "Los siguientes los dispara el final de carrera anterior, alimentado desde la línea",
          "El último final de carrera del grupo conmuta VG al grupo siguiente",
          "El arranque S va en la última línea (activa en reposo)"]
for i, r in enumerate(recipe):
    y = 1.55 + i * 0.62
    circle_num(s, 0.65, y + 0.04, 0.44, str(i + 1), size=13)
    text(s, 1.25, y, 6.75, 0.6, [r], size=15, anchor=MSO_ANCHOR.MIDDLE)
box(s, 8.2, 1.6, 4.5, 4.3, fill=TINT)
text(s, 8.4, 1.7, 4.1, 0.45, ["Ejemplo"], size=17, bold=True, color=NAVY)
text(s, 8.4, 2.25, 4.1, 0.6, [[("A+ B+ ", {"color": DGREEN, "bold": True}), ("|", {"bold": True}),
                              (" B− A−", {"color": ORANGE, "bold": True})]], size=26)
text(s, 8.4, 3.05, 4.1, 2.8, [[("Grupo I: ", {"bold": True, "color": DGREEN}), ("A+ B+", {})],
                              [("Grupo II: ", {"bold": True, "color": ORANGE}), ("B− A−", {})],
                              "2 grupos → 1 válvula VG",
                              [("I → II con ", {}), ("b1", {"bold": True})],
                              [("II → I con ", {}), ("S · a0", {"bold": True})]], size=15)

s = d.content("Cascada A+ B+ | B− A−: el circuito",
              notes="(6 min) Recorrer el circuito siguiendo los colores. Reposo: VG en 12 → línea "
                    "II (naranja) con aire. S·a0 pilota VG14 → línea I (verde): A+ directo. a1 "
                    "(alimentado por I) → B+. b1 (por I) → VG12: cambia a línea II → B− directo. "
                    "b0 (por II) → A−. a0 y S quedan listos para el siguiente ciclo. Como la línea "
                    "I queda SIN aire, a1 ya no puede bloquear B−.")
image(s, "t_cascada_ABBA", 0.4, 1.4, 8.6, 4.7)
image(s, "fase_ABBA_cascada", 9.0, 1.5, 3.75, 2.9)
box(s, 9.0, 4.5, 3.75, 1.45, fill=GTINT)
text(s, 9.12, 4.55, 3.55, 1.35, ["Una señal sin aire no puede bloquear: esa es toda la idea de "
                                 "la cascada."], size=14, color=INK, anchor=MSO_ANCHOR.MIDDLE)

s = d.content("Practiquemos: ¿cuántos grupos?",
              notes="(5 min) Pedir a los alumnos que agrupen en 1 minuto cada secuencia. "
                    "Respuestas: A+B+A−B− → no hay bloqueo, pero en cascada sería A+B+ | A−B− (2). "
                    "A+B+C+(A−B−C−) → A+B+C+ | (A−B−C−): 2 grupos, 1 VG. (A+B+) A− B− → (A+B+) | "
                    "A− B−: 2 grupos. A+ B+ (A−B−) C+ C− → A+B+ | (A−B−) C+ | C−: 3 grupos, PERO el "
                    "último grupo puede fusionarse con el primero (C− A+ B+) porque no repite letra "
                    "→ 2 grupos. Estas tres últimas son las secuencias de la práctica dirigida 11.")
table(s, 0.6, 1.6, 7.6, [["Secuencia", "Grupos", "N.º VG"],
                         ["A+ B+ A− B−", "", ""],
                         ["A+ B+ C+ (A− B− C−)", "", ""],
                         ["(A+ B+) A− B−", "", ""],
                         ["A+ B+ (A− B−) C+ C−", "", ""]],
      [3.2, 3.0, 1.4], size=16, row_h=0.62)
card(s, 8.55, 1.6, 4.15, 4.3, "Pistas", [
    "Corta donde una letra se repetiría",
    "Movimientos simultáneos (…) van en el mismo grupo",
    "El último grupo puede unirse al primero si no repite letras"], size=14, fill=GTINT,
     head_color=DGREEN)

# -------------------------------------------------------------------- cierre
s = d.content("Del enunciado al circuito: metodología",
              notes="(5 min) Esta es la receta que seguiremos en la práctica dirigida para TODOS los "
                    "ejercicios. Pedir que la copien o tengan a mano.")
met = [("Leer", "Identifica actuadores, mandos y condiciones (velocidad, seguridad, posición "
                "inicial)."),
       ("Secuencia", "Escribe A+ B+ … y el diagrama espacio-fase con las señales."),
       ("Potencia", "Elige válvulas (5/2 biestable si hay pulsos) y reguladoras (meter-out)."),
       ("Señales", "Asigna a cada fase su señal: pulsador, final de carrera, O / Y."),
       ("Bloqueos", "¿Alguna señal sigue activa cuando hay que invertir? → cascada."),
       ("Dibujar y simular", "En FluidSim, en reposo, por niveles; simula y verifica cada fase.")]
for i, (h, b) in enumerate(met):
    col, row = i % 3, i // 3
    x, y = 0.6 + col * 4.1, 1.6 + row * 2.2
    box(s, x, y, 3.85, 2.0, fill=TINT if row == 0 else GTINT)
    circle_num(s, x + 0.2, y + 0.2, 0.5, str(i + 1), size=14)
    text(s, x + 0.85, y + 0.22, 2.9, 0.45, [h], size=17, bold=True, color=NAVY)
    text(s, x + 0.2, y + 0.8, 3.5, 1.15, [b], size=15)

s = d.content("Resumen y práctica dirigida",
              notes="(3 min) Cerrar. En la práctica: 30' FluidSim, calentamiento y luego los "
                    "enunciados 10 y 11. Traer la receta de cascada.")
card(s, 0.6, 1.6, 5.9, 4.3, "Hoy aprendimos", [
    "Símbolos ISO 1219: cilindros, válvulas X/Y, accionamientos",
    "Reglas de dibujo: niveles, reposo, nombres a0/a1",
    "Mando indirecto, memoria, meter-out, O / Y",
    "Secuencias y diagrama espacio-fase",
    "Señales bloqueadas y método cascada"])
card(s, 6.8, 1.6, 5.9, 4.3, "En la práctica dirigida (3 h)", [
    "FluidSim: biblioteca, marcas de final de carrera, simulación",
    "Calentamiento: mando indirecto + retorno automático",
    "PD 10: puerta de garaje y cuchara de fundición",
    "PD 11: estampado, dobladora y prensa (cascada)"], size=15, fill=GTINT, head_color=DGREEN)

d.cover()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
d.save(OUT)
print("ok", OUT, len(d.prs.slides))
