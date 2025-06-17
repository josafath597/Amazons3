"""Módulo con widgets para mostrar vista previa de archivos."""

from __future__ import annotations

import os

import customtkinter
from PIL import Image


def crear_preview(parent: customtkinter.CTkBaseClass) -> customtkinter.CTkFrame:
    """Crea un frame oculto con etiquetas de información y área de imagen."""
    frame = customtkinter.CTkFrame(parent)

    label_info = customtkinter.CTkLabel(frame, text="")
    label_info.pack(pady=(5, 0))

    label_image = customtkinter.CTkLabel(frame, text="")
    label_image.pack(pady=5)

    button_hide = customtkinter.CTkButton(
        frame, text="Cerrar", command=lambda: ocultar_preview(frame)
    )
    button_hide.pack(pady=(0, 5))

    frame.label_info = label_info  # type: ignore[attr-defined]
    frame.label_image = label_image  # type: ignore[attr-defined]

    frame.pack(pady=10)
    frame.pack_forget()
    return frame


def _format_size(size: int) -> str:
    """Convierte un tamaño de bytes a un texto legible."""
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.1f} MB"


def mostrar_preview(frame: customtkinter.CTkFrame, path: str) -> None:
    """Llena las etiquetas con datos del archivo y muestra la vista previa."""
    if not os.path.exists(path):
        return

    size = os.path.getsize(path)
    texto = [f"Tamaño: {_format_size(size)}"]

    try:
        img = Image.open(path)
        texto.append(f"Dimensiones: {img.width}x{img.height}")
        max_side = 200
        scale = min(1.0, max_side / max(img.width, img.height))
        preview_size = (int(img.width * scale), int(img.height * scale))
        ctk_img = customtkinter.CTkImage(light_image=img, dark_image=img, size=preview_size)
        frame.label_image.configure(image=ctk_img, text="")  # type: ignore[attr-defined]
        frame.label_image.image = ctk_img  # type: ignore[attr-defined]
    except Exception:
        frame.label_image.configure(text="(Sin vista previa)", image=None)  # type: ignore[attr-defined]

    frame.label_info.configure(text="\n".join(texto))  # type: ignore[attr-defined]
    frame.pack(pady=10)


def ocultar_preview(frame: customtkinter.CTkFrame) -> None:
    """Oculta el frame de vista previa."""
    frame.pack_forget()
