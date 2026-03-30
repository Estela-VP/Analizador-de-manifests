# Analizador de Manifests MPD y HLS

Herramienta CLI y GUI para analizar manifests de DASH (.mpd) e HLS (.m3u8) e identificar el tipo de contenido y extraer información detallada del contenido multimedia.

## Características

### Fase 1: Análisis de URL ✓
- Detección automática del tipo de manifest (MPD/HLS)
- Identificación de tipo de contenido (Live, Start Over, L7D, CPVR, VOD)
- Análisis basado en patrones de URL

### Fase 2: Análisis de Contenido ✓
- **Descarga y Parseo XML**: Análisis profundo del manifest
- **Perfiles de Video**: Extracción de capas/calidades, resoluciones, framerates
  - Perfiles LATAM: Cinema, Sport Simplified, Sport Premium, SD
  - Perfiles Alemania: HD-E1, HD-E2, HD-E3 (Telefónica O2)
- **Detección de Audio**: Identificación de AAC, Dolby Digital, Dolby Atmos
- **Contenido Complementario**: Detección de subtítulos y thumbnails
- **Multikey Detection**: Identificación de múltiples codificaciones de video

## Tipos de Contenido Soportados

- **Live**: Transmisión en vivo
- **Start Over**: Permite reiniciar desde el principio
- **Last Seven Days (L7D)**: Ventana deslizante de 7 días (Catch-up TV)
- **CPVR**: Grabador Personal Continuo (Continuous Personal Video Recorder)
- **VOD**: Video Bajo Demanda

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Interfaz Gráfica (GUI - Recomendado)

Para abrir la aplicación con interfaz gráfica amigable:

```bash
python run_gui.py
```

**Características GUI:**
- Análisis básico con información de tipo de manifest y contenido
- Tab "Contenido" con información detallada del manifest
- Checkbox para habilitar análisis de contenido
- Visualización de perfiles de video, audio codecs y más
- Threading para evitar congelamiento durante descarga

### Modo Línea de Comandos (CLI)

#### Análisis Básico (URL únicamente)

```bash
python -m analizador_manifests "https://example.com/stream.mpd"
```

#### Análisis Básico con Verbose

```bash
python -m analizador_manifests "https://example.com/stream.mpd" --verbose
python -m analizador_manifests "https://example.com/stream.mpd" -v
```

#### Análisis de Contenido (Fase 2)

```bash
# Descargar y analizar contenido del manifest
python -m analizador_manifests "https://example.com/stream.mpd" --content
python -m analizador_manifests "https://example.com/stream.mpd" -c -v
```

#### Salida en JSON

```bash
python -m analizador_manifests "https://example.com/stream.mpd" --content --json
python -m analizador_manifests "https://example.com/stream.mpd" -c -j
```

## Ejemplos

### GUI

```bash
# Ejecutar la interfaz gráfica
python run_gui.py
```

### CLI - Ejemplos

```bash
# Analizar solo URL
python -m analizador_manifests "https://example.com/live.mpd"
> Live

# Analizar URL con verbose
python -m analizador_manifests "https://example.com/live.mpd" -v
# Mostrará: tipo, contenido, confianza

# Analizar contenido del manifest
python -m analizador_manifests "https://example.com/live.mpd" -c -v
# Mostrará: URL, contenido, perfiles de video, audio codecs, subtítulos, etc.

# Salida JSON para programación
python -m analizador_manifests "https://example.com/live.mpd" -c -j
# Retorna JSON estructurado
```

## Ejemplo de Salida Verbose (Fase 2)

```
============================================================
ANÁLISIS DE MANIFEST
============================================================

📋 Información Básica:
  URL: https://example.com/manifest.mpd
  Tipo: MPD
  Contenido: Live
  Confianza: 95%

📹 Contenido del Manifest:
  • Video: SÍ
    - Capas/Perfiles: 3
    - Multikey: NO
    - Resoluciones:
      • 0.50 Mbps (640x360) @ 30fps
      • 1.00 Mbps (1280x720) @ 30fps
      • 2.00 Mbps (1920x1080) @ 30fps
  • Audio: SÍ
    - Audio 1: AAC, 2ch
  • Subtítulos: SÍ
  • Thumbnails: NO

============================================================
```

## Patrones de Detección Implementados

### DASH (MPD)

- **CPVR**: Contiene `/nPVR/` en la ruta
- **L7D**: `/live/` + parámetros `begin=` + `end=` + `movieId=`
- **Start Over**: `/live/` + parámetros `begin=` + `end=` (sin `movieId=`)
- **Live**: `/live/` sin parámetros `begin=` ni `end=`
- **VOD**: Sin `/live/` ni `/nPVR/`

## Análisis de Contenido (Fase 2)

Consulta [FASE2.md](FASE2.md) para información detallada sobre:
- Análisis de perfiles de video
- Detección de codificación de audio
- Identificación de Dolby Atmos
- Detección de Multikey
- Estructura de datos y APIs

## Tests

### Ejecutar Tests de Fase 1

```bash
python tests/test_manifest_types.py
```

### Ejecutar Tests de Fase 2

```bash
python tests/test_manifest_content.py
```

### Ejecutar Ejemplos de Fase 2

```bash
python examples_fase2.py
```

## Plan de Desarrollo

### Fase 1: Análisis de URL (✓ COMPLETADO)
- [x] Detección de tipo de manifest (MPD/HLS)
- [x] Identificación de tipo de contenido basado en patrones de URL
- [x] Validación con ejemplos reales
- [x] Interfaz gráfica amigable

### Fase 2: Análisis de Contenido (✓ COMPLETADO)
- [x] Descarga y parseo de contenido del manifest
- [x] Extracción de perfiles de video (capas, resoluciones, framerates)
- [x] Detección de audio (AAC, Dolby, Dolby Atmos)
- [x] Detección de subtítulos y thumbnails
- [x] Identificación de Multikey
- [x] Tests y ejemplos

### Fase 3: Soporte HLS (Próximamente)
- [ ] Análisis de manifests HLS (.m3u8)
- [ ] Extracción de información equivalente a DASH

### Fase 4: Características Avanzadas
- [ ] Validación de URLs
- [ ] Reconexión automática
- [ ] Análisis de segmentos
- [ ] Estadísticas en tiempo real

## Licencia

MIT

## Autor

Analizador Manifests Team
