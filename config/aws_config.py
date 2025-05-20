"""Este módulo maneja la configuración de AWS para la aplicación."""

import json
import os
from typing import Any, Dict
import boto3
import customtkinter
from botocore.exceptions import ClientError
from s3.client import obtener_carpetas_s3


CONFIG_FILE = "aws_config.json"
config = {"access_key": "", "secret_key": "", "bucket": "", "region": "us-east-1"}


def config_esta_completa(cfg: dict) -> bool:
    """Devuelve True si todos los campos de la configuración AWS están llenos."""
    return all(cfg.get(k) for k in ["access_key", "secret_key", "region", "bucket"])


def guardar_config_archivo():
    """Guarda la configuración en un archivo JSON."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f)


def cargar_config_archivo():
    """Carga la configuración desde un archivo JSON, o devuelve {} si está vacío o dañado."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ El archivo de configuración está vacío o dañado. Se ignorará.")
            return {}
    return {}


def guardar_config(
    entry_access_key: customtkinter.CTkEntry,
    entry_secret_key: customtkinter.CTkEntry,
    entry_region: customtkinter.CTkEntry,
    menu_bucket: customtkinter.CTkOptionMenu,
    label_confirm: customtkinter.CTkLabel,
    refs: Dict[str, Any],
) -> None:
    """Guarda los valores ingresados por el usuario en la configuración."""
    access_key = entry_access_key.get()
    secret_key = entry_secret_key.get()
    region = entry_region.get()
    bucket = menu_bucket.get()

    todos_vacios = not any([access_key, secret_key, region, bucket])
    todos_llenos = all([access_key, secret_key, region, bucket])

    if not todos_vacios and not todos_llenos:
        label_confirm.configure(text="⚠️ Llena todos los campos o déjalos todos vacíos.")
        return

    config["access_key"] = access_key
    config["secret_key"] = secret_key
    config["bucket"] = bucket
    config["region"] = region

    # ✅ Validar si es configuración válida antes de guardar
    if todos_llenos:
        if not validar_config_aws(access_key, secret_key, region, bucket):
            label_confirm.configure(
                text="❌ Configuración no válida. Verifica tus datos."
            )
            return

    guardar_config_archivo()
    label_confirm.configure(text="✅ Configuración guardada con éxito")

    if "boton_seleccionar" in refs:
        refs["boton_seleccionar"].configure(
            state="normal" if todos_llenos else "disabled"
        )
    if "textbox_url" in refs:
        refs["textbox_url"].configure(state="normal")
        refs["textbox_url"].delete("0.0", "end")
        refs["textbox_url"].configure(state="disabled")
    if "label_archivo" in refs:
        refs["label_archivo"].configure(text="Ningún archivo seleccionado aún.")
    if "menu_carpeta" in refs and config_esta_completa(config):
        carpetas = obtener_carpetas_s3(
            config["access_key"],
            config["secret_key"],
            config["region"],
            config["bucket"],
        )
        opciones = ["/"] + carpetas
        refs["menu_carpeta"].configure(values=opciones)
        refs["menu_carpeta"].set("/")
    for k in ("boton_copiar", "boton_publico", "boton_subir"):
        if k in refs:
            refs[k].configure(state="disabled")


def limpiar_campos(
    entry_access_key: customtkinter.CTkEntry,
    entry_secret_key: customtkinter.CTkEntry,
    entry_region: customtkinter.CTkEntry,
    menu_bucket: customtkinter.CTkOptionMenu,
    label_confirm: customtkinter.CTkLabel,
) -> None:
    """Limpia todos los campos de entrada en la interfaz."""
    entry_access_key.delete(0, "end")
    entry_secret_key.delete(0, "end")
    entry_region.delete(0, "end")
    menu_bucket.set("")
    label_confirm.configure(text="")


def validar_config_aws(
    access_key: str, secret_key: str, region: str, bucket: str
) -> bool:
    """
    Valida si la configuración de AWS es correcta intentando acceder al bucket.

    Args:
        access_key (str): Clave de acceso AWS.
        secret_key (str): Clave secreta AWS.
        region (str): Región configurada.
        bucket (str): Nombre del bucket a validar.

    Returns:
        bool: True si la configuración es válida, False si hay error.
    """
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
        s3.head_bucket(Bucket=bucket)
        return True
    except ClientError as e:
        print(f"❌ Error al validar configuración AWS: {e}")
        return False
