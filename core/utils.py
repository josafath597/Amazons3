"""Este módulo contiene funciones relacionadas con el cierre de la aplicación."""

import customtkinter
import re


def cerrar_app(app: customtkinter):
    """Cierra la ventana de la aplicación y detiene el mainloop."""
    app.destroy()  # Cierra la ventana
    app.quit()  # Detiene el mainloop correctamente


def es_uuid(texto: str) -> bool:
    return bool(
        re.fullmatch(
            r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}",
            texto,
            re.IGNORECASE,
        )
    )
