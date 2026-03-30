#!/usr/bin/env python3
"""
Ejemplos de uso de la Fase 2: Análisis de Contenido
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from analizador_manifests.analyzer import ManifestAnalyzer

# Importar manifests de ejemplo
sys.path.insert(0, str(Path(__file__).parent / "tests"))
from sample_manifests import (
    MPD_SIMPLE, MPD_DOLBY_ATMOS, MPD_MULTIKEY, MPD_WITH_THUMBNAILS
)


def example_1_basic_analysis():
    """Ejemplo 1: Análisis básico - Solo URL"""
    print("\n" + "="*70)
    print("EJEMPLO 1: Análisis Básico (solo detección de URL)")
    print("="*70)
    
    analyzer = ManifestAnalyzer()
    url = "https://example.com/live/KiKA/Dashavc/KiKA.mpd"
    result = analyzer.analyze(url, download_content=False)
    
    print(f"URL: {result['url']}")
    print(f"Tipo de Manifest: {result['manifest_type'].upper()}")
    print(f"Tipo de Contenido: {result['content_type']}")
    print(f"Confianza: {result['confidence']:.0%}")


def example_2_content_analysis():
    """Ejemplo 2: Análisis de contenido - Descarga y parseo"""
    print("\n" + "="*70)
    print("EJEMPLO 2: Análisis de Contenido (con descarga)")
    print("="*70)
    
    analyzer = ManifestAnalyzer()
    
    # Mock de descarga para simular
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.__enter__.return_value.read.return_value = MPD_SIMPLE.encode('utf-8')
        mock_urlopen.return_value = mock_response
        
        url = "https://example.com/manifest.mpd"
        result = analyzer.analyze(url, download_content=True)
    
    print(f"URL: {result['url']}")
    print(f"Tipo de Manifest: {result['manifest_type'].upper()}")
    print(f"Tipo de Contenido: {result['content_type']}")
    
    if "content" in result:
        content = result["content"]
        print(f"\n📹 Información del Contenido:")
        print(f"  ├─ Video: {'✓' if content['has_video'] else '✗'}")
        print(f"  ├─ Audio: {'✓' if content['has_audio'] else '✗'}")
        print(f"  ├─ Subtítulos: {'✓' if content['has_subtitles'] else '✗'}")
        print(f"  ├─ Thumbnails: {'✓' if content['has_thumbnails'] else '✗'}")
        print(f"  └─ Multikey: {'✓' if content['is_multikey'] else '✗'}")
        
        # Mostrar capas de video
        if content.get("video_profiles"):
            print(f"\n  📊 Perfiles de Video ({content['num_video_layers']} capas):")
            for i, profile in enumerate(content["video_profiles"], 1):
                bw_mbps = profile["bandwidth"] / 1_000_000
                res = f"{profile.get('width')}x{profile.get('height')}" if profile.get('width') else "?"
                fps = profile.get("framerate", "?")
                print(f"    └─ Capa {i}: {bw_mbps:.2f} Mbps ({res}) @ {fps}fps")
        
        # Mostrar audio
        if content.get("audio_list"):
            print(f"\n  🔊 Configuración de Audio:")
            for i, audio in enumerate(content["audio_list"], 1):
                codec = audio.get("codec_type", "Unknown")
                atmos = " + Atmos" if audio.get("is_atmos") else ""
                print(f"    └─ Audio {i}: {codec}{atmos}")


def example_3_dolby_atmos():
    """Ejemplo 3: Detección de Dolby Atmos"""
    print("\n" + "="*70)
    print("EJEMPLO 3: Detección de Dolby Atmos")
    print("="*70)
    
    analyzer = ManifestAnalyzer()
    
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.__enter__.return_value.read.return_value = MPD_DOLBY_ATMOS.encode('utf-8')
        mock_urlopen.return_value = mock_response
        
        result = analyzer.analyze("https://example.com/manifest.mpd", download_content=True)
    
    if "content" in result:
        content = result["content"]
        print("Análisis de Manifest con Dolby Atmos:\n")
        
        if content.get("audio_list"):
            for i, audio in enumerate(content["audio_list"], 1):
                codec_type = audio.get("codec_type", "Unknown")
                is_atmos = audio.get("is_atmos", False)
                
                print(f"Audio {i}:")
                print(f"  ├─ Tipo de Codec: {codec_type}")
                print(f"  ├─ Codec: {audio.get('codec', 'N/A')}")
                print(f"  ├─ Canales: {audio.get('channels', 'N/A')}")
                print(f"  └─ Dolby Atmos: {'✓ SÍ' if is_atmos else '✗ NO'}")


def example_4_multikey():
    """Ejemplo 4: Detección de Multikey"""
    print("\n" + "="*70)
    print("EJEMPLO 4: Detección de Multikey (múltiples codificaciones)")
    print("="*70)
    
    analyzer = ManifestAnalyzer()
    
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.__enter__.return_value.read.return_value = MPD_MULTIKEY.encode('utf-8')
        mock_urlopen.return_value = mock_response
        
        result = analyzer.analyze("https://example.com/manifest.mpd", download_content=True)
    
    if "content" in result:
        content = result["content"]
        print("Análisis de Manifest Multikey:\n")
        print(f"Multikey Detectado: {'✓ SÍ' if content['is_multikey'] else '✗ NO'}")
        print(f"Total de AdaptationSets: {content['adaptations_count']}")
        
        print(f"\nEsto significa que hay 2 diferentes formas de codificar el video")
        print(f"en el mismo manifest, permitiendo que el cliente elija.")


def example_5_thumbnails():
    """Ejemplo 5: Detección de Thumbnails"""
    print("\n" + "="*70)
    print("EJEMPLO 5: Detección de Thumbnails")
    print("="*70)
    
    analyzer = ManifestAnalyzer()
    
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.__enter__.return_value.read.return_value = MPD_WITH_THUMBNAILS.encode('utf-8')
        mock_urlopen.return_value = mock_response
        
        result = analyzer.analyze("https://example.com/manifest.mpd", download_content=True)
    
    if "content" in result:
        content = result["content"]
        print("Análisis de Manifest con Thumbnails:\n")
        print(f"Video: {'✓' if content['has_video'] else '✗'}")
        print(f"Audio: {'✓' if content['has_audio'] else '✗'}")
        print(f"Subtítulos: {'✓' if content['has_subtitles'] else '✗'}")
        print(f"Thumbnails: {'✓' if content['has_thumbnails'] else '✗'} (para timeline preview)")


def example_6_verbose_output():
    """Ejemplo 6: Salida detallada (verbose)"""
    print("\n" + "="*70)
    print("EJEMPLO 6: Salida Verbose Completa")
    print("="*70)
    
    analyzer = ManifestAnalyzer()
    
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.__enter__.return_value.read.return_value = MPD_SIMPLE.encode('utf-8')
        mock_urlopen.return_value = mock_response
        
        result = analyzer.analyze(
            "https://b791-p1-h73-ag36qr8h-n1-te89de0/live/KiKA/Dashavc/KiKA.mpd",
            download_content=True
        )
    
    print(f"\n{'='*70}")
    print("ANÁLISIS DE MANIFEST")
    print(f"{'='*70}")
    
    print(f"\n📋 Información Básica:")
    print(f"  URL: {result['url']}")
    print(f"  Tipo: {result['manifest_type'].upper()}")
    print(f"  Contenido: {result['content_type']}")
    print(f"  Confianza: {result['confidence']:.0%}")
    
    if "content" in result:
        content = result["content"]
        print(f"\n📹 Contenido del Manifest:")
        
        if content.get('has_video'):
            print(f"  • Video: SÍ")
            print(f"    - Capas/Perfiles: {content['num_video_layers']}")
            print(f"    - Multikey: {'SÍ' if content['is_multikey'] else 'NO'}")
            
            if content.get("video_profiles"):
                print(f"    - Resoluciones:")
                for profile in content["video_profiles"]:
                    bw_mbps = profile["bandwidth"] / 1_000_000
                    res_str = f" ({profile['width']}x{profile['height']})" if profile.get('width') else ""
                    fps_str = f" @ {profile.get('framerate')}fps" if profile.get('framerate') else ""
                    print(f"      • {bw_mbps:.2f} Mbps{res_str}{fps_str}")
        else:
            print(f"  • Video: NO")
        
        if content.get('has_audio'):
            print(f"  • Audio: SÍ")
            for i, audio in enumerate(content["audio_list"], 1):
                codec_type = audio["codec_type"]
                if audio["is_atmos"]:
                    codec_type += " (Atmos)"
                channels = f", {audio['channels']}ch" if audio.get("channels") else ""
                print(f"    - Audio {i}: {codec_type}{channels}")
        else:
            print(f"  • Audio: NO")
        
        if content.get('has_subtitles'):
            print(f"  • Subtítulos: SÍ")
        
        if content.get('has_thumbnails'):
            print(f"  • Thumbnails: SÍ")
    
    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    print("\n🎬 FASE 2: EJEMPLOS DE ANÁLISIS DE CONTENIDO")
    print("="*70)
    
    example_1_basic_analysis()
    example_2_content_analysis()
    example_3_dolby_atmos()
    example_4_multikey()
    example_5_thumbnails()
    example_6_verbose_output()
    
    print("\n" + "="*70)
    print("✓ Ejemplos completados")
    print("="*70)
    print("\n📖 Para más información, ver FASE2.md")
    print("🎯 Próximas fases: HLS support, validación, streamlining, etc.\n")
