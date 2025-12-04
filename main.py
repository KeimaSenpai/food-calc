"""
Food Calculator - Aplicación de escritorio con Flet y Flask
Proporciona una interfaz Flet con un botón para iniciar la app web
"""

import flet as ft
import threading
import webbrowser
import time
from pathlib import Path
import sys

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from assets.app import app as flask_app


class FoodCalculatorApp:
    def __init__(self):
        self.server_thread = None
        self.server_running = False
        self.port = 5000
        self.host = 'localhost'
        
    def start_server(self):
        """Inicia el servidor Flask en un thread separado"""
        if self.server_running:
            return
        
        self.server_running = True
        self.server_thread = threading.Thread(
            target=lambda: flask_app.run(
                debug=False,
                host=self.host,
                port=self.port,
                use_reloader=False
            ),
            daemon=True
        )
        self.server_thread.start()
        
    def open_browser(self):
        """Abre el navegador con la URL de la app"""
        time.sleep(1)  # Esperar a que el servidor inicie
        url = f'http://{self.host}:{self.port}'
        webbrowser.open(url)


def main(page: ft.Page):
    """Función principal de la app Flet"""
    
    # Configurar página
    page.title = "🍳 Food Calculator"
    page.window.width = 600
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Crear instancia de la app
    calc_app = FoodCalculatorApp()
    
    # ===== COMPONENTES =====
    
    # Título
    title = ft.Text(
        "🍳 Food Calculator",
        size=36,
        weight="bold",
        text_align=ft.TextAlign.CENTER,
        color="#1e40af"
    )
    
    # Subtítulo
    subtitle = ft.Text(
        "Aplicación web para calcular cantidades de comida",
        size=14,
        text_align=ft.TextAlign.CENTER,
        color="#64748b"
    )
    
    # Indicador de estado
    status_indicator = ft.Container(
        content=ft.Row(
            [
                ft.Icon(name=ft.Icons.CIRCLE, size=12, color="#ef4444"),
                ft.Text("Servidor detenido", size=12, color="#64748b")
            ],
            spacing=8
        ),
        bgcolor="#fee2e2",
        padding=12,
        border_radius=8,
        visible=True
    )
    
    def update_status(running: bool):
        """Actualiza el indicador de estado"""
        if running:
            status_indicator.content.controls[0].name = ft.Icons.CHECK_CIRCLE
            status_indicator.content.controls[0].color = "#22c55e"
            status_indicator.content.controls[1].value = "Servidor ejecutándose ✓"
            status_indicator.bgcolor = "#dcfce7"
        else:
            status_indicator.content.controls[0].name = ft.Icons.CIRCLE
            status_indicator.content.controls[0].color = "#ef4444"
            status_indicator.content.controls[1].value = "Servidor detenido"
            status_indicator.bgcolor = "#fee2e2"
        page.update()
    
    # Botón principal - Iniciar servidor
    btn_iniciar = ft.ElevatedButton(
        text="▶️ Iniciar Servidor",
        bgcolor="#3b82f6",
        color="white",
        width=300,
        height=60,
        disabled=False
    )
    
    # Botón - Abrir en navegador
    btn_abrir = ft.ElevatedButton(
        text="🌐 Abrir en Navegador",
        bgcolor="#10b981",
        color="white",
        width=300,
        height=60,
        disabled=True
    )
    
    # Botón - Detener servidor
    btn_detener = ft.ElevatedButton(
        text="⏹️ Detener Servidor",
        bgcolor="#ef4444",
        color="white",
        width=300,
        height=60,
        disabled=True
    )
    
    # Información
    info_text = ft.Text(
        "Haz clic en 'Iniciar Servidor' para comenzar",
        size=12,
        text_align=ft.TextAlign.CENTER,
        color="#64748b",
        selectable=True
    )
    
    # URL de acceso
    url_text = ft.Text(
        f"🔗 http://{calc_app.host}:{calc_app.port}",
        size=12,
        text_align=ft.TextAlign.CENTER,
        color="#3b82f6",
        selectable=True,
        visible=False
    )
    
    # Características
    features = ft.Column(
        [
            ft.Row(
                [ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color="#22c55e"),
                 ft.Text("Cálculo de cantidades de comida", size=12)],
                spacing=8
            ),
            ft.Row(
                [ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color="#22c55e"),
                 ft.Text("40+ productos disponibles", size=12)],
                spacing=8
            ),
            ft.Row(
                [ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color="#22c55e"),
                 ft.Text("Búsqueda y filtrado en tiempo real", size=12)],
                spacing=8
            ),
            ft.Row(
                [ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color="#22c55e"),
                 ft.Text("Múltiples formatos de salida", size=12)],
                spacing=8
            ),
            ft.Row(
                [ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color="#22c55e"),
                 ft.Text("Cálculo de ingredientes", size=12)],
                spacing=8
            ),
        ],
        spacing=10
    )
    
    # ===== EVENTOS =====
    
    def on_iniciar_click(e):
        """Evento al hacer clic en Iniciar"""
        try:
            info_text.value = "⏳ Iniciando servidor..."
            page.update()
            
            calc_app.start_server()
            
            # Actualizar UI
            btn_iniciar.disabled = True
            btn_abrir.disabled = False
            btn_detener.disabled = False
            url_text.visible = True
            update_status(True)
            info_text.value = "✓ Servidor iniciado correctamente"
            info_text.color = "#22c55e"
            
        except Exception as ex:
            info_text.value = f"❌ Error: {str(ex)}"
            info_text.color = "#ef4444"
        
        page.update()
    
    def on_abrir_click(e):
        """Evento al hacer clic en Abrir"""
        try:
            url = f'http://{calc_app.host}:{calc_app.port}'
            webbrowser.open(url)
            info_text.value = f"✓ Abriendo {url} en el navegador..."
            info_text.color = "#22c55e"
        except Exception as ex:
            info_text.value = f"❌ Error al abrir navegador: {str(ex)}"
            info_text.color = "#ef4444"
        
        page.update()
    
    def on_detener_click(e):
        """Evento al hacer clic en Detener"""
        try:
            calc_app.server_running = False
            btn_iniciar.disabled = False
            btn_abrir.disabled = True
            btn_detener.disabled = True
            url_text.visible = False
            update_status(False)
            info_text.value = "✓ Servidor detenido"
            info_text.color = "#64748b"
        except Exception as ex:
            info_text.value = f"❌ Error: {str(ex)}"
            info_text.color = "#ef4444"
        
        page.update()
    
    # Asignar eventos
    btn_iniciar.on_click = on_iniciar_click
    btn_abrir.on_click = on_abrir_click
    btn_detener.on_click = on_detener_click
    
    # ===== DISEÑO =====
    
    # Contenedor de botones
    buttons_container = ft.Column(
        [
            btn_iniciar,
            btn_abrir,
            btn_detener,
        ],
        spacing=12,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    # Sección de información
    info_section = ft.Container(
        content=ft.Column(
            [
                ft.Text("📋 Características", size=14, weight="bold"),
                features,
            ],
            spacing=12
        ),
        bgcolor="#f8fafc",
        padding=16,
        border_radius=8,
        border=ft.border.all(1, "#e2e8f0")
    )
    
    # Contenido principal
    main_content = ft.Column(
        [
            title,
            subtitle,
            ft.Divider(height=20),
            status_indicator,
            buttons_container,
            url_text,
            info_text,
            info_section,
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
    
    # Scroll view
    page.add(
        ft.Column(
            [main_content],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    )


def main_app():
    """Inicia la aplicación Flet"""
    ft.app(
        target=main,
        name="Food Calculator",
        assets_dir="assets"
    )


if __name__ == "__main__":
    main_app()
