"""Valida si un archivo tiene una extensión permitida para su carga o procesamiento."""

import os

extensiones_validas = (
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".txt",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".webp",
    ".svg",
)


def archivo_es_valido(ruta_archivo):
    """
    Verifica si la extensión del archivo es válida.

    Args:
        ruta_archivo (str): Ruta del archivo a verificar.

    Returns:
        bool: True si la extensión es válida, False si no.
    """
    return os.path.splitext(ruta_archivo)[1].lower() in extensiones_validas
