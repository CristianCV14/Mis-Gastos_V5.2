MIS GASTOS V5.2

Cambios:
- Selector de período conectado al panel de compromisos.
- Cuotas dinámicas por mes: Cuota X de Y y restantes.
- Las cuotas fuera de período no se muestran como activas.
- Compromisos pausados permanecen en una sección Pausados y pueden reactivarse.
- Pausar no los envía al historial.
- Cancelar marca el compromiso como cancelado.
- La sección de inicio "En qué estás gastando" se elimina cuando puede identificarse por su bloque.
- Estadísticas queda como espacio de análisis de categorías.

Nota de compatibilidad:
La V5.2 mantiene app.js intacto y añade un módulo aislado. Las claves de almacenamiento de compromisos se detectan automáticamente entre nombres comunes. Si la V5 usa una clave distinta, será necesario adaptar el adaptador de persistencia.
