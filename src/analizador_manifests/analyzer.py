"""
Módulo principal para analizar manifests MPD y HLS
"""

from urllib.parse import urlparse, parse_qs
import re
from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
import xml.etree.ElementTree as ET
import urllib.request
import ssl


class ContentType(Enum):
    """Tipos de contenido que puede tener un manifest"""
    LIVE = "Live"
    START_OVER = "Start Over"
    L7D = "L7D"
    CPVR = "CPVR"
    VOD = "VOD"
    UNKNOWN = "Unknown"


class AudioCodecType(Enum):
    """Tipos de codificación de audio soportados"""
    AAC = "AAC"
    DOLBY = "Dolby"
    DOLBY_ATMOS = "Dolby Atmos"
    UNKNOWN = "Unknown"


class StreamingProfile(Enum):
    """Perfiles de streaming soportados para LATAM y GERMANY"""
    # LATAM profiles
    CINEMA = "Cinema"
    SPORT_SIMPLIFIED = "Sport Simplified"
    SPORT_PREMIUM = "Sport Premium"
    SD = "SD"
    # Germany profiles
    GERMANY_HD_E1 = "Germany HD-E1"
    GERMANY_HD_E2 = "Germany HD-E2"
    GERMANY_HD_E3 = "Germany HD-E3"
    UNKNOWN = "Unknown"


# Definición de perfiles de LATAM con sus capas típicas
# Formato: {resolución: bitrate_mbps, ...}
LATAM_PROFILES = {
    StreamingProfile.CINEMA: {
        (1080, 29.97): 2.0,
        (720, 29.97): 4.0,
        (576, 29.97): 1.8,
        (432, 29.97): 1.1,
        (270, 29.97): 0.5,
    },
    StreamingProfile.SPORT_SIMPLIFIED: {
        (720, 59.94): 2.0,
        (720, 29.97): 4.0,
        (576, 29.97): 1.8,
        (432, 29.97): 1.1,
        (270, 29.97): 0.5,
    },
    StreamingProfile.SPORT_PREMIUM: {
        (1080, 59.94): 15.0,
        (720, 59.94): 6.2,
        (720, 29.97): 4.0,
        (576, 29.97): 1.8,
        (432, 29.97): 1.1,
        (270, 29.97): 0.5,
    },
    StreamingProfile.SD: {
        (1080, 59.94): 15.0,
        (720, 29.97): 4.0,
        (576, 29.97): 1.8,
        (432, 29.97): 1.1,
        (270, 29.97): 0.5,
    }
}

# Definición de perfiles de GERMANY (Telefónica O2) con sus capas típicas
# HD-E1: Perfil básico para Live/Start Over/L7D (máx 720p@50)
# HD-E2: Perfil medio para Live/Start Over/L7D (máx 1080p@25)
# HD-E3: Perfil premium para Live/Start Over/L7D (máx 1080p@50)
GERMANY_PROFILES = {
    StreamingProfile.GERMANY_HD_E1: {
        (720, 50.0): 7.0,
        (720, 25.0): 3.0,
        (540, 25.0): 1.5,
        (360, 25.0): 0.7,
    },
    StreamingProfile.GERMANY_HD_E2: {
        (1080, 25.0): 7.0,
        (720, 25.0): 3.0,
        (540, 25.0): 1.5,
        (360, 25.0): 0.7,
    },
    StreamingProfile.GERMANY_HD_E3: {
        (1080, 50.0): 7.0,
        (720, 25.0): 3.0,
        (540, 25.0): 1.5,
        (360, 25.0): 0.7,
    }
}


@dataclass
class VideoProfile:
    """Información sobre un perfil de video"""
    bandwidth: int  # en bits por segundo
    framerate: Optional[str] = None  # ej: "30" o "25"
    width: Optional[int] = None
    height: Optional[int] = None
    codec: Optional[str] = None


@dataclass
class AudioProperties:
    """Información sobre propiedades de audio"""
    codec_type: AudioCodecType
    codec: Optional[str] = None
    channels: Optional[int] = None
    is_atmos: bool = False  # True si tiene JOC o Dolby Atmos


@dataclass
class AdaptationSetContent:
    """Información sobre un AdaptationSet"""
    content_type: str  # "video", "audio", "text", "image"
    id: Optional[str] = None
    # Video properties
    video_profiles: List[VideoProfile] = field(default_factory=list)
    # Audio properties
    audio_properties: Optional[AudioProperties] = None
    # Other properties
    language: Optional[str] = None
    mimetype: Optional[str] = None


