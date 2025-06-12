"""Módulo principal de la interfaz gráfica. Construye la ventana y sus pestañas."""

from typing import Any, Dict

import customtkinter

from core.utils import cerrar_app
from gui.config_tab import crear_tab_config
from gui.upload_tab import crear_tab_subir
from config.aws_config import cargar_config_archivo


def mostrar_ventana() -> None:
    """
    Crea y muestra la ventana principal de la aplicación,
    incluyendo las pestañas de subir y configuración.
    """
    app = customtkinter.CTk()
    app.geometry("600x650")
    app.minsize(600, 650)
    app.resizable(True, True)
    app.title("Subir Archivo a AWS")

    # Encabezado
    customtkinter.CTkLabel(app, text="Subir Archivo a Amazon S3").pack(pady=10)

    # Pestañas
    tabview = customtkinter.CTkTabview(app)
    tabview.pack(padx=10, pady=10, fill="both", expand=True)

    # --- Pestaña SUBIR ---
    tab_subir = tabview.add("Subir archivo")
    tab_conf = tabview.add("Configuración")

    # Construir cada pestaña con funciones auxiliares
    refs: Dict[str, Any] = {}  # diccionario vacío

    # 👉 Carga config desde archivo antes
    datos = cargar_config_archivo()
    hay_config = all(
        datos.get(k) for k in ("access_key", "secret_key", "region", "bucket")
    )

    refs |= crear_tab_subir(app, tab_subir, refs)  # llena refs
    crear_tab_config(tab_conf, refs)

    # Si hay config, activa el botón aquí directamente
    if hay_config and "boton_seleccionar" in refs:
        refs["boton_seleccionar"].configure(state="normal")

    # Handler de cierre
    app.protocol("WM_DELETE_WINDOW", lambda: cerrar_app(app))
    app.mainloop()
