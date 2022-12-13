from django.shortcuts import redirect, render, HttpResponseRedirect,HttpResponse
from .models import *
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import json
import tempfile
#from weasyprint import HTML, CSS
from django.template.loader import render_to_string

# Create your views here.

def inicio(request):             
    if request.method == "POST":        
        return render(request, 'stj/busquedaTesis.html')
    return render(request, 'stj/principal-propuesta2.html')

def stj_busqueda(request):             
    materia_a = request.POST.get('materia_a',None)
    cve_tesis_a = request.POST.get('cve_tesis_a',None)
    rubro_a = request.POST.get('rubro_a',None)
    texto_a = request.POST.get('texto_a',None)
    precedente_a = request.POST.get('precedente_a',None)
    referencia_a = request.POST.get('referencia_a',None)
    sala_pleno_a = request.POST.get('sala_pleno_a',None) 
    if texto_a == "$%&":            
        texto_a ="" 
    if rubro_a == "$%&":
        rubro_a ="" 

    
    if materia_a == None and cve_tesis_a == None and rubro_a == None and texto_a == None and precedente_a == None and referencia_a == None and sala_pleno_a == None:                                      
        materia_a =""
        cve_tesis_a =""
        rubro_a =""
        texto_a =""
        precedente_a =""
        referencia_a =""
        sala_pleno_a =""
        
        return render(request, 'stj/principalBusqueda.html',{"materia_a":materia_a,"cve_tesis_a":cve_tesis_a,"rubro_a":rubro_a,"texto_a":texto_a,"precedente_a":precedente_a,"referencia_a":referencia_a,"sala_pleno_a":sala_pleno_a})
    if materia_a != None and cve_tesis_a != None and rubro_a != None and texto_a != None and precedente_a != None and referencia_a != None and sala_pleno_a != None:        
        return render(request, 'stj/principalBusqueda.html',{"materia_a":materia_a,"cve_tesis_a":cve_tesis_a,"rubro_a":rubro_a,"texto_a":texto_a,"precedente_a":precedente_a,"referencia_a":referencia_a,"sala_pleno_a":sala_pleno_a})
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
        jurisprudencias = request.POST.get('jurisprudencias')          
        identificador = request.POST.get('identificador') 
        rubroRadioEg = request.POST.get('rubroRadioEg') 
        textoRadioEg = request.POST.get('textoRadioEg')       

        materia=materia.strip()
        cve_tesis=cve_tesis.strip()
        precedente=precedente.strip()
        referencia=referencia.strip()
        sala_pleno=sala_pleno.strip()
        
        texto_sin_espacio=texto.strip()
        rubro =  rubro.upper()
        rubro_sin_espacio=rubro.strip()

        if epoca and jurisprudencias == None: 
                     
            if not cve_tesis and not materia and not rubro and not precedente and not precedente and not sala_pleno and not texto and not referencia:                                                
                data_list = Tesis.objects.filter(status__in=[1,2,3,4,5],cve_epoca__in=epoca).order_by('-id')
                paginator = Paginator(data_list, 10)        
                try:
                    tesis = paginator.page(page)
                except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                    tesis = paginator.page(1)
                except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                    tesis = paginator.page(paginator.num_pages)                  


            if  cve_tesis or materia or rubro or  precedente or sala_pleno or referencia or texto:

                # 1 rubroFrase and textoPalabras
                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoPalabras":                                                           
                    texto_palabras=texto_sin_espacio.split(' ')                                        
                    python_indices = []
                    
                    for programming_language in range(len(texto_palabras)):
                        ls=texto_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or  ls == "De" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="El" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls == "LAS" or ls == "de" or ls == "del" or ls == "a" or ls == "e" or ls == "y" or ls == "o" or ls == "los" or ls == "en" or ls == "que" or ls == "al" or ls == "no" or ls == "es" or ls == "lo" or ls == "la" or ls == "su" or ls == "el" or ls == "por" or ls == "i" or ls == "u" or ls == "sus" or ls == "como" or ls == "las" or ls=="":
                            python_indices.append(programming_language)
                    
                    for idx in sorted(python_indices, reverse = True):
                        del texto_palabras[idx]

                    longitud=len(texto_palabras)
                                        
                    for vacios in range(15):
                        texto_palabras.append("")

                    data_list = Tesis.objects.filter(texto__icontains=texto_palabras[0],rubro__icontains=rubro,
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[1,2,3,4,5]).filter(texto__icontains=texto_palabras[1]).filter(texto__icontains=texto_palabras[2]).filter(texto__icontains=texto_palabras[3]).filter(texto__icontains=texto_palabras[4]).filter(texto__icontains=texto_palabras[5]).filter(texto__icontains=texto_palabras[6]).filter(texto__icontains=texto_palabras[7]).filter(texto__icontains=texto_palabras[8]).filter(texto__icontains=texto_palabras[9]).filter(texto__icontains=texto_palabras[10]).filter(texto__icontains=texto_palabras[11]).filter(texto__icontains=texto_palabras[12]).filter(texto__icontains=texto_palabras[13]).filter(texto__icontains=texto_palabras[14]).order_by('-id')
                                                                                                    
                    if longitud >= 16 or not longitud:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                                            
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                # 2 rubroPalabras and textoFrase
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoFrase":                    
                    rubro_palabras=rubro_sin_espacio.split(' ')                                        
                    python_indices = []

                    for programming_language in range(len(rubro_palabras)):                        
                        ls=rubro_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls=="":
                            python_indices.append(programming_language)
                    
                    for idx in sorted(python_indices, reverse = True):
                        del rubro_palabras[idx]

                    longitud=len(rubro_palabras)                 
                    
                    for vacios in range(15):
                        rubro_palabras.append("")

                    data_list = Tesis.objects.filter(rubro__icontains=rubro_palabras[0],texto__icontains=texto,
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[1,2,3,4,5]).filter(rubro__icontains=rubro_palabras[1]).filter(rubro__icontains=rubro_palabras[2]).filter(rubro__icontains=rubro_palabras[3]).filter(rubro__icontains=rubro_palabras[4]).filter(rubro__icontains=rubro_palabras[5]).filter(rubro__icontains=rubro_palabras[6]).filter(rubro__icontains=rubro_palabras[7]).filter(rubro__icontains=rubro_palabras[8]).filter(rubro__icontains=rubro_palabras[9]).filter(rubro__icontains=rubro_palabras[10]).filter(rubro__icontains=rubro_palabras[11]).filter(rubro__icontains=rubro_palabras[12]).filter(rubro__icontains=rubro_palabras[13]).filter(rubro__icontains=rubro_palabras[14]).order_by('-id')
                    
                    if longitud >= 16 or not longitud:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                        
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                    
                # 3 rubroPalabras and textoPalabras
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoPalabras":                    
                    rubro_palabras=rubro_sin_espacio.split(' ')          
                    texto_palabras=texto_sin_espacio.split(' ')   

                    python_indices_texto = []           
                    python_indices_rubro = []           

                    #texto_palabras
                    for programming_language in range(len(texto_palabras)):
                        ls=texto_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or  ls == "De" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="El" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls == "LAS" or ls == "de" or ls == "del" or ls == "a" or ls == "e" or ls == "y" or ls == "o" or ls == "los" or ls == "en" or ls == "que" or ls == "al" or ls == "no" or ls == "es" or ls == "lo" or ls == "la" or ls == "su" or ls == "el" or ls == "por" or ls == "i" or ls == "u" or ls == "sus" or ls == "como" or ls == "las" or ls=="":
                            python_indices_texto.append(programming_language)
                    
                    for idx in sorted(python_indices_texto, reverse = True):
                        del texto_palabras[idx]

                    longitud_texto=len(texto_palabras)
                                        
                    for vacios in range(15):
                        texto_palabras.append("")    

                    #rubro_palabras
                    for programming_language in range(len(rubro_palabras)):
                        ls=rubro_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls=="":
                            python_indices_rubro.append(programming_language)
                    
                    for idx in sorted(python_indices_rubro, reverse = True):
                        del rubro_palabras[idx]

                    longitud_rubro=len(rubro_palabras)                 
                    
                    for vacios in range(15):
                        rubro_palabras.append("")
                    
                    data_list = Tesis.objects.filter(texto__icontains=texto_palabras[0],rubro__icontains=rubro_palabras[0],
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[1,2,3,4,5]).filter(texto__icontains=texto_palabras[1]).filter(texto__icontains=texto_palabras[2]).filter(texto__icontains=texto_palabras[3]).filter(texto__icontains=texto_palabras[4]).filter(texto__icontains=texto_palabras[5]).filter(texto__icontains=texto_palabras[6]).filter(texto__icontains=texto_palabras[7]).filter(texto__icontains=texto_palabras[8]).filter(texto__icontains=texto_palabras[9]).filter(texto__icontains=texto_palabras[10]).filter(texto__icontains=texto_palabras[11]).filter(texto__icontains=texto_palabras[12]).filter(texto__icontains=texto_palabras[13]).filter(texto__icontains=texto_palabras[14]).filter(rubro__icontains=rubro_palabras[1]).filter(rubro__icontains=rubro_palabras[2]).filter(rubro__icontains=rubro_palabras[3]).filter(rubro__icontains=rubro_palabras[4]).filter(rubro__icontains=rubro_palabras[5]).filter(rubro__icontains=rubro_palabras[6]).filter(rubro__icontains=rubro_palabras[7]).filter(rubro__icontains=rubro_palabras[8]).filter(rubro__icontains=rubro_palabras[9]).filter(rubro__icontains=rubro_palabras[10]).filter(rubro__icontains=rubro_palabras[11]).filter(rubro__icontains=rubro_palabras[12]).filter(rubro__icontains=rubro_palabras[13]).filter(rubro__icontains=rubro_palabras[14]).order_by('-id')

                    if longitud_texto >= 16 or not longitud_texto:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                    
                    if longitud_rubro >= 16 or not longitud_rubro:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                        
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)

                # 4 rubroFrase and textoFrase
                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoFrase":                    
                    data_list = Tesis.objects.filter(rubro__icontains=rubro,texto__icontains=texto,materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                    
            return render(request, 'stj/busquedaTesis.html',{"tesis":tesis,"epoca":epoca,"materia":materia,"cve_tesis":cve_tesis,"rubro":rubro,"precedente":precedente,"referencia":referencia,"sala_pleno":sala_pleno,"texto":texto,"jurisprudencias":jurisprudencias,"rubroRadioEg":rubroRadioEg,"textoRadioEg":textoRadioEg})                   
        
        if epoca and jurisprudencias=="NoJurisprudencia":             
            if not cve_tesis and not materia and not rubro and not precedente and not precedente and not sala_pleno and not texto and not referencia:                
                data_list = Tesis.objects.filter(status__in=[1,2,3,4,5],cve_epoca__in=epoca).order_by('-id')
                paginator = Paginator(data_list, 10)        
                try:
                    tesis = paginator.page(page)
                except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                    tesis = paginator.page(1)
                except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                    tesis = paginator.page(paginator.num_pages)
                
                
            if  cve_tesis or materia or rubro or  precedente or sala_pleno or referencia or texto:
                # 1 rubroFrase and textoPalabras
                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoPalabras":                                                           
                    texto_palabras=texto_sin_espacio.split(' ')                                        
                    python_indices = []
                    
                    for programming_language in range(len(texto_palabras)):
                        ls=texto_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or  ls == "De" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="El" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls == "LAS" or ls == "de" or ls == "del" or ls == "a" or ls == "e" or ls == "y" or ls == "o" or ls == "los" or ls == "en" or ls == "que" or ls == "al" or ls == "no" or ls == "es" or ls == "lo" or ls == "la" or ls == "su" or ls == "el" or ls == "por" or ls == "i" or ls == "u" or ls == "sus" or ls == "como" or ls == "las" or ls=="":
                            python_indices.append(programming_language)
                    
                    for idx in sorted(python_indices, reverse = True):
                        del texto_palabras[idx]

                    longitud=len(texto_palabras)
                                        
                    for vacios in range(15):
                        texto_palabras.append("")

                    data_list = Tesis.objects.filter(texto__icontains=texto_palabras[0],rubro__icontains=rubro,
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[1,2,3,4,5]).filter(texto__icontains=texto_palabras[1]).filter(texto__icontains=texto_palabras[2]).filter(texto__icontains=texto_palabras[3]).filter(texto__icontains=texto_palabras[4]).filter(texto__icontains=texto_palabras[5]).filter(texto__icontains=texto_palabras[6]).filter(texto__icontains=texto_palabras[7]).filter(texto__icontains=texto_palabras[8]).filter(texto__icontains=texto_palabras[9]).filter(texto__icontains=texto_palabras[10]).filter(texto__icontains=texto_palabras[11]).filter(texto__icontains=texto_palabras[12]).filter(texto__icontains=texto_palabras[13]).filter(texto__icontains=texto_palabras[14]).order_by('-id')
                                                                                                    
                    if longitud >= 16 or not longitud:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                                            
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                # 2 rubroPalabras and textoFrase
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoFrase":                    
                    rubro_palabras=rubro_sin_espacio.split(' ')                                        
                    python_indices = []

                    for programming_language in range(len(rubro_palabras)):                        
                        ls=rubro_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls=="":
                            python_indices.append(programming_language)
                    
                    for idx in sorted(python_indices, reverse = True):
                        del rubro_palabras[idx]

                    longitud=len(rubro_palabras)                 
                    
                    for vacios in range(15):
                        rubro_palabras.append("")

                    data_list = Tesis.objects.filter(rubro__icontains=rubro_palabras[0],texto__icontains=texto,
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[1,2,3,4,5]).filter(rubro__icontains=rubro_palabras[1]).filter(rubro__icontains=rubro_palabras[2]).filter(rubro__icontains=rubro_palabras[3]).filter(rubro__icontains=rubro_palabras[4]).filter(rubro__icontains=rubro_palabras[5]).filter(rubro__icontains=rubro_palabras[6]).filter(rubro__icontains=rubro_palabras[7]).filter(rubro__icontains=rubro_palabras[8]).filter(rubro__icontains=rubro_palabras[9]).filter(rubro__icontains=rubro_palabras[10]).filter(rubro__icontains=rubro_palabras[11]).filter(rubro__icontains=rubro_palabras[12]).filter(rubro__icontains=rubro_palabras[13]).filter(rubro__icontains=rubro_palabras[14]).order_by('-id')
                    
                    if longitud >= 16 or not longitud:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                        
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                    
                # 3 rubroPalabras and textoPalabras
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoPalabras":                    
                    rubro_palabras=rubro_sin_espacio.split(' ')          
                    texto_palabras=texto_sin_espacio.split(' ')   

                    python_indices_texto = []           
                    python_indices_rubro = []           

                    #texto_palabras
                    for programming_language in range(len(texto_palabras)):
                        ls=texto_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or  ls == "De" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="El" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls == "LAS" or ls == "de" or ls == "del" or ls == "a" or ls == "e" or ls == "y" or ls == "o" or ls == "los" or ls == "en" or ls == "que" or ls == "al" or ls == "no" or ls == "es" or ls == "lo" or ls == "la" or ls == "su" or ls == "el" or ls == "por" or ls == "i" or ls == "u" or ls == "sus" or ls == "como" or ls == "las" or ls=="":
                            python_indices_texto.append(programming_language)
                    
                    for idx in sorted(python_indices_texto, reverse = True):
                        del texto_palabras[idx]

                    longitud_texto=len(texto_palabras)
                                        
                    for vacios in range(15):
                        texto_palabras.append("")    

                    #rubro_palabras
                    for programming_language in range(len(rubro_palabras)):
                        ls=rubro_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls=="":
                            python_indices_rubro.append(programming_language)
                    
                    for idx in sorted(python_indices_rubro, reverse = True):
                        del rubro_palabras[idx]

                    longitud_rubro=len(rubro_palabras)                 
                    
                    for vacios in range(15):
                        rubro_palabras.append("")
                    
                    data_list = Tesis.objects.filter(texto__icontains=texto_palabras[0],rubro__icontains=rubro_palabras[0],
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[1,2,3,4,5]).filter(texto__icontains=texto_palabras[1]).filter(texto__icontains=texto_palabras[2]).filter(texto__icontains=texto_palabras[3]).filter(texto__icontains=texto_palabras[4]).filter(texto__icontains=texto_palabras[5]).filter(texto__icontains=texto_palabras[6]).filter(texto__icontains=texto_palabras[7]).filter(texto__icontains=texto_palabras[8]).filter(texto__icontains=texto_palabras[9]).filter(texto__icontains=texto_palabras[10]).filter(texto__icontains=texto_palabras[11]).filter(texto__icontains=texto_palabras[12]).filter(texto__icontains=texto_palabras[13]).filter(texto__icontains=texto_palabras[14]).filter(rubro__icontains=rubro_palabras[1]).filter(rubro__icontains=rubro_palabras[2]).filter(rubro__icontains=rubro_palabras[3]).filter(rubro__icontains=rubro_palabras[4]).filter(rubro__icontains=rubro_palabras[5]).filter(rubro__icontains=rubro_palabras[6]).filter(rubro__icontains=rubro_palabras[7]).filter(rubro__icontains=rubro_palabras[8]).filter(rubro__icontains=rubro_palabras[9]).filter(rubro__icontains=rubro_palabras[10]).filter(rubro__icontains=rubro_palabras[11]).filter(rubro__icontains=rubro_palabras[12]).filter(rubro__icontains=rubro_palabras[13]).filter(rubro__icontains=rubro_palabras[14]).order_by('-id')

                    if longitud_texto >= 16 or not longitud_texto:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                    
                    if longitud_rubro >= 16 or not longitud_rubro:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                        
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)

                # 4 rubroFrase and textoFrase
                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoFrase":                    
                    data_list = Tesis.objects.filter(rubro__icontains=rubro,texto__icontains=texto,materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)          
            return render(request, 'stj/busquedaTesis.html',{"tesis":tesis,"epoca":epoca,"materia":materia,"cve_tesis":cve_tesis,"rubro":rubro,"precedente":precedente,"referencia":referencia,"sala_pleno":sala_pleno,"texto":texto,"jurisprudencias":jurisprudencias,"rubroRadioEg":rubroRadioEg,"textoRadioEg":textoRadioEg})                   

        #Jurisprudencias
        if jurisprudencias =="jurisprudencias" and epoca:        
            if not cve_tesis and not materia and not rubro and not precedente and not precedente and not sala_pleno and not texto and not referencia:
                data_list = Tesis.objects.filter(status__in=[2,3],cve_epoca__in=epoca).order_by('-id')   
                paginator = Paginator(data_list, 10)        
                try:
                    tesis = paginator.page(page)
                except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                    tesis = paginator.page(1)
                except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                    tesis = paginator.page(paginator.num_pages)         
            if  cve_tesis or materia or rubro or  precedente or sala_pleno or referencia or texto:

                # 1 rubroFrase and textoPalabras
                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoPalabras":                                                           
                    texto_palabras=texto_sin_espacio.split(' ')                                        
                    python_indices = []
                    
                    for programming_language in range(len(texto_palabras)):
                        ls=texto_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or  ls == "De" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="El" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls == "LAS" or ls == "de" or ls == "del" or ls == "a" or ls == "e" or ls == "y" or ls == "o" or ls == "los" or ls == "en" or ls == "que" or ls == "al" or ls == "no" or ls == "es" or ls == "lo" or ls == "la" or ls == "su" or ls == "el" or ls == "por" or ls == "i" or ls == "u" or ls == "sus" or ls == "como" or ls == "las" or ls=="":
                            python_indices.append(programming_language)
                    
                    for idx in sorted(python_indices, reverse = True):
                        del texto_palabras[idx]

                    longitud=len(texto_palabras)
                                        
                    for vacios in range(15):
                        texto_palabras.append("")

                    data_list = Tesis.objects.filter(texto__icontains=texto_palabras[0],rubro__icontains=rubro,
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[2,3]).filter(texto__icontains=texto_palabras[1]).filter(texto__icontains=texto_palabras[2]).filter(texto__icontains=texto_palabras[3]).filter(texto__icontains=texto_palabras[4]).filter(texto__icontains=texto_palabras[5]).filter(texto__icontains=texto_palabras[6]).filter(texto__icontains=texto_palabras[7]).filter(texto__icontains=texto_palabras[8]).filter(texto__icontains=texto_palabras[9]).filter(texto__icontains=texto_palabras[10]).filter(texto__icontains=texto_palabras[11]).filter(texto__icontains=texto_palabras[12]).filter(texto__icontains=texto_palabras[13]).filter(texto__icontains=texto_palabras[14]).order_by('-id')
                                                                                                    
                    if longitud >= 16 or not longitud:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                                            
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                # 2 rubroPalabras and textoFrase
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoFrase":                    
                    rubro_palabras=rubro_sin_espacio.split(' ')                                        
                    python_indices = []

                    for programming_language in range(len(rubro_palabras)):                        
                        ls=rubro_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls=="":
                            python_indices.append(programming_language)
                    
                    for idx in sorted(python_indices, reverse = True):
                        del rubro_palabras[idx]

                    longitud=len(rubro_palabras)                 
                    
                    for vacios in range(15):
                        rubro_palabras.append("")

                    data_list = Tesis.objects.filter(rubro__icontains=rubro_palabras[0],texto__icontains=texto,
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[2,3]).filter(rubro__icontains=rubro_palabras[1]).filter(rubro__icontains=rubro_palabras[2]).filter(rubro__icontains=rubro_palabras[3]).filter(rubro__icontains=rubro_palabras[4]).filter(rubro__icontains=rubro_palabras[5]).filter(rubro__icontains=rubro_palabras[6]).filter(rubro__icontains=rubro_palabras[7]).filter(rubro__icontains=rubro_palabras[8]).filter(rubro__icontains=rubro_palabras[9]).filter(rubro__icontains=rubro_palabras[10]).filter(rubro__icontains=rubro_palabras[11]).filter(rubro__icontains=rubro_palabras[12]).filter(rubro__icontains=rubro_palabras[13]).filter(rubro__icontains=rubro_palabras[14]).order_by('-id')
                    
                    if longitud >= 16 or not longitud:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                        
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                    
                # 3 rubroPalabras and textoPalabras
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoPalabras":                    
                    rubro_palabras=rubro_sin_espacio.split(' ')          
                    texto_palabras=texto_sin_espacio.split(' ')   

                    python_indices_texto = []           
                    python_indices_rubro = []           

                    #texto_palabras
                    for programming_language in range(len(texto_palabras)):
                        ls=texto_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or  ls == "De" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="El" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls == "LAS" or ls == "de" or ls == "del" or ls == "a" or ls == "e" or ls == "y" or ls == "o" or ls == "los" or ls == "en" or ls == "que" or ls == "al" or ls == "no" or ls == "es" or ls == "lo" or ls == "la" or ls == "su" or ls == "el" or ls == "por" or ls == "i" or ls == "u" or ls == "sus" or ls == "como" or ls == "las" or ls=="":
                            python_indices_texto.append(programming_language)
                    
                    for idx in sorted(python_indices_texto, reverse = True):
                        del texto_palabras[idx]

                    longitud_texto=len(texto_palabras)
                                        
                    for vacios in range(15):
                        texto_palabras.append("")    

                    #rubro_palabras
                    for programming_language in range(len(rubro_palabras)):
                        ls=rubro_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls=="":
                            python_indices_rubro.append(programming_language)
                    
                    for idx in sorted(python_indices_rubro, reverse = True):
                        del rubro_palabras[idx]

                    longitud_rubro=len(rubro_palabras)                 
                    
                    for vacios in range(15):
                        rubro_palabras.append("")
                    
                    data_list = Tesis.objects.filter(texto__icontains=texto_palabras[0],rubro__icontains=rubro_palabras[0],
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[2,3]).filter(texto__icontains=texto_palabras[1]).filter(texto__icontains=texto_palabras[2]).filter(texto__icontains=texto_palabras[3]).filter(texto__icontains=texto_palabras[4]).filter(texto__icontains=texto_palabras[5]).filter(texto__icontains=texto_palabras[6]).filter(texto__icontains=texto_palabras[7]).filter(texto__icontains=texto_palabras[8]).filter(texto__icontains=texto_palabras[9]).filter(texto__icontains=texto_palabras[10]).filter(texto__icontains=texto_palabras[11]).filter(texto__icontains=texto_palabras[12]).filter(texto__icontains=texto_palabras[13]).filter(texto__icontains=texto_palabras[14]).filter(rubro__icontains=rubro_palabras[1]).filter(rubro__icontains=rubro_palabras[2]).filter(rubro__icontains=rubro_palabras[3]).filter(rubro__icontains=rubro_palabras[4]).filter(rubro__icontains=rubro_palabras[5]).filter(rubro__icontains=rubro_palabras[6]).filter(rubro__icontains=rubro_palabras[7]).filter(rubro__icontains=rubro_palabras[8]).filter(rubro__icontains=rubro_palabras[9]).filter(rubro__icontains=rubro_palabras[10]).filter(rubro__icontains=rubro_palabras[11]).filter(rubro__icontains=rubro_palabras[12]).filter(rubro__icontains=rubro_palabras[13]).filter(rubro__icontains=rubro_palabras[14]).order_by('-id')

                    if longitud_texto >= 16 or not longitud_texto:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                    
                    if longitud_rubro >= 16 or not longitud_rubro:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                        
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)

                # 4 rubroFrase and textoFrase
                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoFrase":                    
                    data_list = Tesis.objects.filter(rubro__icontains=rubro,texto__icontains=texto,materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[2,3]).order_by('-id')
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)                                               
            
            return render(request, 'stj/busquedaTesis.html',{"tesis":tesis,"epoca":epoca,"materia":materia,"cve_tesis":cve_tesis,"rubro":rubro,"precedente":precedente,"referencia":referencia,"sala_pleno":sala_pleno,"texto":texto,"jurisprudencias":jurisprudencias,"rubroRadioEg":rubroRadioEg,"textoRadioEg":textoRadioEg})                        
        
    return render(request, 'stj/busquedaTesis.html')

