import customtkinter

def cerrar_app(app: customtkinter):
	app.destroy()  # Cierra la ventana
	app.quit()     # Detiene el mainloop correctamente