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
        
        context['viagens'] = models.Bilhete.objects.filter(passageiro = self.request.user)
        context['adicionantes'] = models.Solicitacao.objects.filter(para=self.request.user)
        context['amigos'] = self.request.user.amigos.all()[:5]
        
        bilhetesAmigos = []

        for i in context['amigos']:
            query = models.Bilhete.object.filter(passageiro=i)
            for l in query:
                bilhetesAmigos += [l]

        


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

        if self.request.user.is_anonymous():
            raise PermissionDenied
        else:
            if self.request.user.pk != kwargs['pk']:
                return redirect(reverse_lazy('rede:profile', args=(kwargs['pk'])))
                
        return super(EditProfileView, self).get(request, *args, **kwargs)

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

        print context['form'].visible_fields()

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


class testView(generic.TemplateView):
    
    template_name='User/test.html'
