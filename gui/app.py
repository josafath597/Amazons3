import customtkinter
from typing import Dict, Any
from gui.config_tab import crear_tab_config
from gui.upload_tab import crear_tab_subir
from core.utils import cerrar_app

def mostrar_ventana() -> None:
	app = customtkinter.CTk()
	app.geometry("600x550")
	app.resizable(False, False)
	app.title("Subir Archivo a AWS")

	# Encabezado
	customtkinter.CTkLabel(app, text="Subir Archivo a Amazon S3").pack(pady=10)

	# Pestañas
	tabview = customtkinter.CTkTabview(app, width=690, height=550)
	tabview.pack(padx=10, pady=10)

	# --- Pestaña SUBIR ---
	tab_subir        = tabview.add("Subir archivo")
	tab_conf       = tabview.add("Configuración")

	# Construir cada pestaña con funciones auxiliares
	refs: Dict[str, Any] = {}                 # diccionario vacío
	crear_tab_config(tab_conf, refs)
	refs |= crear_tab_subir(app, tab_subir, refs)   # llena refs

	# Handler de cierre
	app.protocol("WM_DELETE_WINDOW", lambda: cerrar_app(app))
	app.mainloop()