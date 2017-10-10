from __future__ import unicode_literals
from django.http.response import HttpResponse

from django.shortcuts import render
from django.views import generic

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

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        
        context['viagens'] = models.Bilhete.objects.filter(passageiro = self.request.user)
        context['adicionantes'] = models.Solicitacao.objects.filter(para=self.request.user)
        context['amigos'] = self.request.user.amigos.all()[:5]

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

        return self.get(request,*args,**kwargs)

class DeleteBilheteView(generic.DeleteView):
    
    template_name = 'User/deleteBilhete.html'

    model = models.Bilhete

    success_url = reverse_lazy('rede:home')

    def get_context_data(self, **kwargs):
        
        context = super(DeleteBilheteView, self).get_context_data(**kwargs)

        print context

        return context


class DeleteAmigoView(generic.DeleteView):
    
    template_name = 'User/deleteAmigo.html'

    model = models.Bilhete

    success_url = reverse_lazy('rede:home')

    def get_context_data(self, **kwargs):
        
        context = super(DeleteBilheteView, self).get_context_data(**kwargs)

        print context

        return context

class DetailProfileView(generic.DetailView):
    
    template_name = 'User/profile.html'

    model = models.Bilhete

    success_url = reverse_lazy('rede:home')

    def get_context_data(self, **kwargs):
        
        context = super(DeleteBilheteView, self).get_context_data(**kwargs)

        print context

        return context
