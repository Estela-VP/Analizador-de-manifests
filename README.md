# Analizador de Manifests MPD y HLS

Herramienta CLI para analizar manifests de DASH (.mpd) y HLS (.m3u8) e identificar el tipo de contenido.

## Tipos de Contenido Soportados

- **Live**: Transmisión en vivo
- **Start Over**: Permite reiniciar desde el principio
- **Last Seven Days**: Ventana deslizante de 7 días (Catch-up TV)
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

Simplemente:
1. Pega la URL del manifest en el campo de entrada
2. Haz clic en "Analizar"
3. Verás el tipo de manifest, tipo de contenido y nivel de confianza

### Modo Línea de Comandos (CLI)

#### Modo Básico

```bash
python -m analizador_manifests "https://example.com/stream.mpd"
```

#### Modo Verbose

```bash
python -m analizador_manifests "https://example.com/stream.mpd" --verbose
```

o

```bash
python -m analizador_manifests "https://example.com/stream.mpd" -v
```

## Ejemplos

### GUI

```bash
# Ejecutar la interfaz gráfica
python run_gui.py
```

### CLI

```bash
# Analizar un manifest DASH
python -m analizador_manifests "https://example.com/live.mpd"

# Analizar un manifest HLS
python -m analizador_manifests "https://example.com/hls/live.m3u8" -v

# Usar como parámetro nombrado
python -m analizador_manifests --url "https://example.com/vod.mpd"
```

## Patrones de Detección Implementados

### DASH (MPD)

- **CPVR**: Contiene `/nPVR/` en la ruta
- **L7D**: `/live/` + parámetros `begin=` + `end=` + `movieId=`
- **Start Over**: `/live/` + parámetros `begin=` + `end=` (sin `movieId=`)
- **Live**: `/live/` sin parámetros `begin=` ni `end=`
- **VOD**: Sin `/live/` ni `/nPVR/`

## Plan de Desarrollo

### Fase 1: Análisis de URL (COMPLETADO)
- [x] Detección de tipo de manifest (MPD/HLS)
- [x] Identificación de tipo de contenido basado en patrones de URL
- [x] Validación con ejemplos reales de Telefónica
- [x] Interfaz gráfica (GUI) amigable con PySimpleGUI

### Fase 2: Análisis de Contenido
- [ ] Descargar y parsear contenido real del manifest
- [ ] Validar identidad mediante análisis del archivo XML/M3U8
- [ ] Extraer metadata adicional

### Fase 3: Características Avanzadas
- [ ] Análisis de segmentos
- [ ] Validación de URLs
- [ ] Estadísticas de disponibilidad
- [ ] Interfaz web (opcional)

## Licencia

MIT

## Autor

Analizador Manifests Team
