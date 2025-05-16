"""Módulo para obtener y actualizar la lista de buckets desde Amazon S3 en la interfaz gráfica."""

from typing import List

import boto3
import boto3.exceptions
import customtkinter


def obtener_buckets(access_key: str, secret_key: str, region: str) -> List[str]:
    """
    Conecta con Amazon S3 y obtiene la lista de buckets disponibles.

    Args:
        access_key (str): Clave de acceso de AWS.
        secret_key (str): Clave secreta de AWS.
        region (str): Región de AWS.

    Returns:
        List[str]: Lista con los nombres de los buckets disponibles,
        o una lista vacía en caso de error.
    """
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
        response = s3.list_buckets()
        nombres = [bucket["Name"] for bucket in response["Buckets"]]
        return nombres
    except boto3.exceptions.S3UploadFailedError as e:
        print(f"❌ Error al obtener buckets: {e}")
        return []


def actualizar_lista_buckets(
    entry_access_key: customtkinter.CTkEntry,
    entry_secret_key: customtkinter.CTkEntry,
    entry_region: customtkinter.CTkEntry,
    menu_bucket: customtkinter.CTkOptionMenu,
    label_confirm: customtkinter.CTkLabel,
) -> None:
    """
    Actualiza el menú de selección de buckets en la interfaz gráfica usando los datos ingresados.

    Args:
        entry_access_key (CTkEntry): Entrada con la access key.
        entry_secret_key (CTkEntry): Entrada con la secret key.
        entry_region (CTkEntry): Entrada con la región.
        menu_bucket (CTkOptionMenu): Menú desplegable que se llenará con los buckets.
        label_confirm (CTkLabel): Etiqueta para mostrar mensajes de éxito o error.
    """
    buckets = obtener_buckets(
        entry_access_key.get(), entry_secret_key.get(), entry_region.get()
    )
    if buckets:
        menu_bucket.configure(values=buckets)
        menu_bucket.set(buckets[0])  # Selecciona el primero por defecto
        label_confirm.configure(text="✅ Buckets cargados")
    else:
        label_confirm.configure(text="❌ No se pudieron cargar buckets")
