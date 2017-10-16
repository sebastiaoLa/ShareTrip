import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShareTripVs.settings")
django.setup()

from rede.models import *
import datetime

from django.utils import timezone

def maisUmDia(data):
    dia = data.day+1
    mes = data.month
    ano = data.year

    try:
        return datetime.datetime(ano,mes,dia)
    except ValueError as ex:
        dia = 1
        mes = data.month+1
        ano = data.year
        try:
            return datetime.datetime(ano,mes,dia)
        except ValueError as ex:
            dia = 1
            mes = 1
            ano = data.year+1
            return datetime.datetime(ano,mes,dia)


viagens = Viagem.objects.all()

data = timezone.make_aware(maisUmDia(datetime.datetime.now()), timezone.get_current_timezone())

for viagem in viagens:
    if viagem.data<data:
        viagem.delete()


