import os

extensiones_validas = (
	".pdf", ".doc", ".docx", ".xls", ".xlsx",
	".ppt", ".pptx", ".txt", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"
)

def archivo_es_valido(ruta_archivo):
	return os.path.splitext(ruta_archivo)[1].lower() in extensiones_validas