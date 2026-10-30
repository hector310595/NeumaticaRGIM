"""Guía paso a paso para armar y simular las soluciones en FluidSIM (.docx).
Uso: python3 src/build_fluidsim.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from docx_utils import (MUTED, RED, ROOT, bullets, callout, figure, landscape,  # noqa: E402
                        new_doc, numbered, page_break, para, portrait, table)

OUT = os.path.join(ROOT, "docente", "RGIM_Guia_FluidSim_Paso_a_Paso.docx")

# ------------------------------------------------------------------ recetas
# (nombre en la biblioteca, configuración con doble clic)
CIL = ("Cilindro de doble efecto",
       "Dejar la carrera por defecto (p. ej. 100 mm). Debe empezar retraído.")
V32P = ("Válvula de 3/n vías (configurable)",
        "Cuerpo: 3/2 normalmente cerrada. Izquierda: accionamiento manual → pulsador. "
        "Derecha: resorte. Posición inicial: la del resorte.")
V32PED = ("Válvula de 3/n vías (configurable)",
          "Cuerpo: 3/2 NC. Izquierda: accionamiento manual → pedal. Derecha: resorte.")


def V32R(lab):
    return ("Válvula de 3/n vías (configurable)",
            "Cuerpo: 3/2 NC. Izquierda: accionamiento mecánico → rodillo. Derecha: resorte. "
            "Etiqueta / marca: %s." % lab)


V52BI = ("Válvula de 5/n vías (configurable)",
         "Cuerpo: 5/2. Izquierda: pilotaje neumático (14). Derecha: pilotaje neumático (12). "
         "Sin resorte. Posición inicial: derecha (1 → 2).")
V42BI = ("Válvula de 4/n vías (configurable)",
         "Cuerpo: 4/2. Izquierda y derecha: pilotaje neumático (14 y 12). Sin resorte. "
         "Posición inicial: derecha (1 → 2). Si tu versión no tiene 4/n, usa una 5/n igual.")
V52P = ("Válvula de 5/n vías (configurable)",
        "Cuerpo: 5/2. Izquierda: accionamiento manual → pulsador. Derecha: resorte.")
OR = ("Válvula selectora (O)", "No requiere configuración.")
REG = ("Válvula de estrangulación y antirretorno",
       "Apertura ≈ 50 % para empezar (ajústala hasta ver el movimiento lento). Orientación: el "
       "antirretorno deja pasar libre HACIA el cilindro.")
SRC = ("Fuente de aire comprimido", "Una en cada puerto 1 que diga «fuente» en las conexiones.")

# ------------------------------------------------------------------ ejercicios
EJ = [
    dict(
        titulo="PD 10 · Ej. 2 — Cuchara de fundición (A+ A−)", fig="e1_2_cuchara", land=False,
        comps=[("A", CIL), ("VA", V42BI), ("S1", V32P), ("a1", V32R("a1")),
               ("R1, R2", REG), ("3 ×", SRC)],
        marcas=[("A", "a1", "final de la carrera (p. ej. 100 mm)")],
        conex=["VA:4 → R1 → conexión izquierda de A (cámara posterior).",
               "VA:2 → R2 → conexión derecha de A (lado vástago).",
               "Fuente → VA:1; fuente → S1:1; fuente → a1:1.",
               "S1:2 → pilotaje izquierdo de VA (14).",
               "a1:2 → pilotaje derecho de VA (12)."],
        prueba=["Iniciar (F9). A está retraído; la línea VA:2 → R2 → A tiene presión.",
                "Clic en S1: A sale lento.",
                "Al llegar a a1: A regresa solo, también lento.",
                "Mantén apretado S1 (sin soltar el ratón) hasta que A llegue a a1: A se queda "
                "afuera. Es la señal bloqueada que se discute en clase."],
        fallos=["A no regresa: la etiqueta del rodillo no coincide con la marca a1 del cilindro.",
                "Un movimiento es rápido: esa reguladora está invertida (gírala)."]),
    dict(
        titulo="PD 10 · Ej. 1 — Puerta de garaje (botón conmutado)", fig="e1_1_puerta_conmutada",
        land=False,
        comps=[("A", CIL), ("VA", V52BI), ("S1, S2", V32P), ("O", OR),
               ("a0", V32R("a0")), ("a1", V32R("a1")), ("R1", REG), ("3 ×", SRC)],
        marcas=[("A", "a0", "inicio de la carrera (0 mm)"), ("A", "a1", "final de la carrera")],
        conex=["VA:4 → R1 → conexión izquierda de A. VA:2 → conexión derecha de A.",
               "Fuente → VA:1, S1:1 y S2:1.",
               "S1:2 → entrada izquierda de O; S2:2 → entrada derecha de O.",
               "Salida de O → a0:1. Desde a0:1 arrastra otra línea hasta a1:1 (o suelta la "
               "línea sobre la existente para crear la unión en T).",
               "a0:2 → pilotaje 14 de VA (abrir). a1:2 → pilotaje 12 de VA (cerrar)."],
        prueba=["F9: la puerta (A) está cerrada y el rodillo a0 aparece accionado.",
                "Clic en S1: A sale (abre) a velocidad normal.",
                "Clic otra vez en S1 (o en S2): A regresa (cierra) lento.",
                "Pulsa S2 a mitad del recorrido: no pasa nada (comportamiento esperado)."],
        fallos=["a0 no aparece accionado al iniciar: la marca a0 no está en 0 mm.",
                "El cierre no es lento: R1 está en la línea equivocada o invertida; debe frenar "
                "el aire que SALE de la cámara posterior."]),
    dict(
        titulo="PD 11 · Ej. 2 — Dobladora: A+ B+ C+ (A− B− C−)", fig="e2_2_doblado", land=True,
        comps=[("A, B, C", CIL), ("VA, VB, VC", V52BI), ("VG", V52BI), ("S", V32P),
               ("a0, b0, c0", V32R("a0 / b0 / c0")), ("a1, b1, c1", V32R("a1 / b1 / c1")),
               ("RA2, RB2, RC2", REG), ("4 ×", SRC)],
        marcas=[("A", "a0 · a1", "0 mm · final"), ("B", "b0 · b1", "0 mm · final"),
                ("C", "c0 · c1", "0 mm · final")],
        conex=["Potencia: VX:4 → cámara posterior de X; VX:2 → RX2 → lado vástago de X "
               "(X = A, B, C). Fuente en VA:1, VB:1, VC:1 y VG:1.",
               "Línea II (activa en reposo): VG:2 → pilotaje 12 de VA. Luego suelta líneas "
               "desde VB:12, VC:12 y a0:1 sobre esa línea para crear las uniones en T.",
               "Línea I: VG:4 → pilotaje 14 de VA. Luego une a1:1, b1:1 y c1:1 a esa línea.",
               "Arranque en serie: a0:2 → b0:1; b0:2 → c0:1; c0:2 → S:1; S:2 → pilotaje 14 de VG.",
               "a1:2 → VB:14.  b1:2 → VC:14.  c1:2 → pilotaje 12 de VG."],
        prueba=["F9: A, B y C retraídos; a0, b0 y c0 accionados; la línea II con presión.",
                "Clic en S: VG conmuta a la línea I y A sale lento.",
                "A llega a a1 → B sale lento; B llega a b1 → C sale lento.",
                "C llega a c1 → VG vuelve a la línea II → A, B y C regresan juntos.",
                "Pulsa S mientras el ciclo está en marcha: no debe pasar nada."],
        fallos=["B retrocede y vuelve a salir: a1 está alimentada desde una fuente y no desde la "
                "línea I.",
                "S no arranca: una de las marcas a0, b0, c0 no está en 0 mm o la serie está "
                "mal conectada.",
                "Todo empieza en el grupo equivocado: posición inicial de VG distinta de derecha."]),
    dict(
        titulo="PD 11 · Ej. 3 — Prensa: (A+ B+) A− B−", fig="e2_3_prensa", land=True,
        comps=[("A, B", CIL), ("VA, VB, VG", V52BI), ("P", V32PED), ("S", V32P), ("O", OR),
               ("a0, b0", V32R("a0 / b0")), ("a1, b1", V32R("a1 / b1")), ("RA2, RB2", REG),
               ("3 ×", SRC)],
        marcas=[("A", "a0 · a1", "0 mm · final"), ("B", "b0 · b1", "0 mm · final")],
        conex=["Potencia: VX:4 → cámara posterior; VX:2 → RX2 → lado vástago (X = A, B). "
               "Fuente en VA:1, VB:1 y VG:1.",
               "Línea II (activa en reposo): VG:2 → VA:12; une a esa línea P:1, S:1 y a0:1.",
               "Línea I: VG:4 → VA:14; une a esa línea VB:14 y a1:1.",
               "P:2 → entrada izquierda de O; S:2 → entrada derecha de O; salida de O → b0:1; "
               "b0:2 → pilotaje 14 de VG.",
               "a1:2 → b1:1; b1:2 → pilotaje 12 de VG.",
               "a0:2 → VB:12."],
        prueba=["F9: A y B retraídos; a0 y b0 accionados.",
                "Clic en P (o en S): A y B salen juntos, lentos.",
                "Cuando ambos llegan (a1 y b1): A regresa rápido.",
                "A llega a a0: B regresa rápido. El ciclo termina."],
        fallos=["B no sale al inicio: a0 está alimentada desde una fuente (debe ser línea II).",
                "El retorno es lento: la reguladora está invertida."]),
    dict(
        titulo="PD 11 · Ej. 1 — Estampado: A+ B+ (A− B−) C+ C−", fig="e2_1_estampado_ABC",
        land=True,
        comps=[("A, B, C", CIL), ("VA, VB, VC, VG", V52BI), ("S", V32P),
               ("a0, b0, c0", V32R("a0 / b0 / c0")), ("a1, b1, c1", V32R("a1 / b1 / c1")),
               ("D, E, F", CIL), ("SD, SE, SF", V52P), ("7 ×", SRC)],
        marcas=[("A", "a0 · a1", "0 mm · final"), ("B", "b0 · b1", "0 mm · final"),
                ("C", "c0 · c1", "0 mm · final")],
        conex=["Potencia: VX:4 → cámara posterior; VX:2 → lado vástago (X = A, B, C). Fuente en "
               "VA:1, VB:1, VC:1 y VG:1.",
               "Línea I (activa en reposo): VG:2 → VC:12; une a esa línea c0:1, a1:1 y b1:1.",
               "Línea II: VG:4 → VA:12; une a esa línea VB:12, a0:1 y c1:1.",
               "c0:2 → S:1; S:2 → VA:14.",
               "a1:2 → VB:14.  b1:2 → pilotaje 14 de VG.",
               "a0:2 → b0:1; b0:2 → VC:14.  c1:2 → pilotaje 12 de VG.",
               "Selectores (circuitos aparte): SX:4 → cámara posterior de X; SX:2 → lado vástago "
               "(X = D, E, F); fuente en SX:1."],
        prueba=["F9: A, B y C retraídos; línea I con presión.",
                "Clic en S: A sale; al llegar a a1, B sale.",
                "B llega a b1: VG pasa a la línea II y A y B regresan juntos.",
                "A y B en a0 y b0: C sale; C llega a c1: VG vuelve a la línea I y C regresa.",
                "Mantén apretado SD: D sale; al soltar, D regresa (igual con SE y SF)."],
        fallos=["C sale antes de que A y B regresen: a0 y b0 no están en serie.",
                "C no regresa al final: c1 no pilota 12 de VG, o VG no empezó a la derecha."]),
]


def build():
    doc = new_doc("Guía paso a paso en FluidSIM",
                  "Cómo armar y simular las soluciones de las PD 10 y 11",
                  kicker="REPRESENTACIÓN GRÁFICA PARA INGENIERÍA MECATRÓNICA · USO DOCENTE")
    callout(doc, "Versión de FluidSIM:",
            "los pasos siguen FluidSIM Neumática en Windows (versiones 3.x–6). Los nombres de "
            "menús y diálogos pueden variar algo entre versiones y en FluidSIM 365 (versión web); "
            "ante la duda, la ayuda del programa (F1) tiene la ruta exacta. Donde las versiones "
            "difieren, se indican las dos formas.", fill="FFF4E5", color=RED)

    doc.add_heading("1. Procedimiento base (sirve para todos los ejercicios)", 1)
    doc.add_heading("1.1 Crear el circuito e insertar componentes", 2)
    numbered(doc, ["Archivo → Nuevo. Se abre una hoja vacía y, a la izquierda, la biblioteca de "
                   "componentes.",
                   "Arrastra cada componente desde la biblioteca a la hoja. Ordénalos por niveles, "
                   "igual que en el esquema de la solución: cilindros arriba, válvulas de potencia "
                   "al medio, válvulas de señal abajo.",
                   "Para girar o reflejar un componente: selecciónalo y usa clic derecho → Rotar / "
                   "Reflejar (útil para orientar las reguladoras)."])
    doc.add_heading("1.2 Configurar una válvula (doble clic)", 2)
    para(doc, "FluidSIM usa válvulas configurables (3/n, 4/n o 5/n vías). Con doble clic se abre su "
              "diálogo, donde se elige:")
    bullets(doc, [[("Cuerpo de la válvula: ", {"bold": True}),
                   ("el símbolo de cada posición (por ejemplo 3/2 normalmente cerrada).", {})],
                  [("Accionamiento izquierdo y derecho: ", {"bold": True}),
                   ("manual (pulsador, pedal, palanca), mecánico (rodillo, rodillo escamoteable, "
                    "resorte) o neumático (pilotaje).", {})],
                  [("Posición inicial: ", {"bold": True}),
                   ("en qué posición arranca la válvula. Solo se respeta si no contradice al resorte. "
                    "En las 5/2 biestables elige la DERECHA (1 → 2): cilindro retraído y, en la "
                    "selectora VG, la línea que debe estar activa en reposo.", {})],
                  [("Etiqueta: ", {"bold": True}),
                   ("en las válvulas de rodillo escribe el nombre del final de carrera (a0, a1…).",
                    {})]])
    doc.add_heading("1.3 Conectar", 2)
    numbered(doc, ["Acerca el puntero a una conexión (puerto) hasta que cambie de forma; haz clic y "
                   "arrastra hasta la otra conexión. Suelta.",
                   "Para una unión en T, arrastra desde un puerto y suelta sobre una línea ya "
                   "dibujada: FluidSIM crea el punto de unión. Así se arman las líneas de grupo de "
                   "la cascada.",
                   "Coloca una fuente de aire comprimido en cada puerto 1 (o una unidad de "
                   "mantenimiento con líneas a cada válvula). Los escapes 3 y 5 pueden quedar libres.",
                   "Comprobación rápida: mueve un componente; si la línea lo sigue, está conectada. "
                   "El menú del programa también tiene una opción para comprobar el dibujo "
                   "(conexiones abiertas o líneas superpuestas)."])
    doc.add_heading("1.4 Finales de carrera: marcas en el cilindro + etiqueta en el rodillo", 2)
    para(doc, "El rodillo solo se acciona si la marca del cilindro y la etiqueta de la válvula tienen "
              "EXACTAMENTE el mismo nombre (respeta mayúsculas y minúsculas).")
    table(doc, [["Versión", "Cómo poner las marcas en el cilindro"],
                ["FluidSIM 3.x y 4.x",
                 "Arrastra el componente «Regla de distancia» junto al cilindro hasta que encaje sobre "
                 "él. Doble clic en la regla: en cada fila escribe la etiqueta (a0, a1) y su posición "
                 "(a0 = 0 mm; a1 = carrera máxima, p. ej. 100 mm)."],
                ["FluidSIM 5 y 6",
                 "Doble clic en el cilindro → sección de etiquetas o marcas de accionamiento. Agrega "
                 "a0 al inicio (0 mm) y a1 al final de la carrera. Según la versión también puedes "
                 "usar la regla de distancia."]], [3.6, 13.4])
    para(doc, "Luego, doble clic en cada válvula de rodillo → Etiqueta = a0, a1… Si la marca está en "
              "0 mm, al iniciar la simulación el rodillo a0 aparece accionado, como en el esquema.")
    doc.add_heading("1.5 Simular y verificar", 2)
    numbered(doc, ["Ejecutar → Iniciar (F9 en las versiones clásicas). Las líneas con presión cambian "
                   "de color y los cilindros se mueven.",
                   "Un clic en un pulsador lo acciona mientras mantienes el botón del ratón; al soltar "
                   "vuelve por el resorte.",
                   "Para editar, primero detén la simulación.",
                   "Verifica con el «Diagrama de estado»: arrástralo desde la biblioteca y luego "
                   "arrastra los cilindros dentro de él. Compara la curva con el diagrama "
                   "espacio-fase de la solución.",
                   "Guarda el archivo (.ct) con el nombre del ejercicio en la carpeta fluidsim/ "
                   "del repositorio."])
    doc.add_heading("1.6 Problemas frecuentes", 2)
    table(doc, [["Síntoma", "Causa probable", "Solución"],
                ["El rodillo nunca se acciona", "Etiqueta distinta a la marca, o marca fuera de la "
                 "carrera", "Copia el mismo nombre; revisa la posición en mm"],
                ["El cilindro arranca extendido", "Posición inicial de la 5/2 a la izquierda",
                 "Doble clic → posición inicial: derecha"],
                ["La cascada empieza en el grupo equivocado", "Posición inicial de VG",
                 "Derecha (1 → 2): la línea conectada a VG:2 queda activa"],
                ["Un movimiento no es lento o no se mueve", "Reguladora invertida o cerrada (0 %)",
                 "Gírala; sube la apertura"],
                ["El cilindro oscila o no invierte", "Señal bloqueada: rodillo alimentado desde "
                 "una fuente", "En cascada, aliméntalo desde su línea de grupo"],
                ["La línea no transmite presión", "No llegó a la conexión (no hay punto)",
                 "Vuelve a trazarla hasta el puerto"],
                ["No puedo mover ni editar", "La simulación está en marcha", "Detén la simulación"]],
          [4.6, 6.0, 6.4])

    for e in EJ:
        if e["land"]:
            landscape(doc)
        else:
            page_break(doc) if not getattr(build, "_land", False) else portrait(doc)
        build._land = e["land"]
        doc.add_heading(e["titulo"], 1)
        figure(doc, e["fig"], 18.0 if e["land"] else 11.0,
               "Esquema objetivo (en posición de reposo). Arma en FluidSIM exactamente esta "
               "disposición.")
        doc.add_heading("Paso 1 · Coloca y configura los componentes", 2)
        table(doc, [["Ref.", "Componente en la biblioteca", "Configuración (doble clic)"]] +
              [[r, c[0], c[1]] for r, c in e["comps"]],
              [2.6, 4.4, 10.0] if not e["land"] else [3.5, 6.0, 16.0], size=9)
        doc.add_heading("Paso 2 · Marcas de final de carrera", 2)
        table(doc, [["Cilindro", "Marcas", "Posición"]] + [list(m) for m in e["marcas"]],
              [3.0, 4.0, 10.0] if not e["land"] else [4.0, 5.0, 16.5], size=9)
        doc.add_heading("Paso 3 · Conexiones (en este orden)", 2)
        numbered(doc, e["conex"])
        doc.add_heading("Paso 4 · Simula y comprueba", 2)
        numbered(doc, e["prueba"])
        doc.add_heading("Si no funciona", 3)
        bullets(doc, e["fallos"])
        if e["fig"] == "e2_1_estampado_ABC":
            figure(doc, "e2_1_selectores_DEF", 15.0, "Selectores D, E, F (circuitos independientes).")

    portrait(doc)
    doc.add_heading("Fuentes consultadas", 1)
    para(doc, [("Manuales y tutoriales de FluidSIM (versiones 3.6, 4.2 y 6) y guías de prácticas en "
                "español sobre finales de carrera y regla de distancia. Los pasos se verificaron "
                "contra varias fuentes, pero no contra una instalación concreta: confírmalos en tu "
                "versión.", {"color": MUTED})], size=9)
    bullets(doc, ["FluidSIM 6 Component Library — art-systems.de/www/site/en/fluidsim/components.html",
                  "Manual de usuario FluidSIM 4.2 (slideshare.net, ingeltvaf)",
                  "FluidSIM 3.6 Neumática, Manual del usuario (Festo, 662759 ES)",
                  "FluidSim: Regla de Distancia — wikifab.dimf.etsii.upm.es",
                  "Configuración de Finales de Carrera en FluidSim — es.scribd.com/document/411674420",
                  "Electro-Pneumatic Circuit Creation and Simulation Using FluidSIM — control.com"])
    doc.save(OUT)
    return OUT


if __name__ == "__main__":
    print("ok", build())
