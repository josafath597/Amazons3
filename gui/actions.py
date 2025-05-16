import customtkinter
import os
from core.validators import archivo_es_valido
from tkinter import filedialog

def seleccionar_archivo(
		label_archivo: customtkinter.CTkLabel,
		textbox_name_file: customtkinter.CTkEntry,
		textbox_url: customtkinter.CTkTextbox,
		boton_subir: customtkinter.CTkButton,
		boton_hacer_publico: customtkinter.CTkButton,
		boton_copiar: customtkinter.CTkButton
):
	archivo = filedialog.askopenfilename()
	if archivo_es_valido(archivo):
		label_archivo.configure(text=f"Archivo seleccionado:\n{archivo}")

		# Establece por defecto el nombre original en el textbox (sin la ruta)
		nombre_original = os.path.basename(archivo)
		textbox_name_file.delete(0, "end")
		textbox_name_file.insert(0, nombre_original)

		textbox_url.configure(state="normal")
		textbox_url.delete("0.0", "end")
		textbox_url.configure(state="disabled")

		boton_subir.configure(state="normal")
		boton_hacer_publico.configure(state="disabled")
		boton_copiar.configure(state="disabled")
		return archivo
	else:
		label_archivo.configure(text="El archivo seleccionado no es válido.")
		return None

def copiar_url(
		root: customtkinter.CTk,
		textbox_url: customtkinter.CTkTextbox,
		label_archivo: customtkinter.CTkLabel,
) -> None:
	url = textbox_url.get("0.0", "end").strip()
	if not url:
		label_archivo.configure(text="⚠️ No hay URL para copiar")
		return
	root.clipboard_clear()
	root.clipboard_append(url)
	label_archivo.configure(text="📋 URL copiada al portapapeles")