"""
Interfaz CLI para el analizador de manifests
"""

import sys
import argparse
import json
from .analyzer import ManifestAnalyzer


def main():
    """Función principal de la CLI"""
    parser = argparse.ArgumentParser(
        description="Analizador de Manifests MPD y HLS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python -m analizador_manifests https://example.com/stream.mpd
  python -m analizador_manifests --url "https://example.com/live.m3u8" --content
  python -m analizador_manifests https://example.com/stream.mpd -v --content
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
    parser.add_argument(
        "--content",
        "-c",
        action="store_true",
        help="Analizar contenido del manifest (descargar y parsear XML)"
    )
    parser.add_argument(
        "--json",
        "-j",
        action="store_true",
        help="Mostrar resultado en formato JSON"
    )
    
    args = parser.parse_args()
    
    # Obtener URL
    url = args.url or args.url_arg
    if not url:
        parser.print_help()
        return 1
    
    # Analizar manifest
    analyzer = ManifestAnalyzer()
    result = analyzer.analyze(url, download_content=args.content)
    
    # Mostrar resultado
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    elif args.verbose:
        _print_verbose_result(result)
    else:
        print(f"{result['content_type']}")
    
    return 0


def _print_verbose_result(result: dict) -> None:
    """
    Imprime el resultado del análisis en formato verbose
    
    Args:
        result: Diccionario con los resultados del análisis
    """
    print("\n" + "="*60)
    print("ANÁLISIS DE MANIFEST")
    print("="*60)
    
    print(f"\n📋 Información Básica:")
    print(f"  URL: {result['url']}")
    print(f"  Tipo: {result['manifest_type'].upper()}")
    print(f"  Contenido: {result['content_type']}")
    print(f"  Confianza: {result['confidence']:.0%}")
    
    # Mostrar análisis de contenido si está disponible
    if "content" in result:
        content = result["content"]
        print(f"\n📹 Contenido del Manifest:")
        
        if content["has_video"]:
            print(f"  • Video: SÍ")
            print(f"    - Capas/Perfiles: {content['num_video_layers']}")
            print(f"    - Multikey: {'SÍ' if content['is_multikey'] else 'NO'}")
            if content.get("streaming_profile"):
                print(f"    - Perfil: {content['streaming_profile']}")
            
            if content["video_profiles"]:
                print(f"    - Resoluciones:")
                for profile in content["video_profiles"]:
                    res_str = ""
                    if profile.get("width") and profile.get("height"):
                        res_str = f" ({profile['width']}x{profile['height']})"
                    fps_str = f" @ {profile.get('framerate')}fps" if profile.get("framerate") else ""
                    bw_mbps = profile["bandwidth"] / 1_000_000
                    print(f"      • {bw_mbps:.2f} Mbps{res_str}{fps_str}")
        else:
            print(f"  • Video: NO")
        
        if content["has_audio"]:
            print(f"  • Audio: SÍ")
            for i, audio in enumerate(content["audio_list"], 1):
                codec_type = audio["codec_type"]
                if audio["is_atmos"]:
                    codec_type += " (Atmos)"
                channels = f", {audio['channels']}ch" if audio["channels"] else ""
                print(f"    - Audio {i}: {codec_type}{channels}")
        else:
            print(f"  • Audio: NO")
        
        if content["has_subtitles"]:
            print(f"  • Subtítulos: SÍ")
        
        if content["has_thumbnails"]:
            print(f"  • Thumbnails: SÍ")
        
        if content["error"]:
            print(f"\n⚠️  Error: {content['error']}")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    sys.exit(main())
