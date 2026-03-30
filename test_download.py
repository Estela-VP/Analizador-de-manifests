#!/usr/bin/env python3
"""
Script de prueba para verificar que la descarga de manifests funciona
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from analizador_manifests.analyzer import ManifestAnalyzer

def test_url_download(url: str):
    """Intenta descargar y analizar un manifest de una URL real"""
    print(f"\n{'='*70}")
    print(f"Intentando descargar y analizar: {url}")
    print(f"{'='*70}\n")
    
    analyzer = ManifestAnalyzer()
    
    try:
        result = analyzer.analyze(url, download_content=True)
        
        print(f"✓ Análisis completado")
        print(f"  • Tipo: {result['manifest_type'].upper()}")
        print(f"  • Contenido: {result['content_type']}")
        print(f"  • Confianza: {result['confidence']:.0%}")
        
        if "content" in result:
            content = result["content"]
            
            if content.get("error"):
                print(f"\n⚠️  Error en descarga:")
                print(f"  {content['error']}")
            else:
                print(f"\n✓ Contenido analizado exitosamente:")
                print(f"  • Video: {'✓' if content['has_video'] else '✗'}")
                print(f"  • Audio: {'✓' if content['has_audio'] else '✗'}")
                print(f"  • Subtítulos: {'✓' if content['has_subtitles'] else '✗'}")
                print(f"  • Thumbnails: {'✓' if content['has_thumbnails'] else '✗'}")
                print(f"  • Multikey: {'✓' if content['is_multikey'] else '✗'}")
                
                if content.get('video_profiles'):
                    print(f"  • Capas de video: {content['num_video_layers']}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n" + "="*70)
    print("PRUEBA DE DESCARGA DE MANIFESTS")
    print("="*70)
    
    # Ejemplos de URLs públicas conocidas (ajusta según disponibilidad)
    urls_to_test = [
        # Ejemplo: agrega aquí URLs que quieras probar
        # "https://example.com/manifest.mpd",
    ]
    
    if not urls_to_test:
        print("\n📝 INSTRUCCIONES:")
        print("1. Edita este archivo y agrega URLs de manifests en la lista 'urls_to_test'")
        print("2. Las URLs deben ser accesibles y devolver un XML válido")
        print("3. Ejecuta el script para probar la descarga")
        print("\nEjemplo:")
        print('  urls_to_test = [')
        print('      "https://example.com/stream.mpd",')
        print('      "https://example.com/live.m3u8",')
        print('  ]')
        print("\n💡 Notas:")
        print("  • El script ahora soporta certificados SSL autofirmados")
        print("  • Timeout de 10 segundos por descarga")
        print("  • Manejo robusto de errores HTTP y de conexión")
    else:
        success_count = 0
        for url in urls_to_test:
            if test_url_download(url):
                success_count += 1
        
        print(f"\n{'='*70}")
        print(f"Resultados: {success_count}/{len(urls_to_test)} exitosos")
        print(f"{'='*70}\n")