def detalle_tesis(request):
    if request.method == "GET":
        return redirect("/aps-tfja/sctj/") 
    if request.method == "POST":
        pageTesis = 0
        pagina_anterior = request.POST.get('input-pagina-anterior',None)          
        pagina_siguiente = request.POST.get('input-pagina-siguiente',None)
        pagina_ultimo = request.POST.get('input-pagina-ultimo',None)
        pagina_primero = request.POST.get('input-pagina-primero',None)
        pagina_actual = request.POST.get('input-pagina-actual',None)
        current = request.POST.get('current',None)        
        click = request.POST.get('cbp',None) 
        
        if click == "siguiente":                       
            pageTesis = pagina_siguiente
        if click == "anterior":            
            pageTesis = pagina_anterior 
        if click == "anterior":            
            pageTesis = pagina_anterior 
        if click == "ultimo":            
            pageTesis = pagina_ultimo 
        if click == "primero":            
            pageTesis = pagina_primero 
        if click == "current":            
            pageTesis = current
        
        epoca = request.POST.getlist('detalle_checkSelectEg')                                                  
        materia = request.POST.get('detalle_materia', None)        
        cve_tesis = request.POST.get('detalle_cve_tesis', None)
        rubro = request.POST.get('detalle_rubro', None)
        precedente = request.POST.get('detalle_precedente', None)
        referencia = request.POST.get('detalle_referencia', None)
        sala_pleno = request.POST.get('detalle_sala_pleno', None)
        texto = request.POST.get('detalle_texto', None)
        tid = request.POST.get('detalle_tesis_id', None)   
        jurisprudencias = request.POST.get('detalle_jurisprudencias')
        identificador = request.POST.get('detalle_identificador')
        rubroRadioEg = request.POST.get('rubroRadioEg') 
        textoRadioEg = request.POST.get('textoRadioEg')
        rubro =  rubro.upper()
        texto_sin_espacio=texto.strip()
        rubro_sin_espacio=rubro.strip()
        
        if epoca and jurisprudencias=="None":                                
            if not cve_tesis and not materia and not rubro and not precedente and not sala_pleno and not texto and not referencia:
                
                data_list = Tesis.objects.filter(status__in=[1,2,3,4,5],cve_epoca__in=epoca).order_by('-id')
                lista1 = list(data_list) 
                if identificador:
                    for l1 in lista1:                                                            
                        if l1.id == int(identificador):                         
                            posicion = lista1.index(l1)                           
                            pageTesis = posicion + 1   
                if identificador == None:
                    pageTesis=pageTesis

                paginator = Paginator(data_list, 1)        
                try:
                    tesis = paginator.page(pageTesis)
                except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                    tesis = paginator.page(1)
                except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                    tesis = paginator.page(paginator.num_pages)                        
            if  cve_tesis or materia or rubro or  precedente or sala_pleno or referencia or texto:
                
                # rubroFrase and textoPalabras
                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoPalabras":                                                           
                    texto_palabras=texto_sin_espacio.split(' ')                                        
                    python_indices = []
                    
                    for programming_language in range(len(texto_palabras)):
                        ls=texto_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or  ls == "De" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="El" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls == "LAS" or ls == "de" or ls == "del" or ls == "a" or ls == "e" or ls == "y" or ls == "o" or ls == "los" or ls == "en" or ls == "que" or ls == "al" or ls == "no" or ls == "es" or ls == "lo" or ls == "la" or ls == "su" or ls == "el" or ls == "por" or ls == "i" or ls == "u" or ls == "sus" or ls == "como" or ls == "las" or ls=="":
                            python_indices.append(programming_language)
                    
                    for idx in sorted(python_indices, reverse = True):
                        del texto_palabras[idx]

                    longitud=len(texto_palabras)
                                        
                    for vacios in range(15):
                        texto_palabras.append("")

                    data_list = Tesis.objects.filter(texto__icontains=texto_palabras[0],rubro__icontains=rubro,
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[1,2,3,4,5]).filter(texto__icontains=texto_palabras[1]).filter(texto__icontains=texto_palabras[2]).filter(texto__icontains=texto_palabras[3]).filter(texto__icontains=texto_palabras[4]).filter(texto__icontains=texto_palabras[5]).filter(texto__icontains=texto_palabras[6]).filter(texto__icontains=texto_palabras[7]).filter(texto__icontains=texto_palabras[8]).filter(texto__icontains=texto_palabras[9]).filter(texto__icontains=texto_palabras[10]).filter(texto__icontains=texto_palabras[11]).filter(texto__icontains=texto_palabras[12]).filter(texto__icontains=texto_palabras[13]).filter(texto__icontains=texto_palabras[14]).order_by('-id')
                                                                                                    
                    if longitud >= 16 or not longitud:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                                            
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                # rubroPalabras and textoFrase
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoFrase":                    
                    rubro_palabras=rubro_sin_espacio.split(' ')                                        
                    python_indices = []

                    for programming_language in range(len(rubro_palabras)):                        
                        ls=rubro_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls=="":
                            python_indices.append(programming_language)
                    
                    for idx in sorted(python_indices, reverse = True):
                        del rubro_palabras[idx]

                    longitud=len(rubro_palabras)                 
                    
                    for vacios in range(15):
                        rubro_palabras.append("")

                    data_list = Tesis.objects.filter(rubro__icontains=rubro_palabras[0],texto__icontains=texto,
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[1,2,3,4,5]).filter(rubro__icontains=rubro_palabras[1]).filter(rubro__icontains=rubro_palabras[2]).filter(rubro__icontains=rubro_palabras[3]).filter(rubro__icontains=rubro_palabras[4]).filter(rubro__icontains=rubro_palabras[5]).filter(rubro__icontains=rubro_palabras[6]).filter(rubro__icontains=rubro_palabras[7]).filter(rubro__icontains=rubro_palabras[8]).filter(rubro__icontains=rubro_palabras[9]).filter(rubro__icontains=rubro_palabras[10]).filter(rubro__icontains=rubro_palabras[11]).filter(rubro__icontains=rubro_palabras[12]).filter(rubro__icontains=rubro_palabras[13]).filter(rubro__icontains=rubro_palabras[14]).order_by('-id')
                    
                    if longitud >= 16 or not longitud:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                        
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                    
                # rubroPalabras and textoPalabras
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoPalabras":                    
                    rubro_palabras=rubro_sin_espacio.split(' ')          
                    texto_palabras=texto_sin_espacio.split(' ')   

                    python_indices_texto = []           
                    python_indices_rubro = []           

                    #texto_palabras
                    for programming_language in range(len(texto_palabras)):
                        ls=texto_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or  ls == "De" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="El" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls == "LAS" or ls == "de" or ls == "del" or ls == "a" or ls == "e" or ls == "y" or ls == "o" or ls == "los" or ls == "en" or ls == "que" or ls == "al" or ls == "no" or ls == "es" or ls == "lo" or ls == "la" or ls == "su" or ls == "el" or ls == "por" or ls == "i" or ls == "u" or ls == "sus" or ls == "como" or ls == "las" or ls=="":
                            python_indices_texto.append(programming_language)
                    
                    for idx in sorted(python_indices_texto, reverse = True):
                        del texto_palabras[idx]

                    longitud_texto=len(texto_palabras)
                                        
                    for vacios in range(15):
                        texto_palabras.append("")    

                    #rubro_palabras
                    for programming_language in range(len(rubro_palabras)):
                        ls=rubro_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls=="":
                            python_indices_rubro.append(programming_language)
                    
                    for idx in sorted(python_indices_rubro, reverse = True):
                        del rubro_palabras[idx]

                    longitud_rubro=len(rubro_palabras)                 
                    
                    for vacios in range(15):
                        rubro_palabras.append("")
                    
                    data_list = Tesis.objects.filter(texto__icontains=texto_palabras[0],rubro__icontains=rubro_palabras[0],
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[1,2,3,4,5]).filter(texto__icontains=texto_palabras[1]).filter(texto__icontains=texto_palabras[2]).filter(texto__icontains=texto_palabras[3]).filter(texto__icontains=texto_palabras[4]).filter(texto__icontains=texto_palabras[5]).filter(texto__icontains=texto_palabras[6]).filter(texto__icontains=texto_palabras[7]).filter(texto__icontains=texto_palabras[8]).filter(texto__icontains=texto_palabras[9]).filter(texto__icontains=texto_palabras[10]).filter(texto__icontains=texto_palabras[11]).filter(texto__icontains=texto_palabras[12]).filter(texto__icontains=texto_palabras[13]).filter(texto__icontains=texto_palabras[14]).filter(rubro__icontains=rubro_palabras[1]).filter(rubro__icontains=rubro_palabras[2]).filter(rubro__icontains=rubro_palabras[3]).filter(rubro__icontains=rubro_palabras[4]).filter(rubro__icontains=rubro_palabras[5]).filter(rubro__icontains=rubro_palabras[6]).filter(rubro__icontains=rubro_palabras[7]).filter(rubro__icontains=rubro_palabras[8]).filter(rubro__icontains=rubro_palabras[9]).filter(rubro__icontains=rubro_palabras[10]).filter(rubro__icontains=rubro_palabras[11]).filter(rubro__icontains=rubro_palabras[12]).filter(rubro__icontains=rubro_palabras[13]).filter(rubro__icontains=rubro_palabras[14]).order_by('-id')

                    if longitud_texto >= 16 or not longitud_texto:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                    
                    if longitud_rubro >= 16 or not longitud_rubro:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                        
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)

                # rubroFrase and textoFrase
                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoFrase":                    
                    data_list = Tesis.objects.filter(rubro__icontains=rubro,texto__icontains=texto,materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)               

            return render(request, 'stj/detalleTesis.html',{"texto":texto,"tesis":tesis,"epoca":epoca,"materia":materia,"cve_tesis":cve_tesis,"rubro":rubro,"precedente":precedente,"referencia":referencia,"sala_pleno":sala_pleno,"jurisprudencias":jurisprudencias,'identificador':identificador,"rubroRadioEg":rubroRadioEg,"textoRadioEg":textoRadioEg})

        if epoca and jurisprudencias=="NoJurisprudencia":                                          
            if not cve_tesis and not materia and not rubro and not precedente and not precedente and not sala_pleno and not texto and not referencia:
                
                data_list = Tesis.objects.filter(status__in=[1,2,3,4,5],cve_epoca__in=epoca).order_by('-id')
                lista1 = list(data_list) 
                if identificador:
                    for l1 in lista1:                                                            
                        if l1.id == int(identificador):                         
                            posicion = lista1.index(l1)                           
                            pageTesis = posicion + 1   
                if identificador == None:
                    pageTesis=pageTesis

                paginator = Paginator(data_list, 1)        
                try:
                    tesis = paginator.page(pageTesis)
                except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                    tesis = paginator.page(1)
                except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                    tesis = paginator.page(paginator.num_pages)                        
            if  cve_tesis or materia or rubro or  precedente or sala_pleno or referencia or texto:

                # rubroFrase and textoPalabras                
                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoPalabras":                                                           
                    texto_palabras=texto_sin_espacio.split(' ')                                        
                    python_indices = []
                    
                    for programming_language in range(len(texto_palabras)):
                        ls=texto_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or  ls == "De" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="El" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls == "LAS" or ls == "de" or ls == "del" or ls == "a" or ls == "e" or ls == "y" or ls == "o" or ls == "los" or ls == "en" or ls == "que" or ls == "al" or ls == "no" or ls == "es" or ls == "lo" or ls == "la" or ls == "su" or ls == "el" or ls == "por" or ls == "i" or ls == "u" or ls == "sus" or ls == "como" or ls == "las" or ls=="":
                            python_indices.append(programming_language)
                    
                    for idx in sorted(python_indices, reverse = True):
                        del texto_palabras[idx]

                    longitud=len(texto_palabras)
                                        
                    for vacios in range(15):
                        texto_palabras.append("")

                    data_list = Tesis.objects.filter(texto__icontains=texto_palabras[0],rubro__icontains=rubro,
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[1,2,3,4,5]).filter(texto__icontains=texto_palabras[1]).filter(texto__icontains=texto_palabras[2]).filter(texto__icontains=texto_palabras[3]).filter(texto__icontains=texto_palabras[4]).filter(texto__icontains=texto_palabras[5]).filter(texto__icontains=texto_palabras[6]).filter(texto__icontains=texto_palabras[7]).filter(texto__icontains=texto_palabras[8]).filter(texto__icontains=texto_palabras[9]).filter(texto__icontains=texto_palabras[10]).filter(texto__icontains=texto_palabras[11]).filter(texto__icontains=texto_palabras[12]).filter(texto__icontains=texto_palabras[13]).filter(texto__icontains=texto_palabras[14]).order_by('-id')
                                                                                                    
                    if longitud >= 16 or not longitud:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                                            
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                # rubroPalabras and textoFrase
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoFrase":                    
                    rubro_palabras=rubro_sin_espacio.split(' ')                                        
                    python_indices = []

                    for programming_language in range(len(rubro_palabras)):                        
                        ls=rubro_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls=="":
                            python_indices.append(programming_language)
                    
                    for idx in sorted(python_indices, reverse = True):
                        del rubro_palabras[idx]

                    longitud=len(rubro_palabras)                 
                    
                    for vacios in range(15):
                        rubro_palabras.append("")

                    data_list = Tesis.objects.filter(rubro__icontains=rubro_palabras[0],texto__icontains=texto,
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[1,2,3,4,5]).filter(rubro__icontains=rubro_palabras[1]).filter(rubro__icontains=rubro_palabras[2]).filter(rubro__icontains=rubro_palabras[3]).filter(rubro__icontains=rubro_palabras[4]).filter(rubro__icontains=rubro_palabras[5]).filter(rubro__icontains=rubro_palabras[6]).filter(rubro__icontains=rubro_palabras[7]).filter(rubro__icontains=rubro_palabras[8]).filter(rubro__icontains=rubro_palabras[9]).filter(rubro__icontains=rubro_palabras[10]).filter(rubro__icontains=rubro_palabras[11]).filter(rubro__icontains=rubro_palabras[12]).filter(rubro__icontains=rubro_palabras[13]).filter(rubro__icontains=rubro_palabras[14]).order_by('-id')
                    
                    if longitud >= 16 or not longitud:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                        
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                    
                # rubroPalabras and textoPalabras
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoPalabras":                    
                    rubro_palabras=rubro_sin_espacio.split(' ')          
                    texto_palabras=texto_sin_espacio.split(' ')   

                    python_indices_texto = []           
                    python_indices_rubro = []           

                    #texto_palabras
                    for programming_language in range(len(texto_palabras)):
                        ls=texto_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or  ls == "De" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="El" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls == "LAS" or ls == "de" or ls == "del" or ls == "a" or ls == "e" or ls == "y" or ls == "o" or ls == "los" or ls == "en" or ls == "que" or ls == "al" or ls == "no" or ls == "es" or ls == "lo" or ls == "la" or ls == "su" or ls == "el" or ls == "por" or ls == "i" or ls == "u" or ls == "sus" or ls == "como" or ls == "las" or ls=="":
                            python_indices_texto.append(programming_language)
                    
                    for idx in sorted(python_indices_texto, reverse = True):
                        del texto_palabras[idx]

                    longitud_texto=len(texto_palabras)
                                        
                    for vacios in range(15):
                        texto_palabras.append("")    

                    #rubro_palabras
                    for programming_language in range(len(rubro_palabras)):
                        ls=rubro_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls=="":
                            python_indices_rubro.append(programming_language)
                    
                    for idx in sorted(python_indices_rubro, reverse = True):
                        del rubro_palabras[idx]

                    longitud_rubro=len(rubro_palabras)                 
                    
                    for vacios in range(15):
                        rubro_palabras.append("")
                    
                    data_list = Tesis.objects.filter(texto__icontains=texto_palabras[0],rubro__icontains=rubro_palabras[0],
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[1,2,3,4,5]).filter(texto__icontains=texto_palabras[1]).filter(texto__icontains=texto_palabras[2]).filter(texto__icontains=texto_palabras[3]).filter(texto__icontains=texto_palabras[4]).filter(texto__icontains=texto_palabras[5]).filter(texto__icontains=texto_palabras[6]).filter(texto__icontains=texto_palabras[7]).filter(texto__icontains=texto_palabras[8]).filter(texto__icontains=texto_palabras[9]).filter(texto__icontains=texto_palabras[10]).filter(texto__icontains=texto_palabras[11]).filter(texto__icontains=texto_palabras[12]).filter(texto__icontains=texto_palabras[13]).filter(texto__icontains=texto_palabras[14]).filter(rubro__icontains=rubro_palabras[1]).filter(rubro__icontains=rubro_palabras[2]).filter(rubro__icontains=rubro_palabras[3]).filter(rubro__icontains=rubro_palabras[4]).filter(rubro__icontains=rubro_palabras[5]).filter(rubro__icontains=rubro_palabras[6]).filter(rubro__icontains=rubro_palabras[7]).filter(rubro__icontains=rubro_palabras[8]).filter(rubro__icontains=rubro_palabras[9]).filter(rubro__icontains=rubro_palabras[10]).filter(rubro__icontains=rubro_palabras[11]).filter(rubro__icontains=rubro_palabras[12]).filter(rubro__icontains=rubro_palabras[13]).filter(rubro__icontains=rubro_palabras[14]).order_by('-id')

                    if longitud_texto >= 16 or not longitud_texto:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                    
                    if longitud_rubro >= 16 or not longitud_rubro:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                        
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)

                # rubroFrase and textoFrase
                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoFrase":                    
                    data_list = Tesis.objects.filter(rubro__icontains=rubro,texto__icontains=texto,materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)

            return render(request, 'stj/detalleTesis.html',{"texto":texto,"tesis":tesis,"epoca":epoca,"materia":materia,"cve_tesis":cve_tesis,"rubro":rubro,"precedente":precedente,"referencia":referencia,"sala_pleno":sala_pleno,"jurisprudencias":jurisprudencias,'identificador':identificador,"rubroRadioEg":rubroRadioEg,"textoRadioEg":textoRadioEg})

        #Jurisprudencias
        if jurisprudencias =="jurisprudencias" and epoca:                 
            if not cve_tesis and not materia and not rubro and not precedente and not precedente and not sala_pleno and not texto and not referencia:                                
                data_list = Tesis.objects.filter(status__in=[2,3],cve_epoca__in=epoca).order_by('-id')                 
                lista1 = list(data_list) 
                if identificador:
                    for l1 in lista1:                                                            
                        if l1.id == int(identificador):                         
                            posicion = lista1.index(l1)                           
                            pageTesis = posicion + 1   
                if identificador == None:
                    pageTesis=pageTesis
                
                paginator = Paginator(data_list, 1)        
                try:
                    tesis = paginator.page(pageTesis)
                except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                    tesis = paginator.page(1)
                except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                    tesis = paginator.page(paginator.num_pages)         
            if  cve_tesis or materia or rubro or  precedente or sala_pleno or referencia or texto:
                
                # rubroFrase and textoPalabras
                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoPalabras":                                                           
                    texto_palabras=texto_sin_espacio.split(' ')                                        
                    python_indices = []
                    
                    for programming_language in range(len(texto_palabras)):
                        ls=texto_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or  ls == "De" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="El" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls == "LAS" or ls == "de" or ls == "del" or ls == "a" or ls == "e" or ls == "y" or ls == "o" or ls == "los" or ls == "en" or ls == "que" or ls == "al" or ls == "no" or ls == "es" or ls == "lo" or ls == "la" or ls == "su" or ls == "el" or ls == "por" or ls == "i" or ls == "u" or ls == "sus" or ls == "como" or ls == "las" or ls=="":
                            python_indices.append(programming_language)
                    
                    for idx in sorted(python_indices, reverse = True):
                        del texto_palabras[idx]

                    longitud=len(texto_palabras)
                                        
                    for vacios in range(15):
                        texto_palabras.append("")

                    data_list = Tesis.objects.filter(texto__icontains=texto_palabras[0],rubro__icontains=rubro,
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[2,3]).filter(texto__icontains=texto_palabras[1]).filter(texto__icontains=texto_palabras[2]).filter(texto__icontains=texto_palabras[3]).filter(texto__icontains=texto_palabras[4]).filter(texto__icontains=texto_palabras[5]).filter(texto__icontains=texto_palabras[6]).filter(texto__icontains=texto_palabras[7]).filter(texto__icontains=texto_palabras[8]).filter(texto__icontains=texto_palabras[9]).filter(texto__icontains=texto_palabras[10]).filter(texto__icontains=texto_palabras[11]).filter(texto__icontains=texto_palabras[12]).filter(texto__icontains=texto_palabras[13]).filter(texto__icontains=texto_palabras[14]).order_by('-id')
                                                                                                    
                    if longitud >= 16 or not longitud:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                                            
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                # rubroPalabras and textoFrase
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoFrase":                    
                    rubro_palabras=rubro_sin_espacio.split(' ')                                        
                    python_indices = []

                    for programming_language in range(len(rubro_palabras)):                        
                        ls=rubro_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls=="":
                            python_indices.append(programming_language)
                    
                    for idx in sorted(python_indices, reverse = True):
                        del rubro_palabras[idx]

                    longitud=len(rubro_palabras)                 
                    
                    for vacios in range(15):
                        rubro_palabras.append("")

                    data_list = Tesis.objects.filter(rubro__icontains=rubro_palabras[0],texto__icontains=texto,
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[2,3]).filter(rubro__icontains=rubro_palabras[1]).filter(rubro__icontains=rubro_palabras[2]).filter(rubro__icontains=rubro_palabras[3]).filter(rubro__icontains=rubro_palabras[4]).filter(rubro__icontains=rubro_palabras[5]).filter(rubro__icontains=rubro_palabras[6]).filter(rubro__icontains=rubro_palabras[7]).filter(rubro__icontains=rubro_palabras[8]).filter(rubro__icontains=rubro_palabras[9]).filter(rubro__icontains=rubro_palabras[10]).filter(rubro__icontains=rubro_palabras[11]).filter(rubro__icontains=rubro_palabras[12]).filter(rubro__icontains=rubro_palabras[13]).filter(rubro__icontains=rubro_palabras[14]).order_by('-id')
                    
                    if longitud >= 16 or not longitud:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                        
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                    
                # rubroPalabras and textoPalabras
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoPalabras":                    
                    rubro_palabras=rubro_sin_espacio.split(' ')          
                    texto_palabras=texto_sin_espacio.split(' ')   

                    python_indices_texto = []           
                    python_indices_rubro = []           

                    #texto_palabras
                    for programming_language in range(len(texto_palabras)):
                        ls=texto_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or  ls == "De" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="El" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls == "LAS" or ls == "de" or ls == "del" or ls == "a" or ls == "e" or ls == "y" or ls == "o" or ls == "los" or ls == "en" or ls == "que" or ls == "al" or ls == "no" or ls == "es" or ls == "lo" or ls == "la" or ls == "su" or ls == "el" or ls == "por" or ls == "i" or ls == "u" or ls == "sus" or ls == "como" or ls == "las" or ls=="":
                            python_indices_texto.append(programming_language)
                    
                    for idx in sorted(python_indices_texto, reverse = True):
                        del texto_palabras[idx]

                    longitud_texto=len(texto_palabras)
                                        
                    for vacios in range(15):
                        texto_palabras.append("")    

                    #rubro_palabras
                    for programming_language in range(len(rubro_palabras)):
                        ls=rubro_palabras[programming_language]
                        if ls == "DE" or  ls == "DEL" or ls == "A" or ls == "E" or ls == "Y" or ls == "LOS" or ls == "EN" or ls == "QUE" or  ls == "AL" or ls == "NO" or ls == "ES" or ls == "LO"  or ls == "O"  or ls == "LA" or ls == "SU" or ls=="EL" or ls=="POR" or ls=="I" or ls=="U" or ls=="SUS" or ls=="COMO" or ls=="":
                            python_indices_rubro.append(programming_language)
                    
                    for idx in sorted(python_indices_rubro, reverse = True):
                        del rubro_palabras[idx]

                    longitud_rubro=len(rubro_palabras)                 
                    
                    for vacios in range(15):
                        rubro_palabras.append("")
                    
                    data_list = Tesis.objects.filter(texto__icontains=texto_palabras[0],rubro__icontains=rubro_palabras[0],
                    materia__icontains=materia,cve_tesis__icontains=cve_tesis,cve_epoca__in=epoca,
                    precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,
                    referencia__icontains=referencia,status__in=[1,2,3,4,5]).filter(texto__icontains=texto_palabras[1]).filter(texto__icontains=texto_palabras[2]).filter(texto__icontains=texto_palabras[3]).filter(texto__icontains=texto_palabras[4]).filter(texto__icontains=texto_palabras[5]).filter(texto__icontains=texto_palabras[6]).filter(texto__icontains=texto_palabras[7]).filter(texto__icontains=texto_palabras[8]).filter(texto__icontains=texto_palabras[9]).filter(texto__icontains=texto_palabras[10]).filter(texto__icontains=texto_palabras[11]).filter(texto__icontains=texto_palabras[12]).filter(texto__icontains=texto_palabras[13]).filter(texto__icontains=texto_palabras[14]).filter(rubro__icontains=rubro_palabras[1]).filter(rubro__icontains=rubro_palabras[2]).filter(rubro__icontains=rubro_palabras[3]).filter(rubro__icontains=rubro_palabras[4]).filter(rubro__icontains=rubro_palabras[5]).filter(rubro__icontains=rubro_palabras[6]).filter(rubro__icontains=rubro_palabras[7]).filter(rubro__icontains=rubro_palabras[8]).filter(rubro__icontains=rubro_palabras[9]).filter(rubro__icontains=rubro_palabras[10]).filter(rubro__icontains=rubro_palabras[11]).filter(rubro__icontains=rubro_palabras[12]).filter(rubro__icontains=rubro_palabras[13]).filter(rubro__icontains=rubro_palabras[14]).order_by('-id')

                    if longitud_texto >= 16 or not longitud_texto:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                    
                    if longitud_rubro >= 16 or not longitud_rubro:                                                                                                  
                        return render(request, 'stj/busquedaTesis.html')
                                        
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)

                # rubroFrase and textoFrase
                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoFrase":                    
                    data_list = Tesis.objects.filter(rubro__icontains=rubro,texto__icontains=texto,materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,precedente__icontains=precedente,sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages) 
                
            return render(request, 'stj/detalleTesis.html',{"texto":texto,"tesis":tesis,"epoca":epoca,"materia":materia,"cve_tesis":cve_tesis,"rubro":rubro,"precedente":precedente,"referencia":referencia,"sala_pleno":sala_pleno,"jurisprudencias":jurisprudencias,'identificador':identificador,"rubroRadioEg":rubroRadioEg,"textoRadioEg":textoRadioEg})               
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

