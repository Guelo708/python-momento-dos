# Sistema de Análisis de Datos - Aguas Paraíso

Este proyecto es una aplicación modular en **Python** diseñada para el procesamiento, limpieza, integración y análisis de datos de facturación y predios del acueducto comunitario **Aguas Paraíso**.

El objetivo principal es transformar datos crudos en información clave para la toma de decisiones sobre el recaudo de cartera, consumo por sectores y canales de pago preferidos por la comunidad.


## Estructura del Proyecto

python-momento-dos/
│
├── Data/
│   ├── raw/                  # Datos crudos de entrada (CSV)
│   │   ├── predios.csv
│   │   └── facturas.csv
│   └── processed/            # Datos limpios y procesados (CSV)
│       ├── predios_limpio.csv
│       └── facturas_limpio.csv
│
├── .gitignore                # Exclusión de archivos basura y entorno virtual
├── requirements.txt          # Lista de dependencias del proyecto
├── carga.py                  # Módulo para la carga de datos crudos (Opción 1)
├── limpieza.py               # Módulo de sanitización, nulos y duplicados (Opción 2)
├── merge.py                  # Módulo de validación pre-merge y unión (Opción 3)
├── analisis.py               # Módulo de análisis descriptivo con Colorama (Opción 4)
├── main.py                   # Script principal con menú interactivo
└── README.md                 # Documentación del proyecto

# Requisitos Previos e Instalación #

1. CLONAR EL REPOSITORIO


git clone https://github.com/Guelo708/python-momento-dos.git

2. CREAR Y ACTIVAR EL ENTORNO VIRTUAL (.venv)

Es necesario aislar las librerías del proyecto ejecutando los siguientes comandos en PowerShell o Git Bash:
Powershell
python -m venv .venv
.\.venv\Scripts\activate

3. INSTALAR DEPENDENCIAS O LIBRERIAS

Con el entorno virtual activo, instala las librerías necesarias mediante el archivo requirements.txt:

Bash
pip install -r requirements.txt

LAS PRINCIPALES DEPENDENCIAS SON

pandas y numpy: Manipulación, limpieza y análisis de estructuras de datos.
colorama: Formateo de texto con colores en la consola.

## Uso de la Aplicación ##
Para iniciar el sistema interactivo, ejecuta el script principal main.py:

Bash

python main.py

# Flujo de Navegación del Menú:

Opción 1: Carga los archivos crudos predios.csv y facturas.csv desde Data/raw/.

Opción 2: Sanitiza los textos (minúsculas, trim), maneja valores nulos, limpia formatos de moneda y guarda las copias en Data/processed/.

Opción 3: Verifica la integridad referencial de las claves id_predio y genera el DataFrame unificado (merge).

Opción 4: Muestra el reporte técnico a color con análisis de frecuencia, agregación de recaudo por sector, métricas de morosidad y canales de pago.

Opción 5: Finaliza la ejecución de la aplicación.

# Módulos y Preguntas de Análisis 

El módulo analisis.py da respuesta técnica a las siguientes preguntas clave:

Análisis de Frecuencia: Identifica el tipo de predio (Residencial, Comercial, Industrial, Oficial) y el sector con mayor cantidad de registros.

Análisis de Agregación: Calcula el recaudo total y monto promedio agrupado por cada uno de los 5 sectores del acueducto (Sector Tablazo parte Alta, Sector El hoyo, Tablazo parte baja, Sector Colegio y Tablazo Centro).

Análisis de Morosidad (Filtrado y Conteo): Determina el número de facturas vencidas/pendientes, el monto total en riesgo de recaudo y clasifica los sectores con mayor cartera vencida.

Canales de Pago: Muestra la distribución de uso entre plataformas (Nequi, Efectivo, Transferencia, Tarjetas, Recaudo Convenio).

