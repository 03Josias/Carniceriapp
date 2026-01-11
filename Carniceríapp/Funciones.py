import sqlite3 as sql
import re
from datetime import datetime

DB_NAME = "CARNICERIA.db"

# ============================
# 1. INICIALIZACIÓN
# ============================
def inicializar_base_datos():
    """Crea todas las tablas si no existen e inserta categorías por defecto."""
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()

    # TABLA: Categoria
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categoria (
            IDCategoria INTEGER PRIMARY KEY AUTOINCREMENT,
            NombreCategoria TEXT NOT NULL UNIQUE
        )
    """)

    # TABLA: Productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Productos (
            IDProducto INTEGER PRIMARY KEY AUTOINCREMENT,
            NombreProducto TEXT NOT NULL,
            Precio REAL NOT NULL CHECK(Precio > 0),
            IDCategoria INTEGER NOT NULL,
            FOREIGN KEY (IDCategoria) REFERENCES Categoria(IDCategoria)
        )
    """)

    # TABLA: MediasR
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MediasR (
            IDMedia INTEGER PRIMARY KEY AUTOINCREMENT,
            Fecha TEXT NOT NULL,
            Peso REAL NOT NULL CHECK(Peso > 0),
            Precio REAL NOT NULL CHECK(Precio > 0)
        )
    """)

    # TABLA: CortesMedia
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CortesMedia (
            IDCorteMedia INTEGER PRIMARY KEY AUTOINCREMENT,
            IDMedia INTEGER NOT NULL,
            IDProducto INTEGER NOT NULL,
            PesoObtenido REAL NOT NULL CHECK(PesoObtenido > 0),
            FOREIGN KEY (IDMedia) REFERENCES MediasR(IDMedia) ON DELETE CASCADE,
            FOREIGN KEY (IDProducto) REFERENCES Productos(IDProducto)
        )
    """)

    # TABLA: Ventas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ventas (
            IDVenta INTEGER PRIMARY KEY AUTOINCREMENT,
            Fecha TEXT NOT NULL
        )
    """)

    # TABLA: DetalleVenta
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS DetalleVenta (
            IDDetalle INTEGER PRIMARY KEY AUTOINCREMENT,
            IDVenta INTEGER NOT NULL,
            IDProducto INTEGER NOT NULL,
            Peso REAL NOT NULL CHECK(Peso > 0),
            Ingreso REAL NOT NULL CHECK(Ingreso >= 0),
            FOREIGN KEY (IDVenta) REFERENCES Ventas(IDVenta) ON DELETE CASCADE,
            FOREIGN KEY (IDProducto) REFERENCES Productos(IDProducto)
        )
    """)

    # Insertar categorías por defecto
    categorias = ['Vacuno', 'Cerdo', 'Pollo', 'Achuras', 'Preparados']
    for cat in categorias:
        cursor.execute("INSERT OR IGNORE INTO Categoria (NombreCategoria) VALUES (?)", (cat,))

    conn.commit()
    conn.close()

# ============================
# 2. CATEGORÍAS
# ============================
def cargar_categoria(nombre: str) -> int | None:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Categoria (NombreCategoria) VALUES (?)", (nombre,))
        conn.commit()
        return cursor.lastrowid
    except sql.IntegrityError:
        return None
    finally:
        conn.close()

def editar_categoria(id_categoria: int, nombre: str) -> bool:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE Categoria SET NombreCategoria = ? WHERE IDCategoria = ?", (nombre, id_categoria))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def eliminar_categoria(id_categoria: int) -> bool:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Categoria WHERE IDCategoria = ?", (id_categoria,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def listar_categorias():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Categoria ORDER BY IDCategoria")
    rows = cursor.fetchall()
    conn.close()
    return rows

def obtener_categorias():
    return listar_categorias()

# ============================
# 3. PRODUCTOS
# ============================
def cargar_producto(nombre: str, precio: float, id_categoria: int) -> int | None:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Productos (NombreProducto, Precio, IDCategoria) VALUES (?, ?, ?)",
                       (nombre, precio, id_categoria))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def editar_producto(id_producto: int, nombre: str, precio: float, id_categoria: int) -> bool:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE Productos SET NombreProducto = ?, Precio = ?, IDCategoria = ? WHERE IDProducto = ?",
                       (nombre, precio, id_categoria, id_producto))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def eliminar_producto(id_producto: int) -> bool:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Productos WHERE IDProducto = ?", (id_producto,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def listar_productos():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.IDProducto, p.NombreProducto, p.Precio, c.NombreCategoria
        FROM Productos p
        JOIN Categoria c ON p.IDCategoria = c.IDCategoria
        ORDER BY p.IDProducto
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def obtener_producto(id_producto: int):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos WHERE IDProducto = ?", (id_producto,))
    row = cursor.fetchone()
    conn.close()
    return row

