# Instrucciones de la Interfaz Gráfica

## Cómo usar la GUI

### Iniciando la aplicación

```bash
python run_gui.py
```

Se abrirá una ventana con la interfaz gráfica del analizador.

### Pasos para analizar un manifest

1. **Copiar la URL del manifest**
   - Copia la URL completa del manifest (MPD o HLS)
   - Ejemplo: `https://b790-p1-h49-ag3qqr8h-n1-t7b3d1c.1.cdncert.telefonica.com/...`

2. **Pegar en el campo de entrada**
   - Pega la URL en el campo de texto "URL del Manifest"
   - Puedes hacerlo con Ctrl+V o clic derecho > Pegar

3. **Hacer clic en "Analizar"**
   - O presionar Enter después de pegar la URL
   - La aplicación procesará la URL automáticamente

4. **Ver los resultados**
   - **Tipo de Manifest**: MPD o HLS
   - **Tipo de Contenido**: Live, Start Over, L7D, CPVR o VOD
   - **Confianza**: Porcentaje de confianza del análisis (0-100%)
   - **URL Analizada**: La URL completa que se procesó

### Botones disponibles

- **Analizar**: Procesa la URL introducida
- **Limpiar**: Borra todos los campos y resultados
- **Cerrar**: Cierra la aplicación (también puedes usar Alt+F4)

### Ejemplos

- Live DASH: `https://b1108.cdncert.telefonica.com/.../live/NEA427_CI_S/.../NEA427_CI_S.mpd`
- Start Over: URL anterior + `?begin=...&end=...`
- L7D: URL anterior + `&movieId=27457093`
- CPVR: URL con `/nPVR/` en la ruta
- VOD: URL sin `/live/` ni `/nPVR/`

## Requisitos

- Python 3.8+
- Tkinter (incluido con Python por defecto)
- requests

## Solución de problemas

### La ventana no se abre
- Asegúrate de estar en el directorio correcto
- Intenta con: `python -m analizador_manifests.gui`

### El análisis no funciona
- Verifica que la URL sea válida
- La URL debe terminar en `.mpd` o `.m3u8`

### Caracteres especiales en la URL
- Copia la URL exactamente como está en tu navegador
- La aplicación se encarga de procesarla correctamente
