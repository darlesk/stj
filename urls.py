from django.urls import path, re_path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),       
    path('scjn/', views.scjn, name='suprema-corte'),  
    path('sctj-busqueda/', views.stj_busqueda, name='stj_busqueda'), 
    path('busqueda-resultados/', views.stj_resul, name='stj_resul'), 
    path('detalle-tesis/', views.detalle_tesis, name='detalle_tesis'),  
    path('tesis-pdf-detalle/<int:pk>/', views.tesis_pdf_detalle, name='tesis_pdf_detalle'), 
    path('detalle-sentencia/', views.detalle_sentencia, name='detalle_sentencia'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()