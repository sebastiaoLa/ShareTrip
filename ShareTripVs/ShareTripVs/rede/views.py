# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http.response import HttpResponse,HttpResponseForbidden
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render,redirect
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import datetime


from django.core.urlresolvers import reverse_lazy
from rede import models,forms


# Create your views here.
class UserCreateView(generic.CreateView):

    model = models.User
    template_name = 'User/cadastro.html'
    success_url = reverse_lazy('rede:index')

    form_class = forms.UserForm

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['form']['first_name'].label = "Seu nome"
        return context



class HelpView(generic.TemplateView):

    template_name = 'help/help.html'

class HomeView(generic.TemplateView):

    template_name = 'User/home.html'

    def get(self, request, *args, **kwargs):

        if self.request.user.is_anonymous():
            return redirect(reverse_lazy('rede:index'))

        return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        
        amigos = self.request.user.amigos.all()

        context['viagens'] = models.Bilhete.objects.filter(passageiro = self.request.user).order_by("viagem__data")
        context['adicionantes'] = models.Solicitacao.objects.filter(para=self.request.user)
        context['amigos'] = amigos[:5]
        
        

        viagensOther = models.Bilhete.objects.all().order_by("viagem__data")
        context['viagensOther'] = []

        for i in viagensOther:
            if i.passageiro != self.request.user:
                if i.passageiro in amigos:
                    context['viagensOther'] += [(i,(self.request.user.pk,) not in i.viagem.viagem.all().values_list('passageiro_id'))]
        
        
        matchs = []

        for i in viagensOther:
            if i.passageiro != self.request.user and i.passageiro in amigos:
                print i, "(i.viagem,) in self.request.user.passageiro.all().values_list('viagem')", (i.viagem,) in self.request.user.passageiro.all().values_list('viagem')
                if (i.viagem.pk,) in self.request.user.passageiro.all().values_list('viagem'):
                    bilheteUser = self.request.user.passageiro.filter(viagem=i.viagem)[0]
                    if bilheteUser.poltrona%2==0 and bilheteUser.poltrona-1 == i.poltrona:
                        matchs += [(True,i.passageiro,'vai do seu lado :D',i.viagem)]
                    elif bilheteUser.poltrona%2!=0 and bilheteUser.poltrona+1 == i.poltrona:
                        matchs += [(True,i.passageiro,'vai do seu lado :D',i.viagem)]
                    else:
                        matchs += [(False,i.passageiro,"vai no mesmo onibus que você",i.viagem)]
    
    
        context['matchs'] = matchs

        print "#########"

        print context
        return context

    def post(self, request, *args, **kwargs):
        print request   
        print request.POST

        if 'aceitar' in self.request.POST.keys():
            if 'True' in self.request.POST['aceitar']:
                user = models.User.objects.filter(pk = self.request.POST['nome'])[0]
                #user = self.request.POST['nome']
                print user
                self.request.user.amigos.add(user.pk)
                user.amigos.add(self.request.user.pk)
                soli = models.Solicitacao.objects.filter(pk = self.request.POST['soli'])
                soli.delete()
                print "oe"
            else:
                soli = models.Solicitacao.objects.filter(pk = self.request.POST['soli'])
                soli.delete()

        if 'username' in self.request.POST.keys():
            if self.request.user == models.User.objects.get(username=request.POST['username']):
                return self.get(request,UsernameSucesso='False',*args,**kwargs)
            elif len(models.Solicitacao.objects.filter(de=self.request.user, para=models.User.objects.get(username=request.POST['username'])))>0:
                return self.get(request,UsernameSucesso='False',*args,**kwargs)
            else:
                models.Solicitacao(de=self.request.user, para=models.User.objects.get(username=self.request.POST['username'])).save()
                return self.get(request,UsernameSucesso='True',*args,**kwargs)
        
        return self.get(request,*args,**kwargs)

class DeleteBilheteView(generic.DeleteView):
    
    template_name = 'User/deleteBilhete.html'

    model = models.Bilhete

    success_url = reverse_lazy('rede:home')

    def get_context_data(self, **kwargs):
        
        context = super(DeleteBilheteView, self).get_context_data(**kwargs)

        print context

        return context

    def post(self, request, *args, **kwargs):
        algo = super(DeleteBilheteView, self).post(request, *args, **kwargs)
        
        if len(models.Viagem.objects.filter(pk=self.object.viagem)[0].viagem.all()) == 0:
            models.Viagem.objects.filter(pk=self.object.viagem)[0].delete()

        return algo


class DeleteAmigoView(generic.DetailView):
    
    template_name = 'User/deleteAmigo.html'

    model = models.User
      
    def post(self,request,*args,**kwargs):

        userAPk = request.POST['usera']
        usera = models.User.objects.get(pk=userAPk)
        userb = models.User.objects.get(pk=self.request.user.pk)

        usera.amigos.remove(userb)
        userb.amigos.remove(usera)
            
        return redirect(reverse_lazy('rede:home'))


class DetailProfileView(generic.DetailView):
    
    template_name = 'User/profile.html'

    model = models.User

    def get_context_data(self, **kwargs):

        context =  super(DetailProfileView, self).get_context_data(**kwargs)

        context['viagens'] = models.Bilhete.objects.filter(passageiro = self.object.pk)

        print context

        return context

