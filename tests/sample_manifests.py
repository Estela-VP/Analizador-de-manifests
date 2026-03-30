"""
Manifests de ejemplo para testing
"""

# MPD simple con video y audio
MPD_SIMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011" minBufferTime="PT1.5S" type="static" mediaPresentationDuration="PT10M0S" maxSegmentDuration="PT4S" profiles="urn:mpeg:dash:profile:isoff-live:2011">
  <Period start="PT0S">
    <AdaptationSet id="1" contentType="video" segmentAlignment="true" startWithSAP="1">
      <Representation id="video_1" bandwidth="500000" codecs="avc1.4d401e" width="640" height="360" frameRate="30"/>
      <Representation id="video_2" bandwidth="1000000" codecs="avc1.4d401e" width="1280" height="720" frameRate="30"/>
      <Representation id="video_3" bandwidth="2000000" codecs="avc1.4d401e" width="1920" height="1080" frameRate="30"/>
    </AdaptationSet>
    <AdaptationSet id="2" contentType="audio" segmentAlignment="true">
      <Representation id="audio_1" bandwidth="128000" codecs="mp4a.40.2" audioSamplingRate="48000"/>
    </AdaptationSet>
    <AdaptationSet id="3" contentType="text" lang="es">
      <Representation id="subtitle_1" bandwidth="1000" mimeType="application/ttml+xml"/>
    </AdaptationSet>
  </Period>
</MPD>
"""

# MPD con Dolby Digital
MPD_DOLBY = """<?xml version="1.0" encoding="UTF-8"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011" minBufferTime="PT1.5S" type="static">
  <Period>
    <AdaptationSet id="1" contentType="video">
      <Representation id="video_1" bandwidth="2000000" codecs="avc1.4d401e" width="1920" height="1080" frameRate="30"/>
    </AdaptationSet>
    <AdaptationSet id="2" contentType="audio">
      <Representation id="audio_1" bandwidth="128000" codecs="ec-3" audioSamplingRate="48000"/>
    </AdaptationSet>
  </Period>
</MPD>
"""

# MPD con Dolby Atmos
MPD_DOLBY_ATMOS = """<?xml version="1.0" encoding="UTF-8"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011" minBufferTime="PT1.5S" type="static">
  <Period>
    <AdaptationSet id="1" contentType="video">
      <Representation id="video_1" bandwidth="2000000" codecs="avc1.4d401e" width="1920" height="1080" frameRate="30"/>
    </AdaptationSet>
    <AdaptationSet id="2" contentType="audio">
      <Representation id="audio_1" bandwidth="192000" codecs="ec-3"/>
      <AudioChannelConfiguration schemeIdUri="urn:mpeg:mpegB:cicp:ChannelConfiguration" value="F801"/>
      <SupplementalProperty schemeIdUri="urn:dolby:dash:audio_channel_configuration:2011" value="JOC"/>
    </AdaptationSet>
  </Period>
</MPD>
"""

# MPD con múltiples video contentType (Multikey)
MPD_MULTIKEY = """<?xml version="1.0" encoding="UTF-8"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011" minBufferTime="PT1.5S" type="static">
  <Period>
    <AdaptationSet id="1" contentType="video">
      <Representation id="video_1" bandwidth="1000000" codecs="avc1.4d401e" width="1280" height="720" frameRate="30"/>
    </AdaptationSet>
    <AdaptationSet id="2" contentType="video">
      <Representation id="video_2" bandwidth="1000000" codecs="hev1.1.c.L93.b0" width="1280" height="720" frameRate="30"/>
    </AdaptationSet>
    <AdaptationSet id="3" contentType="audio">
      <Representation id="audio_1" bandwidth="128000" codecs="mp4a.40.2"/>
    </AdaptationSet>
  </Period>
</MPD>
"""

# MPD con thumbnails
MPD_WITH_THUMBNAILS = """<?xml version="1.0" encoding="UTF-8"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011" minBufferTime="PT1.5S" type="static">
  <Period>
    <AdaptationSet id="1" contentType="video">
      <Representation id="video_1" bandwidth="1000000" codecs="avc1.4d401e" width="1280" height="720"/>
    </AdaptationSet>
    <AdaptationSet id="2" contentType="audio">
      <Representation id="audio_1" bandwidth="128000" codecs="mp4a.40.2"/>
    </AdaptationSet>
    <AdaptationSet id="3" contentType="image">
      <Representation id="thumb_1" bandwidth="10000" mimeType="image/jpeg" width="160" height="90"/>
    </AdaptationSet>
  </Period>
</MPD>
"""
