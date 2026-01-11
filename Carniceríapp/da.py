import sqlite3 as sql
import random, datetime, os

DB = "CARNICERIA.db"

# Borra si existe
if os.path.exists(DB):
    os.remove(DB)

conn = sql.connect(DB)
cur = conn.cursor()

# ============================
# 1. ESTRUCTURA REAL
# ============================
cur.executescript("""
CREATE TABLE IF NOT EXISTS Categoria (
    IDCategoria INTEGER PRIMARY KEY AUTOINCREMENT,
    NombreCategoria TEXT NOT NULL UNIQUE
);

INSERT OR IGNORE INTO Categoria (NombreCategoria) VALUES 
    ('Vacuno'),
    ('Cerdo'),
    ('Pollo'),
    ('Achuras'),
    ('Preparados');

CREATE TABLE IF NOT EXISTS Productos (
    IDProducto INTEGER PRIMARY KEY AUTOINCREMENT,
    NombreProducto TEXT NOT NULL,
    Precio REAL NOT NULL CHECK(Precio > 0),
    IDCategoria INTEGER NOT NULL,
    FOREIGN KEY (IDCategoria) REFERENCES Categoria(IDCategoria)
);

CREATE TABLE IF NOT EXISTS MediasR (
    IDMedia INTEGER PRIMARY KEY AUTOINCREMENT,
    Fecha TEXT NOT NULL,
    Peso REAL NOT NULL CHECK(Peso > 0),
    Precio REAL NOT NULL CHECK(Precio > 0)
);

CREATE TABLE IF NOT EXISTS CortesMedia (
    IDCorteMedia INTEGER PRIMARY KEY AUTOINCREMENT,
    IDMedia INTEGER NOT NULL,
    IDProducto INTEGER NOT NULL,
    PesoObtenido REAL NOT NULL CHECK(PesoObtenido > 0),
    FOREIGN KEY (IDMedia) REFERENCES MediasR(IDMedia) ON DELETE CASCADE,
    FOREIGN KEY (IDProducto) REFERENCES Productos(IDProducto)
);

CREATE TABLE IF NOT EXISTS Ventas (
    IDVenta INTEGER PRIMARY KEY AUTOINCREMENT,
    Fecha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS DetalleVenta (
    IDDetalle INTEGER PRIMARY KEY AUTOINCREMENT,
    IDVenta INTEGER NOT NULL,
    IDProducto INTEGER NOT NULL,
    Peso REAL NOT NULL CHECK(Peso > 0),
    Ingreso REAL NOT NULL CHECK(Ingreso >= 0),
    FOREIGN KEY (IDVenta) REFERENCES Ventas(IDVenta) ON DELETE CASCADE,
    FOREIGN KEY (IDProducto) REFERENCES Productos(IDProducto)
);
""")

# ============================
# 2. PRODUCTOS REALISTAS
# ============================
productos = [
    # Vacuno
    ("Asado", 5500, 1),
    ("Vacío", 6000, 1),
    ("Bife Angosto", 7500, 1),
    ("Bife Ancho", 7200, 1),
    ("Paleta", 4800, 1),
    ("Aguja", 4500, 1),
    ("Nalga", 5800, 1),
    ("Cuadril", 6500, 1),
    ("Tapa de Asado", 5200, 1),
    ("Falda", 3800, 1),
    # Cerdo
    ("Costilla de Cerdo", 3200, 2),
    ("Lomo de Cerdo", 3500, 2),
    ("Pernil de Cerdo", 3000, 2),
    # Pollo
    ("Pechuga de Pollo", 2800, 3),
    ("Pata Muslo", 1800, 3),
    ("Alitas", 2200, 3),
    ("Cuarto de Pollo", 2000, 3),
    # Achuras
    ("Chinchulines", 1800, 4),
    ("Mollejas", 9000, 4),
    ("Riñón", 2500, 4),
    ("Hígado", 1500, 4),
    ("Corazón", 2000, 4),
    # Preparados
    ("Hamburguesa de Carne", 3200, 5),
    ("Hamburguesa de Pollo", 2800, 5),
    ("Milanesa de Carne", 3500, 5),
    ("Milanesa de Pollo", 3000, 5),
    ("Chorizo", 3200, 5),
    ("Morcilla", 2800, 5),
]

cur.executemany("INSERT INTO Productos (NombreProducto, Precio, IDCategoria) VALUES (?,?,?)", productos)

# ============================
# 3. MEDIAS RES (500 unidades)
# ============================
def fecha_aleatoria():
    inicio = datetime.date(2020, 1, 1)
    fin = datetime.date(2025, 12, 31)
    return (inicio + datetime.timedelta(days=random.randint(0, (fin - inicio).days))).strftime("%Y-%m-%d")

medias = []
for i in range(500):
    peso = round(random.uniform(160, 240), 2)
    precio_kg = round(random.uniform(350, 480), 2)
    medias.append((fecha_aleatoria(), peso, precio_kg))

cur.executemany("INSERT INTO MediasR (Fecha, Peso, Precio) VALUES (?,?,?)", medias)
# ============================
# 4. CORTES POR CADA MEDIA (≈ 10 cortes por media)
# ============================
cortes_por_media = [
    ("Asado", 8, 14),
    ("Vacío", 4, 7),
    ("Bife Angosto", 5, 8),
    ("Bife Ancho", 4, 7),
    ("Paleta", 6, 10),
    ("Aguja", 5, 9),
    ("Nalga", 4, 7),
    ("Cuadril", 4, 7),
    ("Tapa de Asado", 5, 8),
    ("Falda", 4, 7),
]

cortes_data = []
for id_media in range(1, 501):
    for nombre, pmin, pmax in cortes_por_media:
        # Buscar IDProducto por nombre
        cur.execute("SELECT IDProducto FROM Productos WHERE NombreProducto = ?", (nombre,))
        row = cur.fetchone()
        if row:
            id_prod = row[0]
            peso = round(random.uniform(pmin, pmax), 2)
            cortes_data.append((id_media, id_prod, peso))

cur.executemany("INSERT INTO CortesMedia (IDMedia, IDProducto, PesoObtenido) VALUES (?,?,?)", cortes_data)
# ============================
# 5. VENTAS (1000 ventas)
# ============================
ventas_data = []
for i in range(1000):
    ventas_data.append((fecha_aleatoria(),))

cur.executemany("INSERT INTO Ventas (Fecha) VALUES (?)", ventas_data)
# ============================
# 6. DETALLE VENTA (≈ 3 productos por venta)
# ============================
detalle_data = []
cur.execute("SELECT IDProducto, Precio FROM Productos")
productos_precio = cur.fetchall()

for id_venta in range(1, 1001):
    # 2 a 5 productos por venta
    for _ in range(random.randint(2, 5)):
        id_prod, precio = random.choice(productos_precio)
        peso = round(random.uniform(0.5, 5.0), 2)
        ingreso = round(peso * precio, 2)
        detalle_data.append((id_venta, id_prod, peso, ingreso))

cur.executemany("INSERT INTO DetalleVenta (IDVenta, IDProducto, Peso, Ingreso) VALUES (?,?,?,?)", detalle_data)
# ============================
# 7. CERRAR Y LISTO
# ============================
conn.commit()
conn.close()

print("✅ Base de datos CARNICERIA.db creada con éxito")
print("📊 Resumen:")
print(f"   - Categorías: {len(productos)} productos")
print(f"   - MediasR: 500 unidades")
print(f"   - CortesMedia: {len(cortes_data)} cortes")
print(f"   - Ventas: 1000 ventas")
print(f"   - DetalleVenta: {len(detalle_data)} líneas")