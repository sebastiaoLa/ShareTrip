#coding:utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.db.models import Q

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal

from django.utils.timezone import now

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.pk, filename)

# Create your models here.
class User(AbstractUser):

    telefone = models.CharField('telefone',
    max_length=255,
    null = True,
    blank = True
    )

    
    foto = models.FileField('Foto',upload_to=user_directory_path, null=True, blank = True)

    friends = models.ManyToManyField('rede.User', 
                                     related_name = 'amigos',
                                     )
    user_fb_id = models.CharField('UserId',
                                 max_length=255,
                                 null=True,unique = True
                                 )

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        return unicode("%s %s" % (self.first_name, self.last_name))

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        ordering = ["first_name","last_name"]

class Solicitacao(models.Model):

    de = models.ForeignKey(User,
                           related_name="Solicitante",
                           on_delete = models.CASCADE,)

    para = models.ForeignKey(User,
                             related_name = "Solicitado",
                             on_delete = models.CASCADE)

    data = models.DateField('Data',default=now)

    def __str__(self):
        return "%s %s" % (self.de, self.para)

    def __unicode__(self):
        return unicode("%s %s" % (self.de, self.para))

    class Meta:
        verbose_name = 'solicitacao'
        verbose_name_plural = 'solicitacoes'
        ordering = ["data",]


class Empresa(models.Model):

    nome = models.CharField('Nome',
    max_length=255)

    def __str__(self):
        return "%s" % (self.nome)

    def __unicode__(self):
        return unicode("%s" % (self.nome))

    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'
        ordering = ["nome"]

class Viagem(models.Model):

    origem = models.ForeignKey("Cidade",
                               on_delete=models.CASCADE,
                               related_name="origem"
        )

    destino = models.ForeignKey("Cidade",
                                on_delete=models.CASCADE,
                                related_name="destino")

    empresa = models.ForeignKey('Empresa',
        on_delete=models.CASCADE,
        related_name = "Empresa"
    )


    data = models.DateTimeField('Data',
        default=now)

    def __str__(self):
        return "%s, %s, %s" % (self.origem, self.destino, self.data)

    def __unicode__(self):
        return unicode("%s, %s, %s" % (self.origem, self.destino, self.data))

    class Meta:
        verbose_name = 'viagem'
        verbose_name_plural = 'viagens'
        ordering = ["data"]


class Bilhete(models.Model):

    poltrona = models.IntegerField('poltrona',validators=[MinValueValidator(Decimal('0.01'))])

    passageiro = models.ForeignKey("User",
    on_delete=models.CASCADE,
    related_name = "passageiro")

    viagem = models.ForeignKey("Viagem",
    on_delete = models.CASCADE,
    related_name = "viagem")

    def __str__(self):
        return "%s %s %s" % (self.passageiro,self.poltrona,self.viagem.__str__())

    def __unicode__(self):
        return unicode("%s %s %s" % (self.passageiro,self.poltrona,self.viagem.__str__()))

    class Meta:
        verbose_name = 'bilhete'
        verbose_name_plural = 'bilhetes'
        ordering = ["passageiro"]

class Cidade(models.Model):
    nome = models.CharField('nome',
                            max_length=255)

    estado =models.CharField('Estado',
                            max_length=255)
    def __str__(self):
        return "%s (%s)" % (self.nome,self.estado)

    def __unicode__(self):
        return unicode("%s (%s)" % (self.nome,self.estado))

    class Meta:
        verbose_name = 'cidade'
        verbose_name_plural = 'cidades'
        ordering = ["nome"]
