def mostrar_ventana():

	app = customtkinter.CTk()
	app.geometry("600x550")
	app.resizable(False, False)
	app.title("Subir Archivo a AWS")
	label = customtkinter.CTkLabel(app, text="Subir Archivo a Amazon S3")
	label.pack(pady=10)
	# Crear tabview (las pestañas)
	tabview = customtkinter.CTkTabview(app, width=690, height=550)
	tabview.pack(padx=10, pady=10)

	# Agregar pestañas
	subir = "Subir archivo"
	config_tab = "Configuración"
	tabview.add(subir)
	tabview.add(config_tab)
	tabview.set(subir)

	# -------- PESTAÑA SUBIR ARCHIVO --------	
	label_archivo = customtkinter.CTkLabel(tabview.tab("Subir archivo"), text="Ningún archivo seleccionado aún.")
	label_archivo.pack(pady=10)

	frame_nombre_archivo = customtkinter.CTkFrame(tabview.tab("Subir archivo"))
	frame_nombre_archivo.pack(pady=5)

	# Label e input en una misma línea
	customtkinter.CTkLabel(frame_nombre_archivo, text="Nombre del Archivo").grid(row=0, column=0, padx=5, pady=5, sticky="e")

	textbox_name_file = customtkinter.CTkEntry(frame_nombre_archivo, placeholder_text="Nombre del Archivo", width=300)
	textbox_name_file.grid(row=0, column=1, padx=5, pady=5, sticky="w")

	# Caja de texto para mostrar URL

	customtkinter.CTkLabel(tabview.tab("Subir archivo"), text="URL del archivo en S3").pack()
	textbox_url = customtkinter.CTkTextbox(tabview.tab("Subir archivo"), height=40, width=500)
	textbox_url.configure(state="disabled")
	textbox_url.pack(pady=5)

	def copiar_url():
		app.clipboard_clear()
		app.clipboard_append(textbox_url.get("0.0", "end").strip())
		label_archivo.configure(text="📋 URL copiada al portapapeles")
	boton_copiar = customtkinter.CTkButton(tabview.tab("Subir archivo"), text="Copiar URL", command=copiar_url, state="disabled")
	boton_copiar.pack(pady=5)
	es_publico = customtkinter.CTkCheckBox(tabview.tab("Subir archivo"), text="¿Hacer público?")
	es_publico.pack(pady=5)
	es_publico.select()
	boton_seleccionar = customtkinter.CTkButton(tabview.tab("Subir archivo"), text="Seleccionar archivo", command=lambda: seleccionar_archivo(
		label_archivo,
		textbox_name_file,
		textbox_url,
		boton_subir,
		boton_hacer_publico,
		boton_copiar
	))
	boton_seleccionar.pack(pady=10)

	boton_subir = customtkinter.CTkButton(
		tabview.tab("Subir archivo"),
		text="Subir archivo",
		command=lambda: subir_archivo_a_s3(
			entry_access_key,
			entry_secret_key,
			entry_region,
			menu_bucket,
			textbox_name_file,
			es_publico,
			label_archivo,
			textbox_url,
			boton_subir,
			boton_copiar,
			boton_hacer_publico,
		),
		state="disabled" 
	)
	boton_subir.pack(pady=10)

	boton_hacer_publico = customtkinter.CTkButton(
		tabview.tab("Subir archivo"),
		text="Hacer público",
		command=lambda: hacer_publico_ultimo_archivo(
			textbox_url,
			label_archivo,
			entry_access_key,
			entry_secret_key,
			entry_region,
			menu_bucket,
			boton_hacer_publico,
		),
		state="disabled"
	)
	boton_hacer_publico.pack(pady=5)



	# -------- PESTAÑA SUBIR ARCHIVO --------1
	# Contenido de la pestaña "Opciones"
	frame_config = customtkinter.CTkFrame(tabview.tab(config_tab))
	frame_config.pack(pady=10)
	customtkinter.CTkLabel(frame_config, text="🔐 Configuración AWS").grid(row=0, column=0, columnspan=2, pady=(0, 10))

	# ACCESS KEY
	customtkinter.CTkLabel(frame_config, text="Access Key ID").grid(row=1, column=0, sticky="e", padx=5, pady=5)
	entry_access_key = customtkinter.CTkEntry(frame_config, placeholder_text="Access Key ID")
	entry_access_key.grid(row=1, column=1, sticky="w", padx=5, pady=5)

	# SECRET KEY
	customtkinter.CTkLabel(frame_config, text="Secret Access Key").grid(row=2, column=0, sticky="e", padx=5, pady=5)
	entry_secret_key = customtkinter.CTkEntry(frame_config, placeholder_text="Secret Access Key", show="*")
	entry_secret_key.grid(row=2, column=1, sticky="w", padx=5, pady=5)

	# REGIÓN
	customtkinter.CTkLabel(frame_config, text="Región").grid(row=3, column=0, sticky="e", padx=5, pady=5)
	entry_region = customtkinter.CTkEntry(frame_config)
	entry_region.grid(row=3, column=1, sticky="w", padx=5, pady=5)

	# CARGAR BUCKETS
	boton_cargar_buckets = customtkinter.CTkButton(frame_config, text="Cargar Buckets", command=lambda: actualizar_lista_buckets(
		entry_access_key,
		entry_secret_key,
		entry_region,
		menu_bucket,
		label_confirm
	))
	boton_cargar_buckets.grid(row=4, column=0, columnspan=2, pady=5)

	# Menú desplegable vacío por ahora
	# MENÚ DE BUCKETS
	menu_bucket = customtkinter.CTkOptionMenu(frame_config, values=["Sin cargar"])
	menu_bucket.grid(row=5, column=0, columnspan=2, pady=5)

	datos_cargados = cargar_config_archivo()
	if datos_cargados:
		entry_access_key.insert(0, datos_cargados.get("access_key", ""))
		entry_secret_key.insert(0, datos_cargados.get("secret_key", ""))
		entry_region.insert(0, datos_cargados.get("region", "us-east-1"))
		menu_bucket.set(datos_cargados.get("bucket", "Sin cargar"))

    # También lo actualizamos en el dict global
		config.update(datos_cargados)

	label_leyenda_menu = customtkinter.CTkLabel(
    frame_config,
    text="ℹ️ Mantén presionado y arrastra para seleccionar un bucket",
    text_color="gray"
	)
	label_leyenda_menu.grid(row=6, column=0, columnspan=2, pady=(0, 10))

	# GUARDAR
	boton_guardar = customtkinter.CTkButton(frame_config, text="Guardar configuración", command=lambda: guardar_config(
		entry_access_key,
		entry_secret_key,
		entry_region,
		menu_bucket,
		label_confirm
	))
	boton_guardar.grid(row=7, column=0, columnspan=2, pady=20)

	# BOTÓN LIMPIAR
	boton_limpiar = customtkinter.CTkButton(frame_config, text="Limpiar campos", command=lambda: limpiar_campos(
		entry_access_key,
		entry_secret_key,
		entry_region,
		menu_bucket,
		label_confirm
	))
	boton_limpiar.grid(row=8, column=0, columnspan=2, pady=(5, 20))

	# MENSAJE FINAL
	label_confirm = customtkinter.CTkLabel(frame_config, text="")
	label_confirm.grid(row=9, column=0, columnspan=2, pady=5)
	app.after(3000, lambda: label_confirm.configure(text=""))

	app.protocol("WM_DELETE_WINDOW", lambda: cerrar_app(app))
	app.mainloop()

mostrar_ventana()