def pdf_view(request, cadena):    
    if cadena:
        return render(request, 'stj/iframe.html', {'cadena': cadena})
    else:
        return HttpResponseRedirect("/")
    
def tesis_pdf_detalle(request,pk):    
    if not pk:
        return redirect('/aps-tfja/sctj/')     
    post = Tesis.objects.filter(id=int(pk))
    html_string = render_to_string('stj/tesis-detalle-pdf.html',{'post':post})
    html = HTML(string=html_string)
    result = html.write_pdf()
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=detalle_tesis_tfja.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response






#Ambiente de pruebas
def stj_busqueda_ambiente(request):             
    materia_a = request.POST.get('materia_a',None)
    cve_tesis_a = request.POST.get('cve_tesis_a',None)
    rubro_a = request.POST.get('rubro_a',None)
    texto_a = request.POST.get('texto_a',None)    
    precedente_a = request.POST.get('precedente_a',None)
    referencia_a = request.POST.get('referencia_a',None)
    sala_pleno_a = request.POST.get('sala_pleno_a',None)   
    
    

    if materia_a == None and cve_tesis_a == None and rubro_a == None and texto_a == None and precedente_a == None and referencia_a == None and sala_pleno_a == None:                
        materia_a =""
        cve_tesis_a =""
        rubro_a =""
        texto_a =""        
        precedente_a =""
        referencia_a =""
        sala_pleno_a =""
        return render(request, 'stj/principalBusquedaAmbiente.html',{"materia_a":materia_a,"cve_tesis_a":cve_tesis_a,"rubro_a":rubro_a,"texto_a":texto_a,"precedente_a":precedente_a,"referencia_a":referencia_a,"sala_pleno_a":sala_pleno_a})
    if materia_a != None and cve_tesis_a != None and rubro_a != None and texto_a != None  and precedente_a != None and referencia_a != None and sala_pleno_a != None:        
        return render(request, 'stj/principalBusquedaAmbiente.html',{"materia_a":materia_a,"cve_tesis_a":cve_tesis_a,"rubro_a":rubro_a,"texto_a":texto_a,"precedente_a":precedente_a,"referencia_a":referencia_a,"sala_pleno_a":sala_pleno_a})
    if request.method == "POST":        
        return render(request, 'stj/busquedaTesisAmbiente.html')
    return render(request, 'stj/principalBusquedaAmbiente.html')


