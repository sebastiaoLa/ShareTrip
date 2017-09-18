# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from rede import models
from forms import UsuarioForm

# Register your models here.

#===============================================================================
# Usuario
#===============================================================================
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf')
    form = UsuarioForm

admin.site.register(models.Usuario, UsuarioAdmin)

#===============================================================================
# Onibus
#===============================================================================
class OnibusAdmin(admin.ModelAdmin):
    list_display = ('motorista', 'modelo')

admin.site.register(models.Onibus, OnibusAdmin)

#===============================================================================
# Empresa
#===============================================================================
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

admin.site.register(models.Empresa, EmpresaAdmin)

#===============================================================================
# Viagem
#===============================================================================
class ViagemAdmin(admin.ModelAdmin):
    list_display = ('origem', 'destino', 'data')

admin.site.register(models.Viagem, ViagemAdmin)

#===============================================================================
# Bilhete
#===============================================================================
class BilheteAdmin(admin.ModelAdmin):
    list_display = ('passageiro', 'Id')

admin.site.register(models.Bilhete, BilheteAdmin)
