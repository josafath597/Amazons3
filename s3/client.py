"""Módulo para obtener y actualizar la lista de buckets desde Amazon S3 en la interfaz gráfica."""

from typing import List

import boto3
import boto3.exceptions
import customtkinter
from botocore.exceptions import BotoCoreError, ClientError
from core.utils import es_uuid


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
    except (BotoCoreError, ClientError) as e:
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


def obtener_carpetas_s3(
    access_key: str, secret_key: str, region: str, bucket: str
) -> list[str]:
    """
    Obtiene una lista de todas las carpetas (prefixes) dentro de un bucket S3.

    Args:
        access_key (str): Clave de acceso AWS.
        secret_key (str): Clave secreta AWS.
        region (str): Región AWS.
        bucket (str): Nombre del bucket.

    Returns:
        list[str]: Lista de rutas de carpetas, como 'imagenes/vacaciones/'.
    """
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket)

        carpetas = set()

        for page in pages:
            for obj in page.get("Contents", []):
                key = obj["Key"]
                parts = key.split("/")[:-1]
                for i in range(1, len(parts) + 1):
                    ruta_partes = parts[:i]
                    # Verifica si alguno de los niveles de esta ruta es un UUID
                    if any(es_uuid(p) for p in ruta_partes):
                        continue  # Omitimos rutas que contienen UUIDs
                    ruta = "/".join(ruta_partes) + "/"
                    carpetas.add(ruta)
        return sorted(list(carpetas))

    except Exception as e:
        print(f"❌ Error al obtener carpetas: {e}")
        return []