def stj_resul_ambiente(request):     
    if request.method == "GET":
        return redirect("/aps-tfja/sctj/sctj-busqueda-ambiente-pruebas/")
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
        jurisprudencias = request.POST.get('jurisprudencias')          
        identificador = request.POST.get('identificador') 

        rubroRadioEg = request.POST.get('rubroRadioEg') 
        textoRadioEg = request.POST.get('textoRadioEg') 
              
        if epoca and jurisprudencias == None:                    
            if not cve_tesis and not materia and not rubro and not precedente and not sala_pleno and not texto and not referencia:                
                data_list = TesisAmbientePruebas.objects.filter(status__in=[1,2,3,4,5],cve_epoca__in=epoca).order_by('-id')
                paginator = Paginator(data_list, 10)        
                try:
                    tesis = paginator.page(page)
                except PageNotAnInteger:                        
                    tesis = paginator.page(1)
                except EmptyPage:                        
                    tesis = paginator.page(paginator.num_pages)

             
            if  cve_tesis or materia or rubro or  precedente or sala_pleno or referencia or texto:

                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoPalabras":                    
                    texto_palabras = texto.replace(" ", "|" )    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__icontains=rubro,texto__iregex=r'('+texto_palabras+')+',precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoFrase":                                        
                    rubro_palabras = rubro.replace(" ", "|" )  
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__iregex=r'('+rubro_palabras+')+',texto__icontains=texto,precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)


                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoFrase":                    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__icontains=rubro,texto__icontains=texto,precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoPalabras":                    
                    rubro_palabras = rubro.replace(" ", "|" )  
                    texto_palabras = texto.replace(" ", "|" )    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__iregex=r'('+rubro_palabras+')+',texto__iregex=r'('+texto_palabras+')+',precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                                                                     
            return render(request, 'stj/busquedaTesisAmbiente.html',{"tesis":tesis,"epoca":epoca,"materia":materia,"cve_tesis":cve_tesis,"rubro":rubro,"precedente":precedente,"referencia":referencia,"sala_pleno":sala_pleno,"texto":texto,"jurisprudencias":jurisprudencias,"rubroRadioEg":rubroRadioEg,"textoRadioEg":textoRadioEg})
        
        if epoca and jurisprudencias=="NoJurisprudencia":                         
            if not cve_tesis and not materia and not rubro and not precedente and not sala_pleno and not texto and not referencia:                
                data_list = TesisAmbientePruebas.objects.filter(status__in=[1,2,3,4,5],cve_epoca__in=epoca).order_by('-id')
                paginator = Paginator(data_list, 10)        
                try:
                    tesis = paginator.page(page)
                except PageNotAnInteger:                        
                    tesis = paginator.page(1)
                except EmptyPage:                        
                    tesis = paginator.page(paginator.num_pages)

            if  cve_tesis or materia or rubro or  precedente or sala_pleno or referencia or texto:

                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoPalabras":                    
                    texto_palabras = texto.replace(" ", "|" )    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__icontains=rubro,texto__iregex=r'('+texto_palabras+')+',precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoFrase":                                        
                    rubro_palabras = rubro.replace(" ", "|" )  
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__iregex=r'('+rubro_palabras+')+',texto__icontains=texto,precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)


                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoFrase":                    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__icontains=rubro,texto__icontains=texto,precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoPalabras":                    
                    rubro_palabras = rubro.replace(" ", "|" )  
                    texto_palabras = texto.replace(" ", "|" )    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__iregex=r'('+rubro_palabras+')+',texto__iregex=r'('+texto_palabras+')+',precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
            return render(request, 'stj/busquedaTesisAmbiente.html',{"tesis":tesis,"epoca":epoca,"materia":materia,"cve_tesis":cve_tesis,"rubro":rubro,"precedente":precedente,"referencia":referencia,"sala_pleno":sala_pleno,"texto":texto,"jurisprudencias":jurisprudencias,"rubroRadioEg":rubroRadioEg,"textoRadioEg":textoRadioEg})                   

        #Jurisprudencias
        if jurisprudencias =="jurisprudencias" and epoca:                 
            if not cve_tesis and not materia and not rubro and not precedente and not sala_pleno and not texto and not referencia:
                data_list = TesisAmbientePruebas.objects.filter(status__in=[2],cve_epoca__in=epoca).order_by('-id')
                paginator = Paginator(data_list, 10)        
                try:
                    tesis = paginator.page(page)
                except PageNotAnInteger:                        
                    tesis = paginator.page(1)
                except EmptyPage:                        
                    tesis = paginator.page(paginator.num_pages)                                

            if  cve_tesis or materia or rubro or  precedente or sala_pleno or referencia or texto:

                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoPalabras":                                      
                    texto_palabras = texto.replace(" ", "|" )    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__icontains=rubro,texto__iregex=r'('+texto_palabras+')+',precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[2]).order_by('-id')                
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoFrase":                                        
                    rubro_palabras = rubro.replace(" ", "|" )  
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__iregex=r'('+rubro_palabras+')+',texto__icontains=texto,precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[2]).order_by('-id')                
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)


                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoFrase":                    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__icontains=rubro,texto__icontains=texto,precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[2]).order_by('-id')                
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoPalabras":                    
                    rubro_palabras = rubro.replace(" ", "|" )  
                    texto_palabras = texto.replace(" ", "|" )    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__iregex=r'('+rubro_palabras+')+',texto__iregex=r'('+texto_palabras+')+',precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[2]).order_by('-id')                
                    
                    paginator = Paginator(data_list, 10)        
                    try:
                        tesis = paginator.page(page)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)

            return render(request, 'stj/busquedaTesisAmbiente.html',{"tesis":tesis,"epoca":epoca,"materia":materia,"cve_tesis":cve_tesis,"rubro":rubro,"precedente":precedente,"referencia":referencia,"sala_pleno":sala_pleno,"texto":texto,"jurisprudencias":jurisprudencias,"rubroRadioEg":rubroRadioEg,"textoRadioEg":textoRadioEg})
    return render(request, 'stj/busquedaTesisAmbiente.html')


