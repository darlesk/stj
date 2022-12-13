
import datetime
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django import forms

class Tesis(models.Model):    
    ESTADOS = ((1,'tesis'),(2,'jurisprudencia'))
    cve_unica = models.CharField(max_length=500,blank=True, null=True)
    no_reg = models.IntegerField(blank=True,null=True)
    materia = models.TextField(blank=True,null=True)
    cve_tesis = models.CharField(blank=True,null=True,max_length=500)
    cve_epoca = models.CharField(blank=True,null=True,max_length=500)
    rubro = models.TextField(blank=True,null=True)
    texto = models.TextField(blank=True,null=True)
    precedente = models.TextField(blank=True,null=True)
    referencia = models.TextField(blank=True,null=True)
    sala_pleno = models.CharField(blank=True,null=True,max_length=500)
    estado = models.IntegerField()
    acuerdo = models.CharField(max_length=500,blank=True, null=True)
    IUS = models.IntegerField(blank=True, null=True)
    IUS1 = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(choices=ESTADOS,default=1, blank=False)
        
    class Meta:
        verbose_name= 'Administrador Tesis'
        verbose_name_plural = 'Administrador Tesis'
        ordering = ["cve_tesis"]

    def _str_(self):
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

    def _str_(self):
        return self.texto