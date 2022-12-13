from os import stat
from django.shortcuts import render
from .models import  *
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse,HttpResponse, FileResponse,  HttpResponseRedirect

def inicio(request):        
    if request.method == "POST":   
        epoca = request.POST.getlist('checkSelectEg')
        materia = request.POST.get('materia')        
        cve_tesis = request.POST.get('cve_tesis')
        rubro = request.POST.get('rubro')
        precedente = request.POST.get('precedente')
        referencia = request.POST.get('referencia')
        sala_pleno = request.POST.get('sala_pleno')
        texto = request.POST.get('texto')        
        jurisprudencias = request.POST.get('jurisprudencias')
                    
        if epoca and jurisprudencias==None:     
            print("entra epoca")       
            print(materia)       
            print(cve_tesis)       
            if not cve_tesis and not materia and not rubro and not precedente and not precedente and not sala_pleno and not texto and not referencia:
                tesis = Tesis.objects.filter(status__in=[1,2],cve_epoca__in=epoca).order_by('-id')
                print(tesis.query.__str__())
            else:
                tesis = Tesis.objects.filter(materia__icontains=materia, cve_epoca__in=epoca, 
                cve_tesis__icontains=cve_tesis, rubro__icontains=rubro, precedente__icontains=precedente, 
                referencia__icontains=referencia, sala_pleno__icontains=sala_pleno, texto__icontains=texto,status__in=[1,2]).order_by('-id')                            
                print(tesis.query.__str__())
                
                #tesis = Tesis.objects.filter(Q(materia__icontains=materia)|
                #Q(cve_tesis__icontains=cve_tesis) | Q(rubro__icontains=rubro)  | Q(precedente__icontains=precedente) |
                #Q(referencia__icontains=referencia) | Q(sala_pleno__icontains=sala_pleno) | Q(texto__icontains=texto),
                #cve_epoca__in=epoca,status__in=[1,2]).order_by('-id')                            
                #print(tesis.query.__str__())
            return render(request, 'stj/busquedaTesis.html',{"tesis":tesis})
                        
        identificador = request.POST.get('identificador')
        sentencia_relacionada = request.POST.get('sentencia_relacionada')            

        # Identificador de Tesis Precedente
        if identificador:                  
            texto = Tesis.objects.filter(id=identificador).order_by('id')
            return render(request, 'stj/busquedaTesisTexto.html',{"texto":texto})  

        # Sentencia Relacionada Precedente
        if sentencia_relacionada:            
            sentencia = Sentencia.objects.filter(cve_unica=sentencia_relacionada).order_by('id')            
            return render(request, 'stj/detalleSentencia.html',{"sentencia":sentencia}) 


        #Jurisprudencias
        if jurisprudencias =="jurisprudencias" and epoca:
            if not cve_tesis and not materia and not rubro and not precedente and not precedente and not sala_pleno and not texto and not referencia:
                jurisprudencias = Tesis.objects.filter(status=2,cve_epoca__in=epoca).order_by('-id')            
            else:
                jurisprudencias = Tesis.objects.filter(materia__icontains=materia, cve_epoca__in=epoca, 
                cve_tesis__icontains=cve_tesis, rubro__icontains=rubro, precedente__icontains=precedente, 
                referencia__icontains=referencia, sala_pleno__icontains=sala_pleno, texto__icontains=texto,status=2).order_by('-id')
            #Listado de Tesis       
            return render(request, 'stj/busquedaJurisprudencia.html',{"jurisprudencias":jurisprudencias})

        identificadorJuri = request.POST.get('identificadorJuri')
        sentencia_relacionada_juris = request.POST.get('sentencia_relacionada_juris')        

        # Identificador Jurisprudencias
        if identificadorJuri:
            texto = Tesis.objects.filter(id=identificadorJuri).order_by('id')
            return render(request, 'stj/busquedaTesisTextoJuris.html',{"texto":texto})

        # Sentencia Jurisprudencias
        if sentencia_relacionada_juris:            
            sentencia = Sentencia.objects.filter(cve_unica=sentencia_relacionada_juris).order_by('id')             
            return render(request, 'stj/detalleSentenciaJurisprudencia.html',{"sentencia":sentencia})     
    return render(request, 'stj/principal.html')

def pdf_view(request, cadena):    
    if cadena:
        return render(request, 'stj/iframe.html', {'cadena': cadena})
    else:
        return HttpResponseRedirect("/")