def detalle_tesis_ambiente(request):    
    if request.method == "GET":
        return redirect("/aps-tfja/sctj/") 
    if request.method == "POST":
        pageTesis = 0
        pagina_anterior = request.POST.get('input-pagina-anterior',None)          
        pagina_siguiente = request.POST.get('input-pagina-siguiente',None)
        pagina_ultimo = request.POST.get('input-pagina-ultimo',None)
        pagina_primero = request.POST.get('input-pagina-primero',None)
        pagina_actual = request.POST.get('input-pagina-actual',None)
        current = request.POST.get('current',None)        
        click = request.POST.get('cbp',None) 
        
        if click == "siguiente":                       
            pageTesis = pagina_siguiente
        if click == "anterior":            
            pageTesis = pagina_anterior 
        if click == "anterior":            
            pageTesis = pagina_anterior 
        if click == "ultimo":            
            pageTesis = pagina_ultimo 
        if click == "primero":            
            pageTesis = pagina_primero 
        if click == "current":            
            pageTesis = current
        
        epoca = request.POST.getlist('detalle_checkSelectEg')                                                  
        materia = request.POST.get('detalle_materia', None)        
        cve_tesis = request.POST.get('detalle_cve_tesis', None)
        rubro = request.POST.get('detalle_rubro', None)
        precedente = request.POST.get('detalle_precedente', None)
        referencia = request.POST.get('detalle_referencia', None)
        sala_pleno = request.POST.get('detalle_sala_pleno', None)
        texto = request.POST.get('detalle_texto', None)
        tid = request.POST.get('detalle_tesis_id', None)   
        jurisprudencias = request.POST.get('detalle_jurisprudencias')
        identificador = request.POST.get('detalle_identificador')
        rubroRadioEg = request.POST.get('rubroRadioEg') 
        textoRadioEg = request.POST.get('textoRadioEg') 
                      
        if epoca and jurisprudencias=="None":                                    
            if not cve_tesis and not materia and not rubro and not precedente and not sala_pleno and not texto and not referencia:
                data_list = TesisAmbientePruebas.objects.filter(status__in=[1,2,3,4,5],cve_epoca__in=epoca).order_by('-id')
                lista1 = list(data_list) 
                if identificador:
                    for l1 in lista1:                                                            
                        if l1.id == int(identificador):                         
                            posicion = lista1.index(l1)                           
                            pageTesis = posicion + 1   
                if identificador == None:
                    pageTesis=pageTesis

                paginator = Paginator(data_list, 1)        
                try:
                    tesis = paginator.page(pageTesis)
                except PageNotAnInteger:                        
                    tesis = paginator.page(1)
                except EmptyPage:                        
                    tesis = paginator.page(paginator.num_pages)                        
            
            if  cve_tesis or materia or rubro or  precedente or sala_pleno or referencia or texto:

                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoPalabras":                          
                    texto_palabras = texto.replace(" ", "|" )    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__icontains=rubro,texto__iregex=r'('+texto_palabras+')+',precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)                     
                
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoFrase":                                        
                    rubro_palabras = rubro.replace(" ", "|" )  
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__iregex=r'('+rubro_palabras+')+',texto__icontains=texto,precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)


                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoFrase":                    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__icontains=rubro,texto__icontains=texto,precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoPalabras":                    
                    rubro_palabras = rubro.replace(" ", "|" )  
                    texto_palabras = texto.replace(" ", "|" )    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__iregex=r'('+rubro_palabras+')+',texto__iregex=r'('+texto_palabras+')+',precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)

            return render(request, 'stj/detalleTesisAmbiente.html',{"texto":texto,"tesis":tesis,"epoca":epoca,"materia":materia,"cve_tesis":cve_tesis,"rubro":rubro,"precedente":precedente,"referencia":referencia,"sala_pleno":sala_pleno,"jurisprudencias":jurisprudencias,'identificador':identificador,"rubroRadioEg":rubroRadioEg,"textoRadioEg":textoRadioEg})

        if epoca and jurisprudencias=="NoJurisprudencia":            
            if not cve_tesis and not materia and not rubro and not precedente and not sala_pleno and not texto and not referencia:
                data_list = TesisAmbientePruebas.objects.filter(status__in=[1,2,3,4,5],cve_epoca__in=epoca).order_by('-id')
                lista1 = list(data_list) 
                if identificador:
                    for l1 in lista1:                                                            
                        if l1.id == int(identificador):                         
                            posicion = lista1.index(l1)                           
                            pageTesis = posicion + 1   
                if identificador == None:
                    pageTesis=pageTesis

                paginator = Paginator(data_list, 1)        
                try:
                    tesis = paginator.page(pageTesis)
                except PageNotAnInteger:                        
                    tesis = paginator.page(1)
                except EmptyPage:                        
                    tesis = paginator.page(paginator.num_pages)            

            if  cve_tesis or materia or rubro or  precedente or sala_pleno or referencia or texto:

                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoPalabras":                                   
                    texto_palabras = texto.replace(" ", "|" )    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__icontains=rubro,texto__iregex=r'('+texto_palabras+')+',precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)                     
                
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoFrase":                                        
                    rubro_palabras = rubro.replace(" ", "|" )  
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__iregex=r'('+rubro_palabras+')+',texto__icontains=texto,precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)


                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoFrase":                    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__icontains=rubro,texto__icontains=texto,precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoPalabras":                    
                    rubro_palabras = rubro.replace(" ", "|" )  
                    texto_palabras = texto.replace(" ", "|" )    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__iregex=r'('+rubro_palabras+')+',texto__iregex=r'('+texto_palabras+')+',precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[1,2,3,4,5]).order_by('-id')                
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages) 

            return render(request, 'stj/detalleTesisAmbiente.html',{"texto":texto,"tesis":tesis,"epoca":epoca,"materia":materia,"cve_tesis":cve_tesis,"rubro":rubro,"precedente":precedente,"referencia":referencia,"sala_pleno":sala_pleno,"jurisprudencias":jurisprudencias,'identificador':identificador,"rubroRadioEg":rubroRadioEg,"textoRadioEg":textoRadioEg})

        #Jurisprudencias
        if jurisprudencias =="jurisprudencias" and epoca:                             
            if not cve_tesis and not materia and not rubro and not precedente and not sala_pleno and not texto and not referencia:
                data_list = TesisAmbientePruebas.objects.filter(status__in=[2],cve_epoca__in=epoca).order_by('-id')
                lista1 = list(data_list) 
                if identificador:
                    for l1 in lista1:                                                            
                        if l1.id == int(identificador):                         
                            posicion = lista1.index(l1)                           
                            pageTesis = posicion + 1   
                if identificador == None:
                    pageTesis=pageTesis

                paginator = Paginator(data_list, 1)        
                try:
                    tesis = paginator.page(pageTesis)
                except PageNotAnInteger:                        
                    tesis = paginator.page(1)
                except EmptyPage:                        
                    tesis = paginator.page(paginator.num_pages)            

            if  cve_tesis or materia or rubro or  precedente or sala_pleno or referencia or texto:

                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoPalabras":                                     
                    texto_palabras = texto.replace(" ", "|" )    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__icontains=rubro,texto__iregex=r'('+texto_palabras+')+',precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[2]).order_by('-id')                
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)                     
                
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoFrase":                                        
                    rubro_palabras = rubro.replace(" ", "|" )  
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__iregex=r'('+rubro_palabras+')+',texto__icontains=texto,precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[2]).order_by('-id')                
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)


                if rubroRadioEg == "rubroFrase" and textoRadioEg == "textoFrase":                    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__icontains=rubro,texto__icontains=texto,precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[2]).order_by('-id')                
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)
                
                if rubroRadioEg == "rubroPalabras" and textoRadioEg == "textoPalabras":                    
                    rubro_palabras = rubro.replace(" ", "|" )  
                    texto_palabras = texto.replace(" ", "|" )    
                    data_list = TesisAmbientePruebas.objects.filter(materia__icontains=materia,cve_tesis__icontains=cve_tesis,
                    cve_epoca__in=epoca,rubro__iregex=r'('+rubro_palabras+')+',texto__iregex=r'('+texto_palabras+')+',precedente__icontains=precedente,
                    sala_pleno__icontains=sala_pleno,referencia__icontains=referencia,status__in=[2]).order_by('-id')                
                    
                    lista1 = list(data_list) 
                    if identificador:
                        for l1 in lista1:                                                            
                            if l1.id == int(identificador):                         
                                posicion = lista1.index(l1)                           
                                pageTesis = posicion + 1   
                    if identificador == None:
                        pageTesis=pageTesis

                    paginator = Paginator(data_list, 1)        
                    try:
                        tesis = paginator.page(pageTesis)
                    except PageNotAnInteger:                        
                        tesis = paginator.page(1)
                    except EmptyPage:                        
                        tesis = paginator.page(paginator.num_pages)  
                 
            return render(request, 'stj/detalleTesisAmbiente.html',{"texto":texto,"tesis":tesis,"epoca":epoca,"materia":materia,"cve_tesis":cve_tesis,"rubro":rubro,"precedente":precedente,"referencia":referencia,"sala_pleno":sala_pleno,"jurisprudencias":jurisprudencias,'identificador':identificador,"rubroRadioEg":rubroRadioEg,"textoRadioEg":textoRadioEg})               
    return render(request, 'stj/detalleTesisAmbiente.html',{"texto":texto})


