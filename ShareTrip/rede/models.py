# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

# Create your models here.
class Usuario(models.Model):

    nome = models.CharField(
    'nome',
    max_length = 255
    )
    telefone = models.CharField(
    'telefone',
    max_length=255,
    )
    cpf = models.CharField(
    'cpf',
    max_length = 14,
    )

    senha = models.CharField(
    'Senha',
    max_length = 255
    )

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ["nome"]


class Onibus(models.Model):

    motorista = models.CharField(
    'Motorista',
    max_length = 255
    )
    modelo = models.CharField(
    'Modelo',
    max_length=255
    )


    class Meta:
        verbose_name = 'onibus'
        verbose_name_plural = 'onibus'
        ordering = ["motorista"]


class Empresa(models.Model):

    nome = models.CharField(
    'nome',
    max_length = 255
    )
    endereco = models.CharField(
    'Endereço',
    max_length = 255
    )

    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'
        ordering = ["nome"]

class Viagem(models.Model):

    origem = models.CharField(
    'origem',
    max_length = 255
    )
    destino = models.CharField(
    'destino',
    max_length = 255
    )
    horaS = models.CharField(
    'Hora de Saida',
    max_length = 255
    )
    horaC = models.CharField(
    'Hora de Chegada',
    max_length = 255
    )
    empresa = models.ForeignKey(
    'Empresa',
    on_delete=models.CASCADE,
    related_name = "empresa"
    )
    onibus = models.ForeignKey(
    'Onibus',
    on_delete=models.CASCADE,
    related_name = "Onibus"
    )
    data = models.DateTimeField(
        'Data',
        default=datetime.now()
    )

    class Meta:
        verbose_name = 'viagem'
        verbose_name_plural = 'viagens'
        ordering = ["data"]


class Bilhete (models.Model):

    poltrona = models.IntegerField(
    'poltrona',
    )

    passageiro = models.ForeignKey(
    "Usuario",
    on_delete=models.CASCADE,
    related_name = "passageiro"
    )

    Id = models.ForeignKey(
    "Viagem",
    on_delete = models.CASCADE,
    related_name = "viagem"
    )
    class Meta:
        verbose_name = 'bilhete'
        verbose_name_plural = 'bilhetes'
        ordering = ["passageiro"]
