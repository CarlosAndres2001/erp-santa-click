from django.urls import path
from . import views
from .views import (
    cocina_kanban,
    actualizar_estado_cocina, 
    kanban_pedidos_json
)
urlpatterns = [
    # =======================
    # ROL
    # =======================
    path('rol/', views.rol_list, name='rol_list'),
    path('rol/create/', views.rol_create, name='rol_create'),
    path('rol/edit/', views.rol_edit, name='rol_edit'),
    path('rol/delete/', views.rol_delete, name='rol_delete'),
    path('rol/permisos/<int:rol_id>/', views.rol_permisos, name='rol_permisos'),

    # =======================
    # EMPRESA
    # =======================
    path('empresa/', views.empresa_list, name='empresa_list'),
    path('empresa/create/', views.empresa_create, name='empresa_create'),
    path('empresa/edit/', views.empresa_edit, name='empresa_edit'),
    path('empresa/delete/', views.empresa_delete, name='empresa_delete'),
    path('empresa/registro/', views.registro_empresa, name='registro_empresa'),

    # =======================
    # SUCURSAL
    # =======================
    path('sucursal/', views.sucursal_list, name='sucursal_list'),
    path('sucursal/create/', views.sucursal_create, name='sucursal_create'),
    path('sucursal/edit/', views.sucursal_edit, name='sucursal_edit'),
    path('sucursal/delete/', views.sucursal_delete, name='sucursal_delete'),
    
    # ==========================
    # ALMACÉN
    # ==========================
    path('almacenes/', views.almacen_list, name='almacen_list'),
    path('almacenes/crear/', views.almacen_create, name='almacen_create'),
    path('almacenes/editar/', views.almacen_edit, name='almacen_edit'),
    path('almacenes/eliminar/', views.almacen_delete, name='almacen_delete'),
    path('ajax/almacenes-por-sucursal/', views.almacenes_por_sucursal, name='almacenes_por_sucursal'),
    
    # ==========================
    #   USUARIO
    # ==========================
    path('usuario/', views.usuario_list, name='usuario_list'),
    path('usuario/create/', views.usuario_create, name='usuario_create'),
    path('usuario/edit/', views.usuario_edit, name='usuario_edit'),
    path('usuario/delete/', views.usuario_delete, name='usuario_delete'),

    # =======================
    # CANAL DE VENTA
    # =======================
    path('canalventa/', views.canalventa_list, name='canalventa_list'),
    path('canalventa/create/', views.canalventa_create, name='canalventa_create'),
    path('canalventa/edit/', views.canalventa_edit, name='canalventa_edit'),
    path('canalventa/delete/', views.canalventa_delete, name='canalventa_delete'),

    # =======================
    # UNIDAD DE MEDIDA
    # =======================
    path('unidad-medida/', views.unidadmedida_list, name='unidadmedida_list'),
    path('unidad-medida/create/', views.unidadmedida_create, name='unidadmedida_create'),
    path('unidad-medida/edit/', views.unidadmedida_edit, name='unidadmedida_edit'),
    path('unidad-medida/delete/', views.unidadmedida_delete, name='unidadmedida_delete'),

    # =======================
    # CATEGORÍA
    # =======================
    path('categoria/', views.categoria_list, name='categoria_list'),
    path('categoria/create/', views.categoria_create, name='categoria_create'),
    path('categoria/edit/', views.categoria_edit, name='categoria_edit'),
    path('categoria/delete/', views.categoria_delete, name='categoria_delete'),

    # =======================
    # PRODUCTO
    # =======================
    path('productos-terminados/', views.producto_list, name='producto_list'),
    path('productos-terminados/crear/', views.crear_producto_terminado, name='crear_producto_terminado'),
    #path('productos-terminados/editar/', views.producto_terminado_edit, name='producto_terminado_edit'),
    path('productos/variante/<int:variante_id>/editar/', views.producto_variante_edit, name='producto_terminado_edit'),
    path('productos-terminados/eliminar/', views.producto_terminado_delete, name='producto_terminado_delete'),
    path('productos-terminados/importar/', views.importar_productos_terminados, name='importar_productos_terminados'),
    path('productos-terminados/importar/confirmar/', views.importar_productos_terminados_confirmar, name='importar_productos_terminados_confirmar'),

    path('combos/', views.lista_combos, name='lista_combos'),
    path('crear-combo/', views.crear_combo, name='crear_combo'),
    path('api/productos-genericos/', views.obtener_productos_genericos, name='obtener_productos_genericos'),
    path('api/productos-definidos/', views.obtener_productos_definidos, name='obtener_productos_definidos'),
    
    path('reportes/kardex/', views.reporte_kardex, name='reporte_kardex'),
    path('api/reporte-kardex/', views.api_reporte_kardex, name='api_reporte_kardex'),
    #=======================
    # INSUMO
    #=======================
    path('insumos/', views.lista_insumos, name='lista_insumos'),
    path('insumos/crear/', views.crear_insumo, name='crear_insumo'),
    path('insumos/editar/', views.insumo_edit, name='insumo_edit'),
    path('insumos/eliminar/', views.insumo_delete, name='insumo_delete'),
    
    # =======================
    # PRECIO PRODUCTO
    # =======================
    path('precioproducto/', views.registrar_precios_por_sucursal, name='precioproducto_list'),


    # =======================
    # TIPO INGRESO
    # =======================
    path('tiposingreso/', views.tiposingreso_list, name='tiposingreso_list'),
    path('tiposingreso/create/', views.tiposingreso_create, name='tiposingreso_create'),
    path('tiposingreso/edit/', views.tiposingreso_edit, name='tiposingreso_edit'),
    path('tiposingreso/delete/', views.tiposingreso_delete, name='tiposingreso_delete'),

    # =======================
    # INGRESO
    # =======================
    path('ingreso/', views.ingreso_list, name='ingreso_list'),
    path('ingreso/create/', views.ingreso_create, name='ingreso_create'),
    path('ingreso/delete/', views.ingreso_delete, name='ingreso_delete'),

    # =======================
    # TURNO
    # =======================
    path('turnos/', views.turno_list, name='turno_list'),
    path('turnos/create/', views.turno_create, name='turno_create'),
    path('turnos/edit/', views.turno_edit, name='turno_edit'),
    path('turnos/delete/', views.turno_delete, name='turno_delete'),
    
    # =======================
    # CAJA
    # =======================
    path('caja/', views.caja_list, name='caja_list'),
    path('caja/create/', views.caja_create, name='caja_create'),
    path('caja/edit/', views.caja_edit, name='caja_edit'),
    path('caja/delete/', views.caja_delete, name='caja_delete'),

    # ====================================================
    # CAJA TURNO
    # ====================================================
    path('caja_turno/', views.caja_turno_list, name='caja_turno_list'),
    path('caja/abrir/', views.abrir_caja, name='abrir_caja'),
    path('caja/cerrar/', views.cerrar_caja, name='cerrar_caja'),
    path('caja/comprobante/<int:caja_turno_id>/', views.comprobante_cierre_caja, name='comprobante_cierre_caja'),
    path('api/total-efectivo-esperado/', views.total_efectivo_esperado, name='total_efectivo_esperado'),
    path('reporte-cajas/', views.reporte_cajas, name='reporte_cajas'),
    # ====================================================
    # TIPO EGRESO
    # ====================================================
    path('tipo_egreso/', views.tipo_egreso_list, name='tipo_egreso_list'),
    path('tipo_egreso/create/', views.tipo_egreso_create, name='tipo_egreso_create'),
    path('tipo_egreso/edit/', views.tipo_egreso_edit, name='tipo_egreso_edit'),
    path('tipo_egreso/delete/', views.tipo_egreso_delete, name='tipo_egreso_delete'),

    # ====================================================
    # EGRESO (MAESTRO-DETALLE)
    # ====================================================
    path('egreso/', views.egreso_list, name='egreso_list'),
    path('egreso/create/', views.egreso_create, name='egreso_create'),
    path('egreso/edit/', views.egreso_edit, name='egreso_edit'),
    path('egreso/delete/', views.egreso_delete, name='egreso_delete'),

    # ====================================================
    # PROVEEDOR
    # ====================================================
    path('proveedor/', views.proveedor_list, name='proveedor_list'),
    path('proveedor/create/', views.proveedor_create, name='proveedor_create'),
    path('proveedor/edit/', views.proveedor_edit, name='proveedor_edit'),
    path('proveedor/delete/', views.proveedor_delete, name='proveedor_delete'),

    # ====================================================
    # COMPRA (MAESTRO-DETALLE)
    # ====================================================
    path('api/buscar-variantes/', views.buscar_variantes, name='buscar_variantes'),
    path('compra/', views.lista_compras, name='compra_list'),
    path('compra/create/', views.crear_compra, name='compra_create'),
    path('compra/delete/', views.eliminar_compra, name='compra_delete'),
    path('comprobante_compra/<int:compra_id>/', views.comprobante_compra, name='comprobante_compra'),
    
    # ====================================================
    # VENTA (MAESTRO-DETALLE)
    # ====================================================
    path('api/precios-canal/', views.api_precios_canal, name='api_precios_canal'),
    path('venta/', views.venta_list, name='venta_list'),
    path('venta/create/', views.crear_venta, name='crear_venta'),
    path('venta/delete/', views.venta_delete, name='venta_delete'),
    path('api/stocks/', views.obtener_stocks, name='obtener_stocks'),
    path('venta/ticket/<int:venta_id>/',        views.ticket_cliente, name='ticket_cliente'),
    path('venta/ticket-cocina/<int:venta_id>/', views.ticket_cocina,  name='ticket_cocina'),
    path('cocina/', views.cocina_kanban, name='cocina_kanban'),
    path('api/actualizar-estado-cocina/', views.actualizar_estado_cocina, name='actualizar_estado_cocina'),
    path('api/kanban-pedidos-json/', views.kanban_pedidos_json, name='kanban_pedidos_json'),
    path('sse-pedidos/<int:sucursal_id>/', views.sse_nuevos_pedidos, name='sse_nuevos_pedidos'),
    path('api/productos-venta/', views.api_productos_venta, name='api_productos_venta'),
    path('reportes/ventas/', views.reporte_ventas, name='reporte_ventas'),
    path('api/reporte-ventas/', views.api_reporte_ventas, name='api_reporte_ventas'),
    path('api/exportar-ventas/', views.exportar_ventas_excel, name='exportar_ventas_excel'),
    # ====================================================
    # TRASPASO (MAESTRO-DETALLE)
    # ====================================================
    path('traspaso/', views.traspaso_list, name='traspaso_list'),
    path('traspaso/create/', views.traspaso_create, name='traspaso_create'),
    path('traspaso/edit/', views.traspaso_edit, name='traspaso_edit'),
    path('traspaso/delete/', views.traspaso_delete, name='traspaso_delete'),

    # ====================================================
    # EGRESO MONETARIO
    # ====================================================
    path('ingreso-monetario/crear/', views.crear_ingreso_monetario, name='crear_ingreso_monetario'),
    path('egreso-monetario/crear/', views.crear_egreso_monetario, name='crear_egreso_monetario'),
    path('ingreso-monetario/ticket/<int:id>/', views.ticket_ingreso_monetario, name='ticket_ingreso_monetario'),
    path('egreso-monetario/ticket/<int:id>/', views.ticket_egreso_monetario, name='ticket_egreso_monetario'),
    path("reportes/egresos/", views.reporte_egresos, name="reporte_egresos"),
    path("reportes/ingresos/", views.reporte_ingresos, name="reporte_ingresos"),
    path("egresos/<int:pk>/anular/", views.anular_egreso, name="anular_egreso"),
    path("ingresos/<int:pk>/anular/", views.anular_ingreso, name="anular_ingreso"),
    
    # ====================================================
    # PLAN
    # ====================================================
    path('plan/', views.plan_list, name='plan_list'),
    path('plan/create/', views.plan_create, name='plan_create'),
    path('plan/edit/', views.plan_edit, name='plan_edit'),
    path('plan/delete/', views.plan_delete, name='plan_delete'),

    # ====================================================
    # CLIENTE
    # ====================================================
    path('cliente/', views.cliente_list, name='cliente_list'),
    path('cliente/create/', views.cliente_create, name='cliente_create'),
    path('cliente/edit/', views.cliente_edit, name='cliente_edit'),
    path('cliente/delete/', views.cliente_delete, name='cliente_delete'),
    path('api/buscar-clientes/', views.buscar_clientes, name='buscar_clientes'),
    path('api/crear-cliente/', views.crear_cliente, name='crear_cliente'),
    # ====================================================
    # PAGO
    # ====================================================
    path('pago/', views.pago_list, name='pago_list'),
    path('pago/create/', views.pago_create, name='pago_create'),
    path('pago/edit/', views.pago_edit, name='pago_edit'),
    path('pago/delete/', views.pago_delete, name='pago_delete'),

    # ====================================================
    # ASISTENCIA
    # ====================================================
    path('asistencia/', views.asistencia_list, name='asistencia_list'),
    path('asistencia/create/', views.asistencia_create, name='asistencia_create'),
    path('asistencia/edit/', views.asistencia_edit, name='asistencia_edit'),
    path('asistencia/delete/', views.asistencia_delete, name='asistencia_delete'),
    
    # ====================================================
    # METODO DE PAGO
    # ====================================================
    path('metodopago/', views.metodopago_list, name='metodopago_list'),
    path('metodopago/create/', views.metodopago_create, name='metodopago_create'),
    path('metodopago/edit/', views.metodopago_edit, name='metodopago_edit'),
    path('metodopago/delete/', views.metodopago_delete, name='metodopago_delete'),
    # ====================================================
    #  MEMBRESÍAS
    # ====================================================
    path('membresias/', views.membresia_list, name='membresia_list'),
    path('membresias/crear/', views.membresia_create, name='membresia_create'),
    path('membresias/editar/', views.membresia_edit, name='membresia_edit'),
    path('membresias/eliminar/', views.membresia_delete, name='membresia_delete'),
]

