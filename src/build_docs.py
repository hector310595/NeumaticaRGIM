"""Genera la guía del alumno, el solucionario docente y el plan de sesiones (.docx).
Uso: python3 src/build_docs.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from catalogo import CATALOGO, ORDEN  # noqa: E402
from docx_utils import (GREEN, MUTED, NAVY, RED, ROOT, answer_box, bullets, callout,  # noqa: E402
                        figure, image_table, landscape, new_doc, numbered, page_break, para,
                        portrait, table)

D_ALUM = os.path.join(ROOT, "sesion2_practica")
D_DOC = os.path.join(ROOT, "docente")
os.makedirs(D_ALUM, exist_ok=True)
os.makedirs(D_DOC, exist_ok=True)

# =====================================================================
# Enunciados (resumen fiel de PD 10 y PD 11, semestre 2025-1)
# =====================================================================
ENUNCIADOS = {
    "puerta": ("PD 10 · Ejercicio 1 — Puerta de garaje",
               "Diseñe un sistema de apertura y cierre de una puerta de garaje con aire comprimido: "
               "la puerta se abre y se cierra desde el interior y desde el exterior; un actuador es "
               "suficiente; hay un botón en el exterior y otro en el interior, y cada uno puede abrir "
               "y cerrar la puerta; por seguridad, la rapidez de cierre debe estar limitada; al "
               "inicio la puerta está cerrada.", None),
    "cuchara": ("PD 10 · Ejercicio 2 — Cuchara de fundición",
                "Un cilindro levanta una cuchara con metal fundido para verterlo en un molde. Un "
                "operador controla el sistema a distancia con un botón. El vástago sale y se retrae "
                "a baja velocidad, controlado por una válvula 4/2. Al final de la carrera se acciona "
                "un rodillo (válvula 3/2) que manda un pulso a la 4/2 para que el vástago se retraiga. "
                "Componentes: 1 cilindro de doble efecto; 2 reguladoras de caudal unidireccionales; "
                "1 válvula 4/2 accionamiento y retorno por pulso; 1 válvula 3/2 NC con botón y "
                "resorte; 1 válvula 3/2 NC con rodillo y resorte; 1 unidad de mantenimiento.",
                "enunciados/pd10_cuchara"),
    "estampado": ("PD 11 · Ejercicio 1 — Estampado y selección de paquetes",
                  "Con el botón «Iniciar estampado», el cilindro A sale hasta A1 para alimentar y "
                  "fijar el paquete; luego B sale hasta B1 y estampa; luego A y B se retraen hasta A0 "
                  "y B0; entonces C sale hasta C1 para entregar el paquete a la faja y regresa hasta "
                  "C0. En la faja, 3 botones independientes activan los selectores D, E y F (sin "
                  "finales de carrera).", "enunciados/pd11_estampado"),
    "doblado": ("PD 11 · Ejercicio 2 — Dobladora de chapa",
                "El cilindro A sujeta la chapa; B realiza el primer doblado y, al terminar, C el "
                "segundo; luego todos regresan simultáneamente. El ciclo se inicia con un pulsador "
                "alejado de la zona de doblado y se ejecuta automáticamente. La sujeción y el doblado "
                "deben ser lentos. El sistema solo puede iniciarse si el ciclo completo terminó.",
                "enunciados/pd11_dobladora"),
    "prensa": ("PD 11 · Ejercicio 3 — Prensa de bandejas",
               "El operario coloca una lámina y, con un pedal o un pulsador (ambos a 2 m), hace que "
               "las plataformas 3 y 4 se activen y aplasten la lámina. Luego la plataforma 3 se "
               "retira rápidamente y, cuando está contraída, la plataforma 4 también. La plataforma "
               "4 debe estar en su posición inicial antes de empezar; las plataformas salen lento y "
               "se retiran rápido.", "enunciados/pd11_prensa"),
}

PREGUNTAS = {
    "cuchara": ["Escriba la secuencia y dibuje el diagrama espacio-fase indicando la señal de cada fase.",
                "¿Qué señal llega al pilotaje 14 y cuál al 12 de la válvula 4/2?",
                "Ubique las dos reguladoras y el sentido de su antirretorno para frenar ambos "
                "movimientos (meter-out).",
                "En reposo, ¿la válvula de rodillo a1 está accionada? Dibújela como corresponde.",
                "Simule. ¿Qué ocurre si el operador mantiene presionado el botón cuando el vástago "
                "llega a a1? ¿Por qué?"],
    "puerta": ["¿Abrir corresponde a A+ o a A−? ¿En qué posición se dibuja el cilindro?",
               "Hay dos lugares de mando: ¿qué función lógica y qué válvula necesita?",
               "El mismo botón abre y cierra. ¿De qué depende que la orden sea abrir o cerrar? "
               "(Pista: ¿dónde está la puerta?)",
               "¿Qué válvula de potencia mantiene la puerta abierta cuando se suelta el botón?",
               "¿En qué línea y con qué sentido coloca la reguladora para limitar SOLO el cierre?",
               "Simule y discuta: ¿qué pasa si se pulsa a mitad de recorrido? ¿y si se mantiene pulsado?"],
    "doblado": ["Escriba la secuencia (use paréntesis para movimientos simultáneos) y el espacio-fase.",
                "Revise a1 y b1: ¿siguen activos cuando se ordena B− y C−? ¿Hay señales bloqueadas?",
                "Divida en grupos. ¿Cuántas líneas y cuántas válvulas selectoras de grupo necesita?",
                "¿Qué finales de carrera deben estar en serie con el pulsador para garantizar que el "
                "ciclo anterior terminó?",
                "¿Dónde coloca las reguladoras para que la sujeción y el doblado sean lentos?",
                "Dibuje en FluidSim y verifique fase por fase."],
    "prensa": ["Nombre A = plataforma 3 y B = plataforma 4. Escriba la secuencia y el espacio-fase.",
               "¿Cómo combina pedal, pulsador y la condición «plataforma 4 en posición inicial»?",
               "a0 ordena B− y está pisado en reposo: ¿qué problema genera al ordenar B+?",
               "Forme los grupos. ¿Qué señal cambia del grupo I al II?",
               "¿Cómo logra salida lenta y retorno rápido?"],
    "estampado": ["Escriba la secuencia y el diagrama espacio-fase de A, B y C.",
                  "Forme los grupos. ¿Puede unir el último grupo con el primero? ¿Por qué?",
                  "¿Qué señales disparan el arranque y C+?",
                  "Selectores D, E, F sin finales de carrera: ¿qué válvula usa para que el selector "
                  "salga mientras se pulsa y vuelva al soltar?",
                  "Dibuje dos esquemas: estación de estampado (A, B, C) y faja (D, E, F)."],
}


# =====================================================================
# Símbolos
# =====================================================================
def catalogo_simbolos(doc, numero="", claves=None, titulo="Catálogo de símbolos"):
    """Tabla con imagen, nombre/designación, cómo reconocerlo y función."""
    doc.add_heading(numero + titulo, 1)
    para(doc, "Cómo leer una válvula: cada cuadro es una posición; se cuentan los PUERTOS (vías) de "
              "un cuadro y los CUADROS (posiciones) → «3/2» = 3 vías, 2 posiciones. Los puertos se "
              "dibujan solo en el cuadro de reposo. El accionamiento dibujado a un lado lleva la "
              "válvula al cuadro de ese lado. Numeración: 1 presión, 2 y 4 salidas, 3 y 5 escapes, "
              "12 y 14 pilotajes (14 conecta 1 → 4).")
    rows = []
    for k in claves or ORDEN:
        c = CATALOGO[k]
        rows.append([c["img"],
                     [(c["nombre"], {"bold": True, "color": NAVY}), ("\n" + c["designacion"], {})],
                     c["reconocer"], c["funcion"]])
    image_table(doc, ["Símbolo", "Nombre y designación", "Cómo reconocerlo", "Para qué sirve"],
                rows, [3.4, 4.0, 5.6, 4.0], img_w_cm=3.1)
    para(doc, [("Los tres últimos (simple efecto, 5/2 monoestable y rodillo escamoteable) se ven en "
                "teoría pero no son necesarios para resolver las PD 10 y 11.",
                {"italic": True, "color": MUTED})], size=9)


def simbolos_ejercicio(doc, simb, land=False):
    """Tabla por ejercicio: símbolo, nombre, cantidad, referencias en el esquema, función."""
    rows = []
    for k, n, ref, rol in simb:
        c = CATALOGO[k]
        rows.append([c["img"], [(c["nombre"], {"bold": True, "color": NAVY}),
                                ("\n" + c["designacion"], {})],
                     str(n), ref, rol])
    w = [3.0, 6.2, 1.2, 2.8, 5.2] if not land else [3.2, 8.5, 1.4, 4.2, 8.6]
    image_table(doc, ["Símbolo", "Nombre y designación", "Cant.", "Ref. en el esquema",
                      "Función en este circuito"], rows, w, img_w_cm=2.7)


# =====================================================================
# 1. Guía del alumno
# =====================================================================
def guia():
    doc = new_doc("Guía de práctica dirigida", "Representación neumática con FluidSim · Sesión 2 (3 h)")
    doc.add_heading("1. Objetivos y entregables", 1)
    bullets(doc, ["Representar circuitos neumáticos con símbolos ISO 1219, en posición de reposo y "
                  "por niveles.",
                  "Describir secuencias con notación A+ B+ … y con el diagrama espacio-fase.",
                  "Detectar señales bloqueadas y resolverlas con el método cascada.",
                  "Construir y simular cada circuito en FluidSim."])
    para(doc, [("Entregable por ejercicio: ", {"bold": True, "color": NAVY}),
               ("secuencia, diagrama espacio-fase, archivo de FluidSim y una captura de la "
                "simulación funcionando.", {})])

    doc.add_heading("2. Repaso express", 1)
    doc.add_heading("Numeración de puertos", 3)
    table(doc, [["Puerto", "Función", "Puerto", "Función"],
                ["1", "Alimentación (presión)", "12", "Pilotaje que conecta 1 → 2"],
                ["2, 4", "Utilización (salidas)", "14", "Pilotaje que conecta 1 → 4"],
                ["3, 5", "Escape", "X/Y", "N.º de vías / N.º de posiciones"]],
          [1.6, 5.0, 1.6, 5.8])
    catalogo_simbolos(doc, titulo="Símbolos que usarás")
    doc.add_heading("Reglas de dibujo", 3)
    numbered(doc, ["Por niveles: actuadores arriba, válvulas de potencia al medio, señales abajo.",
                   "Todo en reposo: cilindros retraídos; los finales de carrera pisados en reposo "
                   "(a0, b0…) se dibujan accionados.",
                   "Nombres: cilindros A, B, C; válvulas VA, VB; finales de carrera a0/a1 marcados "
                   "también sobre el vástago.",
                   "Líneas continuas = potencia; discontinuas = pilotaje/señal. Punto = unión.",
                   "Velocidad: estrangular el ESCAPE (meter-out); antirretorno con paso libre hacia "
                   "el cilindro."])
    doc.add_heading("Método cascada en 7 pasos", 3)
    numbered(doc, ["Escriba la secuencia y córtela en grupos donde ninguna letra se repita.",
                   "N.º de válvulas selectoras de grupo = n.º de grupos − 1 (2 grupos → 1 VG 5/2 "
                   "biestable).",
                   "Cada grupo es una línea de alimentación; solo una tiene aire a la vez.",
                   "El primer movimiento de cada grupo se pilota directamente desde su línea.",
                   "Los siguientes los dispara el final de carrera anterior, alimentado desde la línea.",
                   "El último final de carrera del grupo conmuta VG al grupo siguiente.",
                   "El arranque S va en la línea activa en reposo, en serie con las condiciones de "
                   "inicio."])
    figure(doc, "t_cascada_ABBA", 13.5, "Ejemplo de cascada para A+ B+ | B− A−.")

    doc.add_heading("3. FluidSim en 20 minutos", 1)
    para(doc, [("Los nombres de los menús pueden variar ligeramente según la versión.",
                {"italic": True, "color": MUTED})], size=9)
    numbered(doc, ["Archivo → Nuevo. Abra la biblioteca de componentes neumáticos.",
                   "Arrastre un cilindro de doble efecto, una válvula configurable, fuentes de aire y "
                   "la unidad de mantenimiento.",
                   "Doble clic en la válvula: elija 3/2, 4/2 o 5/2 y el accionamiento de cada lado "
                   "(pulsador, rodillo, piloto, resorte).",
                   "Conecte arrastrando desde un puerto a otro; verifique el punto de unión.",
                   "Finales de carrera: defina marcas en el cilindro (a0, a1) y escriba la MISMA "
                   "etiqueta en la válvula de rodillo.",
                   "Inicie la simulación y haga clic en los pulsadores. Las líneas con presión cambian "
                   "de color.",
                   "Agregue un diagrama de estado y compárelo con su diagrama espacio-fase."])

    doc.add_heading("4. Calentamiento (20 min)", 1)
    bullets(doc, [[("C1 · Mando indirecto con memoria. ", {"bold": True}),
                   ("Un cilindro de doble efecto sale con S1 y entra con S2 (5/2 biestable).", {})],
                  [("C2 · Retorno automático. ", {"bold": True}),
                   ("S1 hace salir el cilindro; al llegar a a1 regresa solo. Pruebe mantener S1 "
                    "pulsado y explique lo que ocurre.", {})],
                  [("C3 · Velocidad. ", {"bold": True}),
                   ("Haga que solo el avance de C2 sea lento.", {})]])

    for key, sec in (("cuchara", "5"), ("puerta", None), ("doblado", "6"), ("prensa", None),
                     ("estampado", None)):
        if sec == "5":
            page_break(doc)
            doc.add_heading("5. Práctica dirigida 10", 1)
        if sec == "6":
            page_break(doc)
            doc.add_heading("6. Práctica dirigida 11 (método cascada)", 1)
        title, txt, img = ENUNCIADOS[key]
        doc.add_heading(title, 2)
        para(doc, txt)
        if img:
            figure(doc, img, {"cuchara": 6.0, "doblado": 7.0, "prensa": 5.0}.get(key, 11.0))
        doc.add_heading("Preguntas guía", 3)
        numbered(doc, PREGUNTAS[key])
        answer_box(doc, "Secuencia y diagrama espacio-fase", 7)

    doc.add_heading("7. Lista de verificación", 1)
    table(doc, [["✓", "Criterio"],
                ["☐", "Secuencia escrita y diagrama espacio-fase con las señales"],
                ["☐", "Esquema por niveles y en posición de reposo"],
                ["☐", "Nombres A, B, C; VA, VB; a0, a1… también sobre el cilindro"],
                ["☐", "Válvulas de potencia adecuadas (memoria donde hay pulsos)"],
                ["☐", "Reguladoras en el lugar y sentido correctos"],
                ["☐", "Señales bloqueadas resueltas"],
                ["☐", "Condiciones de arranque y seguridad cumplidas"],
                ["☐", "Simulación verificada fase por fase"]], [1.2, 15.8])
    path = os.path.join(D_ALUM, "RGIM_Guia_Practica_Dirigida_Alumno.docx")
    doc.save(path)
    return path


# =====================================================================
# 2. Solucionario docente
# =====================================================================
SOL = [
    dict(key="cuchara", title="PD 10 · Ej. 2 — Cuchara de fundición", seq="A+ A−",
         circuit="e1_2_cuchara", phase="fase_e1_2", width=15.0, land=False,
         analisis=["Un cilindro de doble efecto A (cuchara). Reposo: retraído (posición inicial).",
                   "Válvula de potencia VA 4/2 biestable (pulso/pulso): memoriza la orden.",
                   "S1 (3/2 NC, pulsador) → VA 14: A+. Rodillo a1 (3/2 NC) → VA 12: A−.",
                   "Baja velocidad en ambos sentidos: R1 y R2 meter-out (antirretorno con paso libre "
                   "hacia el cilindro)."],
         simb=[("cil_de", 1, "A", "Mueve la cuchara"),
               ("v42_bi", 1, "VA", "Potencia con memoria (pulso/pulso)"),
               ("v32_boton", 1, "S1", "Orden de inicio (A+) desde el puesto del operador"),
               ("v32_rodillo", 1, "a1", "Detecta el final de carrera y ordena A−"),
               ("reguladora", 2, "R1, R2", "Baja velocidad en ambos sentidos (meter-out)"),
               ("fuente", 3, "—", "Alimentación de VA, S1 y a1"),
               ("escape", 2, "—", "Escapes 3 de las válvulas de señal")],
         con=[["VA:4", "R1 → A (cámara posterior)"], ["VA:2", "R2 → A (lado vástago)"],
              ["S1:2", "VA:14"], ["a1:2", "VA:12"], ["VA:1, S1:1, a1:1", "Alimentación"],
              ["Marca a1", "Final de carrera de A (carrera máxima)"]],
         errores=["Antirretorno invertido: frena el movimiento contrario.",
                  "Si S1 se mantiene pulsado al llegar a a1, VA recibe 14 y 12 y no retrocede "
                  "(señal bloqueada). Solución: rodillo escamoteable o pulsar brevemente."]),
    dict(key="puerta", title="PD 10 · Ej. 1 — Puerta de garaje", seq="A+ (abrir) / A− (cerrar), "
         "un mismo botón conmuta", circuit="e1_1_puerta_conmutada", phase=None, width=11.5, land=False,
         analisis=["A+ = abrir, A− = cerrar. Inicio con la puerta cerrada → cilindro retraído; a0 "
                   "accionado en reposo.",
                   "Dos lugares de mando: S1 (interior) O S2 (exterior) → válvula selectora.",
                   "Un mismo botón abre y cierra: la orden depende de la posición de la puerta. La "
                   "salida de la O alimenta a a0 y a1: con la puerta cerrada pasa por a0 → 14 (abre); "
                   "con la puerta abierta pasa por a1 → 12 (cierra). Es una Y en serie.",
                   "VA 5/2 biestable = memoria: la puerta queda abierta al soltar el botón.",
                   "Cierre lento: R1 en la cámara posterior (es la cámara que se vacía al cerrar), "
                   "antirretorno con paso libre hacia el cilindro."],
         simb=[("cil_de", 1, "A", "Mueve la puerta (A+ abre, A− cierra)"),
               ("v52_bi", 1, "VA", "Potencia con memoria: la puerta queda abierta o cerrada"),
               ("v32_boton", 2, "S1, S2", "Botón interior y exterior"),
               ("or", 1, "O", "Cualquiera de los dos botones da la orden"),
               ("v32_rodillo_acc", 1, "a0", "Puerta cerrada: dirige la orden a 14 (abrir)"),
               ("v32_rodillo", 1, "a1", "Puerta abierta: dirige la orden a 12 (cerrar)"),
               ("reguladora", 1, "R1", "Limita solo la velocidad de cierre"),
               ("fuente", 3, "—", "Alimentación de VA, S1 y S2")],
         con=[["VA:4", "R1 → A (cámara posterior)"], ["VA:2", "A (lado vástago)"],
              ["S1:2, S2:2", "Entradas 1 de la selectora O"], ["O:2", "a0:1 y a1:1"],
              ["a0:2", "VA:14 (abrir)"], ["a1:2", "VA:12 (cerrar)"]],
         errores=["Limitación: si se mantiene el botón, al llegar a a1 la puerta vuelve a cerrar "
                  "(oscila). A mitad de carrera el botón no actúa.",
                  "Variante aceptable (botonera de 4 pulsadores): S1 O S2 → 14 y S3 O S4 → 12 "
                  "(figura siguiente)."],
         extra="e1_1_puerta_botonera"),
    dict(key="doblado", title="PD 11 · Ej. 2 — Dobladora de chapa", seq="A+ B+ C+ (A− B− C−)",
         circuit="e2_2_doblado", phase="fase_e2_2", width=21.5, land=True,
         analisis=["Señales bloqueadas: a1 manda B+ y sigue activa cuando se ordena B−; b1 igual "
                   "con C. → método cascada.",
                   "Grupos: I = A+ B+ C+ ; II = (A− B− C−). 2 grupos → 1 válvula VG 5/2 biestable.",
                   "Reposo: línea II con aire (salida 2 de VG).",
                   "Arranque: línea II → a0 → b0 → c0 → S → VG 14 (solo si el ciclo terminó).",
                   "Lento: reguladoras meter-out en el lado vástago de A, B y C."],
         simb=[("cil_de", 3, "A, B, C", "Sujeción, primer y segundo doblado"),
               ("v52_bi", 4, "VA, VB, VC, VG", "Potencia de cada cilindro + selectora de grupo VG"),
               ("v32_boton", 1, "S", "Pulsador de inicio (alejado)"),
               ("v32_rodillo_acc", 3, "a0, b0, c0", "En serie con S: solo arranca si el ciclo terminó"),
               ("v32_rodillo", 3, "a1, b1, c1", "Disparan B+, C+ y el cambio al grupo II"),
               ("reguladora", 3, "RA2, RB2, RC2", "Sujeción y doblado lentos (meter-out)"),
               ("lineas", 2, "Línea I, II", "Líneas de grupo de la cascada"),
               ("fuente", 4, "—", "Alimentación de VA, VB, VC y VG")],
         con=[["VX:4 / VX:2", "Cámara posterior / reguladora → lado vástago (X = A, B, C)"],
              ["VG:4", "Línea I"], ["VG:2", "Línea II (activa en reposo)"],
              ["Línea II", "VA:12, VB:12, VC:12 y a0:1"],
              ["a0:2 → b0:1 → b0:2 → c0:1 → c0:2 → S:1", "Serie (Y) de arranque"],
              ["S:2", "VG:14"], ["Línea I", "VA:14, a1:1, b1:1, c1:1"],
              ["a1:2 / b1:2 / c1:2", "VB:14 / VC:14 / VG:12"]],
         errores=["Alimentar los rodillos desde la fuente y no desde la línea: reaparecen los bloqueos.",
                  "Dibujar a0, b0, c0 sin accionar.",
                  "Olvidar la serie a0 · b0 · c0 en el arranque (requisito «solo si el ciclo terminó»)."]),
    dict(key="prensa", title="PD 11 · Ej. 3 — Prensa de bandejas", seq="(A+ B+) A− B−",
         circuit="e2_3_prensa", phase="fase_e2_3", width=19.0, land=True,
         analisis=["A = plataforma 3, B = plataforma 4.",
                   "Bloqueo: a0 manda B− y está pisado en reposo cuando se ordena B+ → cascada.",
                   "Grupos: I = (A+ B+) ; II = A− B−. 1 válvula VG. Reposo: línea II.",
                   "Arranque: (pedal P O pulsador S) · b0 → VG 14. P y S se alimentan de la línea II.",
                   "Cambio I → II: a1 · b1 en serie → VG 12. En II: A− directo; a0 → B−.",
                   "Salida lenta: meter-out en el lado vástago. Retorno rápido: sin estrangulación "
                   "(opcional: válvula de escape rápido en la cámara posterior)."],
         simb=[("cil_de", 2, "A, B", "Plataforma 3 (A) y plataforma 4 (B)"),
               ("v52_bi", 3, "VA, VB, VG", "Potencia de cada plataforma + selectora de grupo"),
               ("v32_pedal", 1, "P", "Mando con el pie"),
               ("v32_boton", 1, "S", "Mando con la mano"),
               ("or", 1, "O", "Pedal O pulsador"),
               ("v32_rodillo_acc", 2, "a0, b0", "b0: condición de inicio; a0: ordena B−"),
               ("v32_rodillo", 2, "a1, b1", "En serie: ambas plataformas llegaron → grupo II"),
               ("reguladora", 2, "RA2, RB2", "Salida lenta; el retorno queda libre (rápido)"),
               ("lineas", 2, "Línea I, II", "Líneas de grupo de la cascada"),
               ("fuente", 3, "—", "Alimentación de VA, VB y VG")],
         con=[["VG:4 / VG:2", "Línea I / Línea II (activa en reposo)"],
              ["Línea II", "P:1, S:1, VA:12, a0:1"], ["P:2, S:2", "Entradas de O"],
              ["O:2 → b0:1 ; b0:2", "VG:14"], ["Línea I", "VA:14, VB:14, a1:1"],
              ["a1:2 → b1:1 ; b1:2", "VG:12"], ["a0:2", "VB:12"]],
         errores=["Olvidar b0 en el arranque (condición de seguridad del enunciado).",
                  "Estrangular también el retorno (el enunciado pide retorno rápido)."]),
    dict(key="estampado", title="PD 11 · Ej. 1 — Estampado y selección", seq="A+ B+ (A− B−) C+ C−",
         circuit="e2_1_estampado_ABC", phase="fase_e2_1", width=22.0, land=True,
         analisis=["Grupos sin fusionar: A+ B+ | (A− B−) C+ | C− (3 grupos, 2 VG).",
                   "El último grupo (C−) no repite letras con el primero → se fusionan: "
                   "I = C− A+ B+ ; II = (A− B−) C+. Basta 1 VG.",
                   "Reposo: línea I con aire (C− asegurado). Arranque: línea I → c0 → S → VA 14.",
                   "a1 → B+ ; b1 → VG 14 (pasa a II). En II: A− y B− directos; a0 · b0 → C+ ; "
                   "c1 → VG 12 (vuelve a I, C−).",
                   "Selectores D, E, F: circuitos independientes con 5/2 pulsador/resorte (sale "
                   "mientras se pulsa)."],
         simb=[("cil_de", 6, "A, B, C, D, E, F", "Fijación, estampado, entrega y 3 selectores"),
               ("v52_bi", 4, "VA, VB, VC, VG", "Potencia de A, B, C + selectora de grupo"),
               ("v52_boton", 3, "SD, SE, SF", "Selectores: salen mientras se pulsa"),
               ("v32_boton", 1, "S", "«Iniciar estampado»"),
               ("v32_rodillo_acc", 3, "a0, b0, c0", "c0: condición de inicio; a0 · b0: ordenan C+"),
               ("v32_rodillo", 3, "a1, b1, c1", "Disparan B+, el paso a II y el regreso a I"),
               ("lineas", 2, "Línea I, II", "Líneas de grupo de la cascada"),
               ("fuente", 7, "—", "Alimentación de VA, VB, VC, VG, SD, SE y SF")],
         con=[["VG:2 / VG:4", "Línea I (activa en reposo) / Línea II"],
              ["Línea I", "VC:12, c0:1, a1:1, b1:1"], ["c0:2 → S:1 ; S:2", "VA:14"],
              ["a1:2", "VB:14"], ["b1:2", "VG:14"], ["Línea II", "VA:12, VB:12, a0:1, c1:1"],
              ["a0:2 → b0:1 ; b0:2", "VC:14"], ["c1:2", "VG:12"],
              ["SX:4 / SX:2", "Cámara posterior / lado vástago de X (X = D, E, F)"]],
         errores=["En FluidSim, VG debe arrancar con la salida 2 activa (línea I); si no, el primer "
                  "C− no se asegura.",
                  "Si el grupo no fusiona, la solución con 3 grupos y 2 VG también es correcta."],
         extra="e2_1_selectores_DEF"),
]


def solucionario():
    doc = new_doc("Solucionario docente", "Prácticas dirigidas 10 y 11 · Representación neumática",
                  kicker="REPRESENTACIÓN GRÁFICA PARA INGENIERÍA MECATRÓNICA · USO DOCENTE")
    para(doc, "La sección 0 es el catálogo de los símbolos que aparecen en las soluciones: nombre, "
              "designación, cómo reconocerlos y para qué sirven. Luego, cada solución incluye el "
              "esquema en posición de reposo, el diagrama espacio-fase, el análisis, la tabla de "
              "símbolos que necesita (con cantidades y referencias) y la lista de conexiones para "
              "armarlo en el simulador. Las figuras están en la carpeta figuras/ en PNG y SVG.")
    callout(doc, "Convenciones:", "VX:n = puerto n de la válvula VX; a0/a1 = finales de carrera "
                                  "(válvulas 3/2 NC de rodillo); línea I/II = líneas de grupo de la "
                                  "cascada; líneas discontinuas = pilotaje.")
    catalogo_simbolos(doc, numero="0. ")
    first = False
    prev_land = False
    for s in SOL:
        if s["land"]:
            landscape(doc)
        elif not first:
            portrait(doc) if prev_land else page_break(doc)
        first = False
        prev_land = s["land"]
        doc.add_heading(s["title"], 1)
        para(doc, [("Secuencia: ", {"bold": True, "color": NAVY}), (s["seq"], {"bold": True})])
        if s["land"]:
            figure(doc, s["circuit"], s["width"])
            if s["phase"]:
                figure(doc, s["phase"], 12.0)
        else:
            figure(doc, s["circuit"], s["width"])
            if s["phase"]:
                figure(doc, s["phase"], 8.0)
        doc.add_heading("Análisis", 3)
        bullets(doc, s["analisis"])
        doc.add_heading("Símbolos que necesitas", 3)
        simbolos_ejercicio(doc, s["simb"], s["land"])
        doc.add_heading("Conexiones (para armar en FluidSim)", 3)
        table(doc, [["Desde", "Hacia"]] + s["con"], [7, 10] if not s["land"] else [10, 14])
        doc.add_heading("Errores típicos y variantes", 3)
        bullets(doc, s["errores"])
        if s.get("extra"):
            figure(doc, s["extra"], 11.0 if not s["land"] else 20.0,
                   "Variante / complemento" if s["key"] == "puerta" else "Selectores D, E, F")
    path = os.path.join(D_DOC, "RGIM_Solucionario_Docente.docx")
    doc.save(path)
    return path


# =====================================================================
# 3. Plan de sesiones
# =====================================================================
def plan():
    doc = new_doc("Plan de sesiones", "Semana de representación neumática · 2 h teoría + 3 h práctica",
                  kicker="REPRESENTACIÓN GRÁFICA PARA INGENIERÍA MECATRÓNICA · USO DOCENTE")
    doc.add_heading("Criterio de selección del contenido", 1)
    para(doc, "Las clases de KU Leuven (Mechanical Drive Systems, D. Reynaerts) cubren neumática con "
              "profundidad de curso completo. Para una sola semana centrada en REPRESENTACIÓN se "
              "conservó lo que los alumnos necesitan para resolver las PD 10 y 11, y se dejó el resto "
              "como referencia.")
    table(doc, [["Tema (KU Leuven)", "Decisión", "Motivo"],
                ["Símbolos de válvulas, X/Y, accionamientos", "Se ve", "Base de la representación"],
                ["Válvula selectora (O), reguladora de caudal", "Se ve", "Aparecen en los enunciados"],
                ["Control direccional y de velocidad (meter-in/out)", "Se ve", "Enunciados piden "
                                                                               "velocidad limitada"],
                ["Mando por pilotaje, mono/biestable, memoria", "Se ve", "Mando a distancia, pulsos"],
                ["Secuencias, diagrama, señales bloqueadas", "Se ve", "Núcleo de la PD 11"],
                ["Método cascada (selector de grupo)", "Se ve", "Solución sistemática"],
                ["Rodillo escamoteable, temporizadores", "Se menciona", "Alternativas al bloqueo"],
                ["Termodinámica, consumo, Kv, flujo crítico", "No se ve", "Dimensionamiento, no "
                                                                         "representación"],
                ["Válvulas de asiento vs. corredera", "No se ve", "Detalle constructivo"],
                ["Karnaugh, electroneumática, PLC, Grafcet", "No se ve", "Automatización (otro curso)"],
                ["Hidroneumática, servoneumática, buses", "No se ve", "Fuera de alcance"]],
          [6.6, 2.4, 8.0])

    doc.add_heading("Sesión 1 · Teoría (120 min)", 1)
    para(doc, [("Archivo: ", {"bold": True}),
               ("sesion1_teoria/RGIM_S1_Representacion_Neumatica_Teoria.pptx (30 diapositivas, notas "
                "del orador con tiempos y preguntas).", {})])
    table(doc, [["Min.", "Bloque", "Diapos.", "Actividad"],
                ["0–10", "Apertura y motivación", "1–5", "Objetivos, agenda, por qué neumática, "
                                                         "cadena de energía"],
                ["10–40", "1 · Símbolos ISO 1219", "6–12", "Cilindros, lectura de válvulas, "
                                                           "numeración, accionamientos, memoria, "
                                                           "O / Y / reguladora"],
                ["40–70", "2 · Circuitos básicos", "13–19", "Reglas de dibujo, mando directo e "
                                                            "indirecto, meter-out, lógica, final de "
                                                            "carrera. Pregunta gancho: botón "
                                                            "mantenido"],
                ["70–110", "3 · Secuencias y cascada", "20–27", "Notación, espacio-fase, A+B+A−B−, "
                                                                "bloqueo en A+B+B−A−, receta y circuito "
                                                                "de cascada, ejercicio de agrupación"],
                ["110–120", "Cierre", "28–30", "Metodología del enunciado al circuito, resumen"]],
          [1.6, 3.8, 1.8, 9.8])
    callout(doc, "Actividad en clase:", "en la diapositiva 27 los alumnos agrupan las secuencias de la "
                                        "PD 11 (respuestas en las notas del orador). Es el puente "
                                        "directo con la práctica.")

    doc.add_heading("Sesión 2 · Práctica dirigida (180 min)", 1)
    para(doc, [("Archivos: ", {"bold": True}),
               ("sesion2_practica/RGIM_S2_Practica_Dirigida_FluidSim.pptx (soluciones como "
                "diapositivas ocultas) y RGIM_Guia_Practica_Dirigida_Alumno.docx.", {})])
    table(doc, [["Min.", "Actividad", "Modalidad", "Producto"],
                ["0–20", "FluidSim en 20 minutos (demo en vivo)", "Docente demuestra, alumnos replican",
                 "Cilindro + 5/2"],
                ["20–40", "Calentamiento C1, C2, C3", "Individual", "Memoria y final de carrera"],
                ["40–60", "PD 10 · Ej. 2 Cuchara", "Parejas, 10' autónomo + 10' puesta en común",
                 "Circuito simulado"],
                ["60–90", "PD 10 · Ej. 1 Puerta", "Parejas + discusión de interpretación",
                 "Circuito simulado"],
                ["90–100", "Pausa", "—", "—"],
                ["100–125", "PD 11 · Ej. 2 Dobladora", "Guiado paso a paso (cascada)", "Cascada 2 grupos"],
                ["125–145", "PD 11 · Ej. 3 Prensa", "Parejas", "Cascada con O / Y"],
                ["145–170", "PD 11 · Ej. 1 Estampado", "Parejas (reto)", "Fusión de grupos"],
                ["170–180", "Errores frecuentes y cierre", "Plenario", "Lista de verificación"]],
          [1.7, 5.0, 5.6, 4.7])
    doc.add_heading("Si falta tiempo", 3)
    bullets(doc, ["Dejar el estampado como tarea y publicar la solución después.",
                  "En la puerta, aceptar directamente la variante de botonera (4 pulsadores).",
                  "Mostrar la solución de la cuchara tras 10 minutos para no perder ritmo."])

    doc.add_heading("Preparación previa", 1)
    bullets(doc, ["Verificar licencias/instalación de FluidSim en el laboratorio (versión y biblioteca "
                  "neumática).",
                  "Probar en FluidSim los circuitos del solucionario (las tablas de conexiones están "
                  "pensadas para armarlos en pocos minutos).",
                  "Revisar que las diapositivas de solución sigan ocultas antes de proyectar.",
                  "Imprimir o compartir la guía del alumno."])
    doc.add_heading("Evaluación sugerida", 1)
    para(doc, "Usar la lista de verificación de la guía como rúbrica (8 criterios, 1 punto c/u) sobre "
              "uno de los ejercicios de la PD 11, más 2 puntos por la simulación funcionando.")
    path = os.path.join(D_DOC, "RGIM_Plan_de_Sesiones.docx")
    doc.save(path)
    return path


if __name__ == "__main__":
    for f in (guia(), solucionario(), plan()):
        print("ok", f)
