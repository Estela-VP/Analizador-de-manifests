"""
Módulo principal para analizar manifests MPD y HLS
"""

from urllib.parse import urlparse, parse_qs
import re
from enum import Enum


class ContentType(Enum):
    """Tipos de contenido que puede tener un manifest"""
    LIVE = "Live"
    START_OVER = "Start Over"
    L7D = "L7D"
    CPVR = "CPVR"
    VOD = "VOD"
    UNKNOWN = "Unknown"


class ManifestAnalyzer:
    """Analizador de manifests MPD y HLS"""

    def __init__(self):
        self.content_type = ContentType.UNKNOWN
        self.manifest_url = None
        self.manifest_type = None  # 'mpd' o 'hls'

    def analyze(self, url: str) -> dict:
        """
        Analiza una URL de manifest y determina su tipo de contenido
        
        Args:
            url: URL del manifest (MPD o HLS)
            
        Returns:
            dict con información del manifest
        """
        self.manifest_url = url
        self._detect_manifest_type()
        self._identify_content_type()
        
        return {
            "url": url,
            "manifest_type": self.manifest_type,
            "content_type": self.content_type.value,
            "confidence": self._calculate_confidence()
        }

    def _detect_manifest_type(self) -> None:
        """Detecta si es MPD o HLS basado en la URL y extensión"""
        if self.manifest_url.endswith(".mpd"):
            self.manifest_type = "mpd"
        elif self.manifest_url.endswith(".m3u8"):
            self.manifest_type = "hls"
        elif ".mpd" in self.manifest_url:
            self.manifest_type = "mpd"
        elif ".m3u8" in self.manifest_url:
            self.manifest_type = "hls"
        else:
            # Intenta detectar por el contenido de la URL
            if "dash" in self.manifest_url.lower():
                self.manifest_type = "mpd"
            elif "hls" in self.manifest_url.lower():
                self.manifest_type = "hls"
            else:
                self.manifest_type = "unknown"

    def _identify_content_type(self) -> None:
        """
        Identifica el tipo de contenido basado en patrones de URL
        Orden de evaluación: CPVR > Last 7 Days > Start Over > Live > VOD
        """
        url_lower = self.manifest_url.lower()
        parsed_url = urlparse(self.manifest_url)
        query_params = parse_qs(parsed_url.query)

        # 1. CPVR: Contiene "/nPVR/" en la ruta
        if "/npvr/" in url_lower:
            self.content_type = ContentType.CPVR
            return

        # 2. Si contiene "/live/" evaluamos start-over, L7D o live
        if "/live/" in url_lower:
            # L7D: tiene begin + end + movieId
            if self._has_param(query_params, "movieid"):
                self.content_type = ContentType.L7D
                return
            
            # Start Over: tiene begin + end pero NO movieId
            if (self._has_param(query_params, "begin") and 
                self._has_param(query_params, "end")):
                self.content_type = ContentType.START_OVER
                return
            
            # Live: tiene /live/ pero sin parámetros begin/end
            self.content_type = ContentType.LIVE
            return

        # 3. VOD: No tiene /live/ ni /nPVR/
        self.content_type = ContentType.VOD

    def _has_param(self, query_params: dict, param_name: str) -> bool:
        """
        Verifica si un parámetro existe en los parámetros de query (case-insensitive)
        
        Args:
            query_params: Diccionario de parámetros de query
            param_name: Nombre del parámetro a buscar
            
        Returns:
            True si el parámetro existe y no está vacío
        """
        param_lower = param_name.lower()
        # Buscar el parámetro sin importar mayúsculas/minúsculas
        for key in query_params.keys():
            if key.lower() == param_lower:
                return bool(query_params[key])
        return False

    def _calculate_confidence(self) -> float:
        """
        Calcula el nivel de confianza del análisis (0-1)
        Basado en la cantidad de patrones coincidentes encontrados
        """
        # Por ahora, retorna una confianza fija
        # En el futuro se puede mejorar con análisis más complejos
        return 0.95 if self.content_type != ContentType.UNKNOWN else 0.3
