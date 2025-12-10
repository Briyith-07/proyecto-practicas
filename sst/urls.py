from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings 
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Página de inicio
    path('', views.inicio, name='inicio'),

    # Autenticación
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),


    # Admin personalizado (usa 'panel/' en lugar de 'admin/')
    path('panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('panel/campanas/crear/', views.crear_campaña, name='crear_campaña'),
    path('panel/usuarios/', views.administrar_usuarios, name='admin_usuarios'),

    # CRUD de usuarios (ADMIN)
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', views.crear_usuario_admin, name='crear_usuario'),
    
       # Admin
    path('usuarios_admin/editar_usuario_admin/<int:usuario_id>/', views.editar_usuario_admin, name='editar_usuario_admin'),


    # Empleado
    path('empleado/editar_empleado/', views.editar_empleado, name='editar_empleado'),


    path('usuarios/inhabilitar/<int:usuario_id>/', views.inhabilitar_usuario, name='inhabilitar_usuario'),
    path('usuarios/habilitar/<int:usuario_id>/', views.habilitar_usuario, name='habilitar_usuario'),    

    # Encuestas y Feedback a campañas
    path('campañas/<int:campaña_id>/encuesta/', views.encuesta_campaña, name='encuesta_campana'),
    path('campañas/<int:campaña_id>/feedback/', views.feedback_campaña, name='feedback_campana'),
    
    #CRUD campaña
    path('campañas/', views.listar_campañas, name='listar_campañas'),
    path('campañas/crear/', views.crear_campaña, name='crear_campaña'),
    path('campañas/editar/<int:campaña_id>/', views.editar_campaña, name='editar_campaña'),
    path('campañas/eliminar/<int:id>/', views.eliminar_campaña, name='eliminar_campaña'),
    
    
    #codigos
    path('codigos/', views.listar_codigos, name='listar_codigos'),
    path('codigos/crear/', views.crear_codigo, name='crear_codigo'),
    path('codigos/editar/<int:id>/', views.editar_codigo, name='editar_codigo'),
    path('codigos/eliminar/<int:id>/', views.eliminar_codigo, name='eliminar_codigo'),
    
    #exportacion
    path('usuarios/exportar/pdf/', views.exportar_usuarios_pdf, name='exportar_usuarios_pdf'),
    path('usuarios/exportar/excel/', views.exportar_usuarios_excel, name='exportar_usuarios_excel'),
    
    # recuperación de contraseña
    path('recuperar/', views.enviar_codigo, name='enviar_codigo'),
    path('verificar-codigo/', views.verificar_codigo, name='verificar_codigo'),
    path('restablecer/<int:id>/', views.restablecer_contraseña, name='restablecer_contraseña'),
    
    #exportar campañas
    path('campañas/exportar/pdf/', views.exportar_campañas_pdf, name='exportar_campañas_pdf'),
    path('campañas/exportar/excel/', views.exportar_campañas_excel, name='exportar_campañas_excel'),
    
  
    path('estadisticas/campañas/', views.campañas_completas, name='campañas_completas'),
    path('estadisticas/campañas/resumen/', views.campañas_resumen, name='campañas_resumen'),
    path('empleado/registrar-pausa/<int:campana_id>/', views.registrar_pausa, name='registrar_pausa'),
    path('empleado/campania-realizada/<int:campana_id>/', views.detalle_campania_realizada, name='detalle_campania_realizada'),
    path('campanias/realizadas/', views.campanias_realizadas_empleado, name='campanias_realizadas_empleado'),
    path('campanas_admin/', views.campanas_admin, name='campanas_admin'),
    path('campanas_admin/<int:id>/', views.detalle_campana_admin, name='detalle_campana_admin'),
    path('campanas_admin/<int:id>/aprobar/', views.aprobar_campaña, name='aprobar_campaña'),
    path('campanas_admin/<int:id>/rechazar/', views.rechazar_campaña, name='rechazar_campaña'),
    path('empleado/calendario/', views.calendario_empleado, name='calendario_empleado'),
    path('empleado/historial-participacion/', views.historial_participacion, name='historial_participacion'),
    path('reportes/', views.generar_reportes, name='generar_reportes'),
    path('reportes/exportar/', views.exportar_reportes, name='exportar_reportes'),
    
    path('roles/', views.listar_roles, name='listar_roles'),
    path('roles/crear/', views.crear_rol, name='crear_rol'),
    path('roles/editar/<int:pk>/', views.editar_rol, name='editar_rol'),
    path('roles/eliminar/<int:pk>/', views.eliminar_rol, name='eliminar_rol'),


        # evaluaciones y mensajes
    path('empleado/evaluaciones-sst/', views.evaluaciones_sst, name='evaluaciones_sst'),
    path('empleado/mensajes/', views.mensajes_empleado, name='mensajes_empleado'),
    
     # Vista para empleados: solo listar recursos visibles
    path('empleado/recursos-sst/', views.recursos_sst, name='recursos_sst'),
    
    #mensajes
    
    path('mensajes/', views.panel_mensajes, name='panel_mensajes'),
    path('mensajes/crear/', views.crear_mensaje, name='crear_mensaje'),
    path('mensajes/editar/<int:id>/', views.editar_mensaje, name='editar_mensaje'),
    path('mensajes/eliminar/<int:id>/', views.eliminar_mensaje, name='eliminar_mensaje'),
    
    #mensajes empleado
    path('empleado/mensajes/<int:id>/', views.detalle_mensaje_empleado, name='detalle_mensaje_empleado'),


    # Recursos SST
    path('recursos/crear/', views.crear_recurso, name='crear_recurso'),
    path('recursos/', views.recursos_sst_admin, name='recursos_sst_admin'),
    path('recursos/editar/<int:pk>/', views.editar_recurso, name='editar_recurso'),
    path('recursos/eliminar/<int:pk>/', views.eliminar_recurso, name='eliminar_recurso'),

    #empleados
    path('empleado/dashboard/', views.dashboard_empleado, name='dashboard_empleado'),
    path('empleado/campanas-asignadas/', views.campanas_asignadas, name='campanas_asignadas'),
    path('empleado/detalle-campana/<int:campaña_id>/', views.detalle_campana, name='detalle_campana'),
    path('empleado/registrar-evidencia/<int:campaña_id>/', views.registrar_evidencia_campaña, name='registrar_evidencia_campaña'),
    path('empleado/historial-participacion/', views.historial_participacion, name='historial_participacion'),
    path('empleado/feedback/', views.feedback_empleado, name='feedback'),
    
     # Asignación de usuarios a campañas
    path('campañas/asignar/', views.asignar_usuario_campania, name='asignar_usuario_campania'),
    
    # CRUD de grupos
    path('grupos/', views.listar_grupos, name='listar_grupos'),
    path('grupos/crear/', views.crear_grupo, name='crear_grupo'),
    
    # Notificaciones
    path('listar/', views.listar_notificaciones, name='listar_notificaciones'),
    path("crear/", views.crear_notificacion, name="crear_notificacion"),
    path("notificaciones/json/", views.notificaciones_json, name="notificaciones_json"),
    path("notificaciones/leida/<int:pk>/", views.marcar_notificacion_leida, name="marcar_notificacion_leida"),
    path("api/notificaciones/", views.api_notificaciones, name="api_notificaciones"),
    path("editar/<int:pk>/", views.editar_notificacion, name="editar_notificacion"),
    path("eliminar/<int:pk>/", views.eliminar_notificacion, name="eliminar_notificacion"),
    path("detalle-admin/<int:pk>/", views.detalle_notificacion_admin, name="detalle_notificacion_admin"),
    path('pausa/<int:pausa_id>/ejecutar/', views.ejecutar_pausa, name='ejecutar_pausa'),
    path("empleado/notificacion/<int:pk>/", views.detalle_notificacion_empleado, name="detalle_notificacion_empleado"),


   
    #notificaciones empleado
    path("listar/empleado/", views.listar_notificaciones_empleado, name="listar_notificaciones_empleado"),
    path("notificacion/<int:pk>/", views.detalle_notificacion_empleado, name="detalle_notificacion_empleado"),
    
    #grupos
    path('grupos/', views.listar_grupos, name='listar_grupos'),
    path('grupos/crear/', views.crear_grupo, name='crear_grupo'),
    path('grupos/editar/<int:id>/', views.editar_grupo, name='editar_grupo'),
    path('grupos/eliminar/<int:id>/', views.eliminar_grupo, name='eliminar_grupo'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
