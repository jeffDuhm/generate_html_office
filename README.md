# Conversor personalizado de word a html

Convierte documentos word (.docx) a html utilizando un archivo de configuración personalizado.

## Requisitos

- Python 3.12+
- Dependencias:

```bash
pip install -r requirements.txt
```

## Uso CLI

1. Coloca los archivos `.docx` dentro de la carpeta `input`.

Ejecuta:

```bash
make cli SITE=freeway
```

Sitios disponibles:

* freeway
* ino
* acceptance

Ejemplo:

```bash
make cli SITE=freeway
```

> **Nota**: `freeway` soporta inglés y español.

2. Los archivos convertidos se guardarán en la carpeta `output`.

## Opciones

### Freeway

```bash
make cli SITE=freeway
```

Carga:

```text
config/freeway.json
```

### Ino

```bash
make cli SITE=ino
```
Carga:

```text
config/ino.json
```

### Acceptance

```bash
make cli SITE=acceptance
```
Carga:

```text
config/acceptance.json
```

> **Nota**: Se puede modificar el archivo de configuración (.json) para agregar el texto de widget y modal si es necesario.

