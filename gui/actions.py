"""Funciones relacionadas con acciones de la interfaz gráfica,
como seleccionar archivos y copiar URLs."""

import os
import re
from tkinter import filedialog
from typing import Any, Dict

import customtkinter

from core.validators import archivo_es_valido


def seleccionar_archivo(
    label_archivo: customtkinter.CTkLabel,
    textbox_name_file: customtkinter.CTkEntry,
    textbox_url: customtkinter.CTkTextbox,
    boton_subir: customtkinter.CTkButton,
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


def actualizar_url_preliminar(
    textbox_name: customtkinter.CTkEntry,
    label_url_preliminar: customtkinter.CTkLabel,
    refs: Dict[str, Any],
    carpeta_seleccionada: str,
) -> None:
    """
    Actualiza la etiqueta de URL preliminar con base
    en el nombre del archivo y configuración actual.

    Args:
        textbox_name (CTkEntry): Campo donde se escribe el nombre del archivo.
        label_url_preliminar (CTkLabel): Label donde se mostrará la URL preliminar.
        refs (Dict[str, Any]): Diccionario con entradas de configuración (bucket, región, etc).
        archivo_seleccionado (str): Ruta real del archivo seleccionado.
    """
    nombre_archivo = textbox_name.get().strip()
    if not nombre_archivo:
        label_url_preliminar.configure(text="")
        return
    nombre_sin_ext = os.path.splitext(nombre_archivo)[0].strip()
    nombre_sin_ext = re.sub(r"[^\w\-]", "_", nombre_sin_ext.replace(" ", "_"))
    nombre_sin_ext = nombre_sin_ext.lower()

    bucket = refs["menu_bucket"].get()
    region = refs["entry_region"].get()
    url = f"{bucket}.s3.{region}.amazonaws.com"

    label_url_preliminar.configure(
        text=f"🌐{url}{carpeta_seleccionada}{nombre_sin_ext}"
    )
