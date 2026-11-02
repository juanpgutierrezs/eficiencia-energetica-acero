# Capturas pendientes

Capturas de pantalla que se deben tomar manualmente y guardar en esta carpeta
con exactamente estos nombres (el informe `informe/main.tex` las referencia así):

| Archivo | Contenido |
|---|---|
| `excel_diagnostico.png` | Hoja de diagnóstico de la herramienta en Excel (`excel/herramienta_energia.xlsx`). |
| `excel_dimensionamiento.png` | Hoja de dimensionamiento de la compensación en Excel. |
| `pbi_resumen.png` | Página de resumen ejecutivo del tablero de Power BI. |
| `pbi_anomalias.png` | Página de anomalías del modelo de pronóstico en Power BI. |

Mientras falten, el informe compila igual: la macro `\figura` usa `\IfFileExists`
y muestra un recuadro "Figura pendiente" en lugar de la imagen.
