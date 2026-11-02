# Abrir el proyecto de Power BI

El tablero está guardado como **proyecto de Power BI (PBIP)** en formato de texto:

```
powerbi/
├── EficienciaEnergetica.pbip              ← archivo que se abre
├── EficienciaEnergetica.SemanticModel/    ← modelo semántico en TMDL
│   └── definition/ (database, model, expressions, relationships, tables/*.tmdl)
└── EficienciaEnergetica.Report/           ← informe en formato PBIR
    ├── definition/ (report.json, pages/<página>/visuals/<visual>/visual.json)
    └── StaticResources/RegisteredResources/TemaAcero.json   ← tema (#1F3864)
```

## 1. Versión de Power BI Desktop

- Se necesita **Power BI Desktop de noviembre de 2025 o posterior**. Los archivos del
  informe usan los esquemas PBIR `report 3.0.0`, `page 2.0.0` y `visualContainer 2.4.0`
  (este último se publicó en noviembre de 2025).
- En este equipo está instalada la versión **2.159** (Microsoft Store), que es suficiente.

## 2. Opciones de versión preliminar

En las versiones recientes, PBIP, TMDL y PBIR ya vienen activados y no hay que hacer nada.
Si se usa una versión más antigua y aparecen en
**Archivo → Opciones y configuración → Opciones → Características en versión preliminar**,
hay que activar estas tres y reiniciar Power BI Desktop:

- *Formato de guardado de proyecto de Power BI (.pbip)*
- *Almacenar el modelo semántico con el formato TMDL*
- *Almacenar informes con el formato de metadatos mejorado (PBIR)*

## 3. Abrir

1. Doble clic en `powerbi/EficienciaEnergetica.pbip` (o **Archivo → Abrir** y elegir ese archivo).
2. El modelo se abre **sin datos** porque el repositorio no incluye la caché. Hay que actualizar
   (paso 5) para cargar los CSV.

## 4. Cambiar la ruta de los datos (parámetro `RutaDatos`)

El parámetro apunta por defecto a
`C:\Users\jpgse\Proyectos\eficiencia-energetica-acero\data\processed\`.
Si el repositorio está en otra carpeta:

1. **Inicio → Transformar datos → Editar parámetros**.
2. Cambiar `RutaDatos` por la ruta de `data\processed` en ese equipo. **Debe terminar en `\`**.
3. Aceptar y luego **Aplicar cambios**.

Otra forma: **Transformar datos** → en el editor de Power Query seleccionar `RutaDatos` en
la lista de consultas → cambiar el *Valor actual* → **Cerrar y aplicar**.

## 5. Actualizar

- **Inicio → Actualizar** recarga `energia_horaria.csv` y `pronostico_anomalias.csv` y
  recalcula las tablas `Calendario`, `Factor M` y `Umbral k`.
- Si los CSV cambian (por ejemplo, al volver a ejecutar los notebooks), basta con volver a
  actualizar.
- Si aparece un aviso de nivel de privacidad, elegir *Organizacional* o *Ignorar niveles de
  privacidad* para los archivos locales.

## 6. Guardar y git

- Guardar con **Archivo → Guardar** (no "Guardar como .pbix") para conservar el formato PBIP.
- Power BI crea la carpeta `.pbi/` dentro del modelo y del informe. `localSettings.json` y
  `cache.abf` están en `.gitignore`: la caché con los datos no se sube a GitHub.
- La lista de visuales con sus campos está en [`visuales_powerbi.md`](visuales_powerbi.md),
  por si hay que rehacer alguno a mano.
