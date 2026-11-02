# Prompts para Claude Code

Antes de empezar: copia la carpeta `entregables` (la que descargaste) dentro de
`C:\Users\jpgse\Proyectos\eficiencia-energetica-acero\`. Cierra Excel y Power BI.
Abre la terminal en la carpeta del proyecto y ejecuta `claude`.

---

## PROMPT A — Ubicar entregables, figuras del informe y orden del repositorio

```text
Trabajo en Windows con PowerShell, en el proyecto C:\Users\jpgse\Proyectos\eficiencia-energetica-acero. Responde en español. Antes de cada comando de terminal explícame en una línea qué hace. Usa el Python del entorno .venv. NO modifiques excel/herramienta_energia.xlsx ni los notebooks.

1. Ubicar archivos:
   - Mueve entregables/informe/main.tex a informe/main.tex.
   - Reemplaza README.md de la raíz por entregables/README.md.
   - Mueve entregables/textos_postulacion.md a privado/textos_postulacion.md y agrega la línea "privado/" al .gitignore (ese archivo no debe subirse).
   - Guarda este archivo de prompts en docs/prompts_claude_code.md.
   - Borra la carpeta entregables cuando todo esté movido.

2. Crea src/generar_figuras.py que lea data/processed y guarde en informe/figuras (PNG, 150 dpi, etiquetas en español, estilo sobrio: color principal #1F3864 y gris #A6A6A6, sin títulos dentro de la imagen porque el informe ya tiene pie de figura):
   - perfil_horario.png: dos paneles lado a lado a partir de energia_horaria.csv. Izquierda: kWh promedio por hora del día, una línea para lunes a viernes y otra para sábado y domingo (usa la columna fecha para el día de la semana). Derecha: mediana de la columna FP por hora con una línea punteada en 90.
   - exceso_creg_hora.png: barras con la suma de exceso_kVArh por hora del día, en MVArh (dividir entre 1000), desde energia_horaria.csv.
   - pronostico_semana.png: desde pronostico_anomalias.csv, del 2018-10-15 al 2018-10-21 inclusive: línea de kWh real y línea de pred_kWh ("Pronóstico próxima hora"), eje Y "kWh por hora".
   - anomalias_mes.png: barras apiladas de cantidad de horas por mes según la columna anomalia (solo consumo_alto y consumo_bajo, sin normal), desde pronostico_anomalias.csv.
   Ejecuta el script y confirma que se generaron las 4 imágenes.

3. Crea la carpeta informe/capturas con un archivo LEEME.md que liste las capturas que debo tomar yo: excel_diagnostico.png, excel_dimensionamiento.png, pbi_resumen.png, pbi_anomalias.png.

4. Orden del repositorio: elimina los archivos .gitkeep de carpetas que ya tienen contenido; verifica que requirements.txt esté en texto normal (no UTF-16); no borres nada más.

5. git add, commit "Entregables: informe LaTeX, figuras, README y orden del repositorio", y push.

AL FINAL: resumen de archivos creados o movidos, comandos ejecutados y errores o advertencias.
```

---

## PROMPT B — Tablero de Power BI como proyecto (.pbip)

```text
Trabajo en Windows, en el proyecto C:\Users\jpgse\Proyectos\eficiencia-energetica-acero. Responde en español y explica en una línea cada comando antes de ejecutarlo.

OBJETIVO: crear en powerbi/ un proyecto de Power BI en formato PBIP (texto) que yo abriré en Power BI Desktop: powerbi/EficienciaEnergetica.pbip, con EficienciaEnergetica.SemanticModel (modelo en TMDL) y EficienciaEnergetica.Report (informe en formato PBIR). Sigue estrictamente los esquemas oficiales de Microsoft para PBIP, TMDL y PBIR; valida que todos los JSON sean sintácticamente correctos. PRIORIDAD: el modelo semántico. Si no estás seguro de poder generar correctamente algún visual en PBIR, crea igual las páginas y documenta ese visual en docs/visuales_powerbi.md (tipo de visual, campos y medidas) para que yo lo arme a mano.

MODELO SEMÁNTICO
- Parámetro de Power Query "RutaDatos" (texto) = "C:\Users\jpgse\Proyectos\eficiencia-energetica-acero\data\processed\".
- Tabla Horaria desde RutaDatos & "energia_horaria.csv" (Csv.Document, delimitador coma, encabezados promovidos, tipos con cultura "en-US"): fecha (fecha/hora), kWh, kVArh_ind, kVArh_cap, limite_kVArh, exceso_kVArh, FP (decimales), hora y mes (enteros), dia_semana (texto). Agrega la columna Dia = Date.From([fecha]) de tipo fecha.
- Tabla Anomalias desde "pronostico_anomalias.csv" con fecha, kWh, pred_kWh, residuo (decimales), hora, mes (enteros), tipo_jornada y anomalia (texto) y la columna Dia igual que arriba. Quita las demás columnas.
- Tabla calculada Calendario: CALENDAR(DATE(2018,1,1), DATE(2018,12,31)) con columnas Fecha, Mes (número), NombreMes (FORMAT con "es-CO", ordenada por Mes), DiaSemana (número, lunes = 1) y NombreDia. Márcala como tabla de fechas.
- Relaciones: Calendario[Fecha] 1 a varios con Horaria[Dia] y con Anomalias[Dia], dirección simple.
- Parámetros de hipótesis (tablas con GENERATESERIES y medida SELECTEDVALUE con valor por defecto): "Factor M" de 1 a 12, paso 1, por defecto 1; "Umbral k" de 1 a 5, paso 0,5, por defecto 3.
- Medidas (carpeta "Energía"): Energía activa (kWh) = SUM(Horaria[kWh]); Energía activa (MWh); Reactiva inductiva (kVArh); Factor de potencia = DIVIDE([Energía activa (kWh)], SQRT([Energía activa (kWh)]^2 + [Reactiva inductiva (kVArh)]^2)).
- Medidas (carpeta "CREG"): Límite CREG = 0.5; Cargo D (COP/kVArh) = 77.22; Exceso reactiva (kVArh) = SUMX(Horaria, MAX(0, Horaria[kVArh_ind] - [Límite CREG] * Horaria[kWh])); Horas con exceso; % horas con exceso (sobre COUNTROWS(Horaria)); Días con exceso (días con al menos una hora con exceso, usando VALUES(Horaria[Dia])); Horas con inyección capacitiva (kVArh_cap > kVArh_ind); Costo reactiva (COP) = [Exceso reactiva (kVArh)] * [Cargo D (COP/kVArh)] * valor de Factor M.
- Medidas (carpeta "Modelo"): MAE (kWh) = AVERAGEX(Anomalias, ABS(Anomalias[residuo])); CV(RMSE) %; Sesgo %; Umbral (kWh) = valor de Umbral k * MAE calculado sobre ALL(Anomalias); Horas anómalas (|residuo| > Umbral); Horas consumo alto; Horas consumo bajo; kWh sobre lo esperado (suma de residuo en horas con residuo > Umbral).
- Formatos: energía con separador de miles, FP con 2 decimales, porcentajes con 1 decimal, costos como moneda sin decimales.

INFORME (PBIR), 5 páginas, tema sobrio con color principal #1F3864 (crea un tema JSON y aplícalo):
1. "Resumen": tarjetas de Energía activa (MWh), Factor de potencia, % horas con exceso, Días con exceso, Costo reactiva (COP) y Horas anómalas; gráfico de columnas de Energía activa (MWh) por Calendario[NombreMes]; segmentador del parámetro Factor M.
2. "Perfil y FP": columnas de Energía activa (kWh) promedio por Horaria[hora] (crea la medida que haga falta); líneas de Factor de potencia por Horaria[hora]; segmentador de Calendario[NombreDia].
3. "Reactiva CREG": columnas de Exceso reactiva (kVArh) por Horaria[hora]; columnas de Exceso reactiva por Calendario[NombreMes]; tarjetas de Horas con exceso y Horas con inyección capacitiva; segmentador de mes.
4. "Anomalías": líneas de kWh real y pred_kWh por Anomalias[fecha]; columnas apiladas de horas anómalas por mes (alto y bajo); tarjetas de Horas anómalas y kWh sobre lo esperado; segmentador del parámetro Umbral k; segmentador de fechas.
5. "Modelo": tarjetas de MAE, CV(RMSE) y Sesgo; dispersión de kWh real contra pred_kWh.

OTROS
- Agrega al .gitignore: powerbi/**/.pbi/localSettings.json y powerbi/**/.pbi/cache.abf.
- Crea docs/abrir_powerbi.md con los pasos para abrir el proyecto: versión de Power BI Desktop necesaria, opciones de versión preliminar que haya que activar (formato PBIP y PBIR, si aplican), cómo cambiar el parámetro RutaDatos y cómo actualizar.
- git add, commit "Power BI: proyecto PBIP con modelo semántico, medidas DAX e informe", push.

AL FINAL: resumen de lo creado, qué visuales quedaron generados y cuáles quedaron documentados para armar a mano, y cualquier advertencia.
```
