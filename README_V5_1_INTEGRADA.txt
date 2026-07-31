MIS GASTOS V5.1 INTEGRADA

Esta versión parte de la V5 funcional y añade únicamente un selector de período aislado.

IMPORTANTE:
- No se reemplaza app.js.
- No se sobrescribe la función render existente.
- No se sustituyen los manejadores de formularios.
- El selector emite el evento "misgastos:periodchange" para futuras integraciones.
- La lógica de gastos de la V5 original queda intacta.

Prueba inicial:
1. Abrir index.html.
2. Agregar un gasto.
3. Editar/eliminar un gasto.
4. Usar el selector de mes.
5. Confirmar que los botones originales siguen funcionando.

La lógica de gastos fijos y cuotas por período debe integrarse después de validar esta capa aislada.
