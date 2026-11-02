# Visuales del tablero de Power BI

Los 26 visuales de las 5 páginas están generados en formato PBIR dentro de
`powerbi/EficienciaEnergetica.Report/definition/pages/`. Todos los JSON pasan la validación
contra los esquemas oficiales de Microsoft. Aun así, esa validación revisa la estructura y no
puede comprobar cómo Power BI Desktop dibuja cada visual. Si alguno no se ve bien al abrirlo,
esta es la especificación para rehacerlo a mano.

Lienzo: 1280 × 720 px, "Ajustar a la página". Tema: `TemaAcero.json` (color principal #1F3864,
secundario #A6A6A6).

Notación: `Tabla[columna]` es una columna; `[Medida]` es una medida. Las medidas de energía y
CREG están en la tabla **Horaria**, las del modelo en **Anomalias** y las de los parámetros en
sus propias tablas.

## 1. Resumen

| Visual | Tipo | Campos |
|---|---|---|
| Tarjeta | Tarjeta | Valores: `[Energía activa (MWh)]` |
| Tarjeta | Tarjeta | Valores: `[Factor de potencia]` |
| Tarjeta | Tarjeta | Valores: `[% horas con exceso]` |
| Tarjeta | Tarjeta | Valores: `[Días con exceso]` |
| Tarjeta | Tarjeta | Valores: `[Costo reactiva (COP)]` |
| Tarjeta | Tarjeta | Valores: `[Horas anómalas]` |
| Energía activa por mes (MWh) | Gráfico de columnas agrupadas | Eje X: `Calendario[NombreMes]`; Eje Y: `[Energía activa (MWh)]`. Orden: NombreMes ascendente |
| Factor M (multiplicador CREG) | Segmentación, desplegable, selección única | Campo: `'Factor M'[Factor M]` |

## 2. Perfil y FP

| Visual | Tipo | Campos |
|---|---|---|
| Energía activa promedio por hora del día (kWh) | Columnas agrupadas | Eje X: `Horaria[hora]`; Eje Y: `[Energía promedio por hora (kWh)]` (= `AVERAGE(Horaria[kWh])`). Orden: hora ascendente |
| Factor de potencia por hora del día | Gráfico de líneas | Eje X: `Horaria[hora]`; Eje Y: `[Factor de potencia]`. Orden: hora ascendente |
| Día de la semana | Segmentación, lista | Campo: `Calendario[NombreDia]` (ordenado por `DiaSemana`) |

## 3. Reactiva CREG

| Visual | Tipo | Campos |
|---|---|---|
| Tarjeta | Tarjeta | Valores: `[Horas con exceso]` |
| Tarjeta | Tarjeta | Valores: `[Horas con inyección capacitiva]` |
| Reactiva en exceso por hora del día (kVArh) | Columnas agrupadas | Eje X: `Horaria[hora]`; Eje Y: `[Exceso reactiva (kVArh)]` |
| Reactiva en exceso por mes (kVArh) | Columnas agrupadas | Eje X: `Calendario[NombreMes]`; Eje Y: `[Exceso reactiva (kVArh)]` |
| Mes | Segmentación, lista | Campo: `Calendario[NombreMes]` |

## 4. Anomalías

| Visual | Tipo | Campos |
|---|---|---|
| Tarjeta | Tarjeta | Valores: `[Horas anómalas]` |
| Tarjeta | Tarjeta | Valores: `[kWh sobre lo esperado]` |
| Consumo real y pronóstico de la próxima hora (kWh) | Gráfico de líneas | Eje X: `Anomalias[fecha]` (continuo); Eje Y: `[kWh real]` (= `SUM(Anomalias[kWh])`) y `[kWh pronosticado]` (= `SUM(Anomalias[pred_kWh])`) |
| Horas anómalas por mes | Columnas apiladas | Eje X: `Calendario[NombreMes]`; Eje Y: `[Horas consumo alto]` y `[Horas consumo bajo]` |
| Umbral k (veces el MAE) | Segmentación, desplegable, selección única | Campo: `'Umbral k'[Umbral k]` |
| Rango de fechas | Segmentación "Entre" | Campo: `Calendario[Fecha]` |

## 5. Modelo

| Visual | Tipo | Campos |
|---|---|---|
| Tarjeta | Tarjeta | Valores: `[MAE (kWh)]` |
| Tarjeta | Tarjeta | Valores: `[CV(RMSE) %]` |
| Tarjeta | Tarjeta | Valores: `[Sesgo %]` |
| Consumo real frente a pronóstico (kWh por hora) | Gráfico de dispersión | Valores (detalle): `Anomalias[fecha]`; Eje X: `[kWh real]`; Eje Y: `[kWh pronosticado]` |

## Notas

- La tarjeta clásica (`card`) sigue siendo compatible. Para usar la tarjeta nueva, se cambia el
  tipo de visual en el panel de visualizaciones y se conservan los campos.
- La dispersión tiene unas 8.600 horas. Power BI muestra una muestra representativa si se
  supera su límite de puntos.
- Las medidas `kWh real`, `kWh pronosticado` y `Energía promedio por hora (kWh)` se agregaron
  porque el modelo tiene activado *Desalentar medidas implícitas*: los gráficos usan siempre
  medidas explícitas.
