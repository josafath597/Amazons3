"""Funciones relacionadas con acciones de la interfaz gráfica,
como seleccionar archivos y copiar URLs."""

import os
from tkinter import filedialog
from typing import Any, Dict

import customtkinter

from core.validators import archivo_es_valido


def seleccionar_archivo(
    label_archivo: customtkinter.CTkLabel,
    textbox_name_file: customtkinter.CTkEntry,
    textbox_url: customtkinter.CTkTextbox,
    boton_subir: customtkinter.CTkButton,
    boton_hacer_publico: customtkinter.CTkButton,
    boton_copiar: customtkinter.CTkButton,
):
    """
    Abre un cuadro de diálogo para seleccionar un archivo
    y actualiza la interfaz si el archivo es válido.

    Args:
        label_archivo (CTkLabel): Etiqueta para mostrar el estado del archivo seleccionado.
        textbox_name_file (CTkEntry): Entrada donde se mostrará el nombre del archivo.
        textbox_url (CTkTextbox): Cuadro de texto para la URL.
        boton_subir (CTkButton): Botón para subir el archivo.
        boton_hacer_publico (CTkButton): Botón para hacer público el archivo.
        boton_copiar (CTkButton): Botón para copiar la URL.

    Returns:
        str | None: La ruta del archivo si es válido, de lo contrario None.
    """
    archivo = filedialog.askopenfilename()
    if archivo_es_valido(archivo):
        label_archivo.configure(text=f"Archivo seleccionado:\n{archivo}")

        # Establece por defecto el nombre original en el textbox (sin la ruta)
        nombre_original = os.path.basename(archivo)
        textbox_name_file.delete(0, "end")
        textbox_name_file.insert(0, nombre_original)

        textbox_url.configure(state="normal")
        textbox_url.delete("0.0", "end")
        textbox_url.configure(state="disabled")

        boton_subir.configure(state="normal")
        boton_hacer_publico.configure(state="disabled")
        boton_copiar.configure(state="disabled")
        return archivo
    label_archivo.configure(text="El archivo seleccionado no es válido.")
    return None


def copiar_url(
    root: customtkinter.CTk,
    textbox_url: customtkinter.CTkTextbox,
    label_archivo: customtkinter.CTkLabel,
) -> None:
    """
    Copia el contenido del textbox al portapapeles si contiene una URL.

    Args:
        root (CTk): Raíz de la aplicación para acceder al portapapeles.
        textbox_url (CTkTextbox): Cuadro de texto que contiene la URL.
        label_archivo (CTkLabel): Etiqueta donde se muestra el estado del copiado.
    """
    url = textbox_url.get("0.0", "end").strip()
    if not url:
        label_archivo.configure(text="⚠️ No hay URL para copiar")
        return
    root.clipboard_clear()
    root.clipboard_append(url)
    label_archivo.configure(text="📋 URL copiada al portapapeles")


def limpiar_tab_subir(refs: Dict[str, Any]) -> None:
    if "textbox_url" in refs:
        refs["textbox_url"].configure(state="normal")
        refs["textbox_url"].delete("0.0", "end")
        refs["textbox_url"].configure(state="disabled")
    if "label_archivo" in refs:
        refs["label_archivo"].configure(text="Ningún archivo seleccionado aún.")
    for k in ("boton_copiar", "boton_publico", "boton_subir"):
        if k in refs:
            refs[k].configure(state="disabled")
