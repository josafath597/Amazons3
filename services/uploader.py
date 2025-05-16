import customtkinter
from s3.upload import subir_archivo_a_s3
from s3.client import actualizar_lista_buckets
from widgets.loader import ocultar_loader

def subir_archivo_worker(*args, loader: customtkinter.CTkProgressBar, root: customtkinter.CTk, **kwargs):
    """
    Corre subir_archivo_a_s3 en un hilo y oculta el loader al terminar,
    sin importar si hubo error o no.
    """
    try:
        subir_archivo_a_s3(*args, **kwargs)
    finally:
        # volvemos al hilo principal para tocar la GUI
        root.after(0, lambda: ocultar_loader(loader))

def actualizar_lista_worker(*args, loader: customtkinter.CTkProgressBar, root: customtkinter.CTk, **kwargs):
    try:
        actualizar_lista_buckets(*args, **kwargs)
    finally:
        root.after(0, lambda: ocultar_loader(loader))
        