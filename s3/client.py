import customtkinter
import boto3
from typing import List

def obtener_buckets(access_key: str, secret_key: str, region: str) -> List[str]:
	try:
		s3 = boto3.client(
			"s3",
			aws_access_key_id=access_key,
			aws_secret_access_key=secret_key,
			region_name=region
		)
		response = s3.list_buckets()
		nombres = [bucket["Name"] for bucket in response["Buckets"]]
		return nombres
	except Exception as e:
		print(f"❌ Error al obtener buckets: {e}")
		return []
	
def actualizar_lista_buckets(
	entry_access_key: customtkinter.CTkEntry,
	entry_secret_key: customtkinter.CTkEntry,
	entry_region: customtkinter.CTkEntry,
	menu_bucket: customtkinter.CTkOptionMenu,
	label_confirm: customtkinter.CTkLabel,
) -> None:
	buckets = obtener_buckets(
		entry_access_key.get(),
		entry_secret_key.get(),
		entry_region.get()
	)
	if buckets:
		menu_bucket.configure(values=buckets)
		menu_bucket.set(buckets[0])  # Selecciona el primero por defecto
		label_confirm.configure(text="✅ Buckets cargados")
	else:
		label_confirm.configure(text="❌ No se pudieron cargar buckets")