def detalle_sentencia_ambiente(request):
    if request.method == "GET":
        return redirect("/aps-tfja/sctj/") 
    if request.method == "POST":
        sentencia_relacionada = request.POST.get('sentencia_relacionada') 
        sentencia = SentenciaAmbientePruebas.objects.filter(cve_unica=sentencia_relacionada).order_by('id')            
        return render(request, 'stj/detalleSentenciaAmbiente.html',{"sentencia":sentencia})         

    
def tesis_pdf_detalle_ambiente(request,pk):    
    if not pk:
        return redirect('/aps-tfja/sctj/')     
    post = TesisAmbientePruebas.objects.filter(id=int(pk))
    html_string = render_to_string('stj/tesis-detalle-pdfAmbiente.html',{'post':post})
    html = HTML(string=html_string)
    result = html.write_pdf()
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=detalle_tesis_tfja.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response

def registros(request): 
    publicadas = Tesis.objects.filter(status__in=[1,2]).count()
    suspendidas = Tesis.objects.filter(status=3).count()
    modificadas = Tesis.objects.filter(status=4).count()
    excepciones = Tesis.objects.filter(status=5).count()
    #Ambiente de Pruebas 
    publicadasAp = TesisAmbientePruebas.objects.filter(status__in=[1,2]).count()
    suspendidasAp = TesisAmbientePruebas.objects.filter(status=3).count()
    modificadasAp = TesisAmbientePruebas.objects.filter(status=4).count()
    excepcionesAp = TesisAmbientePruebas.objects.filter(status=5).count()
    return render(request, 'stj/registros.html',{"publicadas":publicadas,"suspendidas":suspendidas,"modificadas":modificadas,"excepciones":excepciones,"publicadasAp":publicadasAp,"suspendidasAp":suspendidasAp,"modificadasAp":modificadasAp,"excepcionesAp":excepcionesAp})
