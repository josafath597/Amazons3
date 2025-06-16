"""Workers para ejecutar funciones de carga y
subida en hilos separados, sin bloquear la interfaz."""

import customtkinter

from s3.client import actualizar_lista_buckets
from s3.upload import subir_archivo_a_s3
from config.aws_config import cargar_carpetas
from widgets.loader import ocultar_loader_grid, ocultar_loader


def subir_archivo_worker(
    *args,
    loader: customtkinter.CTkProgressBar,
    root: customtkinter.CTk,
    refs: dict,
    **kwargs,
) -> None:
    """
    Ejecuta la función subir_archivo_a_s3 en un hilo separado y oculta el loader al finalizar.

    Args:
        *args: Argumentos posicionales para subir_archivo_a_s3.
        loader (CTkProgressBar): Barra de progreso a ocultar.
        root (CTk): Ventana principal, usada para volver al hilo principal.
        refs (dict): Referencias a widgets compartidos.
        **kwargs: Argumentos con nombre para subir_archivo_a_s3.
    """
    try:
        subir_archivo_a_s3(*args, **kwargs)
    finally:
        # volvemos al hilo principal para tocar la GUI
        root.after(0, lambda: ocultar_loader(loader))
        root.after(0, lambda: cargar_carpetas(refs))


def actualizar_lista_worker(
    *args, loader: customtkinter.CTkProgressBar, root: customtkinter.CTk, **kwargs
) -> None:
    """
    Ejecuta la función actualizar_lista_buckets en un hilo separado y oculta el loader al finalizar.

    Args:
        *args: Argumentos posicionales para actualizar_lista_buckets.
        loader (CTkProgressBar): Barra de progreso a ocultar.
        root (CTk): Ventana principal, usada para volver al hilo principal.
        **kwargs: Argumentos con nombre para actualizar_lista_buckets.
    """
    boton_seleccionar = kwargs.pop("boton_seleccionar", None)
    try:
        actualizar_lista_buckets(*args, **kwargs)
        if boton_seleccionar:
            root.after(0, lambda: boton_seleccionar.configure(state="normal"))
    finally:
        root.after(0, lambda: ocultar_loader_grid(loader))
