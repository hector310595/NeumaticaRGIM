"""Catálogo de símbolos ISO 1219 usados en las prácticas dirigidas 10 y 11.

Cada entrada: imagen (figuras/<img>.png), nombre, designación completa (cómo se pide en un
enunciado o en la biblioteca del simulador), cómo se reconoce en el esquema y para qué sirve.
"""

CATALOGO = {
    "cil_de": dict(
        img="sym_cil_de", nombre="Cilindro de doble efecto",
        designacion="Actuador lineal de doble efecto",
        reconocer="Rectángulo con émbolo (barra gruesa) y vástago que sale por la derecha; "
                  "DOS conexiones abajo: cámara posterior y lado vástago. Sin resorte.",
        funcion="Avance (A+) y retroceso (A−) con aire. Se dibuja retraído."),
    "cil_se": dict(
        img="sym_cil_se", nombre="Cilindro de simple efecto",
        designacion="Actuador lineal de simple efecto, retorno por resorte",
        reconocer="Como el de doble efecto pero con UNA sola conexión y un resorte dibujado "
                  "en el lado del vástago.",
        funcion="Avanza con aire y retrocede por el resorte."),
    "marcas": dict(
        img="sym_marcas", nombre="Marcas de final de carrera",
        designacion="Posiciones a0 (retraído) y a1 (extendido) del cilindro A",
        reconocer="Trazos verticales sobre el vástago con su nombre (a0, a1). El mismo nombre "
                  "aparece junto al rodillo de la válvula que lo detecta.",
        funcion="Indican DÓNDE está físicamente el rodillo que se dibuja abajo."),
    "v32_boton": dict(
        img="sym_32_boton", nombre="Válvula 3/2 NC con pulsador",
        designacion="Válvula distribuidora 3/2, normalmente cerrada, accionamiento por pulsador, "
                    "retorno por resorte",
        reconocer="2 cuadros y 3 puertos (1, 2, 3). En el cuadro de reposo (derecha) el 1 está "
                  "bloqueado (símbolo T) y 2 descarga a 3. A la izquierda la «seta» del pulsador; "
                  "a la derecha el resorte.",
        funcion="Elemento de señal manual (S, S1…): mientras se pulsa, envía aire por 2."),
    "v32_pedal": dict(
        img="sym_32_pedal", nombre="Válvula 3/2 NC con pedal",
        designacion="Válvula distribuidora 3/2 NC, accionamiento por pedal, retorno por resorte",
        reconocer="Igual que la de pulsador, pero el accionamiento es una palanca inclinada "
                  "(pedal) a la izquierda.",
        funcion="Señal manual accionada con el pie."),
    "v32_rodillo": dict(
        img="sym_32_rodillo", nombre="Válvula 3/2 NC con rodillo (final de carrera)",
        designacion="Válvula distribuidora 3/2 NC, accionamiento por rodillo, retorno por resorte",
        reconocer="3/2 con un pequeño CÍRCULO (rodillo) en un vástago a la izquierda y su nombre "
                  "(a1, b1…). Dibujada en reposo: puertos en el cuadro derecho, 1 bloqueado.",
        funcion="Detecta que el cilindro llegó a esa posición y envía una señal."),
    "v32_rodillo_acc": dict(
        img="sym_32_rodillo_accionado", nombre="Válvula 3/2 con rodillo, dibujada accionada",
        designacion="La misma válvula de rodillo, pisada por el vástago en la posición inicial",
        reconocer="Los puertos están conectados al cuadro IZQUIERDO: la flecha 1 → 2 queda en línea "
                  "con los puertos. Así se dibujan a0, b0, c0 porque en reposo el vástago las pisa.",
        funcion="Confirma que el cilindro está en su posición inicial (retraído)."),
    "v32_rodillo_esc": dict(
        img="sym_32_rodillo_esc", nombre="Válvula 3/2 con rodillo escamoteable",
        designacion="Válvula 3/2 NC, rodillo abatible (actúa en un solo sentido)",
        reconocer="El rodillo está sobre una palanca articulada y lleva una flecha que indica el "
                  "único sentido en que actúa.",
        funcion="Da solo un pulso: alternativa sencilla para evitar señales bloqueadas."),
    "v52_bi": dict(
        img="sym_52_biestable", nombre="Válvula 5/2 biestable (piloto / piloto)",
        designacion="Válvula distribuidora 5/2, accionamiento neumático por ambos lados (14 y 12)",
        reconocer="2 cuadros y 5 puertos: arriba 4 y 2, abajo 5, 1 y 3. Un triángulo de pilotaje "
                  "a CADA lado (14 a la izquierda, 12 a la derecha) y NINGÚN resorte.",
        funcion="Válvula de potencia con MEMORIA: un pulso en 14 → A+, un pulso en 12 → A−. "
                "También es la selectora de grupo VG en la cascada."),
    "v42_bi": dict(
        img="sym_42_biestable", nombre="Válvula 4/2 biestable (piloto / piloto)",
        designacion="Válvula distribuidora 4/2, accionamiento y retorno por pulso neumático",
        reconocer="2 cuadros y 4 puertos: arriba 4 y 2, abajo 1 y 3. En reposo las flechas se "
                  "cruzan (1→2, 4→3). Pilotajes 14 y 12, sin resorte.",
        funcion="Igual que la 5/2 biestable, con un solo escape."),
    "v52_boton": dict(
        img="sym_52_boton", nombre="Válvula 5/2 con pulsador y resorte",
        designacion="Válvula distribuidora 5/2 monoestable, accionamiento por pulsador, "
                    "retorno por resorte",
        reconocer="5 puertos como la 5/2 biestable, pero con pulsador a la izquierda y resorte a "
                  "la derecha.",
        funcion="Mando directo: el cilindro sale mientras se pulsa y vuelve al soltar."),
    "v52_mono": dict(
        img="sym_52_pilot_resorte", nombre="Válvula 5/2 monoestable (piloto / resorte)",
        designacion="Válvula distribuidora 5/2, pilotaje neumático 14, retorno por resorte",
        reconocer="Triángulo de pilotaje solo a la izquierda y resorte a la derecha.",
        funcion="Necesita señal mantenida; al quitarla vuelve al reposo."),
    "or": dict(
        img="sym_or", nombre="Válvula selectora (función O)",
        designacion="Válvula selectora de circuito («shuttle»)",
        reconocer="Rectángulo horizontal con una BOLA en el centro y un asiento a cada lado; dos "
                  "entradas 1 (izquierda y derecha) y una salida 2 arriba.",
        funcion="Hay aire en 2 si llega por una entrada U otra (dos lugares de mando)."),
    "and": dict(
        img="sym_and", nombre="Válvula de simultaneidad (función Y)",
        designacion="Válvula de simultaneidad (de dos presiones)",
        reconocer="Rectángulo horizontal con dos pequeños cuadros unidos por una barra; dos "
                  "entradas 1 y salida 2.",
        funcion="Hay aire en 2 solo si llega por AMBAS entradas. Equivale a dos válvulas en serie."),
    "reguladora": dict(
        img="sym_reguladora", nombre="Reguladora de caudal unidireccional",
        designacion="Válvula de estrangulación y antirretorno (regulación en un sentido)",
        reconocer="Recuadro con dos ramas en paralelo: una estrangulación (dos arcos con flecha "
                  "diagonal = regulable) y un antirretorno (bola sobre un asiento en V).",
        funcion="Frena el flujo en un sentido y deja pasar libre en el otro. Se monta para "
                "estrangular el ESCAPE (meter-out)."),
    "fuente": dict(
        img="sym_fuente", nombre="Fuente de aire comprimido",
        designacion="Toma de presión / alimentación",
        reconocer="Círculo pequeño con un triángulo relleno, colgado del puerto 1.",
        funcion="Representa la alimentación ya tratada; evita dibujar toda la red."),
    "escape": dict(
        img="sym_escape", nombre="Escape a la atmósfera",
        designacion="Escape sin conexión",
        reconocer="Triángulo abierto (sin relleno) bajo los puertos 3 y 5.",
        funcion="Salida del aire usado."),
    "unidad": dict(
        img="sym_unidad", nombre="Fuente + unidad de mantenimiento",
        designacion="Compresor y unidad de mantenimiento (filtro, regulador, manómetro)",
        reconocer="Círculo con triángulo (fuente) seguido de un recuadro discontinuo con un rombo "
                  "(filtro).",
        funcion="Trata el aire antes de llegar a las válvulas. Se dibuja una vez."),
    "lineas": dict(
        img="sym_lineas", nombre="Tipos de línea",
        designacion="Trabajo, pilotaje, grupo, unión y cruce",
        reconocer="Continua = potencia; discontinua = señal/pilotaje; gruesa de color = línea de "
                  "grupo de la cascada; punto = unión; cruce sin punto = no hay conexión.",
        funcion="Leer por dónde va la potencia y por dónde la información."),
}

# Orden en que se presenta el catálogo
ORDEN = ["cil_de", "marcas", "v32_boton", "v32_pedal", "v32_rodillo", "v32_rodillo_acc", "v52_bi",
         "v42_bi", "v52_boton", "or", "and", "reguladora", "fuente", "escape", "unidad", "lineas",
         "cil_se", "v52_mono", "v32_rodillo_esc"]