@dataclass
class ManifestContent:
    """Información completa del contenido del manifest"""
    has_video: bool = False
    has_audio: bool = False
    has_subtitles: bool = False
    has_thumbnails: bool = False
    is_multikey: bool = False  # Si tiene múltiples contentType="video"
    
    video_profiles: List[VideoProfile] = field(default_factory=list)
    audio_list: List[AudioProperties] = field(default_factory=list)
    adaptation_sets: List[AdaptationSetContent] = field(default_factory=list)
    
    # Información adicional
    num_video_layers: int = 0  # Cantidad de capas de video
    streaming_profile: str = "Unknown"  # Perfil de streaming identificado (Cinema, Sport, etc)
    error: Optional[str] = None  # Error en caso de que haya


class ManifestAnalyzer:
    """Analizador de manifests MPD y HLS"""

    def __init__(self):
        self.content_type = ContentType.UNKNOWN
        self.manifest_url = None
        self.manifest_type = None  # 'mpd' o 'hls'
        self.manifest_content = ManifestContent()
        self.manifest_xml = None  # Contenido descargado del manifest

    def analyze(self, url: str, download_content: bool = True) -> dict:
        """
        Analiza una URL de manifest y determina su tipo de contenido
        
        Args:
            url: URL del manifest (MPD o HLS)
            download_content: Si True, intenta descargar y analizar el contenido
            
        Returns:
            dict con información del manifest
        """
        # Reinicializar estado para cada análisis (evita contaminar datos anteriores)
        self.manifest_content = ManifestContent()
        self.content_type = ContentType.UNKNOWN
        self.manifest_type = None
        self.manifest_xml = None
        
        self.manifest_url = url
        self._detect_manifest_type()
        self._identify_content_type()
        
        result = {
            "url": url,
            "manifest_type": self.manifest_type,
            "content_type": self.content_type.value,
            "confidence": self._calculate_confidence()
        }
        
        # Si se solicita análisis de contenido y es MPD, intenta descargar y parsear
        if download_content and self.manifest_type == "mpd":
            try:
                if self._download_manifest():
                    self._analyze_mpd_content()
                    result["content"] = self._manifest_content_to_dict()
            except Exception as e:
                self.manifest_content.error = str(e)
                result["content"] = self._manifest_content_to_dict()
        
        return result

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

    def _download_manifest(self) -> bool:
        """
        Descarga el contenido del manifest desde la URL
        
        Returns:
            True si la descarga fue exitosa, False en caso contrario
        """
        try:
            req = urllib.request.Request(
                self.manifest_url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            # Crear contexto SSL sin verificación (para certificados autofirmados)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
                self.manifest_xml = response.read().decode('utf-8')
            return True
        except urllib.error.URLError as e:
            self.manifest_content.error = f"Error de URL: {str(e)}"
            return False
        except urllib.error.HTTPError as e:
            self.manifest_content.error = f"Error HTTP {e.code}: {e.reason}"
            return False
        except Exception as e:
            self.manifest_content.error = f"Error descargando manifest: {str(e)}"
            return False

    def _analyze_mpd_content(self) -> None:
        """
        Analiza el contenido XML del manifest MPD y extrae información
        """
        if not self.manifest_xml:
            return
        
        try:
            root = ET.fromstring(self.manifest_xml)
            # El namespace típico de MPD
            namespace = {'mpd': 'urn:mpeg:dash:schema:mpd:2011'}
            
            # Buscar todos los AdaptationSets
            adaptation_sets = root.findall('.//mpd:AdaptationSet', namespace)
            if not adaptation_sets:
                # Intentar sin namespace
                adaptation_sets = root.findall('.//AdaptationSet')
            
            self._process_adaptation_sets(adaptation_sets, namespace)
            
        except Exception as e:
            self.manifest_content.error = f"Error analizando XML: {str(e)}"

    def _process_adaptation_sets(self, adaptation_sets: List[Any], namespace: Dict[str, str]) -> None:
        """
        Procesa los AdaptationSets encontrados en el manifest
        
        Args:
            adaptation_sets: Lista de elementos AdaptationSet
            namespace: Diccionario de namespaces XML
        """
        video_count = 0
        
        for ad_set in adaptation_sets:
            content_type_attr = ad_set.get('contentType', '')
            ad_set_id = ad_set.get('id', '')
            
            content_obj = AdaptationSetContent(
                content_type=content_type_attr or "unknown",
                id=ad_set_id,
                language=ad_set.get('lang'),
                mimetype=ad_set.get('mimeType')
            )
            
            if content_type_attr == 'video':
                self.manifest_content.has_video = True
                video_count += 1
                self._process_video_adaptation_set(ad_set, content_obj, namespace)
                self.manifest_content.video_profiles.extend(content_obj.video_profiles)
                
            elif content_type_attr == 'audio':
                self.manifest_content.has_audio = True
                self._process_audio_adaptation_set(ad_set, content_obj, namespace)
                if content_obj.audio_properties:
                    self.manifest_content.audio_list.append(content_obj.audio_properties)
                    
            elif content_type_attr == 'text':
                self.manifest_content.has_subtitles = True
                
            elif content_type_attr == 'image':
                self.manifest_content.has_thumbnails = True
            
            self.manifest_content.adaptation_sets.append(content_obj)
        
        # Detectar Multikey (más de un contentType="video")
        self.manifest_content.is_multikey = video_count > 1
        self.manifest_content.num_video_layers = len(self.manifest_content.video_profiles)
        
        # Identificar perfil de streaming basado en las capas de video
        self._identify_streaming_profile()

    def _process_video_adaptation_set(self, ad_set: Any, content_obj: AdaptationSetContent, 
                                      namespace: Dict[str, str]) -> None:
        """
        Procesa un AdaptationSet de video y extrae información de perfiles
        Solo incluye capas que tienen un framerate válido
        
        Args:
            ad_set: Elemento AdaptationSet
            content_obj: Objeto AdaptationSetContent a llenar
            namespace: Diccionario de namespaces XML
        """
        # Buscar todas las Representations dentro del AdaptationSet
        representations = ad_set.findall('.//mpd:Representation', namespace)
        if not representations:
            representations = ad_set.findall('.//Representation')
        
        for rep in representations:
            # Extraer y validar framerate primero
            framerate = self._validate_framerate(rep.get('frameRate') or ad_set.get('frameRate'))
            
            # Solo incluir capas con framerate válido
            if framerate is None:
                continue
            
            bandwidth_str = rep.get('bandwidth', '0')
            try:
                bandwidth = int(bandwidth_str)
            except ValueError:
                bandwidth = 0
            
            # Extraer dimensiones
            width = None
            height = None
            if 'width' in rep.attrib:
                try:
                    width = int(rep.get('width'))
                except ValueError:
                    pass
            if 'height' in rep.attrib:
                try:
                    height = int(rep.get('height'))
                except ValueError:
                    pass
            
            codec = rep.get('codecs') or ad_set.get('codecs')
            
            video_profile = VideoProfile(
                bandwidth=bandwidth,
                framerate=framerate,
                width=width,
                height=height,
                codec=codec
            )
            
            content_obj.video_profiles.append(video_profile)

    def _process_audio_adaptation_set(self, ad_set: Any, content_obj: AdaptationSetContent,
                                      namespace: Dict[str, str]) -> None:
        """
        Procesa un AdaptationSet de audio y detecta tipo de codec
        
        Args:
            ad_set: Elemento AdaptationSet
            content_obj: Objeto AdaptationSetContent a llenar
            namespace: Diccionario de namespaces XML
        """
        # Obtener codec del AdaptationSet o de las Representations
        codec_str = None
        
        representations = ad_set.findall('.//mpd:Representation', namespace)
        if not representations:
            representations = ad_set.findall('.//Representation')
        
        if representations:
            codec_str = representations[0].get('codecs') or ad_set.get('codecs')
        else:
            codec_str = ad_set.get('codecs')
        
        # Detectar tipo de codec
        audio_codec_type = self._detect_audio_codec_type(codec_str)
        
        # Detectar si es Dolby Atmos
        is_atmos = self._detect_dolby_atmos(ad_set, namespace)
        
        # Extraer número de canales si está disponible
        channels = None
        audio_channel_config = ad_set.find('.//mpd:AudioChannelConfiguration', namespace)
        if audio_channel_config is None:
            audio_channel_config = ad_set.find('.//AudioChannelConfiguration')
        
        if audio_channel_config is not None:
            # Primero intentar obtener del atributo 'channels'
            channels_attr = audio_channel_config.get('channels')
            if channels_attr:
                try:
                    channels = int(channels_attr)
                except ValueError:
                    pass
            else:
                # Si no está disponible, intentar del atributo 'value'
                channels_value = audio_channel_config.get('value', '')
                if channels_value:
                    try:
                        # El value puede ser un formato hexadecimal o campo de bits
                        # Para formato estándar como "F801" ignorar por ahora
                        # Solo tomar si es un número simple
                        channels = int(channels_value)
                    except ValueError:
                        pass
        
        audio_props = AudioProperties(
            codec_type=audio_codec_type,
            codec=codec_str,
            channels=channels,
            is_atmos=is_atmos
        )
        
        content_obj.audio_properties = audio_props

    def _detect_audio_codec_type(self, codec_str: Optional[str]) -> AudioCodecType:
        """
        Detecta el tipo de codec de audio basado en la cadena de codec
        
        Args:
            codec_str: Cadena de codec (ej: "mp4a.40.2", "ec-3")
            
        Returns:
            AudioCodecType detectado
        """
        if not codec_str:
            return AudioCodecType.UNKNOWN
        
        codec_lower = codec_str.lower()
        
        # AAC: mp4a.40.2 (típicamente)
        if 'mp4a' in codec_lower or 'aac' in codec_lower:
            return AudioCodecType.AAC
        
        # Dolby: ec-3, ac-3, etc.
        if 'ec-3' in codec_lower or 'ac-3' in codec_lower:
            return AudioCodecType.DOLBY
        
        return AudioCodecType.UNKNOWN

    def _detect_dolby_atmos(self, ad_set: Any, namespace: Dict[str, str]) -> bool:
        """
        Detecta si el audio es Dolby Atmos
        Busca AudioChannelConfiguration y/o SupplementalProperty con value="JOC"
        
        Args:
            ad_set: Elemento AdaptationSet
            namespace: Diccionario de namespaces XML
            
        Returns:
            True si se detecta Dolby Atmos, False en caso contrario
        """
        # Buscar SupplementalProperty con value="JOC"
        supp_properties = ad_set.findall('.//mpd:SupplementalProperty', namespace)
        if not supp_properties:
            supp_properties = ad_set.findall('.//SupplementalProperty')
        
        for prop in supp_properties:
            if prop.get('value', '').upper() == 'JOC':
                return True
        
        # Buscar AudioChannelConfiguration con schemeIdUri conteniendo JOC
        audio_channel_configs = ad_set.findall('.//mpd:AudioChannelConfiguration', namespace)
        if not audio_channel_configs:
            audio_channel_configs = ad_set.findall('.//AudioChannelConfiguration')
        
        for config in audio_channel_configs:
            scheme_id = config.get('schemeIdUri', '').upper()
            if 'JOC' in scheme_id:
                return True
        
        return False

    def _validate_framerate(self, framerate_str: Optional[str]) -> Optional[str]:
        """
        Valida que el framerate sea un número simple (no fracción como "25/56")
        
        Args:
            framerate_str: String con el framerate a validar
            
        Returns:
            El framerate si es válido, None si contiene "/" o es inválido
        """
        if not framerate_str:
            return None
        
        # Rechazar framerates con formato de fracción (Ej: "25/56")
        if '/' in framerate_str:
            return None
        
        # Intentar validar que sea un número válido
        try:
            float(framerate_str)
            return framerate_str
        except ValueError:
            return None

    def _identify_streaming_profile(self) -> None:
        """
        Identifica el perfil de streaming basándose en las capas de video
        Compara contra los perfiles conocidos de LATAM y GERMANY
        
        Actualiza: self.manifest_content.streaming_profile
        """
        if not self.manifest_content.video_profiles:
            self.manifest_content.streaming_profile = "Unknown"
            return
        
        # Crear conjunto de (resolución, framerate) del manifest para comparar
        manifest_layers = set()
        for profile in self.manifest_content.video_profiles:
            if profile.height and profile.framerate:
                try:
                    fps = float(profile.framerate)
                    manifest_layers.add((profile.height, fps))
                except (ValueError, TypeError):
                    pass
        
        if not manifest_layers:
            self.manifest_content.streaming_profile = "Unknown"
            return
        
        # Comparar contra cada perfil conocido (LATAM + GERMANY)
        best_match = StreamingProfile.UNKNOWN
        best_match_count = 0
        
        # Combinar ambos diccionarios de perfiles
        all_profiles = {**LATAM_PROFILES, **GERMANY_PROFILES}
        
        for profile_name, profile_layers in all_profiles.items():
            # Convertir capas del perfil a set de (height, fps)
            profile_set = set()
            for (height, fps), _ in profile_layers.items():
                profile_set.add((height, fps))
            
            # Contar cuántas capas coinciden
            matches = len(manifest_layers.intersection(profile_set))
            
            # Si este perfil coincide mejor, actualizamos
            if matches > best_match_count:
                best_match_count = matches
                best_match = profile_name
        
        self.manifest_content.streaming_profile = best_match.value

    def _manifest_content_to_dict(self) -> dict:
        """
        Convierte el objeto ManifestContent a un diccionario
        
        Returns:
            Diccionario con la información del contenido
        """
        return {
            "has_video": self.manifest_content.has_video,
            "has_audio": self.manifest_content.has_audio,
            "has_subtitles": self.manifest_content.has_subtitles,
            "has_thumbnails": self.manifest_content.has_thumbnails,
            "is_multikey": self.manifest_content.is_multikey,
            "num_video_layers": self.manifest_content.num_video_layers,
            "streaming_profile": self.manifest_content.streaming_profile,
            "video_profiles": [asdict(vp) for vp in self.manifest_content.video_profiles],
            "audio_list": [
                {
                    "codec_type": ap.codec_type.value,
                    "codec": ap.codec,
                    "channels": ap.channels,
                    "is_atmos": ap.is_atmos
                }
                for ap in self.manifest_content.audio_list
            ],
            "adaptations_count": len(self.manifest_content.adaptation_sets),
            "error": self.manifest_content.error
        }
