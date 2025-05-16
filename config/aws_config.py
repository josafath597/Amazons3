"""Este módulo maneja la configuración de AWS para la aplicación."""

import json
import os

import customtkinter

CONFIG_FILE = "aws_config.json"
config = {"access_key": "", "secret_key": "", "bucket": "", "region": "us-east-1"}


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
) -> None:
    """Guarda los valores ingresados por el usuario en la configuración."""
    config["access_key"] = entry_access_key.get()
    config["secret_key"] = entry_secret_key.get()
    config["bucket"] = menu_bucket.get()
    config["region"] = entry_region.get()
    guardar_config_archivo()
    label_confirm.configure(text="✅ Configuración guardada con éxito")


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
    menu_bucket.set("Sin cargar")
    label_confirm.configure(text="")