class EditProfileView(generic.UpdateView):
    template_name = 'User/editProfile.html'

    model = models.User

    fields = ('foto','first_name','username','email','telefone')

    def get(self, request, *args, **kwargs):
        print "oe"
        if self.request.user.is_anonymous():
            raise PermissionDenied
        else:
            if self.request.user != models.User.objects.get(pk=kwargs['pk']):
                print self.request.user,models.User.objects.get(pk=kwargs['pk'])
                return redirect(reverse_lazy('rede:profile', args=(kwargs['pk'])))
                
        return super(EditProfileView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        print request.POST

        return super(EditProfileView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)

        return context

    def get_success_url(self):

        
        return reverse_lazy('rede:profile',args = (self.object.pk,))




class BilheteCreateView(generic.CreateView):

    model = models.Bilhete
    template_name = 'User/CadastrarViagem.html'
    success_url = reverse_lazy('rede:home')

    fields = ('poltrona','viagem',)

    def get_context_data(self, **kwargs):

        context = super(BilheteCreateView, self).get_context_data(**kwargs)

        print context

        context['cidades'] = models.Cidade.objects.all()
        context['tempo'] = timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())
        context['empresas'] = models.Empresa.objects.all()
        
        return context

    def post(self, request, *args, **kwargs):
        
        print request.POST

        dia = int(request.POST['data'][:2])
        mes = int(request.POST['data'][3:5])
        ano = int(request.POST['data'][6:10])
        hora = int(request.POST['hora'][:2])
        minutos = int(request.POST['hora'][3:5])

        datatempo = timezone.make_aware(datetime.datetime(ano,mes,dia,hora,minutos), timezone.get_current_timezone())
        
        viagem = models.Viagem.objects.filter(origem= request.POST['origem'],destino=request.POST['destino'] , data=datatempo, empresa = models.Empresa.objects.get(pk=request.POST['empresa']))

        if len(viagem)>0:
            models.Bilhete(poltrona=request.POST['poltrona'], passageiro= self.request.user, viagem=viagem[0]).save()
        else:
            viagem = models.Viagem(origem=models.Cidade.objects.get(pk=request.POST['origem']), destino=models.Cidade.objects.get(pk=request.POST['destino']), data=datatempo, empresa = models.Empresa.objects.get(pk=request.POST['empresa']))
            viagem.save()
            models.Bilhete(poltrona=request.POST['poltrona'], passageiro= self.request.user, viagem=viagem).save()

        
        return redirect(reverse_lazy('rede:home'),ViagemSucess='True')


class BilheteCreateViewPk(generic.DetailView):

    model = models.Viagem
    template_name = 'User/CadastrarViagem.html'

    def get_context_data(self, **kwargs):

        context = super(BilheteCreateViewPk, self).get_context_data(**kwargs)

        print context

        context['cidades'] = models.Cidade.objects.all()
        context['tempo'] = timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone())
        context['empresas'] = models.Empresa.objects.all()
        
        return context

    def post(self, request, *args, **kwargs):
        
        print request.POST

        dia = int(request.POST['data'][:2])
        mes = int(request.POST['data'][3:5])
        ano = int(request.POST['data'][6:10])
        hora = int(request.POST['hora'][:2])
        minutos = int(request.POST['hora'][3:5])

        datatempo = timezone.make_aware(datetime.datetime(ano,mes,dia,hora,minutos), timezone.get_current_timezone())
        
        viagem = models.Viagem.objects.filter(origem= request.POST['origem'],destino=request.POST['destino'] , data=datatempo, empresa = models.Empresa.objects.get(pk=request.POST['empresa']))

        if len(viagem)>0:
            models.Bilhete(poltrona=request.POST['poltrona'], passageiro= self.request.user, viagem=viagem[0]).save()
        else:
            viagem = models.Viagem(origem=models.Cidade.objects.get(pk=request.POST['origem']), destino=models.Cidade.objects.get(pk=request.POST['destino']), data=datatempo, empresa = models.Empresa.objects.get(pk=request.POST['empresa']))
            viagem.save()
            models.Bilhete(poltrona=request.POST['poltrona'], passageiro= self.request.user, viagem=viagem).save()

        
        return redirect(reverse_lazy('rede:home'),ViagemSucess='True')


class EditBilheteView(generic.DetailView):
    template_name = 'User/editarViagem.html'

    model = models.Bilhete

    def get(self, request, *args, **kwargs):

        if self.request.user.is_anonymous():
            raise PermissionDenied
        else:
            if self.request.user.pk != models.Bilhete.objects.get(pk=kwargs['pk']).passageiro.pk:
                raise PermissionDenied
                
        return super(EditBilheteView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EditBilheteView, self).get_context_data(**kwargs)

        context['cidades'] = models.Cidade.objects.all()
        context['empresas'] = models.Empresa.objects.all()

        return context


    def post(self, request, *args, **kwargs):
        
        objeto = models.Bilhete.objects.get(pk = request.POST['objeto'])

        dia = int(request.POST['data'][:2])
        mes = int(request.POST['data'][3:5])
        ano = int(request.POST['data'][6:10])
        hora = int(request.POST['hora'][:2])
        minutos = int(request.POST['hora'][3:5])

        datatempo = timezone.make_aware(datetime.datetime(ano,mes,dia,hora,minutos), timezone.get_current_timezone())
        
        viagem = models.Viagem.objects.filter(origem= request.POST['origem'],destino=request.POST['destino'] , data=datatempo, empresa = models.Empresa.objects.get(pk=request.POST['empresa']))
        
        objeto.viagem = viagem[0]
        objeto.poltrona = request.POST['poltrona']
        objeto.passageiro = self.request.user

        objeto.save()

        return redirect(reverse_lazy('rede:home'))

