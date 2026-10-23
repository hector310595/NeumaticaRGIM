# Representación neumática · RGIM (PUCP)

Material para la semana de **representación neumática** del curso *Representación Gráfica para
Ingeniería Mecatrónica*: 2 h de teoría y 3 h de práctica dirigida en FluidSim. El contenido se
seleccionó a partir de las clases de KU Leuven (*Mechanical Drive Systems*, D. Reynaerts).
Se conservó solo lo necesario para resolver las prácticas dirigidas 10 y 11.

## Contenido

| Carpeta / archivo | Para quién | Qué es |
|---|---|---|
| `sesion1_teoria/RGIM_S1_Representacion_Neumatica_Teoria.pptx` | Docente (proyectar) | 30 diapositivas con plantilla PUCP; notas del orador con tiempos y preguntas |
| `sesion2_practica/RGIM_S2_Practica_Dirigida_FluidSim.pptx` | Docente (proyectar) | Guía paso a paso de la práctica; **las soluciones son diapositivas ocultas** |
| `sesion2_practica/RGIM_Guia_Practica_Dirigida_Alumno.docx` | Alumnos | Repaso con catálogo de símbolos, FluidSim, calentamiento, enunciados con preguntas guía y lista de verificación |
| `docente/RGIM_Solucionario_Docente.docx` | Docente | Catálogo de símbolos (nombre, designación, cómo reconocerlo, función) y las 5 soluciones: esquema, espacio-fase, análisis, símbolos que necesita cada una (cantidad y referencias) y conexiones |
| `docente/RGIM_Plan_de_Sesiones.docx` | Docente | Criterio de selección del contenido, cronograma minuto a minuto y preparación |
| `figuras/` | — | Todos los esquemas y diagramas en PNG y SVG (reutilizables) |
| `fluidsim/` | Docente | Cómo armar los circuitos en FluidSim (ver nota sobre archivos `.ct`) |
| `plantilla/` | — | Plantilla PowerPoint PUCP usada para las presentaciones |
| `src/` | — | Generadores (Python) de todo el material |

## Alcance de la semana

**Se ve:** símbolos ISO 1219 (cilindros, válvulas X/Y, accionamientos, selectora O,
simultaneidad Y, reguladora unidireccional), reglas de dibujo por niveles y en reposo,
mando directo e indirecto, memoria (válvula biestable) y regulación *meter-out*. También
secuencias y diagrama espacio-fase, señales bloqueadas y **método cascada**.

**No se ve** (está en las clases de KU Leuven, pero corresponde a otros cursos):
termodinámica del aire y dimensionamiento, coeficientes de caudal, Karnaugh,
electroneumática, PLC/Grafcet, hidroneumática y servoneumática.

## Regenerar el material

```bash
./build_all.sh
```

Los esquemas se dibujan con una mini librería de símbolos (`src/simbolos.py`). Para modificar un
circuito, edita su función en `src/circuitos.py` y vuelve a ejecutar el script.
