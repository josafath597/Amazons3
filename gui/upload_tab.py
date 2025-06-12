"""Módulo que construye la pestaña de subida de archivos en la interfaz principal."""

import threading
from typing import Any, Dict

import customtkinter

from services.uploader import subir_archivo_worker
from widgets.loader import crear_loader_padre, mostrar_loader
from gui.actions import copiar_url, seleccionar_archivo, actualizar_url_preliminar
from CTkScrollableDropdown import CTkScrollableDropdown


def crear_tab_subir(
    root: customtkinter.CTk, tab: customtkinter.CTkFrame, refs: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Construye la pestaña de subida de archivos a Amazon S3, incluyendo selección de archivo,
    entrada del nombre, opciones de visibilidad pública, botones de acción y carga asincrónica.

    Args:
        root (CTk): Ventana principal de la aplicación.
        tab (CTkFrame): Contenedor donde se insertan los elementos de esta pestaña.
        refs (Dict[str, Any]): Diccionario de referencias cruzadas con widgets de configuración.

    Returns:
        Dict[str, Any]: Diccionario con referencias a widgets relevantes para futuras operaciones.
    """
    # --- Widgets principales ---
    label_archivo = customtkinter.CTkLabel(tab, text="Ningún archivo seleccionado aún.")
    label_archivo.pack(pady=10)

    # Nombre de archivo
    frame_nombre = customtkinter.CTkFrame(tab)
    frame_nombre.pack(pady=5)

    textbox_name = customtkinter.CTkEntry(
        frame_nombre, placeholder_text="Nombre del Archivo", width=300
    )
    textbox_name.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    title = customtkinter.CTkLabel(tab, text="URL preliminar:")
    title.pack(pady=(5, 0))

    label_url_preliminar = customtkinter.CTkLabel(tab, text="")
    label_url_preliminar.pack(pady=(5, 0))

    customtkinter.CTkLabel(tab, text="Carpeta destino (dentro del bucket)").pack(
        pady=(5, 0)
    )

    carpeta_seleccionada = "/"

    def on_carpeta_change(value):
        nonlocal carpeta_seleccionada
        menu_carpeta.set(value)
        carpeta_seleccionada = value
        actualizar_url_preliminar(
            textbox_name, label_url_preliminar, refs, carpeta_seleccionada
        )
        tab.focus_set()

    menu_carpeta = customtkinter.CTkComboBox(tab, values=["/"])
    menu_carpeta.pack(pady=(5, 10))
    menu_carpeta.set("/")

    dropdown_carpeta = CTkScrollableDropdown(
        attach=menu_carpeta,
        values=["/"],  # se actualizará luego
        width=400,  # ancho del popup
        height=500,  # alto del popup
        x=-130,  # desplaza a la izquierda ≈ (400-240)/2
        y=30,  # unos píxeles debajo del OptionMenu,
        justify="left",
        button_color="transparent",
        command=on_carpeta_change,  # clic o Enter → callback
        resize=False,
    )

    textbox_name_file = customtkinter.CTkEntry(
        frame_nombre, placeholder_text="Nombre del Archivo", width=300
    )

    textbox_name.bind(
        "<KeyRelease>",
        lambda *_: actualizar_url_preliminar(
            textbox_name, label_url_preliminar, refs, carpeta_seleccionada
        ),
    )

    # URL
    customtkinter.CTkLabel(tab, text="URL del archivo en S3").pack()
    textbox_url = customtkinter.CTkTextbox(tab, height=40, width=500, state="disabled")
    textbox_url.pack(pady=5)

    # Botones
    boton_copiar = customtkinter.CTkButton(tab, text="Copiar URL", state="disabled")
    boton_copiar.pack(pady=5)

    boton_seleccionar = customtkinter.CTkButton(
        tab, text="Seleccionar archivo", state="disabled"
    )
    boton_subir = customtkinter.CTkButton(tab, text="Subir archivo", state="disabled")

    boton_seleccionar.pack(pady=10)
    boton_subir.pack(pady=10)

    archivo_seleccionado = None

    def seleccionar_y_guardar():
        nonlocal archivo_seleccionado
        archivo_seleccionado = seleccionar_archivo(
            label_archivo,
            textbox_name,
            textbox_url,
            boton_subir,
            boton_copiar,
        )
        actualizar_url_preliminar(
            textbox_name, label_url_preliminar, refs, carpeta_seleccionada
        )

    # ---- Conectar callbacks (lambda o funciones aparte) ----
    boton_seleccionar.configure(command=seleccionar_y_guardar)

    loader = crear_loader_padre(tab)

    def lanzar_subida():
        mostrar_loader(loader)
        threading.Thread(
            target=subir_archivo_worker,
            kwargs={
                "archivo_seleccionado": archivo_seleccionado,
                "entry_access_key": refs["entry_access"],
                "entry_secret_key": refs["entry_secret"],
                "entry_region": refs["entry_region"],
                "menu_bucket": refs["menu_bucket"],
                "textbox_name_file": textbox_name,
                "label_archivo": label_archivo,
                "textbox_url": textbox_url,
                "boton_subir": boton_subir,
                "boton_copiar": boton_copiar,
                "carpeta_seleccionada": carpeta_seleccionada,
                "loader": loader,
                "root": root,
            },
            daemon=True,
        ).start()

    boton_subir.configure(command=lanzar_subida)

    boton_copiar.configure(command=lambda: copiar_url(root, textbox_url, label_archivo))

    # Devolver referencias compartidas
    return {
        "title": title,
        "label_archivo": label_archivo,
        "textbox_name": textbox_name,
        "textbox_url": textbox_url,
        "boton_subir": boton_subir,
        "boton_copiar": boton_copiar,
        "boton_seleccionar": boton_seleccionar,
        "label_url_preliminar": label_url_preliminar,
        "textbox_name_file": textbox_name_file,
        "menu_carpeta": menu_carpeta,
        "dropdown_carpeta": dropdown_carpeta,
    }
