"""Este módulo contiene funciones relacionadas con el cierre de la aplicación."""

import customtkinter


def cerrar_app(app: customtkinter):
    """Cierra la ventana de la aplicación y detiene el mainloop."""
    app.destroy()  # Cierra la ventana
    app.quit()  # Detiene el mainloop correctamente