def obtener_productos_por_categoria(id_categoria: int):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos WHERE IDCategoria = ?", (id_categoria,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def obtener_productos_combo():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT IDProducto, NombreProducto FROM Productos ORDER BY NombreProducto")
    rows = cursor.fetchall()
    conn.close()
    return [(row[0], f"{row[0]} - {row[1]}") for row in rows]

def obtener_precio_producto(id_producto: int) -> float:
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT Precio FROM Productos WHERE IDProducto = ?", (id_producto,))
    row = cursor.fetchone()
    conn.close()
    return float(row[0]) if row else 0.0

# ============================
# 4. MEDIASR
# ============================
def cargar_media(fecha: str, peso: float, precio: float) -> int | None:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO MediasR (Fecha, Peso, Precio) VALUES (?, ?, ?)", (fecha, peso, precio))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def editar_media(id_media: int, fecha: str, peso: float, precio: float) -> bool:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE MediasR SET Fecha = ?, Peso = ?, Precio = ? WHERE IDMedia = ?",
                       (fecha, peso, precio, id_media))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def eliminar_media(id_media: int) -> bool:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM MediasR WHERE IDMedia = ?", (id_media,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def listar_medias():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MediasR ORDER BY IDMedia DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def obtener_media(id_media: int):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MediasR WHERE IDMedia = ?", (id_media,))
    row = cursor.fetchone()
    conn.close()
    return row

# ============================
# 5. CORTESMEDIA
# ============================
def guardar_corte_media(id_media: int, id_producto: int, peso_obtenido: float) -> int | None:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO CortesMedia (IDMedia, IDProducto, PesoObtenido) VALUES (?, ?, ?)",
                       (id_media, id_producto, peso_obtenido))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()
def listar_corte_medias():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CortesMedia ORDER BY IDCorteMedia DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
def obtener_cortes_media(id_media: int):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.NombreProducto, cm.PesoObtenido, p.Precio
        FROM CortesMedia cm
        JOIN Productos p ON cm.IDProducto = p.IDProducto
        WHERE cm.IDMedia = ?
        ORDER BY p.NombreProducto
    """, (id_media,))
    rows = cursor.fetchall()
    conn.close()
    return rows
def eliminar_cortes_media(id_media: int):
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM CortesMedia WHERE IDMedia = ?", (id_media,))
        conn.commit()
    finally:
        conn.close()

# ============================
# 6. VENTAS
# ============================
def cargar_venta_db(fecha: str) -> int | None:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Ventas (Fecha) VALUES (?)", (fecha,))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def editar_venta(id_venta: int, fecha: str) -> bool:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE Ventas SET Fecha = ? WHERE IDVenta = ?", (fecha, id_venta))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def eliminar_venta(id_venta: int) -> bool:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ventas WHERE IDVenta = ?", (id_venta,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def listar_ventas():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Ventas ORDER BY IDVenta DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ============================
# 7. DETALLEVENTA
# ============================
def cargar_detalle_venta_db(id_venta: int, id_producto: int, peso: float, ingreso: float) -> int | None:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO DetalleVenta (IDVenta, IDProducto, Peso, Ingreso) VALUES (?, ?, ?, ?)",
                       (id_venta, id_producto, peso, ingreso))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def editar_detalle_venta(id_detalle: int, id_venta: int, id_producto: int, peso: float) -> bool:
    precio = obtener_precio_producto(id_producto)
    ingreso = peso * precio
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE DetalleVenta SET IDVenta = ?, IDProducto = ?, Peso = ?, Ingreso = ? WHERE IDDetalle = ?",
                       (id_venta, id_producto, peso, ingreso, id_detalle))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def eliminar_detalle_venta(id_detalle: int) -> bool:
    try:
        conn = sql.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM DetalleVenta WHERE IDDetalle = ?", (id_detalle,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def listar_detalles_venta():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dv.IDDetalle, dv.IDVenta, p.NombreProducto, dv.Peso, dv.Ingreso
        FROM DetalleVenta dv
        JOIN Productos p ON dv.IDProducto = p.IDProducto
        ORDER BY dv.IDDetalle DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

# ============================
# 8. DASHBOARD
# ============================
def obtener_recaudacion_hoy() -> float:
    hoy = datetime.today().strftime("%Y-%m-%d")
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(dv.Ingreso)
        FROM DetalleVenta dv
        JOIN Ventas v ON dv.IDVenta = v.IDVenta
        WHERE v.Fecha = ?
    """, (hoy,))
    row = cursor.fetchone()
    conn.close()
    return float(row[0]) if row[0] else 0.0

