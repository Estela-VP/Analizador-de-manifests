"""
Interfaz CLI para el analizador de manifests
"""

import sys
import argparse
from .analyzer import ManifestAnalyzer


def main():
    """Función principal de la CLI"""
    parser = argparse.ArgumentParser(
        description="Analizador de Manifests MPD y HLS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python -m analizador_manifests https://example.com/stream.mpd
  python -m analizador_manifests --url "https://example.com/live.m3u8"
        """
    )
    
    parser.add_argument(
        "url",
        nargs="?",
        help="URL del manifest (MPD o HLS)"
    )
    parser.add_argument(
        "--url",
        dest="url_arg",
        help="URL del manifest (alternativa)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Mostrar información detallada"
    )
    
    args = parser.parse_args()
    
    # Obtener URL
    url = args.url or args.url_arg
    if not url:
        parser.print_help()
        return 1
    
    # Analizar manifest
    analyzer = ManifestAnalyzer()
    result = analyzer.analyze(url)
    
    # Mostrar resultado
    if args.verbose:
        print("\n=== Análisis de Manifest ===")
        print(f"URL: {result['url']}")
        print(f"Tipo de Manifest: {result['manifest_type']}")
        print(f"Tipo de Contenido: {result['content_type']}")
        print(f"Confianza: {result['confidence']:.0%}")
    else:
        print(f"{result['content_type']}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
