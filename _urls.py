from django.urls import path, re_path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),    
    #path('pdf/(?P<cadena>.+)/$', views.pdf_view, name='pdf'),
    re_path('pdf/(?P<cadena>.+)/$', views.pdf_view, name='pdf'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

