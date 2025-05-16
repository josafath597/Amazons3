"""Módulo que construye la pestaña de subida de archivos en la interfaz principal."""

import threading
from typing import Any, Dict

import customtkinter

from s3.upload import hacer_publico_ultimo_archivo
from services.uploader import subir_archivo_worker
from widgets.loader import crear_loader_padre, mostrar_loader
from gui.actions import copiar_url, seleccionar_archivo


def crear_tab_subir(
    root: customtkinter.CTk, tab: customtkinter.CTkFrame, refs: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Construye la pestaña de subida de archivos a Amazon S3, incluyendo selección de archivo,
    entrada del nombre, opciones de visibilidad pública, botones de acción y carga asincrónica.

    Args:
        root (CTk): Ventana principal de la aplicación.
        tab (CTkFrame): Contenedor donde se insertan los elementos de esta pestaña.
        refs (Dict[str, Any]): Diccionario de referencias cruzadas con widgets de configuración.

    Returns:
        Dict[str, Any]: Diccionario con referencias a widgets relevantes para futuras operaciones.
    """
    # --- Widgets principales ---
    label_archivo = customtkinter.CTkLabel(tab, text="Ningún archivo seleccionado aún.")
    label_archivo.pack(pady=10)

    # Nombre de archivo
    frame_nombre = customtkinter.CTkFrame(tab)
    frame_nombre.pack(pady=5)

    customtkinter.CTkLabel(frame_nombre, text="Nombre del Archivo").grid(
        row=0, column=0, padx=5, pady=5, sticky="e"
    )
    textbox_name = customtkinter.CTkEntry(
        frame_nombre, placeholder_text="Nombre del Archivo", width=300
    )
    textbox_name.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # URL
    customtkinter.CTkLabel(tab, text="URL del archivo en S3").pack()
    textbox_url = customtkinter.CTkTextbox(tab, height=40, width=500, state="disabled")
    textbox_url.pack(pady=5)

    # Botones
    boton_copiar = customtkinter.CTkButton(tab, text="Copiar URL", state="disabled")
    boton_copiar.pack(pady=5)

    es_publico = customtkinter.CTkCheckBox(tab, text="¿Hacer público?")
    es_publico.select()
    es_publico.pack(pady=5)

    boton_seleccionar = customtkinter.CTkButton(
        tab, text="Seleccionar archivo", state="normal"
    )
    boton_subir = customtkinter.CTkButton(tab, text="Subir archivo", state="disabled")
    boton_publico = customtkinter.CTkButton(tab, text="Hacer público", state="disabled")

    boton_seleccionar.pack(pady=10)
    boton_subir.pack(pady=10)
    boton_publico.pack(pady=5)

    archivo_seleccionado = None

    def seleccionar_y_guardar():
        nonlocal archivo_seleccionado
        archivo_seleccionado = seleccionar_archivo(
            label_archivo,
            textbox_name,
            textbox_url,
            boton_subir,
            boton_publico,
            boton_copiar,
        )

    # ---- Conectar callbacks (lambda o funciones aparte) ----
    boton_seleccionar.configure(command=seleccionar_y_guardar)

    loader = crear_loader_padre(tab)

    def lanzar_subida():
        mostrar_loader(loader)
        threading.Thread(
            target=subir_archivo_worker,
            kwargs={
                "archivo_seleccionado": archivo_seleccionado,
                "entry_access_key": refs["entry_access"],
                "entry_secret_key": refs["entry_secret"],
                "entry_region": refs["entry_region"],
                "menu_bucket": refs["menu_bucket"],
                "textbox_name_file": textbox_name,
                "es_publico": es_publico,
                "label_archivo": label_archivo,
                "textbox_url": textbox_url,
                "boton_subir": boton_subir,
                "boton_copiar": boton_copiar,
                "boton_hacer_publico": boton_publico,
                "loader": loader,
                "root": root,
            },
            daemon=True,
        ).start()

    boton_subir.configure(command=lanzar_subida)

    boton_copiar.configure(command=lambda: copiar_url(root, textbox_url, label_archivo))

    boton_publico.configure(
        command=lambda: hacer_publico_ultimo_archivo(
            textbox_url,
            label_archivo,
            refs["entry_access"],
            refs["entry_secret"],
            refs["entry_region"],
            refs["menu_bucket"],
            boton_publico,
        )
    )

    # Devolver referencias compartidas
    return {
        "label_archivo": label_archivo,
        "textbox_name": textbox_name,
        "textbox_url": textbox_url,
        "boton_subir": boton_subir,
        "boton_publico": boton_publico,
        "boton_copiar": boton_copiar,
        "es_publico": es_publico,
    }
