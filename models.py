from django.db import models

class Tesis(models.Model): 
    ESTADOS = ((1,'tesis'),(2,'jurisprudencia'),(3,'jurisprudencia-suspendida'),(4,'modificadas'),(5,'excepciones'))
    cve_unica = models.CharField(max_length=500,blank=True, null=True)
    no_reg = models.IntegerField()
    materia = models.TextField(blank=True,null=True)
    cve_tesis = models.CharField(max_length=500)
    cve_epoca = models.CharField(max_length=500)
    rubro = models.TextField()
    texto = models.TextField()
    precedente = models.TextField()
    referencia = models.TextField()
    sala_pleno = models.CharField(max_length=500)
    estado = models.IntegerField(blank=True,default=1)
    acuerdo = models.CharField(max_length=500,blank=True, null=True)
    #acuerdoDoc = models.FileField(upload_to="cesmdfa_portal/difusion/",null=True, blank=True)    
    IUS = models.IntegerField(blank=True, null=True)
    IUS1 = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(choices=ESTADOS,default=1, blank=False)
    nota = models.TextField(max_length=500,blank=True)
      
    class Meta:
        verbose_name= 'Administrador Tesis'
        verbose_name_plural = 'Administrador Tesis'
        ordering = ["cve_tesis"]

    def str(self):
        return self.cve_tesis


class Sentencia(models.Model):
    cve_unica = models.CharField(max_length=500)
    no_reg = models.IntegerField()
    clave = models.CharField(max_length=500,blank=True, null=True)
    cve_epoca = models.CharField(max_length=500)
    rubro = models.TextField(blank=True, null=True)
    texto = models.TextField(blank=True, null=True)
    referencia = models.TextField(max_length=500,blank=True, null=True)
    sala_pleno = models.CharField(max_length=500,blank=True, null=True)    
    IDSCJN = models.IntegerField(blank=True, null=True)
    IDSCJN1 = models.IntegerField(blank=True, null=True)
        
    class Meta:
        verbose_name= 'Administrador Sentencias'
        verbose_name_plural = 'Administrador Sentencias'
        ordering = ["texto"]

    def str(self):
        return self.texto
