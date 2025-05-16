import customtkinter

def crear_loader_padre(parent: customtkinter.CTkBaseClass, *, width: int = 300, pady: int = 5) -> customtkinter.CTkProgressBar:
    """
    Crea una CTkProgressBar 'indeterminate', la deja oculta y
    devuelve la referencia.
    El contenedor `parent` DEBE usar el gestor de geometría pack().
    """
    loader = customtkinter.CTkProgressBar(parent, mode="indeterminate", width=width)
    loader.pack(pady=pady)    # la empaquetamos…
    loader.stop()             # …pero sin animarla todavía
    loader.pack_forget()      # …y la ocultamos
    return loader

def mostrar_loader(loader: customtkinter.CTkProgressBar) -> None:
	# vuelve a “empacar” la barra (por si estaba oculta)
	loader.pack(pady=5)
	loader.start()

def ocultar_loader(loader: customtkinter.CTkProgressBar) -> None:
	loader.stop()
	loader.pack_forget()

def crear_loader_grid(parent, row=0, column=0, columnspan=1, width=300, pady=5):
    loader = customtkinter.CTkProgressBar(parent, mode="indeterminate", width=width)
    loader.grid(row=row, column=column, columnspan=columnspan, pady=pady)
    loader.stop()
    loader.grid_remove()
    return loader

def mostrar_loader_grid(loader):  loader.grid(); loader.start()
def ocultar_loader_grid(loader):  loader.stop(); loader.grid_remove()