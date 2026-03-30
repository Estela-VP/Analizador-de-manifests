#!/usr/bin/env python3
"""
Test para verificar que framerates como "25/56" se filtran correctamente
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent / "src"))

from analizador_manifests.analyzer import ManifestAnalyzer

# Manifest MPD con framerates inválidos
MPD_WITH_INVALID_FRAMERATES = """<?xml version="1.0" encoding="UTF-8"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011" minBufferTime="PT1.5S" type="static">
  <Period>
    <AdaptationSet id="1" contentType="video" frameRate="25/56">
      <Representation id="video_1" bandwidth="500000" codecs="avc1.4d401e" width="640" height="360"/>
      <Representation id="video_2" bandwidth="1000000" codecs="avc1.4d401e" width="1280" height="720" frameRate="30"/>
      <Representation id="video_3" bandwidth="2000000" codecs="avc1.4d401e" width="1920" height="1080" frameRate="50/60"/>
    </AdaptationSet>
    <AdaptationSet id="2" contentType="audio">
      <Representation id="audio_1" bandwidth="128000" codecs="mp4a.40.2" audioSamplingRate="48000"/>
    </AdaptationSet>
  </Period>
</MPD>
"""

def test_framerate_validation():
    """Prueba que framerates inválidos como "25/56" se filtran"""
    print("\n" + "="*70)
    print("TEST: Validación de Framerates")
    print("="*70 + "\n")
    
    analyzer = ManifestAnalyzer()
    
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.__enter__.return_value.read.return_value = MPD_WITH_INVALID_FRAMERATES.encode('utf-8')
        mock_urlopen.return_value = mock_response
        
        result = analyzer.analyze("https://example.com/manifest.mpd", download_content=True)
    
    if "content" in result:
        content = result["content"]
        
        print("Manifest con framerates inválidos:")
        print("  • AdaptationSet: frameRate=\"25/56\" (DEBE IGNORARSE)")
        print("  • Representation 1: Sin frameRate")
        print("  • Representation 2: frameRate=\"30\" (VÁLIDO)")
        print("  • Representation 3: frameRate=\"50/60\" (DEBE IGNORARSE)\n")
        
        print("✓ Resultados después del filtrado:\n")
        
        video_profiles = content.get("video_profiles", [])
        print(f"  Total de capas después del filtrado: {len(video_profiles)}")
        
        for i, profile in enumerate(video_profiles, 1):
            framerate = profile.get("framerate")
            bandwidth = profile["bandwidth"] / 1_000_000
            
            print(f"  Capa {i}: {bandwidth:.2f} Mbps - Framerate = {framerate} fps")
        
        print("\n" + "="*70)
        
        # Verificar que solo las capas válidas se mantienen
        if len(video_profiles) == 1 and video_profiles[0]["framerate"] == "30":
            print("\n✓ TEST PASADO: Solo se incluye la capa con framerate válido (30 fps)")
            print("  Las capas sin framerate o con formato inválido se filtraron correctamente")
        else:
            print(f"\n❌ TEST FALLÓ: Se esperaba 1 capa con framerate='30', pero se encontraron {len(video_profiles)} capas")

if __name__ == "__main__":
    test_framerate_validation()
