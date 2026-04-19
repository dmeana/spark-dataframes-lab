# spark-dataframes-lab · Análisis de Datos con PySpark en Docker

**Versión:** `v1.0`
**Contexto:** Proyecto de procesamiento de datos, limpieza y analítica utilizando Apache Spark y la DataFrame API.

Este repositorio contiene un flujo de trabajo completo de datos (*Data Pipeline*) desarrollado para una pequeña empresa de comercio electrónico. El sistema procesa ficheros de datos con problemas habituales en entornos reales (duplicados, valores nulos, inconsistencias de formato) para generar información limpia y útil para la toma de decisiones.

---

## Objetivo del Proyecto
El proyecto implementa una arquitectura **ETL (Extracción, Transformación y Carga)** estructurada en los siguientes pasos técnicos:

1. **Extracción (Lectura de datos):** Carga de ficheros CSV (`clientes.csv` y `pedidos.csv`) definiendo correctamente sus esquemas y opciones de lectura (`sep`, `header`, `inferSchema`).
2. **Transformación y Limpieza:** * Eliminación de registros duplicados en el fichero de clientes.
   * Limpieza de inconsistencias de formato (eliminación de espacios en blanco con `trim`).
   * Tratamiento y gestión segura de valores nulos.
   * Creación de nuevas variables de negocio (ej. `importe = cantidad * precio_unitario`).
3. **Integración:** Combinación de ambas fuentes de datos mediante un cruce relacional (`join`), analizando la correspondencia entre tablas y la pérdida de registros huérfanos.
4. **Análisis y SQL:** Cálculo de métricas clave (número de pedidos, ingresos totales y ticket medio) mediante agrupaciones (`groupBy`), clasificación condicional (`when`) y el uso de **Spark SQL** a través de vistas temporales.
5. **Muestreo y Carga (Persistencia):** División del dataset (`randomSplit` y `sample`) y exportación del resultado final unificado en formato **Parquet** para optimizar futuras lecturas.

---

## Estructura del repositorio

```text
spark-dataframes-lab/
├── docs/                                     # Documentación técnica y justificación
│   ├── enunciado.md                          # Contexto y requisitos del proyecto
│   ├── evidencias.md                         # Evidencias de ejecución y resultados
│   └── pistas.md                             # Pistas y ayudas técnicas del proyecto
├── img/                                      # Imágenes para la documentación
├── spark_jupyter/                            # Entorno dockerizado (Spark + Jupyter)
│   ├── apps/
│   │   ├── datos/                            # Ficheros CSV originales (clientes y pedidos)
│   │   └── salida/                           # Directorio con los resultados en formato Parquet
│   ├── notebooks/
│   │   ├── iniciar_spark.py                  # Script de inicialización de la sesión de Spark
│   │   └── practica_clientes_pedidos.ipynb   # Cuaderno principal con el código PySpark
│   ├── docker-compose-jupyter.yml            # Configuración de orquestación para levantar el clúster
│   ├── Dockerfile                            # Receta de construcción de la imagen base
│   └── Dockerfile.jupyter                    # Receta de construcción del entorno Jupyter
└── README.md                                 # Documentación principal (Este archivo)
```

---

## Arquitectura del proyecto

![Arquitectura proyecto](./img/arquitectura_proyecto.png)

---

## Pasos de Ejecución (Reproducibilidad)

El proyecto está diseñado para ejecutarse en un entorno contenedorizado, asegurando que las dependencias de Apache Spark funcionen en cualquier máquina.

### Paso 1: Levantar el entorno Dockerizado
Sitúate dentro de la carpeta `spark_jupyter/` y levanta el clúster (que incluye un Master, Workers y JupyterLab) ejecutando:

```bash
docker compose -f docker-compose-jupyter.yml up -d --build
```

### Paso 2: Servicios del entorno
Accede a JupyterLab y abre el cuaderno `practica_clientes_pedidos.ipynb`. Las rutas de los datos ya están mapeadas dentro del contenedor (`/opt/spark-apps/datos/`). Ejecuta todas las celdas secuencialmente para observar el proceso de transformación hasta la escritura del fichero Parquet.

---

## Decisiones de Arquitectura y Limpieza

Durante el desarrollo del análisis, se tomaron decisiones importantes para garantizar la fiabilidad de los datos:

1. **Uso de un Inner Join:** Al unir los clientes con sus pedidos, se utilizó un `inner join`. Esto permitió identificar y descartar registros inconsistentes (como pedidos asociados a IDs de cliente que no existían en el fichero de clientes), evitando generar categorías vacías en el análisis final.

2. **Imputación de Nulos vs Eliminación:** En lugar de borrar las filas con valores nulos (lo que habría supuesto perder ventas válidas), se aplicó una estrategia de relleno (`fillna`). Los productos vacíos se etiquetaron como "Desconocido" y las cantidades nulas se convirtieron en `0.0`, permitiendo que las operaciones matemáticas posteriores (como calcular el importe total) funcionaran sin errores.

3. **Muestreo (Sample) vs Partición (RandomSplit):** Se aplicaron ambas funciones entendiendo sus diferencias. `sample()` se utilizó para perfilado rápido, mientras que `randomSplit(0.8, 0.2)` se aplicó para dividir el total de los datos en conjuntos de Entrenamiento y Prueba, dejando el dataset preparado para modelos predictivos.