def obtener_productos_vendidos_hoy():
    hoy = datetime.today().strftime("%Y-%m-%d")
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.NombreProducto, c.NombreCategoria, SUM(dv.Peso), SUM(dv.Ingreso)
        FROM DetalleVenta dv
        JOIN Ventas v ON dv.IDVenta = v.IDVenta
        JOIN Productos p ON dv.IDProducto = p.IDProducto
        JOIN Categoria c ON p.IDCategoria = c.IDCategoria
        WHERE v.Fecha = ?
        GROUP BY p.IDProducto
        ORDER BY SUM(dv.Ingreso) DESC
    """, (hoy,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# ============================
# 9. RECAUDACIONES
# ============================
def obtener_recaudacion_por_producto(fecha_desde: str):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.Fecha, p.NombreProducto, SUM(dv.Peso), SUM(dv.Ingreso)
        FROM DetalleVenta dv
        JOIN Ventas v ON dv.IDVenta = v.IDVenta
        JOIN Productos p ON dv.IDProducto = p.IDProducto
        WHERE v.Fecha >= ?
        GROUP BY v.Fecha, p.IDProducto
        ORDER BY v.Fecha, SUM(dv.Ingreso) DESC
    """, (fecha_desde,))
    rows = cursor.fetchall()
    total = sum(r[3] for r in rows)
    conn.close()
    return total, rows

def obtener_recaudacion_por_fecha(fecha_desde: str):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.Fecha, SUM(dv.Ingreso) AS Recaudacion
        FROM DetalleVenta dv
        JOIN Ventas v ON dv.IDVenta = v.IDVenta
        WHERE v.Fecha >= ?
        GROUP BY v.Fecha
        ORDER BY v.Fecha
    """, (fecha_desde,))
    rows = cursor.fetchall()
    total = sum(r[1] for r in rows)
    conn.close()
    return total, rows

def obtener_recaudacion_por_categoria(fecha_desde: str):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.Fecha, c.NombreCategoria, SUM(dv.Ingreso) 
        FROM DetalleVenta dv
        JOIN Ventas v ON dv.IDVenta = v.IDVenta
        JOIN Productos p ON dv.IDProducto = p.IDProducto
        JOIN Categoria c ON p.IDCategoria = c.IDCategoria
        WHERE v.Fecha >= ?
        GROUP BY v.Fecha, c.NombreCategoria
        ORDER BY v.Fecha, SUM(dv.Ingreso) DESC
    """, (fecha_desde,))
    rows = cursor.fetchall()
    total = sum(r[2] for r in rows)
    conn.close()
    return total, rows

# ============================
# 10. UTILIDADES
# ============================
def obtener_columnas(tabla: str):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({tabla})")
    cols = [row[1] for row in cursor.fetchall()]
    conn.close()
    return cols

def ordenar_por(tabla: str, columna: str, direccion: str):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    query = f"SELECT * FROM {tabla} ORDER BY {columna} {direccion}"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def editar_registro_db(tabla: str, nuevos_valores: dict, id_columna: str, id_valor):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    set_clause = ", ".join([f"{col} = ?" for col in nuevos_valores.keys()])
    valores = list(nuevos_valores.values()) + [id_valor]
    query = f"UPDATE {tabla} SET {set_clause} WHERE {id_columna} = ?"
    cursor.execute(query, valores)
    conn.commit()
    conn.close()

def eliminar_registro_db(tabla: str, id_valor, id_columna: str):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {tabla} WHERE {id_columna} = ?", (id_valor,))
    conn.commit()
    conn.close()

# ============================
# 11. VALIDACIONES
# ============================
def validar_formato_fecha(fecha_str: str) -> bool:
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha_str):
        return False
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def producto_tiene_ventas(id_producto: int) -> bool:
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM DetalleVenta WHERE IDProducto = ?", (id_producto,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0