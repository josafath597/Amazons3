"""Utilidades para crear, mostrar y ocultar
barras de progreso (loaders) con CustomTkinter."""

import customtkinter


def crear_loader_padre(
    parent: customtkinter.CTkBaseClass, *, width: int = 300, pady: int = 5
) -> customtkinter.CTkProgressBar:
    """
    Crea una CTkProgressBar con modo indeterminado, la oculta inicialmente
    y devuelve la referencia. Requiere que el contenedor use `pack()`.

    Args:
        parent (CTkBaseClass): Contenedor padre.
        width (int): Ancho de la barra. Default 300.
        pady (int): Padding vertical. Default 5.

    Returns:
        CTkProgressBar: La barra de progreso lista para usarse.
    """
    loader = customtkinter.CTkProgressBar(parent, mode="indeterminate", width=width)
    loader.pack(pady=pady)  # la empaquetamos…
    loader.stop()  # …pero sin animarla todavía
    loader.pack_forget()  # …y la ocultamos
    return loader


def mostrar_loader(loader: customtkinter.CTkProgressBar) -> None:
    """
    Muestra la barra de progreso y empieza su animación.

    Args:
        loader (CTkProgressBar): Barra de progreso previamente creada.
    """
    loader.pack(pady=5)
    loader.start()


def ocultar_loader(loader: customtkinter.CTkProgressBar) -> None:
    """
    Detiene y oculta la barra de progreso.

    Args:
        loader (CTkProgressBar): Barra de progreso a ocultar.
    """
    loader.stop()
    loader.pack_forget()


def crear_loader_grid(parent, row=0, column=0, columnspan=1, width=300, pady=5):
    """
    Crea una CTkProgressBar configurada para usarse con el gestor `grid()`.

    Args:
        parent: Contenedor padre.
        row (int): Fila en la grilla.
        column (int): Columna en la grilla.
        columnspan (int): Columnas que debe ocupar. Default 1.
        width (int): Ancho de la barra. Default 300.
        pady (int): Padding vertical. Default 5.

    Returns:
        CTkProgressBar: La barra de progreso configurada.
    """
    loader = customtkinter.CTkProgressBar(parent, mode="indeterminate", width=width)
    loader.grid(row=row, column=column, columnspan=columnspan, pady=pady)
    loader.stop()
    loader.grid_remove()
    return loader


def mostrar_loader_grid(loader):
    """
    Muestra y activa una barra de progreso que fue creada con `grid()`.

    Args:
        loader: Barra de progreso creada previamente.
    """
    loader.grid()
    loader.start()


def ocultar_loader_grid(loader):
    """
    Detiene y oculta una barra de progreso que fue creada con `grid()`.

    Args:
        loader: Barra de progreso a ocultar.
    """
    loader.stop()
    loader.grid_remove()
