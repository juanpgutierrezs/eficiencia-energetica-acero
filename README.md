# Eficiencia energética en una planta siderúrgica

Diagnóstico de energía reactiva según la regulación colombiana, dimensionamiento de la compensación, evaluación económica y pronóstico de consumo con aprendizaje automático, usando un año de mediciones reales de una acería. Incluye una herramienta en Excel para el ingeniero de planta y un tablero en Power BI para la jefatura de mantenimiento.

## Resultados principales

- **El FP anual (0,90) oculta el problema:** evaluada hora por hora con la Resolución CREG 015 de 2018, la planta superaría el límite de reactiva en el **54,7 % de las horas** y en los **365 días** del año.
- **Causa:** la compensación funciona por horario. Falta de noche (P ≈ 13 kW, Q ≈ 19 kVAr) y en el arranque de las 8 h, y sobra al mediodía y al final del turno (2147 horas con inyección capacitiva).
- **Solución:** 15 kVAr fijos + banco automático de 90 kVAr en 6 pasos, y control por regulador de la compensación existente.
- **Economía:** cobro mínimo de ~5,65 millones COP/año (M = 1); retorno de **4,6 años con M = 1** y de **menos de 2 años** si los excesos se repiten (análisis de sensibilidad por costo y factor M).
- **Modelo:** gradient boosting para el pronóstico de la próxima hora: **MAE de 19,4 kWh frente a 39,9 kWh** del método de referencia. Para el día siguiente no supera al perfil por hora y tipo de jornada, que es el que se usa.
- **Anomalías:** 928 horas fuera de ±3 veces el error medio (550 de consumo alto y 378 de consumo bajo).

## Datos

[Steel Industry Energy Consumption](https://archive.ics.uci.edu/dataset/851) (UCI, n.º 851): DAEWOO Steel, Gwangyang (Corea del Sur), 2018, cada 15 minutos, 35 040 registros. Licencia CC BY 4.0. Tarifas de referencia: pliego de Air-e, agosto de 2026, nivel de tensión 2.

## Estructura

```
data/raw/          Datos originales
data/processed/    Tablas limpias: 15 min, horaria, perfiles, pronóstico y anomalías
notebooks/         01_viabilidad (exploración y diagnóstico), 02_pronostico (modelo y anomalías)
src/               Script de figuras del informe
excel/             Herramienta de diagnóstico (herramienta_energia.xlsx)
powerbi/           Tablero (proyecto de Power BI)
informe/           Informe técnico en LaTeX, figuras y capturas
```

## Cómo reproducir

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

1. Ejecutar `notebooks/01_viabilidad.ipynb` y luego `notebooks/02_pronostico.ipynb`.
2. Generar las figuras: `python src/generar_figuras.py`.
3. Abrir `excel/herramienta_energia.xlsx` y usar **Datos > Actualizar todo** (ajustar las rutas de Power Query si el proyecto está en otra carpeta).
4. Abrir el proyecto de Power BI en `powerbi/` y actualizar.

## Limitaciones

- La reactiva medida es neta: incluye la compensación existente, cuyo tamaño se desconoce.
- El dimensionamiento usa la mediana de un día laborable; un diseño real requiere un analizador de redes y revisión de armónicos.
- El costo por kVAr es un valor de trabajo; por eso se presenta un análisis de sensibilidad.
- No hay datos de producción ni de clima; el CO2 y el FP del dataset se derivan del consumo y no se usaron como entradas del modelo.

## Autor

Juan Pablo Gutiérrez Sánchez — Ingeniería Electrónica, Universidad del Norte.
