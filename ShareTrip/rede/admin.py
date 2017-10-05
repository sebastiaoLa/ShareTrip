# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as auth_UserAdmin

from rede import models
from forms import UserAdminCreationForm,UserAdminChangeForm
from django.utils.translation import ugettext, ugettext_lazy as _

# Register your models here.

#===============================================================================
# Usuario
#===============================================================================

#admin.site.register(models.User, UserAdmin)

class UserAdmin(auth_UserAdmin):
    list_display = ('first_name', 'cpf')
    add_form = UserAdminCreationForm
    form = UserAdminChangeForm
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(UserAdmin,self).get_fieldsets(request,obj)
        if obj:
            fieldsets = fieldsets + ((_('Outras Informacoes'), {'fields': ('telefone', 'cpf')}),)
        return fieldsets

admin.site.register(models.User, UserAdmin)

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
    list_display = ('passageiro', 'viagem')

admin.site.register(models.Bilhete, BilheteAdmin)
