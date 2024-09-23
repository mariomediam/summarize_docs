# API de Extracción de Información de Documentos Word

Esta API utiliza el modelo de lenguaje de OpenAI, Django y LangChain para procesar documentos Word (informes, formatos, etc.) y extraer información clave como el número del documento, año, oficina de destino y un resumen, devolviéndolo en formato JSON. Este proyecto ha sido implementado en un sistema legado desarrollado con **Visual FoxPro 8.0**.

## Características

- **Carga de documentos Word**: Sube documentos Word (.docx) para su procesamiento.
- **Extracción automática**: El sistema analiza el documento y extrae información relevante.
- **Formato JSON**: La API devuelve la información en formato JSON, facilitando su integración con otros sistemas.
- **Integración con sistemas heredados**: Funciona en sistemas antiguos basados en Visual FoxPro 8.0.

## Tecnologías Utilizadas

- **Django**: Framework web usado para construir la API.
- **LangChain**: Utilizado para la manipulación y procesamiento avanzado del lenguaje natural.
- **OpenAI**: Modelo de inteligencia artificial que facilita la comprensión y extracción de texto en los documentos.
- **Visual FoxPro 8.0**: Sistema legado en el que se ha implementado la API. 🦊

## Cómo Funciona

1. **Subir el archivo**: Carga un archivo Word mediante una solicitud a la API.
2. **Procesamiento del documento**: El archivo se procesa utilizando OpenAI para extraer el número del documento, el año, la oficina de destino y un resumen del contenido.
3. **Resultado en JSON**: El servidor devuelve un archivo JSON con la información extraída.

## Ejemplo de Respuesta JSON

```json
{
    "message": "",
    "content": {
        "summarize": "Se informa sobre el seguimiento y control de la ejecución del servicio de implementación de videovigilancia con cámaras y alarmas en puntos críticos de la urbanización Ignacio Merino. Se detalla la verificación de la instalación y configuración realizada por la empresa SERVITEC PIURA IMPORT SAC, así como el cumplimiento de los términos de referencia. Se recomienda dar la conformidad respectiva del servicio.",
        "fecha_doc": "31/05/2024",
        "tipo_doc": "INFORME",
        "number_doc": "61",
        "year_doc": "2024",
        "siglas_doc": "OGTI/MPP",
        "oficina_destino": "GERENCIA DE SEGURIDAD CIUDADANA, FISCALIZACION Y CONTROL Y GESTION DE RIESGOS DE DESASTRES",
        "cod_oficina_destino": 110656
    }
}
```

## Deploy con docker compose
Antes de empezar, [instala Compose](https://docs.docker.com/compose/install/).

```
$ docker compose up -d
```

Después de que se inicie la aplicación, llame a la API `http://localhost:8000/summarize-docs/` tal como se aprecia en el video anterior 👍


