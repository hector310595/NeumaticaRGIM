# Circuitos para FluidSim

FluidSim guarda los circuitos en un formato propietario (`.ct`) que no se puede generar
de forma fiable fuera del programa. Por eso aquí no hay archivos `.ct`. En su lugar, cada
circuito trae lo necesario para armarlo en pocos minutos:

| Ejercicio | Esquema (PNG/SVG) | Componentes y conexiones |
|---|---|---|
| PD 10 · Ej. 1 Puerta de garaje | `figuras/e1_1_puerta_conmutada` (variante: `e1_1_puerta_botonera`) | Solucionario, sección «Puerta de garaje» |
| PD 10 · Ej. 2 Cuchara de fundición | `figuras/e1_2_cuchara` | Solucionario, sección «Cuchara» |
| PD 11 · Ej. 1 Estampado y selección | `figuras/e2_1_estampado_ABC`, `figuras/e2_1_selectores_DEF` | Solucionario, sección «Estampado» |
| PD 11 · Ej. 2 Dobladora | `figuras/e2_2_doblado` | Solucionario, sección «Dobladora» |
| PD 11 · Ej. 3 Prensa | `figuras/e2_3_prensa` | Solucionario, sección «Prensa» |

El solucionario está en `docente/RGIM_Solucionario_Docente.docx`.

## Cómo armar un circuito a partir de la tabla de conexiones

1. Coloca los componentes de la tabla «Componentes». Usa la válvula configurable y elige el
   tipo (3/2, 4/2, 5/2) y el accionamiento de cada lado.
2. En cada cilindro define las marcas de final de carrera (`a0` al inicio de la carrera y `a1`
   al final). Usa la **misma etiqueta** en la válvula de rodillo correspondiente.
3. Conecta según la tabla «Conexiones». `VX:n` es el puerto *n* de la válvula *VX*.
   En la cascada, «Línea I/II» son las salidas 4/2 de la válvula selectora de grupo `VG`.
4. Verifica la posición inicial: cilindros retraídos y `VG` con la línea activa en reposo
   (la que indica el solucionario).
5. Simula fase por fase y compara con el diagrama espacio-fase (`figuras/fase_*`).

Cuando tengas los `.ct` funcionando, guárdalos en esta carpeta, con el nombre del
ejercicio, para versionarlos junto al resto del material.
