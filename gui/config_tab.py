"""Crea y configura la pestaña de ajustes de AWS dentro de la interfaz gráfica."""

from typing import Any, Dict

import customtkinter

from config.aws_config import (
    cargar_config_archivo,
    config,
    guardar_config,
    limpiar_campos,
)
from s3.client import actualizar_lista_buckets


def crear_tab_config(tab: customtkinter.CTkFrame, refs: Dict[str, Any]) -> None:
    """
    Construye la pestaña de configuración AWS, incluyendo campos de acceso, región,
    carga de buckets, guardado de configuración y limpieza de campos.

    Args:
        tab (CTkFrame): Contenedor donde se insertan los widgets de configuración.
        refs (Dict[str, Any]): Diccionario para almacenar referencias a widgets reutilizables.
    """
    tab.grid_columnconfigure(0, weight=1)
    tab.grid_columnconfigure(1, weight=1)
    customtkinter.CTkLabel(tab, text="🔐 Configuración AWS").grid(
        row=0, column=0, columnspan=2, pady=(0, 10)
    )

    # Entradas
    entry_access = customtkinter.CTkEntry(tab, placeholder_text="Access Key ID")
    entry_access.grid(row=1, column=1, padx=5, pady=5)
    entry_secret = customtkinter.CTkEntry(
        tab, placeholder_text="Secret Access Key", show="*"
    )
    entry_secret.grid(row=2, column=1, padx=5, pady=5)
    entry_region = customtkinter.CTkEntry(tab, placeholder_text="us-east-1")
    entry_region.grid(row=3, column=1, padx=5, pady=5)

    # Labels
    customtkinter.CTkLabel(tab, text="Access Key ID").grid(
        row=1, column=0, sticky="e", padx=5, pady=5
    )
    customtkinter.CTkLabel(tab, text="Secret Access Key").grid(
        row=2, column=0, sticky="e", padx=5, pady=5
    )
    customtkinter.CTkLabel(tab, text="Región").grid(
        row=3, column=0, sticky="e", padx=5, pady=5
    )

    # Menú Bucket y Botones
    menu_bucket = customtkinter.CTkOptionMenu(tab, values=["Sin cargar"])
    menu_bucket.grid(row=5, column=0, columnspan=2, pady=5)

    datos = cargar_config_archivo()
    if datos:
        entry_access.insert(0, datos.get("access_key", ""))
        entry_secret.insert(0, datos.get("secret_key", ""))
        entry_region.insert(0, datos.get("region", ""))
        menu_bucket.set(datos.get("bucket", "Sin cargar"))
        config.update(datos)

    boton_cargar = customtkinter.CTkButton(
        tab,
        text="Cargar Buckets",
        command=lambda: actualizar_lista_buckets(
            entry_access, entry_secret, entry_region, menu_bucket, label_confirm
        ),
    )
    boton_cargar.grid(row=4, column=0, columnspan=2, pady=5)

    label_confirm = customtkinter.CTkLabel(tab, text="")
    label_confirm.grid(row=9, column=0, columnspan=2, pady=5)

    # Guardar y limpiar
    boton_guardar = customtkinter.CTkButton(
        tab,
        text="Guardar configuración",
        command=lambda: guardar_config(
            entry_access, entry_secret, entry_region, menu_bucket, label_confirm
        ),
    )
    boton_guardar.grid(row=7, column=0, columnspan=2, pady=20)

    boton_limpiar = customtkinter.CTkButton(
        tab,
        text="Limpiar campos",
        command=lambda: limpiar_campos(
            entry_access, entry_secret, entry_region, menu_bucket, label_confirm
        ),
    )
    boton_limpiar.grid(row=8, column=0, columnspan=2, pady=(5, 20))

    # 👉 Almacena referencias para la pestaña de subir
    refs.update(
        entry_access=entry_access,
        entry_secret=entry_secret,
        entry_region=entry_region,
        menu_bucket=menu_bucket,
        label_confirm=label_confirm,
    )
