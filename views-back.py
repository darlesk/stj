from django.shortcuts import redirect, render
from .models import *
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import json

# Create your views here.

def inicio(request):             
    if request.method == "POST":        
        return render(request, 'stj/busquedaTesis.html')
    return render(request, 'stj/principal.html')

def stj_busqueda(request):             
    if request.method == "POST":        
        return render(request, 'stj/busquedaTesis.html')
    return render(request, 'stj/principalBusqueda.html')

def stj_resul(request): 
    if request.method == "GET":
        return redirect("/aps-tfja/sctj/")
    if request.method == "POST": 
        page = 1
        pagina_anterior = request.POST.get('input-pagina-anterior',None)          
        pagina_siguiente = request.POST.get('input-pagina-siguiente',None)
        pagina_ultimo = request.POST.get('input-pagina-ultimo',None)
        pagina_primero = request.POST.get('input-pagina-primero',None)
        pagina_actual = request.POST.get('input-pagina-actual',None)
        current = request.POST.get('current',None)        
        click = request.POST.get('cbp',None) 
        
        if click == "siguiente":                       
            page = pagina_siguiente
        if click == "anterior":            
            page = pagina_anterior 
        if click == "anterior":            
            page = pagina_anterior 
        if click == "ultimo":            
            page = pagina_ultimo 
        if click == "primero":            
            page = pagina_primero 
        if click == "current":            
            page = current    
   
        epoca = request.POST.getlist('checkSelectEg')                                                  
        materia = request.POST.get('materia', None)        
        cve_tesis = request.POST.get('cve_tesis', None)
        rubro = request.POST.get('rubro', None)
        precedente = request.POST.get('precedente', None)
        referencia = request.POST.get('referencia', None)
        sala_pleno = request.POST.get('sala_pleno', None)
        texto = request.POST.get('texto', None)                        
        data_list = Tesis.objects.filter(cve_epoca__in=epoca, materia__icontains=materia, 
        cve_tesis__icontains=cve_tesis, rubro__icontains=rubro, precedente__icontains=precedente, 
        referencia__icontains=referencia, sala_pleno__icontains=sala_pleno, texto__icontains=texto).order_by('-id')
        paginator = Paginator(data_list, 5)        
        try:
            tesis = paginator.page(page)
        except PageNotAnInteger:
                # If page is not an integer, deliver first page.
            tesis = paginator.page(1)
        except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
            tesis = paginator.page(paginator.num_pages) 

        return render(request, 'stj/busquedaTesis.html',{"tesis":tesis,"epoca":epoca,"materia":materia,"cve_tesis":cve_tesis,"rubro":rubro,"precedente":precedente,"referencia":referencia,"sala_pleno":sala_pleno,"texto":texto})
    return render(request, 'stj/busquedaTesis.html')

def detalle_tesis(request):
    if request.method == "GET":
        return redirect("/aps-tfja/sctj/") 
    if request.method == "POST":
        identificador = request.POST.get('identificador')  
        texto = Tesis.objects.filter(id=identificador).order_by('id')
        return render(request, 'stj/detalleTesis.html',{"texto":texto})

def detalle_sentencia(request):
    if request.method == "GET":
        return redirect("/aps-tfja/sctj/") 
    if request.method == "POST":
        sentencia_relacionada = request.POST.get('sentencia_relacionada') 
        sentencia = Sentencia.objects.filter(cve_unica=sentencia_relacionada).order_by('id')            
        return render(request, 'stj/detalleSentencia.html',{"sentencia":sentencia})         

def scjn(request): 
    return render(request, 'stj/scjn.html')
