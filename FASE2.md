# Fase 2: Análisis de Contenido del Manifest

## Descripción General

Fase 2 implementa análisis profundo del contenido del manifest, extrayendo información detallada sobre:
- **Perfiles de Video**: Capas/calidades, resoluciones, framerates y bandwidths
- **Codificación de Audio**: Detección de AAC, Dolby Digital y Dolby Atmos
- **Contenido Complementario**: Subtítulos, Thumbnails
- **Identificación de Multikey**: Detección de múltiples codificaciones de video

## Características Implementadas

### 1. Análisis de AdaptationSets
El parser XML identifica todos los `AdaptationSet` en el manifest MPD y clasifica por tipo de contenido:
- **contentType="video"**: Información sobre perfiles de video
- **contentType="audio"**: Detección de codec y tipo de audio
- **contentType="text"**: Presencia de subtítulos
- **contentType="image"**: Presencia de thumbnails

### 2. Perfiles de Video
Para cada video `Representation`, se extrae:
- **Bandwidth**: Bitrate en bps, indicando la capa/calidad (Ej: 500k, 1M, 2M)
- **Resolución**: Ancho y alto en píxeles
- **Framerate**: FPS (frames por segundo)
- **Codec**: Información del codec de video

**Ejemplo:**
```
Capas/Perfiles: 3
Resoluciones:
  • 0.50 Mbps (640x360) @ 30fps
  • 1.00 Mbps (1280x720) @ 30fps
  • 2.00 Mbps (1920x1080) @ 30fps
```

### 3. Detección de Audio
Análisis automático del codec de audio basado en la etiqueta `codecs`:

#### AAC (Advanced Audio Codec)
- Patrón: `codecs="mp4a.40.2"`
- Uso común: Streaming de audio estándar

#### Dolby Digital (Dolby Atmos compatible)
- Patrón: `codecs="ec-3"` o `codecs="ac-3"`
- Identificación de Dolby Atmos: Busca etiqueta `SupplementalProperty` con `value="JOC"`

**Ejemplo Dolby Atmos en XML:**
```xml
<AdaptationSet id="2" contentType="audio">
  <Representation id="audio_1" bandwidth="192000" codecs="ec-3"/>
  <AudioChannelConfiguration schemeIdUri="urn:mpeg:mpegB:cicp:ChannelConfiguration" value="F801"/>
  <SupplementalProperty schemeIdUri="urn:dolby:dash:audio_channel_configuration:2011" value="JOC"/>
</AdaptationSet>
```

### 4. Multikey Detection
Detecta si el manifest contiene múltiples `AdaptationSet` con `contentType="video"`.
- Indica uso de diferentes codificadores (Ej: H.264 y H.265)
- Permite al cliente elegir el mejor perfil según sus capacidades

### 5. Identificación Automática de Perfiles de Streaming

El sistema identifica automáticamente el perfil de streaming basándose en las capas de video presentes en el manifest. Compara las resoluciones y framerates contra perfiles conocidos:

#### Perfiles LATAM (Basados en DIRECTV/Telefónica LATAM)
- **Cinema**: Máx. 1080p@29.97fps
  - Capas: (1080p, 720p, 576p, 432p, 270p) @ 29.97fps
- **Sport Simplified**: Máx. 720p@59.94fps
  - Capas: (720p@59.94, 720p@29.97, 576p@29.97, 432p@29.97, 270p@29.97)
- **Sport Premium**: Máx. 1080p@59.94fps
  - Capas: (1080p@59.94, 720p@59.94, 720p@29.97, 576p@29.97, 432p@29.97, 270p@29.97)
- **SD**: Máx. 576p@29.97fps
  - Capas: (1080p@59.94, 720p@29.97, 576p@29.97, 432p@29.97, 270p@29.97)

#### Perfiles Alemania (Telefónica O2) - Live, Start Over, L7D
- **HD-E1**: Máx. 720p@50fps
  - Capas: (720p@50, 720p@25, 540p@25, 360p@25)
- **HD-E2**: Máx. 1080p@25fps
  - Capas: (1080p@25, 720p@25, 540p@25, 360p@25)
- **HD-E3**: Máx. 1080p@50fps
  - Capas: (1080p@50, 720p@25, 540p@25, 360p@25)

**Algoritmo de Identificación:**
1. Extrae las capas (altura, fps) del manifest
2. Compara contra todos los perfiles conocidos (LATAM + GERMANY)
3. Cuenta intersecciones de capas coincidentes
4. Selecciona el perfil con mayor número de coincidencias
5. Si no hay coincidencias, marca como "Unknown"

**Ejemplo Output:**
```json
{
  "streaming_profile": "Cinema",
  "num_video_layers": 5,
  "video_profiles": [
    {"bandwidth": 2000000, "height": 1080, "width": 1920, "framerate": "29.97"},
    {"bandwidth": 1000000, "height": 720, "width": 1280, "framerate": "29.97"},
    ...
  ]
}
```

### 6. Descarga y Parseo de XML
- Descarga automática del manifest MPD desde la URL
- Parseo robusto de XML con namespace support
- Fallback a parsing sin namespace para mayor compatibilidad
- Manejo de errores con mensajes descriptivos

## Nuevas Clases de Datos

### `AudioCodecType` (Enum)
```python
class AudioCodecType(Enum):
    AAC = "AAC"
    DOLBY = "Dolby"
    DOLBY_ATMOS = "Dolby Atmos"
    UNKNOWN = "Unknown"
```

