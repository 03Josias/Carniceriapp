# Carniceriapp
Aplicación Python + Tkinter + SQLite que automatiza la gestión de inventario, compras, ventas y recaudaciones de una carnicería, con trazabilidad completa desde la compra de media res hasta la venta por corte
Sistema completo de escritorio para la administración integral de carnicerías
Construido con Python + Tkinter + SQLite3, sin dependencias externas.
Ideal para negocios que buscan automatizar sus procesos sin costos de licencia.
Descripción general
Carnicería Gestión Total es una aplicación de escritorio que centraliza la operación diaria de un negocio de carnes:
desde la compra de media res, su desposte en cortes, la venta al público y la generación de reportes detallados de recaudaciones.
100 % offline – no requiere internet
Sin licencias – Python + SQLite3 son gratuitos
Listo para usar – incluye script que genera miles de registros de prueba
Interfaz intuitiva – pensada para usuarios no técnicos
Funcionalidades principales
Catálogo
Alta, baja y modificación de productos, categorías y precios por kilogramo.
Medias Res
Registro de compras con peso total y precio pagado al proveedor.
CortesMedia
Desposte de cada media en cortes individuales con peso real y cálculo de merma.
Ventas
Venta por producto y peso con cálculo automático de ingresos.
Recaudaciones
Filtros por producto, fecha o categoría con totales detallados.
Dashboard
Recaudación del día, productos más vendidos y últimas ventas.
Ordenamiento
Click en encabezados de tabla para ordenar ascendente o descendente.
Carga rápida
Menú superior para cargar media, producto o venta en dos clics.
Stack técnico
Python 3.8+ : lógica de negocio y UI
Tkinter / ttk : interfaz gráfica nativa sin librerías externas
SQLite3 : base de datos embebida, portable y liviana
datetime / random : generación de fechas y datos de prueba
MVC ligero : separación clara entre UI, lógica y datos
Uso rápido
Cargar una media res
Menú superior → Cargar Datos → Media Res
Vender un corte
Menú superior → Cargar Datos → Venta
Ver recaudaciones
Sidebar → Recaudaciones
Ver dashboard
Sidebar → Dashboard (inicio por defecto)
Estructura de la base de datos
Categoria : clasificación (Vacuno, Cerdo, Pollo, Achuras, Preparados)
Productos : catálogo con precio por kg
MediasR : compra de media res (fecha, peso, precio proveedor)
CortesMedia : corte obtenido al despostar (peso real)
Ventas : encabezado de venta (solo fecha)
DetalleVenta : líneas de venta (producto, peso, ingreso)
