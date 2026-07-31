MIS GASTOS V5.2 ESTABLE

Esta versión parte de la V5.2 que ya permitía registrar, editar y eliminar gastos, y aplica las mejoras de compromisos directamente sobre la aplicación existente.

Cambios:
- Selector de mes conectado al cálculo del dashboard, gastos y compromisos.
- El bloque "¿En qué estás gastando?" se elimina de Inicio; queda en Estadísticas.
- Agregar gasto permite elegir: Gasto normal, Gasto fijo mensual o Compra en cuotas.
- Gastos fijos y compras en cuotas usan el mismo almacenamiento de compromisos existente.
- Las cuotas muestran Cuota X de Y y avanzan según el mes seleccionado.
- Una cuota finalizada deja de aparecer en Activos y queda en Historial.
- Pausar mueve el compromiso a la pestaña Pausados, no al historial.
- Reactivar devuelve el compromiso a Activos.
- Las pausas de compras en cuotas congelan el avance: los meses pausados no consumen cuotas.
- Cancelar lleva el compromiso al Historial como Cancelado.
- "Ver todos" abre correctamente la pantalla de Compromisos.
- El presupuesto del período descuenta las cuotas y gastos fijos activos de ese período.
- Service Worker actualizado para forzar la nueva versión en GitHub Pages.

Publicación:
1. Descomprimir el ZIP.
2. Subir los archivos a la raíz del repositorio de GitHub Pages.
3. Mantener index.html en la raíz.
4. Si el celular conserva la versión anterior, cerrar la PWA/página y abrirla nuevamente; el Service Worker usa una caché nueva.
