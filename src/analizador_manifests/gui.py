"""
Interfaz gráfica para el analizador de manifests usando Tkinter
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import threading
from .analyzer import ManifestAnalyzer, ContentType


class ManifestGUI:
    """Interfaz gráfica para analizar manifests"""

    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Manifests MPD y HLS")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        
        self.analyzer = ManifestAnalyzer()
        self.analyzing = False
        self._setup_ui()

    def _setup_ui(self):
        """Configura la interfaz de usuario"""
        # Estilo
        style = ttk.Style()
        style.theme_use("clam")
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title = ttk.Label(
            main_frame,
            text="Analizador de Manifests MPD y HLS",
            font=("Helvetica", 18, "bold"),
        )
        title.pack(pady=(0, 20))

        # Frame de entrada
        input_frame = ttk.LabelFrame(main_frame, text="URL del Manifest", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 20))

        self.url_entry = ttk.Entry(input_frame, width=100)
        self.url_entry.pack(fill=tk.X)
        self.url_entry.bind("<Return>", lambda e: self._analyze())
        
        # Opciones
        options_frame = ttk.Frame(input_frame)
        options_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.analyze_content_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="Analizar contenido (descargar y parsear XML)",
            variable=self.analyze_content_var
        ).pack(anchor=tk.W)

        # Frame de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))

        self.analyze_button = ttk.Button(
            button_frame,
            text="Analizar",
            command=self._analyze,
            width=20,
        )
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            button_frame,
            text="Limpiar",
            command=self._clear,
            width=20,
        ).pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(button_frame, text="", foreground="#666666")
        self.status_label.pack(side=tk.LEFT, padx=(20, 0))

        # Notebook para tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Tab 1: Información Básica
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="Información Básica")
        self._setup_basic_tab(basic_frame)
        
        # Tab 2: Contenido del Manifest
        content_frame = ttk.Frame(self.notebook)
        self.notebook.add(content_frame, text="Contenido")
        self._setup_content_tab(content_frame)

        # Footer
        footer = ttk.Label(
            main_frame,
            text="© 2026 Analizador de Manifests - Fase 1 & 2: Análisis de URL y Contenido",
            font=("Helvetica", 9),
            foreground="#777777",
        )
        footer.pack()

    def _setup_basic_tab(self, parent):
        """Configura el tab de información básica"""
        frame = ttk.LabelFrame(parent, text="Resultados del Análisis", padding="15")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Manifest Type
        ttk.Label(frame, text="Tipo de Manifest:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        self.manifest_type_label = ttk.Label(
            frame, text="", font=("Helvetica", 10), foreground="#0078d4"
        )
        self.manifest_type_label.pack(anchor=tk.W, pady=(0, 10))

        # Content Type
        ttk.Label(frame, text="Tipo de Contenido:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        self.content_type_label = ttk.Label(
            frame, text="", font=("Helvetica", 11, "bold")
        )
        self.content_type_label.pack(anchor=tk.W, pady=(0, 10))

        # Confidence
        ttk.Label(frame, text="Confianza:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        self.confidence_label = ttk.Label(frame, text="", font=("Helvetica", 10))
        self.confidence_label.pack(anchor=tk.W, pady=(0, 20))

        # URL Output
        ttk.Label(frame, text="URL Analizada:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        self.url_output = tk.Text(frame, height=8, width=100, wrap=tk.WORD)
        self.url_output.pack(fill=tk.BOTH, expand=True)
        self.url_output.config(state=tk.DISABLED)

    def _setup_content_tab(self, parent):
        """Configura el tab de contenido del manifest"""
        frame = ttk.LabelFrame(parent, text="Información del Contenido", padding="15")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas con scrollbar para permitir scroll
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenedor para el contenido
        self.content_container = scrollable_frame

    def _refresh_content_tab(self, result):
        """Actualiza el contenido del tab de contenido"""
        # Limpiar contenedor anterior
        for widget in self.content_container.winfo_children():
            widget.destroy()
        
        if "content" not in result:
            ttk.Label(
                self.content_container,
                text="⚠️  Análisis de contenido no disponible",
                font=("Helvetica", 10)
            ).pack(anchor=tk.W, pady=10)
            return
        
        content = result["content"]
        
        if content.get("error"):
            ttk.Label(
                self.content_container,
                text=f"❌ Error: {content['error']}",
                font=("Helvetica", 10),
                foreground="#d13438"
            ).pack(anchor=tk.W, pady=10)
            return
        
        # Video Info
        video_frame = ttk.LabelFrame(self.content_container, text="📹 Video", padding="10")
        video_frame.pack(fill=tk.X, pady=(0, 10))
        
        if content.get("has_video"):
            ttk.Label(video_frame, text=f"✓ Video: SÍ", font=("Helvetica", 10)).pack(anchor=tk.W)
            ttk.Label(
                video_frame, 
                text=f"Capas/Perfiles: {content['num_video_layers']}",
                font=("Helvetica", 9)
            ).pack(anchor=tk.W, padx=20)
            
            multikey_text = "SÍ" if content.get("is_multikey") else "NO"
            ttk.Label(
                video_frame, 
                text=f"Multikey: {multikey_text}",
                font=("Helvetica", 9)
            ).pack(anchor=tk.W, padx=20)
            
            if content.get("streaming_profile"):
                ttk.Label(
                    video_frame, 
                    text=f"Perfil: {content['streaming_profile']}",
                    font=("Helvetica", 9)
                ).pack(anchor=tk.W, padx=20)
            
            if content.get("video_profiles"):
                ttk.Label(video_frame, text="Resoluciones:", font=("Helvetica", 9, "bold")).pack(anchor=tk.W, padx=20)
                for profile in content["video_profiles"]:
                    res_str = ""
                    if profile.get("width") and profile.get("height"):
                        res_str = f" ({profile['width']}x{profile['height']})"
                    fps_str = f" @ {profile.get('framerate')}fps" if profile.get("framerate") else ""
                    bw_mbps = profile["bandwidth"] / 1_000_000
                    ttk.Label(
                        video_frame,
                        text=f"• {bw_mbps:.2f} Mbps{res_str}{fps_str}",
                        font=("Helvetica", 9)
                    ).pack(anchor=tk.W, padx=40)
        else:
            ttk.Label(video_frame, text="✗ Video: NO", font=("Helvetica", 10)).pack(anchor=tk.W)
        
        # Audio Info
        audio_frame = ttk.LabelFrame(self.content_container, text="🔊 Audio", padding="10")
        audio_frame.pack(fill=tk.X, pady=(0, 10))
        
        if content.get("has_audio"):
            ttk.Label(audio_frame, text=f"✓ Audio: SÍ", font=("Helvetica", 10)).pack(anchor=tk.W)
            for i, audio in enumerate(content.get("audio_list", []), 1):
                codec_type = audio.get("codec_type", "Unknown")
                if audio.get("is_atmos"):
                    codec_type += " (Atmos)"
                channels = f", {audio.get('channels', '?')}ch" if audio.get("channels") else ""
                ttk.Label(
                    audio_frame,
                    text=f"Audio {i}: {codec_type}{channels}",
                    font=("Helvetica", 9)
                ).pack(anchor=tk.W, padx=20)
        else:
            ttk.Label(audio_frame, text="✗ Audio: NO", font=("Helvetica", 10)).pack(anchor=tk.W)
        
        # Subtitles
        if content.get("has_subtitles"):
            sub_frame = ttk.LabelFrame(self.content_container, text="📄 Subtítulos", padding="10")
            sub_frame.pack(fill=tk.X, pady=(0, 10))
            ttk.Label(sub_frame, text="✓ Subtítulos disponibles", font=("Helvetica", 10)).pack(anchor=tk.W)
        
        # Thumbnails
        if content.get("has_thumbnails"):
            thumb_frame = ttk.LabelFrame(self.content_container, text="🖼️  Thumbnails", padding="10")
            thumb_frame.pack(fill=tk.X, pady=(0, 10))
            ttk.Label(thumb_frame, text="✓ Thumbnails disponibles", font=("Helvetica", 10)).pack(anchor=tk.W)

    def _analyze(self):
        """Analiza la URL introducida"""
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Por favor, pega una URL válida")
            return
        
        if self.analyzing:
            return
        
        self.analyzing = True
        self.analyze_button.config(state=tk.DISABLED)
        self.status_label.config(text="Analizando...")
        self.root.update()

        try:
            # Ejecutar análisis en un thread separado para no congelar la GUI
            thread = threading.Thread(target=self._analyze_thread, args=(url,))
            thread.start()
        except Exception as e:
            self.analyzing = False
            self.analyze_button.config(state=tk.NORMAL)
            self.status_label.config(text="")
            messagebox.showerror("Error", f"Error al analizar: {str(e)}")

    def _analyze_thread(self, url):
        """Ejecuta el análisis en un thread separado"""
        try:
            download_content = self.analyze_content_var.get()
            result = self.analyzer.analyze(url, download_content=download_content)
            self.root.after(0, self._display_result, result)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error al analizar: {str(e)}"))
        finally:
            self.analyzing = False
            self.root.after(0, lambda: self.analyze_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.status_label.config(text=""))

    def _display_result(self, result):
        """Muestra el resultado del análisis"""
        manifest_type = (result.get("manifest_type") or "unknown").upper()
        content_type = result.get("content_type") or "Unknown"
        confidence = f"{result.get('confidence', 0):.0%}"
        url = result.get("url", "")

        self.manifest_type_label.config(text=manifest_type)
        self.content_type_label.config(text=content_type)
        self.confidence_label.config(text=confidence)

        self.url_output.config(state=tk.NORMAL)
        self.url_output.delete(1.0, tk.END)
        self.url_output.insert(1.0, url)
        self.url_output.config(state=tk.DISABLED)
        
        # Actualizar tab de contenido
        self._refresh_content_tab(result)

    def _clear(self):
        """Limpia todos los campos"""
        self.url_entry.delete(0, tk.END)
        self.manifest_type_label.config(text="")
        self.content_type_label.config(text="")
        self.confidence_label.config(text="")
        self.url_output.config(state=tk.NORMAL)
        self.url_output.delete(1.0, tk.END)
        self.url_output.config(state=tk.DISABLED)
        
        # Limpiar content tab
        for widget in self.content_container.winfo_children():
            widget.destroy()


def main():
    """Función principal para la GUI"""
    root = tk.Tk()
    app = ManifestGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
