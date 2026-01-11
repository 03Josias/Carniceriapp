import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, END, StringVar
from Funciones import *
from datetime import datetime

# ============================
# CONFIGURACIÓN GLOBAL
# ============================
COLOR_BG = "#f5f5f5"
COLOR_SIDEBAR = "#2c3e50"
COLOR_SIDEBAR_HOVER = "#34495e"
COLOR_ACCENT = "#3498db"
COLOR_HEADER = "#ecf0f1"
COLOR_TEXT = "#2c3e50"
COLOR_BTN_SUCCESS = "#27ae60"
COLOR_BTN_DANGER = "#e74c3c"
COLOR_BTN_PRIMARY = "#3498db"
COLOR_WHITE = "#ffffff"

class CarniceriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carnicería - Gestión Total")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        self.tabla_actual = None
        self.tree = None
        self.orden_columnas = {}


        self.crear_sidebar()
        self.crear_area_contenido()
        self.mostrar_dashboard()

    # ============================
    # SIDEBAR
    # ============================
    def crear_sidebar(self):
        sidebar = tk.Frame(self.root, bg=COLOR_SIDEBAR, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        titulo = tk.Label(sidebar, text="CARNICERÍA", font=("Arial", 15, "bold"), bg=COLOR_SIDEBAR, fg="white")
        titulo.pack(pady=(20, 0))
        subtitulo = tk.Label(sidebar, text="Gestión Total", font=("Arial", 8), bg=COLOR_SIDEBAR, fg="#95a5a6")
        subtitulo.pack(pady=(0, 30))

        botones = [
            ("Dashboard", "Dashboard"),
            ("MediasR", "MediasR"),
            ("Cortes", "CortesMedia"),
            ("Productos", "Productos"),
            ("Categorías", "Categoria"),
            ("Ventas", "Ventas"),
            ("DetalleVenta", "DetalleVenta"),
            ("🔍 Recaudaciones", "Recaudaciones")
        ]

        for texto, tabla in botones:
            btn = tk.Button(
                sidebar,
                text=texto,
                font=("Arial", 11),
                bg=COLOR_SIDEBAR,
                fg="white",
                activebackground=COLOR_SIDEBAR_HOVER,
                activeforeground="white",
                relief="flat",
                bd=0,
                padx=20,
                pady=14,
                anchor="w",
                cursor="hand2",
                command=lambda t=tabla: self.seleccionar_vista(t)
            )
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLOR_SIDEBAR_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_SIDEBAR))

    # ============================
    # ÁREA DE CONTENIDO
    # ============================
    def crear_area_contenido(self):
        self.contenido = tk.Frame(self.root, bg=COLOR_BG)
        self.contenido.pack(side="right", fill="both", expand=True)

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def seleccionar_vista(self, tabla):
        self.tabla_actual = tabla
        if tabla == "Dashboard":
            self.mostrar_dashboard()
        elif tabla == "Recaudaciones":
            self.mostrar_recaudaciones()
        else:
            self.mostrar_tabla(tabla)

    # ============================
    # DASHBOARD
    # ============================
    def mostrar_dashboard(self):
        self.limpiar_contenido()
        self.tabla_actual = "Dashboard"

        titulo = tk.Label(self.contenido, text="DASHBOARD", font=("Arial", 16, "bold"), bg=COLOR_BG, fg=COLOR_TEXT)
        titulo.pack(pady=20)

        # Recaudación del día
        frame_recaudacion = tk.Frame(self.contenido, bg=COLOR_WHITE, relief="solid", bd=1)
        frame_recaudacion.pack(fill="x", padx=20, pady=(0, 15))

        header = tk.Frame(frame_recaudacion, bg=COLOR_WHITE)
        header.pack(fill="x", padx=20, pady=(15, 5))
        tk.Label(header, text="RECAUDACIÓN DEL DÍA", font=("Arial", 12, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT).pack(side="left")
        btn_actualizar = tk.Button(header, text="Actualizar", font=("Arial", 9), bg=COLOR_BTN_PRIMARY, fg="white", relief="flat", padx=15, pady=5, cursor="hand2", command=self.actualizar_dashboard)
        btn_actualizar.pack(side="right")

        self.lbl_monto = tk.Label(frame_recaudacion, text="$ 0.00", font=("Arial", 32, "bold"), bg=COLOR_WHITE, fg=COLOR_ACCENT)
        self.lbl_monto.pack(pady=(10, 5))
        self.lbl_timestamp = tk.Label(frame_recaudacion, text="Última actualización: --", font=("Arial", 9), bg=COLOR_WHITE, fg="#7f8c8d")
        self.lbl_timestamp.pack(pady=(0, 15))

        # Productos vendidos hoy
        frame_tabla = tk.Frame(self.contenido, bg=COLOR_WHITE, relief="solid", bd=1)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tk.Label(frame_tabla, text="PRODUCTOS VENDIDOS HOY", font=("Arial", 11, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w", padx=20, pady=(15, 10))

        self.tree_dashboard = ttk.Treeview(frame_tabla, columns=("Producto", "Categoría", "Peso", "Ingreso"), show="headings", height=12, style="Custom.Treeview")
        for col in self.tree_dashboard["columns"]:
            self.tree_dashboard.heading(col, text=col)
            self.tree_dashboard.column(col, anchor="center", width=150)
        self.tree_dashboard.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.actualizar_dashboard()

    def actualizar_dashboard(self):
        total = obtener_recaudacion_hoy()
        self.lbl_monto.config(text=f"$ {total:,.2f}")
        self.lbl_timestamp.config(text=f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        productos = obtener_productos_vendidos_hoy()
        self.tree_dashboard.delete(*self.tree_dashboard.get_children())
        for i, (nombre, categoria, peso, ingreso) in enumerate(productos):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree_dashboard.insert("", "end", values=(nombre, categoria, f"{peso:.2f}", f"${ingreso:,.2f}"), tags=(tag,))
        self.tree_dashboard.tag_configure("evenrow", background=COLOR_WHITE)
        self.tree_dashboard.tag_configure("oddrow", background="#f8f9fa")

    # ============================
    # VISTA TABLAS
    # ============================
    def mostrar_tabla(self, tabla):
        self.limpiar_contenido()

        titulo = tk.Label(self.contenido, text=tabla.upper(), font=("Arial", 16, "bold"), bg=COLOR_BG, fg=COLOR_TEXT)
        titulo.pack(pady=20)

        columnas = obtener_columnas(tabla)
        self.tree = ttk.Treeview(self.contenido, columns=columnas, show="headings", height=15, style="Custom.Treeview")
        for col in columnas:
            self.tree.heading(col, text=col, command=lambda c=col: self.ordenar_por_columna(c))
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(fill="both", expand=True, padx=20)

        self.actualizar_vista_tabla(tabla)

        frame_botones = tk.Frame(self.contenido, bg=COLOR_BG)
        frame_botones.pack(fill="x", padx=20, pady=15)

        if tabla != "CortesMedia":
            btn_agregar = tk.Button(frame_botones, text="Agregar", font=("Arial", 10, "bold"), bg=COLOR_BTN_SUCCESS, fg="white", relief="flat", padx=25, pady=12, cursor="hand2", command=lambda: self.agregar_registro(tabla))
            btn_agregar.pack(side="left", padx=5)

        btn_editar = tk.Button(frame_botones, text="Editar", font=("Arial", 10, "bold"), bg=COLOR_BTN_PRIMARY, fg="white", relief="flat", padx=25, pady=12, cursor="hand2", command=lambda: self.editar_registro(tabla))
        btn_editar.pack(side="left", padx=5)

        btn_eliminar = tk.Button(frame_botones, text="Eliminar", font=("Arial", 10, "bold"), bg=COLOR_BTN_DANGER, fg="white", relief="flat", padx=25, pady=12, cursor="hand2", command=lambda: self.eliminar_registro(tabla))
        btn_eliminar.pack(side="left", padx=5)

        if tabla == "MediasR":
            btn_conteo = tk.Button(frame_botones, text="Hacer Conteo", font=("Arial", 10, "bold"), bg=COLOR_BTN_PRIMARY, fg="white", relief="flat", padx=25, pady=12, cursor="hand2", command=self.hacer_conteo)
            btn_conteo.pack(side="left", padx=5)

    def actualizar_vista_tabla(self, tabla=None):
        if not tabla:
            tabla = self.tabla_actual
        datos = []
        if tabla == "Productos":
            datos = listar_productos()
        elif tabla == "Categoria":
            datos = listar_categorias()
        elif tabla == "MediasR":
            datos = listar_medias()
        elif tabla == "CortesMedia":
            datos = listar_corte_medias()
        elif tabla == "Ventas":
            datos = listar_ventas()
        elif tabla == "DetalleVenta":
            datos = listar_detalles_venta()

        self.tree.delete(*self.tree.get_children())
        for i, fila in enumerate(datos):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=fila, tags=(tag,))
        self.tree.tag_configure("evenrow", background=COLOR_WHITE)
        self.tree.tag_configure("oddrow", background="#f8f9fa")

    def ordenar_por_columna(self, columna):
        direccion = "DESC" if self.orden_columnas.get(columna) == "ASC" else "ASC"
        self.orden_columnas[columna] = direccion
        datos = ordenar_por(self.tabla_actual, columna, direccion)
        self.tree.delete(*self.tree.get_children())
        for i, fila in enumerate(datos):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=fila, tags=(tag,))
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col + (" ▲" if col == columna and direccion == "ASC" else " ▼" if col == columna else ""))

    # ============================
    # AGREGAR REGISTRO
    # ============================
    def agregar_registro(self, tabla):
        if tabla == "Productos":
            self.ventana_agregar_producto()
        elif tabla == "Categoria":
            self.ventana_agregar_categoria()
        elif tabla == "MediasR":
            self.cargar_media_res()
        elif tabla == "Ventas":
            self.cargar_venta()
        elif tabla == "DetalleVenta":
            self.cargar_venta()

    def ventana_agregar_producto(self):
        ventana = Toplevel(self.root)
        ventana.title("Agregar Producto")
        ventana.geometry("420x300")
        ventana.resizable(False, False)
        ventana.configure(bg=COLOR_WHITE)
        ventana.transient(self.root)
        ventana.grab_set()

        tk.Label(ventana, text="Nombre del Producto:", bg=COLOR_WHITE, fg=COLOR_TEXT, font=("Arial", 10)).grid(row=0, column=0, padx=20, pady=12, sticky="e")
        entry_nombre = tk.Entry(ventana, font=("Arial", 10), relief="solid", bd=1, width=22)
        entry_nombre.grid(row=0, column=1, padx=20, pady=12)

        tk.Label(ventana, text="Precio por kg:", bg=COLOR_WHITE, fg=COLOR_TEXT, font=("Arial", 10)).grid(row=1, column=0, padx=20, pady=12, sticky="e")
        entry_precio = tk.Entry(ventana, font=("Arial", 10), relief="solid", bd=1, width=22)
        entry_precio.grid(row=1, column=1, padx=20, pady=12)

        tk.Label(ventana, text="Categoría:", bg=COLOR_WHITE, fg=COLOR_TEXT, font=("Arial", 10)).grid(row=2, column=0, padx=20, pady=12, sticky="e")
        categorias = obtener_categorias()
        nombres = [c[1] for c in categorias]
        combo = ttk.Combobox(ventana, values=nombres, state="readonly", font=("Arial", 10), width=20)
        combo.grid(row=2, column=1, padx=20, pady=12)
        if nombres:
            combo.set(nombres[0])

        lbl_mensaje = tk.Label(ventana, text="", font=("Arial", 9), bg=COLOR_WHITE)
        lbl_mensaje.grid(row=3, column=0, columnspan=2, pady=5)

        def guardar():
            nombre = entry_nombre.get().strip()
            try:
                precio = float(entry_precio.get())
                if precio <= 0:
                    raise ValueError("Precio debe ser > 0")
                id_cat = next(c[0] for c in categorias if c[1] == combo.get())
                cargar_producto(nombre, precio, id_cat)
                lbl_mensaje.config(text="✓ Producto agregado", fg=COLOR_BTN_SUCCESS)
                ventana.after(800, ventana.destroy)
                self.actualizar_vista_tabla("Productos")
            except Exception as e:
                lbl_mensaje.config(text=f"Error: {e}", fg=COLOR_BTN_DANGER)

        tk.Button(ventana, text="Guardar", font=("Arial", 10, "bold"), bg=COLOR_BTN_SUCCESS, fg="white", relief="flat", padx=30, pady=10, cursor="hand2", command=guardar).grid(row=4, column=0, columnspan=2, pady=15)

    def ventana_agregar_categoria(self):
        ventana = Toplevel(self.root)
        ventana.title("Agregar Categoría")
        ventana.geometry("400x200")
        ventana.resizable(False, False)
        ventana.configure(bg=COLOR_WHITE)
        ventana.transient(self.root)
        ventana.grab_set()

        tk.Label(ventana, text="Nombre de Categoría:", bg=COLOR_WHITE, fg=COLOR_TEXT, font=("Arial", 10)).grid(row=0, column=0, padx=20, pady=20, sticky="e")
        entry = tk.Entry(ventana, font=("Arial", 10), relief="solid", bd=1, width=22)
        entry.grid(row=0, column=1, padx=20, pady=20)

        lbl_mensaje = tk.Label(ventana, text="", font=("Arial", 9), bg=COLOR_WHITE)
        lbl_mensaje.grid(row=1, column=0, columnspan=2, pady=5)

        def guardar():
            nombre = entry.get().strip()
            if not nombre:
                lbl_mensaje.config(text="El nombre no puede estar vacío", fg=COLOR_BTN_DANGER)
                return
            try:
                cargar_categoria(nombre)
                lbl_mensaje.config(text="✓ Categoría agregada", fg=COLOR_BTN_SUCCESS)
                ventana.after(800, ventana.destroy)
                self.actualizar_vista_tabla("Categoria")
            except Exception as e:
                lbl_mensaje.config(text=f"Error: {e}", fg=COLOR_BTN_DANGER)

        tk.Button(ventana, text="Guardar", font=("Arial", 10, "bold"), bg=COLOR_BTN_SUCCESS, fg="white", relief="flat", padx=30, pady=10, cursor="hand2", command=guardar).grid(row=2, column=0, columnspan=2, pady=15)

    # ============================
    # EDITAR REGISTRO
    # ============================
    def editar_registro(self, tabla):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Debe seleccionar un registro para editar")
            return

        valores = self.tree.item(selected[0], "values")
        columnas = obtener_columnas(tabla)

        ventana = Toplevel(self.root)
        ventana.title(f"Editar {tabla}")
        ventana.geometry("450x400")
        ventana.resizable(False, False)
        ventana.configure(bg=COLOR_WHITE)
        ventana.transient(self.root)
        ventana.grab_set()

        widgets = {}
        categorias = obtener_categorias() if tabla == "Productos" else []

        for i, col in enumerate(columnas):
            tk.Label(ventana, text=f"{col}:", bg=COLOR_WHITE, fg=COLOR_TEXT, font=("Arial", 10)).grid(row=i, column=0, padx=20, pady=8, sticky="e")
            if i == 0:
                tk.Label(ventana, text=valores[i], bg="#ecf0f1", fg=COLOR_TEXT, font=("Arial", 10), relief="solid", bd=1, width=22, anchor="w").grid(row=i, column=1, padx=20, pady=8)
            else:
                if tabla == "Productos" and "IDCategoria" in col:
                    nombres = [c[1] for c in categorias]
                    combo = ttk.Combobox(ventana, values=nombres, state="readonly", font=("Arial", 10), width=20)
                    combo.grid(row=i, column=1, padx=20, pady=8)
                    actual = next((c[1] for c in categorias if str(c[0]) == valores[i]), "")
                    combo.set(actual)
                    widgets[col] = ("combo", combo, categorias)
                else:
                    entry = tk.Entry(ventana, font=("Arial", 10), relief="solid", bd=1, width=22)
                    entry.grid(row=i, column=1, padx=20, pady=8)
                    entry.insert(0, valores[i])
                    widgets[col] = ("entry", entry)

        lbl_mensaje = tk.Label(ventana, text="", font=("Arial", 9), bg=COLOR_WHITE)
        lbl_mensaje.grid(row=len(columnas), column=0, columnspan=2, pady=5)

        def guardar_cambios():
            try:
                nuevos = {}
                for col, (tipo, widget, *extra) in widgets.items():
                    if tipo == "entry":
                        nuevos[col] = widget.get().strip()
                    elif tipo == "combo":
                        nombre = widget.get()
                        id_cat = next(c[0] for c in extra[0] if c[1] == nombre)
                        nuevos[col] = id_cat

                if tabla == "Productos":
                    if not nuevos["NombreProducto"]:
                        raise ValueError("El nombre no puede estar vacío")
                    nuevos["Precio"] = float(nuevos["Precio"])
                    if nuevos["Precio"] <= 0:
                        raise ValueError("El precio debe ser > 0")

                editar_registro_db(tabla, nuevos, columnas[0], valores[0])
                lbl_mensaje.config(text="✓ Registro actualizado", fg=COLOR_BTN_SUCCESS)
                ventana.after(800, ventana.destroy)
                self.actualizar_vista_tabla(tabla)
            except Exception as e:
                lbl_mensaje.config(text=f"Error: {e}", fg=COLOR_BTN_DANGER)

        tk.Button(ventana, text="Guardar Cambios", font=("Arial", 10, "bold"), bg=COLOR_BTN_PRIMARY, fg="white", relief="flat", padx=30, pady=10, cursor="hand2", command=guardar_cambios).grid(row=len(columnas) + 1, column=0, columnspan=2, pady=15)

    # ============================
    # ELIMINAR REGISTRO
    # ============================
    def eliminar_registro(self, tabla):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Debe seleccionar un registro para eliminar")
            return

        valores = self.tree.item(selected[0], "values")
        id_valor = valores[0]

        if tabla == "Productos" and producto_tiene_ventas(id_valor):
            messagebox.showerror("No se puede eliminar", "Este producto tiene ventas asociadas.")
            return

        ventana = Toplevel(self.root)
        ventana.title("Eliminar Registro")
        ventana.geometry("400x220")
        ventana.resizable(False, False)
        ventana.configure(bg=COLOR_WHITE)
        ventana.transient(self.root)
        ventana.grab_set()

        tk.Label(ventana, text="⚠️", font=("Arial", 30), bg=COLOR_WHITE, fg="#f39c12").pack(pady=(20, 10))
        tk.Label(ventana, text="¿Está seguro de que desea\neliminar este registro?", font=("Arial", 12), bg=COLOR_WHITE, fg=COLOR_TEXT, justify="center").pack(pady=5)
        tk.Label(ventana, text="Esta acción no se puede deshacer.", font=("Arial", 9), bg=COLOR_WHITE, fg="#7f8c8d").pack(pady=5)

        def confirmar():
            try:
                eliminar_registro_db(tabla, id_valor, obtener_columnas(tabla)[0])
                ventana.destroy()
                self.actualizar_vista_tabla(tabla)
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
            except Exception as e:
                ventana.destroy()
                messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")

        frame_botones = tk.Frame(ventana, bg=COLOR_WHITE)
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="Cancelar", font=("Arial", 10), bg="#95a5a6", fg="white", relief="flat", padx=30, pady=10, cursor="hand2", command=ventana.destroy).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Eliminar", font=("Arial", 10, "bold"), bg=COLOR_BTN_DANGER, fg="white", relief="flat", padx=30, pady=10, cursor="hand2", command=confirmar).pack(side="left", padx=10)

    # ============================
    # CARGAR MEDIA RES + CORTES
    # ============================
    def cargar_media_res(self):
        ventana = Toplevel(self.root)
        ventana.title("Cargar Media Res")
        ventana.geometry("420x280")
        ventana.resizable(False, False)
        ventana.configure(bg=COLOR_WHITE)
        ventana.transient(self.root)
        ventana.grab_set()

        tk.Label(ventana, text="DATOS DE LA MEDIA", font=("Arial", 11, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT).grid(row=0, column=0, columnspan=2, padx=20, pady=(15, 5), sticky="w")
        tk.Frame(ventana, height=2, bg=COLOR_HEADER).grid(row=1, column=0, columnspan=2, sticky="ew", padx=20)

        tk.Label(ventana, text="Fecha (YYYY-MM-DD):", bg=COLOR_WHITE, fg=COLOR_TEXT, font=("Arial", 10)).grid(row=2, column=0, padx=20, pady=12, sticky="e")
        entry_fecha = tk.Entry(ventana, font=("Arial", 10), relief="solid", bd=1, width=22)
        entry_fecha.grid(row=2, column=1, padx=20, pady=12)
        entry_fecha.insert(0, datetime.today().strftime("%Y-%m-%d"))

        tk.Label(ventana, text="Peso total (kg):", bg=COLOR_WHITE, fg=COLOR_TEXT, font=("Arial", 10)).grid(row=3, column=0, padx=20, pady=12, sticky="e")
        entry_peso = tk.Entry(ventana, font=("Arial", 10), relief="solid", bd=1, width=22)
        entry_peso.grid(row=3, column=1, padx=20, pady=12)

        tk.Label(ventana, text="Precio por kg:", bg=COLOR_WHITE, fg=COLOR_TEXT, font=("Arial", 10)).grid(row=4, column=0, padx=20, pady=12, sticky="e")
        entry_precio = tk.Entry(ventana, font=("Arial", 10), relief="solid", bd=1, width=22)
        entry_precio.grid(row=4, column=1, padx=20, pady=12)

        lbl_mensaje = tk.Label(ventana, text="", font=("Arial", 9), bg=COLOR_WHITE)
        lbl_mensaje.grid(row=5, column=0, columnspan=2, pady=5)

        def continuar():
            try:
                fecha = entry_fecha.get()
                peso = float(entry_peso.get())
                precio = float(entry_precio.get())
                if peso <= 0 or precio <= 0:
                    raise ValueError("Peso y precio deben ser > 0")
                id_media = cargar_media(fecha, peso, precio)
                lbl_mensaje.config(text=f"✓ Media N° {id_media} cargada", fg=COLOR_BTN_SUCCESS)
                ventana.destroy()
                self.mostrar_formulario_cortes(id_media, peso)
            except Exception as e:
                lbl_mensaje.config(text=f"Error: {e}", fg=COLOR_BTN_DANGER)

        tk.Button(ventana, text="Cargar y Continuar", font=("Arial", 10, "bold"), bg=COLOR_BTN_PRIMARY, fg="white", relief="flat", padx=25, pady=10, cursor="hand2", command=continuar).grid(row=6, column=0, columnspan=2, pady=15)

    def mostrar_formulario_cortes(self, id_media, peso_media):
        ventana = Toplevel(self.root)
        ventana.title(f"Cargar Cortes - Media N° {id_media}")
        ventana.geometry("500x700")
        ventana.resizable(False, False)
        ventana.configure(bg=COLOR_WHITE)
        ventana.transient(self.root)
        ventana.grab_set()

        tk.Label(ventana, text=f"Media: {peso_media} kg @ $480/kg = ${peso_media * 480:,.2f}", font=("Arial", 10), bg="#ecf0f1", fg=COLOR_TEXT).pack(pady=10)
        tk.Label(ventana, text="CORTES OBTENIDOS", font=("Arial", 11, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT).pack(pady=(10, 5))
        tk.Label(ventana, text="(Ingrese el peso de cada corte)", font=("Arial", 9), bg=COLOR_WHITE, fg="#7f8c8d").pack(pady=(0, 15))

        frame_scroll = tk.Frame(ventana, bg=COLOR_WHITE)
        frame_scroll.pack(fill="both", expand=True, padx=20)

        canvas = tk.Canvas(frame_scroll, bg=COLOR_WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        frame_cortes = tk.Frame(canvas, bg=COLOR_WHITE)

        frame_cortes.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_cortes, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        productos = obtener_productos_por_categoria(1)
        entries = {}

        for i, (id_prod, nombre, precio, _) in enumerate(productos):
            tk.Label(frame_cortes, text=f"{nombre}:", bg=COLOR_WHITE, fg=COLOR_TEXT, font=("Arial", 10), width=18, anchor="e").grid(row=i, column=0, padx=10, pady=8, sticky="e")
            entry = tk.Entry(frame_cortes, font=("Arial", 10), relief="solid", bd=1, width=10)
            entry.grid(row=i, column=1, padx=5, pady=8)
            entry.insert(0, "0.0")
            tk.Label(frame_cortes, text="kg", bg=COLOR_WHITE, fg=COLOR_TEXT, font=("Arial", 10)).grid(row=i, column=2, padx=(0, 10), pady=8, sticky="w")
            entries[id_prod] = entry

        tk.Frame(ventana, height=2, bg=COLOR_HEADER).pack(fill="x", padx=20, pady=15)

        lbl_total = tk.Label(ventana, text=f"Total pesado: 0.0 kg / {peso_media} kg", font=("Arial", 10), bg=COLOR_WHITE, fg=COLOR_TEXT)
        lbl_total.pack()
        lbl_merma = tk.Label(ventana, text=f"Diferencia (Merma): {peso_media} kg (100.0%)", font=("Arial", 10), bg=COLOR_WHITE, fg="#e74c3c")
        lbl_merma.pack(pady=(5, 10))

        def actualizar_totales():
            total = 0.0
            for id_prod, entry in entries.items():
                try:
                    total += float(entry.get())
                except ValueError:
                    pass
            merma = peso_media - total
            porc = (merma / peso_media * 100) if peso_media > 0 else 0
            lbl_total.config(text=f"Total pesado: {total:.2f} kg / {peso_media} kg")
            lbl_merma.config(text=f"Diferencia (Merma): {merma:.2f} kg ({porc:.1f}%)", fg="#e74c3c" if porc > 15 else "#f39c12")

        for entry in entries.values():
            entry.bind("<KeyRelease>", lambda e: actualizar_totales())

        lbl_mensaje = tk.Label(ventana, text="", font=("Arial", 9), bg=COLOR_WHITE)
        lbl_mensaje.pack(pady=10)

                # === BOTONES ===
        frame_botones = tk.Frame(ventana, bg=COLOR_WHITE)
        frame_botones.pack(pady=15)

        def guardar_cortes():
            try:
                cortes = []
                for id_prod, entry in entries.items():
                    val = entry.get().strip()
                    if val and float(val) > 0:
                        cortes.append((id_media, id_prod, float(val)))
                if not cortes:
                    raise ValueError("Debe ingresar al menos un corte con peso > 0")
                for id_med, id_prod, peso in cortes:
                    guardar_corte_media(id_med, id_prod, peso)
                lbl_mensaje.config(text=f"✓ {len(cortes)} cortes guardados", fg=COLOR_BTN_SUCCESS)
                ventana.after(800, ventana.destroy)
                self.actualizar_vista_tabla("CortesMedia")
            except Exception as e:
                lbl_mensaje.config(text=f"Error: {e}", fg=COLOR_BTN_DANGER)

        tk.Button(frame_botones, text="Cancelar", font=("Arial", 10), bg="#95a5a6", fg="white", relief="flat", padx=25, pady=10, cursor="hand2", command=ventana.destroy).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Guardar Cortes", font=("Arial", 10, "bold"), bg=COLOR_BTN_SUCCESS, fg="white", relief="flat", padx=25, pady=10, cursor="hand2", command=guardar_cortes).pack(side="left", padx=10)
    # ============================
    # HACER CONTEO
    # ============================
    def hacer_conteo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Debe seleccionar una media para hacer el conteo")
            return

        id_media = self.tree.item(selected[0], "values")[0]
        datos = obtener_media(id_media)
        if not datos:
            messagebox.showerror("Error", "No se encontró la media seleccionada")
            return

        id_m, fecha, peso_media, precio_kg = datos
        total_pagado = peso_media * precio_kg
        cortes = obtener_cortes_media(id_media)

        ventana = Toplevel(self.root)
        ventana.title(f"Conteo de Media N° {id_media}")
        ventana.geometry("550x700")
        ventana.resizable(False, False)
        ventana.configure(bg=COLOR_WHITE)
        ventana.transient(self.root)

        # Centrar
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ventana.winfo_width() // 2)
        y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
        ventana.geometry(f"+{x}+{y}")

        # Datos de compra
        frame_compra = tk.Frame(ventana, bg=COLOR_WHITE)
        frame_compra.pack(fill="x", padx=20, pady=(20, 15))
        tk.Label(frame_compra, text="DATOS DE COMPRA", font=("Arial", 12, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")
        tk.Frame(frame_compra, height=2, bg=COLOR_HEADER).pack(fill="x", pady=5)

        info = [("Fecha:", fecha), ("Peso:", f"{peso_media} kg"), ("Precio/kg:", f"${precio_kg:,.2f}"), ("Total Pagado:", f"${total_pagado:,.2f}")]
        for label, valor in info:
            f = tk.Frame(frame_compra, bg=COLOR_WHITE)
            f.pack(fill="x", pady=3)
            tk.Label(f, text=label, font=("Arial", 10, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT, width=15, anchor="w").pack(side="left")
            tk.Label(f, text=valor, font=("Arial", 10), bg=COLOR_WHITE, fg=COLOR_TEXT).pack(side="left", padx=10)

        # Cortes
        frame_cortes = tk.Frame(ventana, bg=COLOR_WHITE)
        frame_cortes.pack(fill="both", expand=True, padx=20, pady=15)
        tk.Label(frame_cortes, text="CORTES OBTENIDOS", font=("Arial", 12, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")

        tree = ttk.Treeview(frame_cortes, columns=("Corte", "Peso", "Precio"), show="headings", height=10, style="Custom.Treeview")
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)
        tree.pack(fill="both", expand=True, pady=5)

        total_cortes = 0.0
        valor_potencial = 0.0
        for i, (nombre, peso, precio) in enumerate(cortes):
            total_cortes += peso
            valor_potencial += peso * precio
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=(nombre, f"{peso:.2f}", f"${precio:,.2f}"), tags=(tag,))
        tree.tag_configure("evenrow", background=COLOR_WHITE)
        tree.tag_configure("oddrow", background="#f8f9fa")

        # Resumen
        frame_resumen = tk.Frame(ventana, bg="#ecf0f1")
        frame_resumen.pack(fill="x", padx=20, pady=15)
        tk.Label(frame_resumen, text="RESUMEN", font=("Arial", 11, "bold"), bg="#ecf0f1", fg=COLOR_TEXT).pack(anchor="w", padx=15, pady=(10, 5))

        merma = peso_media - total_cortes
        porc_merma = (merma / peso_media * 100) if peso_media > 0 else 0
        ganancia = valor_potencial - total_pagado
        porc_ganancia = (ganancia / total_pagado * 100) if total_pagado > 0 else 0

        resumen = [("Total Cortes:", f"{total_cortes:.2f} kg"), ("Merma:", f"{merma:.2f} kg ({porc_merma:.1f}%)"), ("Valor Potencial:", f"${valor_potencial:,.2f}"), ("Ganancia Potencial:", f"${ganancia:,.2f} ({porc_ganancia:.1f}%)")]
        for label, valor in resumen:
            f = tk.Frame(frame_resumen, bg="#ecf0f1")
            f.pack(fill="x", pady=3)
            tk.Label(f, text=label, font=("Arial", 10, "bold"), bg="#ecf0f1", fg=COLOR_TEXT, width=18, anchor="w").pack(side="left")
            color = COLOR_TEXT if "Ganancia" not in label else (COLOR_BTN_SUCCESS if ganancia > 0 else COLOR_BTN_DANGER)
            tk.Label(f, text=valor, font=("Arial", 10), bg="#ecf0f1", fg=color).pack(side="left", padx=10)

        tk.Button(ventana, text="Cerrar", font=("Arial", 10, "bold"), bg=COLOR_BTN_PRIMARY, fg="white", relief="flat", padx=40, pady=10, cursor="hand2", command=ventana.destroy).pack(pady=(0, 20))

    # ============================
    # CARGAR VENTA
    # ============================
    def cargar_venta(self):
        ventana = Toplevel(self.root)
        ventana.title("Nueva Venta")
        ventana.geometry("650x680")
        ventana.resizable(False, False)
        ventana.configure(bg=COLOR_WHITE)
        ventana.transient(self.root)
        ventana.grab_set()

        id_venta_actual = None
        productos_agregados = []

        # Sección 1: Iniciar venta
        frame_inicio = tk.Frame(ventana, bg=COLOR_WHITE)
        frame_inicio.pack(fill="x", padx=20, pady=(20, 10))
        tk.Label(frame_inicio, text="INICIAR VENTA", font=("Arial", 12, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")
        tk.Frame(frame_inicio, height=2, bg=COLOR_HEADER).pack(fill="x", pady=5)

        f = tk.Frame(frame_inicio, bg=COLOR_WHITE)
        f.pack(fill="x", pady=10)
        tk.Label(f, text="Fecha:", bg=COLOR_WHITE, fg=COLOR_TEXT, font=("Arial", 10), width=10, anchor="w").pack(side="left")
        entry_fecha = tk.Entry(f, font=("Arial", 10), relief="solid", bd=1, width=15)
        entry_fecha.pack(side="left", padx=10)
        entry_fecha.insert(0, datetime.today().strftime("%Y-%m-%d"))
        btn_iniciar = tk.Button(f, text="Iniciar Venta", font=("Arial", 10, "bold"), bg=COLOR_BTN_PRIMARY, fg="white", relief="flat", padx=20, pady=7, cursor="hand2")
        btn_iniciar.pack(side="left", padx=5)
        lbl_msg_inicio = tk.Label(frame_inicio, text="", font=("Arial", 9), bg=COLOR_WHITE)
        lbl_msg_inicio.pack(anchor="w", pady=5)

        # Sección 2: Agregar productos
        frame_prod = tk.Frame(ventana, bg=COLOR_WHITE)
        frame_prod.pack(fill="x", padx=20, pady=10)
        tk.Label(frame_prod, text="AGREGAR PRODUCTOS", font=("Arial", 12, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")
        tk.Frame(frame_prod, height=2, bg=COLOR_HEADER).pack(fill="x", pady=5)

        f1 = tk.Frame(frame_prod, bg=COLOR_WHITE)
        f1.pack(fill="x", pady=8)
        tk.Label(f1, text="Producto:", bg=COLOR_WHITE, fg=COLOR_TEXT, font=("Arial", 10), width=10, anchor="w").pack(side="left")
        productos = obtener_productos_combo()
        combo = ttk.Combobox(f1, values=[p[1] for p in productos], state="disabled", font=("Arial", 10), width=38)
        combo.pack(side="left", padx=10)
        combo.set("Seleccionar producto")

        f2 = tk.Frame(frame_prod, bg=COLOR_WHITE)
        f2.pack(fill="x", pady=8)
        tk.Label(f2, text="Peso (kg):", bg=COLOR_WHITE, fg=COLOR_TEXT, font=("Arial", 10), width=10, anchor="w").pack(side="left")
        entry_peso = tk.Entry(f2, font=("Arial", 10), relief="solid", bd=1, width=15, state="disabled")
        entry_peso.pack(side="left", padx=10)
        btn_agregar = tk.Button(f2, text="Agregar Producto", font=("Arial", 10, "bold"), bg=COLOR_BTN_SUCCESS, fg="white", relief="flat", padx=20, pady=7, cursor="hand2", state="disabled")
        btn_agregar.pack(side="left", padx=5)
        lbl_msg_prod = tk.Label(frame_prod, text="", font=("Arial", 9), bg=COLOR_WHITE)
        lbl_msg_prod.pack(anchor="w", pady=5)

        # Sección 3: Lista de productos
        frame_lista = tk.Frame(ventana, bg=COLOR_WHITE)
        frame_lista.pack(fill="both", expand=True, padx=20, pady=10)
        tk.Label(frame_lista, text="PRODUCTOS EN LA VENTA", font=("Arial", 11, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT).pack(anchor="w")

        tree_frame = tk.Frame(frame_lista, bg=COLOR_WHITE)
        tree_frame.pack(fill="both", expand=True, pady=5)
        tree_prod = ttk.Treeview(tree_frame, columns=("ID", "Producto", "Peso", "Ingreso"), show="headings", height=8, style="Custom.Treeview")
        for col in tree_prod["columns"]:
            tree_prod.heading(col, text=col)
            tree_prod.column(col, anchor="center", width=150)
        tree_prod.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_prod.yview)
        scroll.pack(side="right", fill="y")
        tree_prod.configure(yscrollcommand=scroll.set)

        lbl_total = tk.Label(frame_lista, text="Total: $0.00", font=("Arial", 13, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT)
        lbl_total.pack(anchor="e", pady=10)

        btn_finalizar = tk.Button(frame_lista, text="Finalizar Venta", font=("Arial", 11, "bold"), bg=COLOR_BTN_PRIMARY, fg="white", relief="flat", padx=40, pady=12, cursor="hand2", state="disabled")
        btn_finalizar.pack(side="right", pady=(0, 20))

        # Funciones internas
        def iniciar():
            nonlocal id_venta_actual
            fecha = entry_fecha.get()
            if not validar_formato_fecha(fecha):
                lbl_msg_inicio.config(text="Formato de fecha inválido (YYYY-MM-DD)", fg=COLOR_BTN_DANGER)
                return
            try:
                id_venta_actual = cargar_venta_db(fecha)
                lbl_msg_inicio.config(text=f"✓ Venta N° {id_venta_actual} iniciada", fg=COLOR_BTN_SUCCESS)
                entry_fecha.config(state="disabled")
                btn_iniciar.config(state="disabled")
                combo.config(state="readonly")
                entry_peso.config(state="normal")
                btn_agregar.config(state="normal")
                btn_finalizar.config(state="normal")
                entry_peso.focus()
            except Exception as e:
                lbl_msg_inicio.config(text=f"Error: {e}", fg=COLOR_BTN_DANGER)

        def agregar():
            if not id_venta_actual:
                lbl_msg_prod.config(text="Debe iniciar una venta primero", fg=COLOR_BTN_DANGER)
                return
            seleccion = combo.get()
            try:
                peso = float(entry_peso.get())
                if peso <= 0:
                    raise ValueError("Peso debe ser > 0")
                id_producto = int(seleccion.split(" - ")[0])
                nombre = seleccion.split(" - ", 1)[1]
                precio = obtener_precio_producto(id_producto)
                ingreso = peso * precio
                cargar_detalle_venta_db(id_venta_actual, id_producto, peso, ingreso)
                tree_prod.insert("", "end", values=(id_producto, nombre, f"{peso:.2f}", f"${ingreso:,.2f}"))
                productos_agregados.append(ingreso)
                total = sum(productos_agregados)
                lbl_total.config(text=f"Total: ${total:,.2f}")
                combo.set("Seleccionar producto")
                entry_peso.delete(0, END)
                lbl_msg_prod.config(text="✓ Producto agregado", fg=COLOR_BTN_SUCCESS)
                entry_peso.focus()
            except Exception as e:
                lbl_msg_prod.config(text=f"Error: {e}", fg=COLOR_BTN_DANGER)

        def finalizar():
            if not productos_agregados:
                lbl_msg_prod.config(text="Debe agregar al menos un producto", fg=COLOR_BTN_DANGER)
                return
            ventana.destroy()
            self.actualizar_vista_tabla("DetalleVenta")

        btn_iniciar.config(command=iniciar)
        btn_agregar.config(command=agregar)
        btn_finalizar.config(command=finalizar)

    # ============================
    # RECAUDACIONES
    # ============================
    def mostrar_recaudaciones(self):
        self.limpiar_contenido()

        titulo = tk.Label(self.contenido, text="RECAUDACIONES", font=("Arial", 16, "bold"), bg=COLOR_BG, fg=COLOR_TEXT)
        titulo.pack(pady=20)

        # Controles
        frame_controles = tk.Frame(self.contenido, bg=COLOR_WHITE, relief="solid", bd=1)
        frame_controles.pack(fill="x", padx=20, pady=(20, 15))

        tk.Label(frame_controles, text="Desde:", font=("Arial", 10), bg=COLOR_WHITE, fg=COLOR_TEXT).grid(row=0, column=0, padx=(20, 10), pady=15, sticky="w")
        entry_fecha = tk.Entry(frame_controles, font=("Arial", 10), relief="solid", bd=1, width=12)
        entry_fecha.grid(row=0, column=1, padx=5, pady=15)
        entry_fecha.insert(0, datetime.today().strftime("%Y-%m-%d"))

        tk.Label(frame_controles, text="Filtrar por:", font=("Arial", 10), bg=COLOR_WHITE, fg=COLOR_TEXT).grid(row=0, column=2, padx=(30, 10), pady=15)
        filtro_var = tk.StringVar(value="Producto") 
        combo_filtro = ttk.Combobox(frame_controles,textvariable=filtro_var, values=["Producto", "Fecha", "Categoría"], state="readonly", font=("Arial", 10), width=12)
        combo_filtro.grid(row=0, column=3, padx=5, pady=15)
        

        btn_aplicar = tk.Button(frame_controles, text="Aplicar", font=("Arial", 10, "bold"), bg=COLOR_BTN_PRIMARY, fg="white", relief="flat", padx=20, pady=8, cursor="hand2")
        btn_aplicar.grid(row=0, column=4, padx=(20, 20), pady=15)

        # Total
        frame_total = tk.Frame(self.contenido, bg=COLOR_WHITE, relief="solid", bd=1)
        frame_total.pack(fill="x", padx=20, pady=(0, 15))
        lbl_total = tk.Label(frame_total, text="TOTAL RECAUDADO: $ 0.00", font=("Arial", 14, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT)
        lbl_total.pack(pady=20)

        # Resultados
        frame_resultados = tk.Frame(self.contenido, bg=COLOR_WHITE, relief="solid", bd=1)
        frame_resultados.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.tree_recaudaciones = ttk.Treeview(frame_resultados, show="headings", style="Custom.Treeview")
        self.tree_recaudaciones.pack(fill="both", expand=True, padx=20, pady=20)
        
        scroll = ttk.Scrollbar(frame_resultados, orient="vertical", command=self.tree_recaudaciones.yview)
        scroll.pack(side="right", fill="y")
        self.tree_recaudaciones.configure(yscrollcommand=scroll.set)

        def aplicar():
            fecha = entry_fecha.get()
            filtro = filtro_var.get()

            if not validar_formato_fecha(fecha):
                lbl_total.config(text="ERROR: Formato de fecha inválido (usar YYYY-MM-DD)", fg=COLOR_BTN_DANGER)
                return
            try:
                if filtro == "Producto":
                    total, datos = obtener_recaudacion_por_producto(fecha)
                    columnas = ("Fecha", "Producto", "Peso (kg)", "Recaudación")
                elif filtro == "Fecha":
                    total, datos = obtener_recaudacion_por_fecha(fecha)
                    columnas = ("Fecha", "Recaudación")
                elif filtro == "Categoría":
                    total, datos = obtener_recaudacion_por_categoria(fecha)
                    columnas = ("Fecha", "Categoría", "Recaudación")
                else:
                    return

                lbl_total.config(text=f"TOTAL RECAUDADO: $ {total:,.2f}", fg=COLOR_TEXT)
                # LIMPIAR Y RECONFIGURAR TREEVIEW

                self.tree_recaudaciones.delete(*self.tree_recaudaciones.get_children())
                self.tree_recaudaciones["columns"] = columnas
                for col in columnas:
                    self.tree_recaudaciones.heading(col, text=col)
                    self.tree_recaudaciones.column(col, anchor="center", width=150)

                
                for i, fila in enumerate(datos):
                    tag = "evenrow" if i % 2 == 0 else "oddrow"
                    fila_fmt = list(fila)
                    
                    if filtro == "Producto" and len(fila) == 4:
                        fila_fmt[2] = f"{fila[2]:.2f}"
                        fila_fmt[3] = f"${fila[3]:,.2f}"
                    elif filtro == "Fecha" and len(fila) == 2:
                        fila_fmt[1] = f"${fila[1]:,.2f}"
                    elif filtro == "Categoría" and len(fila) == 3:
                        fila_fmt[2] = f"${fila[2]:,.2f}"
                        
                    self.tree_recaudaciones.insert("", "end", values=tuple(fila_fmt), tags=(tag,))
                
                self.tree_recaudaciones.tag_configure("evenrow", background=COLOR_WHITE)
                self.tree_recaudaciones.tag_configure("oddrow", background="#f8f9fa")
            except Exception as e:
                lbl_total.config(text=f"Error: {e}", fg=COLOR_BTN_DANGER)

        btn_aplicar.config(command=aplicar)
        

# ============================
# MAIN
# ============================
if __name__ == "__main__":
    inicializar_base_datos()
    root = tk.Tk()
    app = CarniceriaApp(root)
    root.mainloop()