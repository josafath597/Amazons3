"""Funciones para subir archivos a Amazon S3 y
gestionar su visibilidad pública desde la interfaz gráfica."""

import os
import re
import boto3
import boto3.exceptions
import customtkinter


def url_es_de_s3(url: str) -> bool:
    """
    Verifica si una URL corresponde a un objeto en Amazon S3.

    Args:
        url (str): La URL a validar.

    Returns:
        bool: True si parece ser una URL de S3, False en caso contrario.
    """
    return url.startswith("https://") and ".s3." in url


def hacer_publico_ultimo_archivo(
    textbox_url: customtkinter.CTkTextbox,
    label_archivo: customtkinter.CTkLabel,
    entry_access_key: customtkinter.CTkEntry,
    entry_secret_key: customtkinter.CTkEntry,
    entry_region: customtkinter.CTkEntry,
    menu_bucket: customtkinter.CTkOptionMenu,
    boton_hacer_publico: customtkinter.CTkButton,
):
    """
    Cambia la visibilidad del último archivo subido a público (lectura sin restricciones).

    Args:
        textbox_url (CTkTextbox): Cuadro de texto con la URL del archivo.
        label_archivo (CTkLabel): Etiqueta para mostrar mensajes.
        entry_access_key (CTkEntry): Entrada de Access Key de AWS.
        entry_secret_key (CTkEntry): Entrada de Secret Key de AWS.
        entry_region (CTkEntry): Entrada de la región AWS.
        menu_bucket (CTkOptionMenu): Menú con el nombre del bucket.
        boton_hacer_publico (CTkButton): Botón que activa esta función.
    """
    url = textbox_url.get("0.0", "end").strip()
    # ⛔ 1. Si no hay URL, nada que hacer
    if not url:
        label_archivo.configure(text="⚠️ Primero sube un archivo.")
        return
    if not url_es_de_s3(url):
        label_archivo.configure(text="⚠️ La URL no parece ser de Amazon S3.")
        return
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=entry_access_key.get(),
            aws_secret_access_key=entry_secret_key.get(),
            region_name=entry_region.get(),
        )

        nombre_bucket = menu_bucket.get()
        nombre_objeto = url.split("/")[-1]

        s3.put_object_acl(Bucket=nombre_bucket, Key=nombre_objeto, ACL="public-read")

        label_archivo.configure(text=f"🌍 Archivo ahora es público:\n{nombre_objeto}")
        # # ✔️ Deshabilitamos el botón; ya quedó público
        boton_hacer_publico.configure(state="disabled")
    except boto3.exceptions.Boto3Error as e:
        label_archivo.configure(text=f"❌ Error al cambiar visibilidad:\n{e}")


def subir_archivo_a_s3(
    archivo_seleccionado: str,
    entry_access_key: customtkinter.CTkEntry,
    entry_secret_key: customtkinter.CTkEntry,
    entry_region: customtkinter.CTkEntry,
    menu_bucket: customtkinter.CTkOptionMenu,
    textbox_name_file: customtkinter.CTkEntry,
    es_publico: customtkinter.CTkCheckBox,
    label_archivo: customtkinter.CTkLabel,
    textbox_url: customtkinter.CTkTextbox,
    boton_subir: customtkinter.CTkButton,
    boton_copiar: customtkinter.CTkButton,
    boton_hacer_publico: customtkinter.CTkButton,
):
    """
    Sube un archivo seleccionado a Amazon S3 con opción de hacerlo público.

    Args:
        archivo_seleccionado (str): Ruta del archivo a subir.
        entry_access_key (CTkEntry): Entrada de Access Key.
        entry_secret_key (CTkEntry): Entrada de Secret Key.
        entry_region (CTkEntry): Entrada de región AWS.
        menu_bucket (CTkOptionMenu): Menú de buckets.
        textbox_name_file (CTkEntry): Entrada del nombre personalizado.
        es_publico (CTkCheckBox): Checkbox para visibilidad pública.
        label_archivo (CTkLabel): Etiqueta de estado.
        textbox_url (CTkTextbox): Cuadro con la URL del archivo subido.
        boton_subir (CTkButton): Botón de subir.
        boton_copiar (CTkButton): Botón de copiar URL.
        boton_hacer_publico (CTkButton): Botón de hacer público.
    """
    if not archivo_seleccionado:
        return

    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=entry_access_key.get(),
            aws_secret_access_key=entry_secret_key.get(),
            region_name=entry_region.get(),
        )

        nombre_bucket = menu_bucket.get()
        nombre_personalizado = textbox_name_file.get().strip()
        nombre_objeto = (
            nombre_personalizado
            if nombre_personalizado
            else os.path.basename(archivo_seleccionado)
        )

        nombre_objeto = re.sub(r"[^\w\-. ]", "_", nombre_objeto)

        if "." not in nombre_objeto:
            extension = os.path.splitext(archivo_seleccionado)[1]
            nombre_objeto += extension

        extra_args = {}
        if es_publico.get():
            extra_args["ACL"] = "public-read"

        with open(archivo_seleccionado, "rb") as f:
            if extra_args:
                s3.upload_fileobj(f, nombre_bucket, nombre_objeto, ExtraArgs=extra_args)
            else:
                s3.upload_fileobj(f, nombre_bucket, nombre_objeto)

        # URL pública
        region = entry_region.get()
        url = f"https://{nombre_bucket}.s3.{region}.amazonaws.com/{nombre_objeto}"

        label_archivo.configure(text=f"✅ Archivo subido:\n{nombre_objeto}")
        textbox_url.configure(state="normal")
        textbox_url.delete("0.0", "end")
        textbox_url.insert("0.0", url)
        textbox_url.configure(state="disabled")
        boton_subir.configure(state="disabled")
        boton_copiar.configure(state="normal")
        if not es_publico.get():
            boton_hacer_publico.configure(state="normal")
    except boto3.exceptions.Boto3Error as e:
        label_archivo.configure(text=f"❌ Error al subir archivo:\n{e}")
