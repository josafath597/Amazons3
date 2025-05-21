"""Helperps para la carpeta de Gui"""

from typing import Any, Dict, List


def set_menu_carpeta(refs: Dict[str, Any], carpetas: List[str]) -> None:
    """Rellena el OptionMenu de carpetas con la lista recibida.

    Agrega la raíz «/», actualiza los valores y selecciona «/» como predeterminado.
    Se ignora la llamada si el diccionario no contiene la clave "menu_carpeta".
    """
    if "menu_carpeta" not in refs:
        return

    opciones = ["/"] + carpetas
    refs["menu_carpeta"].configure(values=opciones)
    refs["menu_carpeta"].set("/")
