from django.contrib import admin
from .models import *

class TesisAdmin(admin.ModelAdmin):
    list_display = ('cve_tesis',)
    list_filter = ('cve_epoca',)    
    search_fields = ('id','cve_epoca')
    list_per_page = 200
    fields = ('status','cve_unica','no_reg','materia','cve_tesis', 'cve_epoca','rubro','texto','precedente','referencia','sala_pleno','acuerdo','nota')    
    
class SentenciaAdmin(admin.ModelAdmin):
    list_display = ('id','cve_unica')
    list_filter = ('cve_epoca',)    
    search_fields = ('id','cve_unica')
    list_per_page = 200
    fields = ('cve_unica','no_reg','clave','cve_epoca','rubro', 'texto','referencia','sala_pleno')    

admin.site.register(Tesis,TesisAdmin)
admin.site.register(Sentencia,SentenciaAdmin)