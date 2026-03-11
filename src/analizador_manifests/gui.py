"""
Interfaz gráfica para el analizador de manifests usando Tkinter
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
from .analyzer import ManifestAnalyzer, ContentType


class ManifestGUI:
    """Interfaz gráfica para analizar manifests"""

    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Manifests MPD y HLS")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        self.analyzer = ManifestAnalyzer()
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

        # Frame de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Button(
            button_frame,
            text="Analizar",
            command=self._analyze,
            width=20,
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            button_frame,
            text="Limpiar",
            command=self._clear,
            width=20,
        ).pack(side=tk.LEFT)

        # Frame de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Manifest Type
        ttk.Label(results_frame, text="Tipo de Manifest:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        self.manifest_type_label = ttk.Label(
            results_frame, text="", font=("Helvetica", 10), foreground="#0078d4"
        )
        self.manifest_type_label.pack(anchor=tk.W, pady=(0, 10))

        # Content Type
        ttk.Label(results_frame, text="Tipo de Contenido:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        self.content_type_label = ttk.Label(
            results_frame, text="", font=("Helvetica", 11, "bold")
        )
        self.content_type_label.pack(anchor=tk.W, pady=(0, 10))

        # Confidence
        ttk.Label(results_frame, text="Confianza:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        self.confidence_label = ttk.Label(results_frame, text="", font=("Helvetica", 10))
        self.confidence_label.pack(anchor=tk.W, pady=(0, 10))

        # URL Output
        ttk.Label(results_frame, text="URL Analizada:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        self.url_output = tk.Text(results_frame, height=6, width=100, wrap=tk.WORD)
        self.url_output.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.url_output.config(state=tk.DISABLED)

        # Footer
        footer = ttk.Label(
            main_frame,
            text="© 2026 Analizador de Manifests - Fase 1: Análisis de URL",
            font=("Helvetica", 9),
            foreground="#777777",
        )
        footer.pack()

    def _analyze(self):
        """Analiza la URL introducida"""
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Por favor, pega una URL válida")
            return

        try:
            result = self.analyzer.analyze(url)
            self._display_result(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar: {str(e)}")

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

    def _clear(self):
        """Limpia todos los campos"""
        self.url_entry.delete(0, tk.END)
        self.manifest_type_label.config(text="")
        self.content_type_label.config(text="")
        self.confidence_label.config(text="")
        self.url_output.config(state=tk.NORMAL)
        self.url_output.delete(1.0, tk.END)
        self.url_output.config(state=tk.DISABLED)


def main():
    """Función principal para la GUI"""
    root = tk.Tk()
    app = ManifestGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
