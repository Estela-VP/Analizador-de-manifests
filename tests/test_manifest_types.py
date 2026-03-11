"""
Tests para verificar la detección de tipos de manifests
"""

import sys
from pathlib import Path

# Agregar src al path para importar el módulo
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from analizador_manifests.analyzer import ManifestAnalyzer, ContentType


class TestManifestDetection:
    """Tests para la detección de tipos de contenido"""

    def test_live_dash(self):
        """Prueba detección de Live en DASH"""
        url = "https://b791-p1-h73-ag36qr8h-n1-te89de0.1.cdncert.telefonica.com/_791/_-_eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlkyUnVPakUzTmpnek9VUXpOREk9In0.eyJpYXQiOjE3NzMxMzA5OTgsInVpcCI6IiIsInVpZCI6IktaUHVHWTI2aWlNSFBKZ3M1Y0ViTlBJMTBsdGhLQnVVSHlmdmxEQXFLVzAiLCJ3bCI6ZmFsc2V9.7EfzmqH3VJyTC2pmYKQb_G2OKtrhX86AiUWnqv0HbocXOsyRccM1SqF3qJAigYdN7wCO5p8xYZbJWrEZrYTsGA_-_/live/KiKA/Dashavc/KiKA.mpd"
        analyzer = ManifestAnalyzer()
        result = analyzer.analyze(url)
        assert result["content_type"] == ContentType.LIVE.value
        assert result["manifest_type"] == "mpd"
        print("✓ Live DASH detectado correctamente")

    def test_start_over_dash(self):
        """Prueba detección de Start Over en DASH"""
        url = "https://b790-p1-h49-ag3qqr8h-n1-t7b3d1c.1.cdncert.telefonica.com/_790/_-_eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlkyUnVPakUzTmpnek9VUXpOREk9In0.eyJpYXQiOjE3NzMxMzA5OTgsInVpcCI6IiIsInVpZCI6IktaUHVHWTI2aWlNSFBKZ3M1Y0ViTlBJMTBsdGhLQnVVSHlmdmxEQXFLVzAiLCJ3bCI6ZmFsc2V9.7EfzmqH3VJyTC2pmYKQb_G2OKtrhX86AiUWnqv0HbocXOsyRccM1SqF3qJAigYdN7wCO5p8xYZbJWrEZrYTsGA_-_/live/ONE/Dashavc/ONE.mpd?begin=2026-03-10T07:40:00Z&end=2026-03-10T16:30:00Z&gvpPodType=2&tcdn-bitrate-filter=O2LIVE&t=1773131110091"
        analyzer = ManifestAnalyzer()
        result = analyzer.analyze(url)
        assert result["content_type"] == ContentType.START_OVER.value
        assert result["manifest_type"] == "mpd"
        print("✓ Start Over DASH detectado correctamente")

    def test_l7d_dash(self):
        """Prueba detección de L7D en DASH"""
        url = "https://b790.cdncert.telefonica.com/790/_-_eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlkyUnVPakUzTmpnek9VUXpOREk9In0.eyJpYXQiOjE3NzMxMzA5OTgsInVpcCI6IiIsInVpZCI6IktaUHVHWTI2aWlNSFBKZ3M1Y0ViTlBJMTBsdGhLQnVVSHlmdmxEQXFLVzAiLCJ3bCI6ZmFsc2V9.7EfzmqH3VJyTC2pmYKQb_G2OKtrhX86AiUWnqv0HbocXOsyRccM1SqF3qJAigYdN7wCO5p8xYZbJWrEZrYTsGA_-_/live/ONE/Dashavc/ONE.mpd?begin=2026-03-09T19:15:00Z&end=2026-03-09T20:45:00Z&gvpPodType=2&tcdn-bitrate-filter=O2LIVE&movieId=27455513"
        analyzer = ManifestAnalyzer()
        result = analyzer.analyze(url)
        assert result["content_type"] == ContentType.L7D.value
        assert result["manifest_type"] == "mpd"
        print("✓ L7D DASH detectado correctamente")

    def test_cpvr_dash(self):
        """Prueba detección de CPVR en DASH"""
        url = "https://b795-p1-hea-ag3qqr8h-n1-t414e1e.1.cdncert.telefonica.com/_795/_-_eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlkyUnVPakUzTmpnek9VUXpOREk9In0.eyJpYXQiOjE3NzMxMzA5OTgsInVpcCI6IiIsInVpZCI6IktaUHVHWTI2aWlNSFBKZ3M1Y0ViTlBJMTBsdGhLQnVVSHlmdmxEQXFLVzAiLCJ3bCI6ZmFsc2V9.7EfzmqH3VJyTC2pmYKQb_G2OKtrhX86AiUWnqv0HbocXOsyRccM1SqF3qJAigYdN7wCO5p8xYZbJWrEZrYTsGA_-_/nPVR/152703/Dashavc-HighDefinition/Manifest.mpd"
        analyzer = ManifestAnalyzer()
        result = analyzer.analyze(url)
        assert result["content_type"] == ContentType.CPVR.value
        assert result["manifest_type"] == "mpd"
        print("✓ CPVR DASH detectado correctamente")

    def test_vod_dash(self):
        """Prueba detección de VOD en DASH"""
        url = "https://b413.cdncert.telefonica.com/413/_-_eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlkyUnVPakUzTmpnek9VUXpOREk9In0.eyJpYXQiOjE3NzMxMzE0NjAsInVpcCI6IiIsInVpZCI6IktaUHVHWTI2aWlNSFBKZ3M1Y0ViTlBJMTBsdGhLQnVVSHlmdmxEQXFLVzAiLCJ3bCI6ZmFsc2V9.vNtvxlv1UuJjZ1w4k2Kwom_7AgezAY9vb_SEUFq3kIWrDWxlrdHuudwg388DoZ7084TpeZiK7EqdVGE5mTp8gw_-_/00/75/70/75708905_B5A381779755D3A7/PR_4K_SDR_AM_169__9d8994e856e44c8d.mpd"
        analyzer = ManifestAnalyzer()
        result = analyzer.analyze(url)
        assert result["content_type"] == ContentType.VOD.value
        assert result["manifest_type"] == "mpd"
        print("✓ VOD DASH detectado correctamente")


    def test_live_hls(self):
        """Prueba detección de Live en HLS"""
        url = "https://b1108.cdncert.telefonica.com/1108/_-_eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlkyUnVPakUzTmpnek9UUXpOREk9In0.eyJpYXQiOjE3NzMxMzI1NjMsInVpcCI6Ijg4LjI2Ljg3LjE3MiIsInVpZCI6InFVZEQ4X25SbnB1dDdVNWFfYkpOWkI5VzZTdk9VTmhwREJjUl9DdHlQZ3JScXpfVVkzdTVBZEJVb09WcXYyRERSdi1mdy1YbTgweG4tSE1wM1VTQ0dBIiwiYWNjIjoiZXZvbHRlYyIsImRpZCI6IjY0RjhGQzkxLTBFQUEtNDU2Ni04MTgyLTU4MUMzODBCNEI5MiIsImR0IjoiMzEwIiwid2wiOmZhbHNlfQ.WuWAUbLsnNQqXr7etPmINRAuLb0k2g6tcvo0d0iFgnp8iIkqT9h0rmDhsh2P7vx5ryEu0oRR9nhUdYQ-JoTfeg_-_/live/NEA427_CI_S/cpix-Hls/NEA427_CI_S.m3u8"
        analyzer = ManifestAnalyzer()
        result = analyzer.analyze(url)
        assert result["content_type"] == ContentType.LIVE.value
        assert result["manifest_type"] == "hls"
        print("✓ Live HLS detectado correctamente")

    def test_start_over_hls(self):
        """Prueba detección de Start Over en HLS"""
        url = "https://b1108.cdncert.telefonica.com/1108/_-_eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlkyUnVPakUzTmpnek9UUXpOREk9In0.eyJpYXQiOjE3NzMxMzI4NjAsInVpcCI6Ijg4LjI2Ljg3LjE3MiIsInVpZCI6InFVZEQ4X25SbnB1dDdVNWFfYkpOWkI5VzZTdk9VTmhwREJjUl9DdHlQZ3JScXpfVVkzdTVBZEJVb09WcXYyRERSdi1mdy1YbTgweG4tSE1wM1VTQ0dBIiwiYWNjIjoiZXZvbHRlYyIsImRpZCI6IjY0RjhGQzkxLTBFQUEtNDU2Ni04MTgyLTU4MUMzODBCNEI5MiIsImR0IjoiMzEwIiwid2wiOmZhbHNlfQ.2LOYxrT5QiVTDCa5QFy1aMODvtHfnPgu1Pvw0-32aVMxwoEJTw21Q4Ukd6XbYT--yEp2LsP4SZ1qijzBaIonBw_-_/live/NEA427_CI_S/cpix-Hls/NEA427_CI_S.m3u8?begin=2026-03-09T08:48:55Z&end=2026-03-09T09:00:05Z&tcdn-bitrate-filter=NONE"
        analyzer = ManifestAnalyzer()
        result = analyzer.analyze(url)
        assert result["content_type"] == ContentType.START_OVER.value
        assert result["manifest_type"] == "hls"
        print("✓ Start Over HLS detectado correctamente")

    def test_l7d_hls(self):
        """Prueba detección de L7D en HLS"""
        url = "https://b1108.cdncert.telefonica.com/1108/_-_eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlkyUnVPakUzTmpnek9UUXpOREk9In0.eyJpYXQiOjE3NzMxMzI4NjAsInVpcCI6Ijg4LjI2Ljg3LjE3MiIsInVpZCI6InFVZEQ4X25SbnB1dDdVNWFfYkpOWkI5VzZTdk9VTmhwREJjUl9DdHlQZ3JScXpfVVkzdTVBZEJVb09WcXYyRERSdi1mdy1YbTgweG4tSE1wM1VTQ0dBIiwiYWNjIjoiZXZvbHRlYyIsImRpZCI6IjY0RjhGQzkxLTBFQUEtNDU2Ni04MTgyLTU4MUMzODBCNEI5MiIsImR0IjoiMzEwIiwid2wiOmZhbHNlfQ.2LOYxrT5QiVTDCa5QFy1aMODvtHfnPgu1Pvw0-32aVMxwoEJTw21Q4Ukd6XbYT--yEp2LsP4SZ1qijzBaIonBw_-_/live/NEA427_CI_S/cpix-Hls/NEA427_CI_S.m3u8?begin=2026-03-09T08:48:55Z&end=2026-03-09T09:00:05Z&tcdn-bitrate-filter=NONE&gvpPodType=2&movieId=27457093"
        analyzer = ManifestAnalyzer()
        result = analyzer.analyze(url)
        assert result["content_type"] == ContentType.L7D.value
        assert result["manifest_type"] == "hls"
        print("✓ L7D HLS detectado correctamente")

    def test_cpvr_hls(self):
        """Prueba detección de CPVR en HLS"""
        url = "http://b795.cdncert.telefonica.com/795/_-_eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlkyUnVPakUzTmpnek9UUXpOREk9In0.eyJpYXQiOjE3NzMxMzM3NDQsInVpcCI6IiIsInVpZCI6IjlUYVEtdzlTb0FrZ2ItXzI4OXd3WGtCaDgteWowZ1pJOTBqMFdERUlKQ0sxdE85OV94bHAwUzA0NnpsUXF0S2VhcFNRZ3U0VEgxR0JObG5IVXdCRTRBIiwid2wiOmZhbHNlfQ.pYOUsPFMnbbec1r0XUgLHuMnipYdFz5BCUmwauYCzKQFU47f5UKja605lnKb0yDdMZdd3Ikd1cJxIGcCV85AFw_-_/nPVR/148761/Hls-HighDefinition-Fairplay/index.m3u8"
        analyzer = ManifestAnalyzer()
        result = analyzer.analyze(url)
        assert result["content_type"] == ContentType.CPVR.value
        assert result["manifest_type"] == "hls"
        print("✓ CPVR HLS detectado correctamente")

    def test_vod_hls(self):
        """Prueba detección de VOD en HLS"""
        url = "http://b20.cdnprepro.telefonica.com/20/_-_eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlkyUnVPakUzTmpBNE56YzFOREk9In0.eyJpYXQiOjE3NjExMTk5MzAsInVpcCI6Ijg4LjI2LjEwMy4xNzEiLCJ1aWQiOiJxVWREOF9uUm5wdXQ3VTVhX2JKTlpCOVc2U3ZPVU5ocERCY1JfQ3R5UGdyUnF6X1VZM3U1QWRCVW9PVnF2MkREUnYtZnctWG04MHhuLUhNcDNVU0NHQSIsImFjYyI6ImV2b2x0ZWMiLCJkaWQiOiI2NEY4RkM5MS0wRUFBLTQ1NjYtODE4Mi01ODFDMzgwQjRCOTIiLCJkdCI6IjMxMCIsIndsIjpmYWxzZX0.NLYzMlU9nOttSXBxi8QD5sxcoGXjpIT3hmswMK3Xh5evqYawvlB4xt3bRMYLE9OzxGfCH4uTGDZIfe43425D6Q_-_/01/00/45/100455321_38E2653DF584BFCE/master.m3u8?tcdn-bitrate-filter=NONE"
        analyzer = ManifestAnalyzer()
        result = analyzer.analyze(url)
        assert result["content_type"] == ContentType.VOD.value
        assert result["manifest_type"] == "hls"
        print("✓ VOD HLS detectado correctamente")


if __name__ == "__main__":
    test = TestManifestDetection()
    # Pruebas DASH
    test.test_live_dash()
    test.test_start_over_dash()
    test.test_l7d_dash()
    test.test_cpvr_dash()
    test.test_vod_dash()
    # Pruebas HLS
    test.test_live_hls()
    test.test_start_over_hls()
    test.test_l7d_hls()
    test.test_cpvr_hls()
    test.test_vod_hls()
    print("\n✓ Todos los tests (DASH y HLS) pasaron correctamente")
