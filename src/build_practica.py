"""Sesión 2 (práctica dirigida, 3 h) en FluidSim.  Uso: python3 src/build_practica.py

Las diapositivas de SOLUCIÓN se generan ocultas (no se proyectan en modo presentación);
el docente puede mostrarlas con clic derecho → "Mostrar diapositiva"."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pptx_utils import (DGREEN, GTINT, INK, MUTED, NAVY, RED, ROOT, TINT, Deck, box,  # noqa: E402
                        caption, card, circle_num, image, table, text)
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402

OUT = os.path.join(ROOT, "sesion2_practica", "RGIM_S2_Practica_Dirigida_FluidSim.pptx")

d = Deck("Representación neumática · Práctica dirigida")


def steps_slide(title, statement_img, statement, steps, notes, img_w=4.6):
    s = d.content(title, notes=notes)
    box(s, 0.6, 1.55, img_w, 4.4, fill=TINT)
    if statement_img:
        image(s, statement_img, 0.75, 1.65, img_w - 0.3, 2.6)
        text(s, 0.75, 4.35, img_w - 0.3, 1.55, statement, size=13, color=INK)
    else:
        text(s, 0.8, 1.7, img_w - 0.4, 0.4, ["Enunciado"], size=16, bold=True, color=NAVY)
        text(s, 0.8, 2.2, img_w - 0.4, 3.6, statement, size=16, color=INK)
    x = 0.6 + img_w + 0.35
    w = 12.75 - x
    text(s, x, 1.5, w, 0.4, ["Paso a paso"], size=18, bold=True, color=DGREEN)
    for i, st in enumerate(steps):
        y = 2.0 + i * (3.95 / len(steps))
        circle_num(s, x, y + 0.02, 0.42, str(i + 1), size=13)
        text(s, x + 0.55, y - 0.03, w - 0.55, 3.95 / len(steps), [st], size=15)
    return s


def solution_slide(title, circuit, phase, notes_list, notes, circ_w=8.4):
    s = d.content(title, notes=notes, hidden=True)
    image(s, circuit, 0.4, 1.4, circ_w, 4.7)
    x = 0.4 + circ_w + 0.2
    w = 12.75 - x
    if phase:
        image(s, phase, x, 1.45, w, 2.1)
        y = 3.65
    else:
        y = 1.55
    box(s, x, y, w, 6.0 - y, fill=GTINT)
    text(s, x + 0.12, y + 0.08, w - 0.24, 6.0 - y - 0.16, notes_list, size=14, bullets=True,
         space_after=3)
    return s


# ------------------------------------------------------------------ apertura
d.cover()
d.title_slide("Práctica dirigida: representación neumática",
              "Del enunciado al circuito en FluidSim\nSesión práctica · 3 h",
              notes="Material para proyectar durante la práctica. Las diapositivas de solución están "
                    "OCULTAS: no aparecen al presentar. Para mostrarlas: clic derecho en la miniatura "
                    "→ Mostrar diapositiva.")

s = d.content("Plan de la sesión (180 min)",
              notes="Ajustar tiempos según el avance. Si el grupo va lento, el ejercicio de estampado "
                    "(el más largo) puede quedar como tarea, con la solución publicada después.")
table(s, 0.6, 1.55, 7.6, [
    ["Tiempo", "Actividad"],
    ["0:00 – 0:20", "FluidSim en 20 minutos"],
    ["0:20 – 0:40", "Calentamiento: memoria y retorno automático"],
    ["0:40 – 1:00", "PD 10 · Ej. 2 — Cuchara de fundición"],
    ["1:00 – 1:30", "PD 10 · Ej. 1 — Puerta de garaje"],
    ["1:30 – 1:40", "Pausa"],
    ["1:40 – 2:05", "PD 11 · Ej. 2 — Dobladora (cascada)"],
    ["2:05 – 2:25", "PD 11 · Ej. 3 — Prensa de bandejas"],
    ["2:25 – 2:50", "PD 11 · Ej. 1 — Estampado y selección"],
    ["2:50 – 3:00", "Errores frecuentes y cierre"],
], [1.9, 5.7], size=14, row_h=0.43)
card(s, 8.55, 1.6, 4.2, 4.3, "Entregable por ejercicio", [
    "Secuencia y diagrama espacio-fase",
    "Circuito en FluidSim (archivo .ct)",
    "Captura de la simulación funcionando"], fill=GTINT, head_color=DGREEN)

# ---------------------------------------------------------------- FluidSim
d.section("0", "FluidSim en 20 minutos", "Lo mínimo para dibujar y simular",
          notes="Hacer una demostración en vivo mientras los alumnos replican: un cilindro de doble "
                "efecto con una 5/2 de pulsador. Los nombres de menú pueden variar ligeramente según "
                "la versión de FluidSim.")

s = d.content("Flujo de trabajo en FluidSim",
              notes="Demostrar cada paso. Puntos donde se traban los alumnos: (1) la válvula "
                    "configurable se edita con doble clic; (2) los finales de carrera solo funcionan "
                    "si la etiqueta del rodillo coincide EXACTAMENTE con la marca del cilindro; "
                    "(3) una conexión sin el punto negro no está conectada.")
fl = [("Nuevo circuito", "Archivo → Nuevo. Abre la biblioteca de componentes neumáticos."),
      ("Arrastrar componentes", "Cilindro de doble efecto, válvula configurable, fuente de aire, "
                                "unidad de mantenimiento."),
      ("Configurar válvulas", "Doble clic: elige 3/2, 4/2 o 5/2 y el accionamiento de cada lado "
                              "(pulsador, rodillo, piloto, resorte)."),
      ("Conectar", "Arrastra desde un puerto hasta otro. Revisa que aparezca el punto de unión."),
      ("Finales de carrera", "En el cilindro define marcas (a0, a1); en la válvula de rodillo "
                             "escribe la MISMA etiqueta."),
      ("Simular", "Botón Iniciar simulación. Clic en los pulsadores. Azul oscuro = línea con presión."),
      ("Verificar", "Agrega un diagrama de estado y compáralo con tu diagrama espacio-fase.")]
for i, (h, b) in enumerate(fl):
    col = 0 if i < 4 else 1
    row = i if i < 4 else i - 4
    x, y = 0.6 + col * 6.15, 1.55 + row * 1.12
    circle_num(s, x, y + 0.08, 0.5, str(i + 1), size=14)
    text(s, x + 0.65, y, 5.3, 0.4, [h], size=16, bold=True, color=NAVY)
    text(s, x + 0.65, y + 0.38, 5.3, 0.7, [b], size=13, color=INK)
box(s, 6.75, 4.95, 6.0, 1.0, fill=GTINT)
text(s, 6.9, 5.0, 5.75, 0.9, [[("Tip: ", {"bold": True, "color": DGREEN}),
                               ("dibuja siempre en reposo y por niveles, igual que en la teoría; "
                                "FluidSim no ordena el esquema por ti.", {})]], size=13,
     anchor=MSO_ANCHOR.MIDDLE)

s = d.content("Calentamiento (20 min)",
              notes="C1: repasa mando indirecto y memoria. C2: agrega un final de carrera. Pedir que "
                    "prueben mantener S1 presionado en C2 y que expliquen por qué el cilindro no "
                    "regresa: es la primera 'señal bloqueada'. C3 (opcional): agregar regulación "
                    "meter-out al avance y comprobar en la simulación que solo el avance es lento.")
image(s, "t_mando_indirecto_memoria", 0.6, 1.5, 3.9, 3.6)
caption(s, 0.6, 5.15, 3.9, "C1 · S1 → A+, S2 → A− con 5/2 biestable", size=13, color=INK)
image(s, "t_semiautomatico", 4.7, 1.5, 4.3, 3.6)
caption(s, 4.7, 5.15, 4.3, "C2 · S1 → A+, a1 → A− (retorno automático)", size=13, color=INK)
card(s, 9.25, 1.6, 3.5, 4.3, "Reto", [
    "En C2 mantén S1 presionado: ¿qué pasa? ¿por qué?",
    "C3: haz que solo el avance sea lento (meter-out)"], fill=GTINT, head_color=DGREEN, size=15)

# --------------------------------------------------------------------- PD 10
d.section("10", "Práctica dirigida 10", "Cuchara de fundición y puerta de garaje",
          notes="Empezamos por la cuchara (un cilindro, un final de carrera) y luego la puerta, "
                "que introduce lógica O / Y y memoria.")

steps_slide("PD 10 · Ej. 2 — Cuchara de fundición", "enunciados/pd10_cuchara",
            ["Un operador, a distancia, inicia con un botón. El vástago sale y se retrae a baja "
             "velocidad; al final de carrera un rodillo invierte el movimiento. Componentes: "
             "4/2 pulso/pulso, 3/2 pulsador, 3/2 rodillo, 2 reguladoras."],
            ["Escribe la secuencia y su diagrama espacio-fase.",
             "¿Qué señal pilota 14 y cuál 12 de la 4/2?",
             "¿Dónde van las 2 reguladoras y en qué sentido el antirretorno?",
             "Dibuja en reposo: ¿el rodillo a1 está accionado al inicio?",
             "Simula. ¿Qué pasa si mantienes el botón presionado?"],
            notes="Dejar 10 minutos de trabajo autónomo antes de discutir. Pistas: la 4/2 biestable "
                  "es la memoria; 'baja velocidad en ambos sentidos' = reguladora en cada línea, "
                  "estrangulando el escape (antirretorno con paso libre hacia el cilindro).")
solution_slide("Solución · Cuchara: A+ A−", "e1_2_cuchara", "fase_e1_2", [
    "S1 (3/2 NC) → 14 de VA: A+",
    "a1 (3/2 rodillo) → 12 de VA: A−",
    "R1 y R2 meter-out: paso libre hacia el cilindro",
    "a1 NO está accionado en reposo",
    "Si S1 sigue pulsado al llegar a a1, VA recibe 14 y 12 → no retrocede (señal bloqueada)"],
               notes="Comentar que la 4/2 equivale a una 5/2 con escapes unidos. Variante de "
                     "discusión: ¿cómo evitar el bloqueo si el operario mantiene el botón? → rodillo "
                     "escamoteable o S1 en serie con a0.")

steps_slide("PD 10 · Ej. 1 — Puerta de garaje", None,
            ["Abrir y cerrar desde dentro y desde fuera. Un actuador. Un botón exterior y otro "
             "interior, cada uno abre Y cierra. Cierre con velocidad limitada. Al inicio la puerta "
             "está cerrada."],
            ["¿Qué movimiento es abrir: A+ o A−? ¿Cómo empieza el cilindro?",
             "Dos lugares de mando → ¿qué función lógica?",
             "Un mismo botón abre y cierra: ¿de qué depende la orden?",
             "¿Qué válvula de potencia 'recuerda' si la puerta quedó abierta?",
             "¿Dónde limitas solo la velocidad de cierre?"],
            notes="Pista clave del paso 3: la orden depende de DÓNDE está la puerta. Si está cerrada "
                  "(a0) el botón debe abrir; si está abierta (a1) debe cerrar → Y entre el botón y "
                  "cada final de carrera (en serie: la salida de la O alimenta a a0 y a1). Aceptar "
                  "también la variante de 4 pulsadores (abrir/cerrar en cada lado) si el grupo "
                  "interpreta 'botón' como botonera.", img_w=4.6)
s = solution_slide("Solución · Puerta: botón conmutado", "e1_1_puerta_conmutada", None, [
    "S1 O S2 (selectora) alimenta a los rodillos a0 y a1",
    "Puerta cerrada → a0 pisado → 14: abre (A+)",
    "Puerta abierta → a1 pisado → 12: cierra (A−)",
    "VA 5/2 biestable = memoria",
    "R1 en la cámara posterior: frena el escape al cerrar (A−)",
    "A mitad de carrera el botón no hace nada; si se mantiene pulsado, la puerta oscila"],
    notes="Discutir la limitación: si el usuario mantiene el botón, al llegar a a1 la puerta "
          "vuelve a cerrarse. En la práctica real se agregaría un temporizador o se usaría "
          "electroneumática.", circ_w=6.0)
solution_slide("Variante · Puerta con botonera (4 pulsadores)", "e1_1_puerta_botonera", None, [
    "Abrir: S1 (interior) O S2 (exterior) → 14",
    "Cerrar: S3 (interior) O S4 (exterior) → 12",
    "Dos válvulas selectoras",
    "Más simple de razonar; usa más pulsadores"],
    notes="Usar si el grupo interpreta 'un botón que abre y cierra' como un panel con dos "
          "pulsadores.", circ_w=7.0)

# --------------------------------------------------------------------- PD 11
d.section("11", "Práctica dirigida 11", "Secuencias con método cascada",
          notes="Orden sugerido: dobladora (la cascada más limpia), prensa (agrega O / Y en el "
                "arranque) y estampado (fusión de grupos + selectores manuales).")

steps_slide("PD 11 · Ej. 2 — Dobladora de chapa", "enunciados/pd11_dobladora",
            ["A sujeta, B hace el 1.er doblez, C el 2.º; luego todos regresan a la vez. Pulsador "
             "alejado. Sujeción y doblado lentos. Solo se inicia si el ciclo terminó."],
            ["Secuencia: A+ B+ C+ (A− B− C−). Dibuja el espacio-fase.",
             "¿Hay señales bloqueadas? Revisa a1 y b1 al retroceder.",
             "Forma los grupos. ¿Cuántas válvulas selectoras?",
             "Condición de arranque: ¿qué finales de carrera van en serie con S?",
             "Reguladoras: ¿en qué línea frenas el avance?"],
            notes="a1 manda B+ y sigue pisado cuando se ordena B− (retroceso simultáneo): bloqueo. "
                  "Grupos: I = A+ B+ C+, II = A− B− C− → 1 VG. Arranque: S · a0 · b0 · c0 en la "
                  "línea II.")
solution_slide("Solución · Dobladora (2 grupos)", "e2_2_doblado", "fase_e2_2", [
    "I: A+ directo; a1 → B+; b1 → C+; c1 → II",
    "II: A−, B−, C− directos",
    "Arranque: a0 · b0 · c0 · S → VG 14",
    "Meter-out en lado vástago (avance lento)",
    "a0, b0, c0 dibujados accionados"],
    notes="Remarcar la cadena en serie a0-b0-c0-S como función Y: 'solo se puede iniciar si el "
          "ciclo completo ha terminado'.")

steps_slide("PD 11 · Ej. 3 — Prensa de bandejas", "enunciados/pd11_prensa",
            ["Pedal O pulsador (a 2 m). Las plataformas 3 y 4 salen a la vez y aplastan la lámina; "
             "luego 3 se retira rápido y, cuando está contraída, 4 también. Salida lenta, retorno "
             "rápido. La plataforma 4 debe estar en su posición inicial para empezar."],
            ["Nombra A = plataforma 3, B = plataforma 4. Escribe la secuencia.",
             "Arranque: ¿cómo combinas pedal, pulsador y b0?",
             "¿a0 bloquea algo? (pista: a0 manda B− y está pisado al inicio)",
             "Grupos y válvula selectora.",
             "¿Cómo logras salida lenta y retorno rápido?"],
            notes="Secuencia (A+ B+) A− B−. a0 está activo en reposo y manda B− mientras queremos "
                  "B+ → bloqueo → cascada: I = (A+ B+), II = A− B−. Cambio I→II con a1 · b1 en "
                  "serie. Arranque (P O S) · b0. Retorno rápido: sin estrangulación en el retorno "
                  "(opcional: válvula de escape rápido).")
solution_slide("Solución · Prensa (2 grupos)", "e2_3_prensa", "fase_e2_3", [
    "Arranque: (P O S) · b0 → VG 14",
    "I: A+ y B+ directos",
    "a1 · b1 (serie) → VG 12",
    "II: A− directo; a0 → B−",
    "Meter-out en el avance; retorno libre"],
    notes="Si se quiere un retorno aún más rápido: válvula de escape rápido en la cámara "
          "posterior (no es necesaria para la práctica).")

steps_slide("PD 11 · Ej. 1 — Estampado y selección", "enunciados/pd11_estampado",
            ["Botón 'Iniciar estampado': A sujeta, B estampa, A y B se retraen, C entrega a la faja "
             "y regresa. En la faja, 3 botones independientes accionan los selectores D, E, F "
             "(sin finales de carrera)."],
            ["Secuencia: A+ B+ (A− B−) C+ C−. Espacio-fase.",
             "Agrupa. ¿Puedes unir el último grupo con el primero?",
             "¿Qué señales disparan C+ y el arranque?",
             "Selectores D, E, F: ¿qué válvula usas si no hay finales de carrera?",
             "Dibuja dos esquemas: estación de estampado y faja."],
            notes="Grupos: A+ B+ | (A− B−) C+ | C−. El último (C−) no repite letras con el primero "
                  "→ se fusionan: I = C− A+ B+, II = A− B− C+ → solo 1 VG. Arranque: S · c0 en la "
                  "línea I. C+ con a0 · b0. Selectores: 5/2 pulsador/resorte → el cilindro sale "
                  "mientras se mantiene el pulsador.", img_w=5.0)
solution_slide("Solución · Estampado (2 grupos tras fusionar)", "e2_1_estampado_ABC", "fase_e2_1", [
    "I = C− A+ B+ ; II = A− B− C+",
    "Reposo: línea I con aire (C− asegurado)",
    "S · c0 → A+ ; a1 → B+ ; b1 → II",
    "II: A−, B− directos; a0 · b0 → C+ ; c1 → I",
    "Sin fusionar serían 3 grupos (2 VG)"],
    notes="Si el grupo prefiere 3 grupos sin fusionar, también es correcto: necesita 2 válvulas "
          "selectoras en cascada.")
s = d.content("Solución · Selectores D, E, F", hidden=True,
              notes="Tres circuitos independientes. Con 5/2 monoestable (pulsador/resorte) el "
                    "selector sale mientras se mantiene presionado y vuelve solo al soltarlo; no "
                    "necesita finales de carrera.")
image(s, "e2_1_selectores_DEF", 0.6, 1.6, 12.1, 3.4)
box(s, 0.6, 5.1, 12.1, 0.85, fill=GTINT)
text(s, 0.8, 5.15, 11.7, 0.75, ["Cada selector: 5/2 pulsador/resorte + cilindro de doble efecto "
                                "(alternativa: 3/2 + simple efecto)."], size=15,
     anchor=MSO_ANCHOR.MIDDLE)

# -------------------------------------------------------------------- cierre
s = d.content("Errores frecuentes",
              notes="Repasar con ejemplos reales de lo que se vio durante la sesión.")
errs = [("a0 dibujado sin accionar", "En reposo el vástago pisa a0: se dibuja accionado."),
        ("Antirretorno al revés", "Frena el movimiento equivocado: paso libre HACIA el cilindro."),
        ("Monoestable con pulsos", "El cilindro regresa al soltar: usa 5/2 biestable."),
        ("Rodillos alimentados desde la fuente", "En cascada se alimentan desde la línea del grupo."),
        ("Arranque sin condición", "S debe ir en serie con el final del ciclo (a0, b0…)."),
        ("Etiquetas que no coinciden", "En FluidSim el rodillo 'a1' no actúa si la marca del "
                                       "cilindro se llama distinto.")]
for i, (h, b) in enumerate(errs):
    col, row = i % 2, i // 2
    x, y = 0.6 + col * 6.15, 1.6 + row * 1.45
    box(s, x, y, 5.95, 1.3, fill=TINT if col == 0 else GTINT)
    text(s, x + 0.2, y + 0.1, 5.6, 0.45, [h], size=16, bold=True, color=RED)
    text(s, x + 0.2, y + 0.55, 5.6, 0.7, [b], size=14, color=INK)

s = d.content("Lista de verificación de tu circuito",
              notes="Puede usarse como rúbrica rápida de evaluación (1 punto por ítem).")
chk = ["Secuencia escrita y diagrama espacio-fase con las señales",
       "Esquema por niveles y en posición de reposo",
       "Nombres: A, B, C; VA, VB; a0, a1… también en el cilindro",
       "Válvulas de potencia adecuadas (memoria donde hay pulsos)",
       "Reguladoras en el lugar y sentido correctos",
       "Señales bloqueadas resueltas (cascada o escamoteable)",
       "Condición de arranque y de seguridad cumplida",
       "Simulación verificada fase por fase"]
for i, c in enumerate(chk):
    col, row = i // 4, i % 4
    x, y = 0.6 + col * 6.15, 1.6 + row * 1.05
    box(s, x, y + 0.12, 0.45, 0.45, fill=GTINT, radius=False)
    text(s, x + 0.65, y, 5.4, 0.75, [c], size=16, anchor=MSO_ANCHOR.MIDDLE)

d.cover()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
d.save(OUT)
print("ok", OUT, len(d.prs.slides))