### `StreamingProfile` (Enum)
```python
class StreamingProfile(Enum):
    # LATAM profiles
    CINEMA = "Cinema"
    SPORT_SIMPLIFIED = "Sport Simplified"
    SPORT_PREMIUM = "Sport Premium"
    SD = "SD"
    # Germany profiles
    GERMANY_HD_E1 = "Germany HD-E1"
    GERMANY_HD_E2 = "Germany HD-E2"
    GERMANY_HD_E3 = "Germany HD-E3"
    UNKNOWN = "Unknown"
```

### `VideoProfile` (Dataclass)
```python
@dataclass
class VideoProfile:
    bandwidth: int  # bits por segundo
    framerate: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    codec: Optional[str] = None
```

### `AudioProperties` (Dataclass)
```python
@dataclass
class AudioProperties:
    codec_type: AudioCodecType
    codec: Optional[str] = None
    channels: Optional[int] = None
    is_atmos: bool = False
```

### `AdaptationSetContent` (Dataclass)
Representa información sobre un AdaptationSet individual.

### `ManifestContent` (Dataclass)
Contiene toda la información análisis del contenido del manifest.

## Interfaz CLI - Nuevas Opciones

### Flag `--content` o `-c`
Habilita descarga y análisis del contenido XML.

### Flag `--json` o `-j`
Salida en formato JSON.

### Ejemplos de uso:

```bash
# Análisis de URL únicamente (Fase 1)
python -m analizador_manifests https://example.com/manifest.mpd

# Análisis con contenido (Fase 2)
python -m analizador_manifests https://example.com/manifest.mpd --content -v

# Salida JSON
python -m analizador_manifests https://example.com/manifest.mpd --content --json

# Con detalle verbose
python -m analizador_manifests "https://example.com/live/channel.mpd" -c -v
```

### Ejemplo de salida verbose:

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

## Interfaz GUI - Mejoras

1. **Checkbox "Analizar contenido"**: Permite habilitar/deshabilitar análisis de contenido
2. **Tab "Contenido"**: Muestra información detallada del contenido del manifest
3. **Visualización Mejorada**: 
   - Iconos para cada tipo de contenido (📹 Video, 🔊 Audio, 📄 Subtítulos, 🖼️ Thumbnails)
   - Perfiles de video en formato legible
   - Información de codec con detección de Atmos
4. **Threading**: Análisis en thread separado para no congelar la interfaz
5. **Status Updates**: Indicador de estado durante el análisis

## Modelos de Respuesta

### Análisis sin contenido (Fase 1):
```json
{
  "url": "https://...",
  "manifest_type": "mpd",
  "content_type": "Live",
  "confidence": 0.95
}
```

### Análisis con contenido (Fase 2):
```json
{
  "url": "https://...",
  "manifest_type": "mpd",
  "content_type": "Live",
  "confidence": 0.95,
  "content": {
    "has_video": true,
    "has_audio": true,
    "has_subtitles": true,
    "has_thumbnails": false,
    "is_multikey": false,
    "num_video_layers": 3,
    "video_profiles": [
      {
        "bandwidth": 500000,
        "framerate": "30",
        "width": 640,
        "height": 360,
        "codec": "avc1.4d401e"
      },
      ...
    ],
    "audio_list": [
      {
        "codec_type": "AAC",
        "codec": "mp4a.40.2",
        "channels": 2,
        "is_atmos": false
      }
    ],
    "adaptations_count": 3,
    "error": null
  }
}
```

## Tests

Los tests de Fase 2 están en `tests/test_manifest_content.py` y cubren:

✓ Análisis de MPD simple con video y audio
✓ Extracción de perfiles de video
✓ Detección de audio AAC
✓ Detección de audio Dolby Digital
✓ Detección de audio Dolby Atmos
✓ Detección de Multikey
✓ Detección de Thumbnails
✓ Compatibilidad con detección de URL
✓ Análisis sin descarga
✓ Comportamiento de HLS (sin análisis de contenido en Fase 2)

### Ejecutar tests:
```bash
python tests/test_manifest_content.py
```

## Limitaciones y Consideraciones

1. **Fase 2 solo para MPD**: El análisis de contenido actualmente solo funciona para manifests DASH (MPD). HLS (.m3u8) será implementado en futuras fases.
2. **Descargas**: Se requiere acceso a internet para descargar el manifest. Las URLs sin acceso directo pueden fallar.
3. **Timeouts**: La descarga tiene un timeout de 10 segundos para evitar cuelgues.
4. **Namespaces**: Soporta tanto MPD con namespace estándar como sin namespace.
5. **Errores graceful**: Si la descarga o parseo falla, se retorna información con el error descripto.

## Arquitectura del Código

```
analyzer.py
├── Enums
│   ├── ContentType (Fase 1)
│   ├── AudioCodecType (Fase 2)
│   └── StreamingProfile (Fase 2)
│
├── Data Classes (Fase 2)
│   ├── VideoProfile
│   ├── AudioProperties
│   ├── AdaptationSetContent
│   └── ManifestContent
│
├── ManifestAnalyzer
│   ├── Phase 1 Methods
│   │   ├── _detect_manifest_type()
│   │   ├── _identify_content_type()
│   │   └── _has_param()
│   │
│   └── Phase 2 Methods
│       ├── _download_manifest()
│       ├── _analyze_mpd_content()
│       ├── _process_adaptation_sets()
│       ├── _process_video_adaptation_set()
│       ├── _process_audio_adaptation_set()
│       ├── _detect_audio_codec_type()
│       ├── _detect_dolby_atmos()
│       ├── _identify_streaming_profile()
│       └── _manifest_content_to_dict()
```

## Próximas Fases

- **Fase 3**: Soporte completo para HLS (.m3u8) con análisis similar al MPD
- **Fase 4**: Validación de URLs y reconexión automática
- **Fase 5**: Análisis de segmentos y métricas en tiempo real
- **Fase 6**: Reportes detallados y exportación de datos
