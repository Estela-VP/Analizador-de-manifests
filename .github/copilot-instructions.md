<!-- Use this file to provide workspace-specific custom instructions to Copilot. -->

# Analizador de Manifests MPD y HLS

## Contexto del Proyecto

Analizador CLI para identificar el tipo de contenido de manifests DASH (.mpd) y HLS (.m3u8).

**Lenguaje**: Python  
**Tipo**: CLI Application  
**Etapa**: Fase 1 - Análisis de URL

## Arquitectura

- `/src/analizador_manifests/analyzer.py`: Lógica principal de análisis
- `/src/analizador_manifests/cli.py`: Interfaz de línea de comandos
- `/src/analizador_manifests/__init__.py`: Punto de entrada del módulo

## Convenciones de Código

- Usar `ContentType` enum para tipos de contenido
- Métodos privados con prefijo `_`
- Docstrings en español (por ahora)
- Type hints en todas las funciones

## Patrones de Detección (DASH/MPD)

1. **CPVR**: `/nPVR/` en la URL
2. **L7D**: `/live/` + `begin=` + `end=` + `movieId=` (en query params)
3. **Start Over**: `/live/` + `begin=` + `end=` (sin `movieId=`)
4. **Live**: `/live/` sin parámetros `begin=`/`end=`
5. **VOD**: Sin `/live/` ni `/nPVR/`

Nota: Los parámetros de query son case-insensitive.

## Próximas Funcionalidades

1. Soporte para HLS (.m3u8) con patrones equivalentes
2. Implementar descarga y análisis de contenido real
3. Parser para XML (DASH) y M3U8
4. Validación de URLs antes de análisis

## Instrucciones para Copilot

- Mantener compatibilidad con Python 3.8+
- Evitar dependencias externas innecesarias
- Priorizar precisión en la detección
- Documentar cambios significativos
- Cuando se agreguen nuevos patrones, actualizar los tests en `tests/test_manifest_types.py`
