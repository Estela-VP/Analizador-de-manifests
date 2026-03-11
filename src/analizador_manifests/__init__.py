"""
Analizador de Manifests MPD y HLS
Identifica el tipo de contenido (Live, Start Over, Last 7 Days, CPVR, VOD) desde una URL
"""

__version__ = "0.1.0"
__author__ = "Analizador Manifests"

from .analyzer import ManifestAnalyzer

__all__ = ["ManifestAnalyzer"]
