"""
Tests para análisis de contenido de manifests (Fase 2)
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Agregar src al path para importar el módulo
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from analizador_manifests.analyzer import (
    ManifestAnalyzer, ContentType, AudioCodecType, 
    VideoProfile, AudioProperties
)
from sample_manifests import (
    MPD_SIMPLE, MPD_DOLBY, MPD_DOLBY_ATMOS, 
    MPD_MULTIKEY, MPD_WITH_THUMBNAILS
)


class TestManifestContentAnalysis:
    """Tests para análisis de contenido de manifests"""

    def test_analyze_simple_mpd(self):
        """Prueba análisis de un MPD simple con video y audio"""
        analyzer = ManifestAnalyzer()
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.__enter__.return_value.read.return_value = MPD_SIMPLE.encode('utf-8')
            mock_urlopen.return_value = mock_response
            
            result = analyzer.analyze("https://example.com/manifest.mpd", download_content=True)
        
        assert result["manifest_type"] == "mpd"
        assert "content" in result
        assert result["content"]["has_video"] is True
        assert result["content"]["has_audio"] is True
        assert result["content"]["has_subtitles"] is True
        assert result["content"]["num_video_layers"] == 3  # 3 capas de video
        print("✓ Análisis de MPD simple correctamente")

    def test_video_profiles_extraction(self):
        """Prueba extracción de perfiles de video"""
        analyzer = ManifestAnalyzer()
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.__enter__.return_value.read.return_value = MPD_SIMPLE.encode('utf-8')
            mock_urlopen.return_value = mock_response
            
            result = analyzer.analyze("https://example.com/manifest.mpd", download_content=True)
        
        content = result["content"]
        assert len(content["video_profiles"]) == 3
        
        # Verificar que las capas están ordenadas por baudrate
        bandwidths = [vp["bandwidth"] for vp in content["video_profiles"]]
        assert 500000 in bandwidths
        assert 1000000 in bandwidths
        assert 2000000 in bandwidths
        
        # Verificar que se extrajo frameRate
        for profile in content["video_profiles"]:
            assert profile["framerate"] == "30"
        
        print("✓ Perfiles de video extraídos correctamente")

    def test_audio_aac_detection(self):
        """Prueba detección de audio AAC"""
        analyzer = ManifestAnalyzer()
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.__enter__.return_value.read.return_value = MPD_SIMPLE.encode('utf-8')
            mock_urlopen.return_value = mock_response
            
            result = analyzer.analyze("https://example.com/manifest.mpd", download_content=True)
        
        content = result["content"]
        assert len(content["audio_list"]) == 1
        assert content["audio_list"][0]["codec_type"] == "AAC"
        assert content["audio_list"][0]["codec"] == "mp4a.40.2"
        print("✓ Audio AAC detectado correctamente")

    def test_audio_dolby_detection(self):
        """Prueba detección de audio Dolby Digital"""
        analyzer = ManifestAnalyzer()
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.__enter__.return_value.read.return_value = MPD_DOLBY.encode('utf-8')
            mock_urlopen.return_value = mock_response
            
            result = analyzer.analyze("https://example.com/manifest.mpd", download_content=True)
        
        content = result["content"]
        assert len(content["audio_list"]) == 1
        assert content["audio_list"][0]["codec_type"] == "Dolby"
        assert content["audio_list"][0]["codec"] == "ec-3"
        print("✓ Audio Dolby detectado correctamente")

    def test_audio_dolby_atmos_detection(self):
        """Prueba detección de audio Dolby Atmos"""
        analyzer = ManifestAnalyzer()
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.__enter__.return_value.read.return_value = MPD_DOLBY_ATMOS.encode('utf-8')
            mock_urlopen.return_value = mock_response
            
            result = analyzer.analyze("https://example.com/manifest.mpd", download_content=True)
        
        content = result["content"]
        assert len(content["audio_list"]) == 1
        assert content["audio_list"][0]["codec_type"] == "Dolby"
        assert content["audio_list"][0]["is_atmos"] is True
        print("✓ Audio Dolby Atmos detectado correctamente")

    def test_multikey_detection(self):
        """Prueba detección de Multikey (múltiples contentType video)"""
        analyzer = ManifestAnalyzer()
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.__enter__.return_value.read.return_value = MPD_MULTIKEY.encode('utf-8')
            mock_urlopen.return_value = mock_response
            
            result = analyzer.analyze("https://example.com/manifest.mpd", download_content=True)
        
        content = result["content"]
        assert content["is_multikey"] is True
        print("✓ Multikey detectado correctamente")

    def test_thumbnails_detection(self):
        """Prueba detección de thumbnails"""
        analyzer = ManifestAnalyzer()
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.__enter__.return_value.read.return_value = MPD_WITH_THUMBNAILS.encode('utf-8')
            mock_urlopen.return_value = mock_response
            
            result = analyzer.analyze("https://example.com/manifest.mpd", download_content=True)
        
        content = result["content"]
        assert content["has_thumbnails"] is True
        print("✓ Thumbnails detectados correctamente")

    def test_url_type_detection_with_content(self):
        """Prueba que la detección de URL continúa funcionando con análisis de contenido"""
        analyzer = ManifestAnalyzer()
        
        # URL de Live
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.__enter__.return_value.read.return_value = MPD_SIMPLE.encode('utf-8')
            mock_urlopen.return_value = mock_response
            
            url = "https://example.com/live/KiKA/Dashavc/KiKA.mpd"
            result = analyzer.analyze(url, download_content=True)
        
        assert result["content_type"] == ContentType.LIVE.value
        assert result["manifest_type"] == "mpd"
        assert "content" in result
        print("✓ Detección de tipo de contenido combinada con análisis de contenido correctamente")

    def test_analysis_without_download(self):
        """Prueba análisis sin descargar contenido"""
        analyzer = ManifestAnalyzer()
        
        url = "https://example.com/manifest.mpd"
        result = analyzer.analyze(url, download_content=False)
        
        assert result["manifest_type"] == "mpd"
        assert "content" not in result  # No debe incluir contenido sin download
        print("✓ Análisis sin descarga funcionando correctamente")

    def test_hls_no_content_analysis(self):
        """Prueba que HLS no intenta análisis de contenido en fase 2"""
        analyzer = ManifestAnalyzer()
        
        url = "https://example.com/manifest.m3u8"
        result = analyzer.analyze(url, download_content=True)
        
        assert result["manifest_type"] == "hls"
        assert "content" not in result  # No debe incluir contenido para HLS en fase 2
        print("✓ HLS no intenta análisis de contenido correctamente")


if __name__ == "__main__":
    test_suite = TestManifestContentAnalysis()
    
    print("\n" + "="*60)
    print("TESTS DE FASE 2: ANÁLISIS DE CONTENIDO")
    print("="*60 + "\n")
    
    test_suite.test_analyze_simple_mpd()
    test_suite.test_video_profiles_extraction()
    test_suite.test_audio_aac_detection()
    test_suite.test_audio_dolby_detection()
    test_suite.test_audio_dolby_atmos_detection()
    test_suite.test_multikey_detection()
    test_suite.test_thumbnails_detection()
    test_suite.test_url_type_detection_with_content()
    test_suite.test_analysis_without_download()
    test_suite.test_hls_no_content_analysis()
    
    print("\n" + "="*60)
    print("✓ TODOS LOS TESTS DE FASE 2 PASARON")
    print("="*60)
