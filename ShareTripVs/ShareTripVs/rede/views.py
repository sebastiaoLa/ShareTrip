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
        

        print self.request.method
        if self.request.method == "POST":
            if 'aceitar' in self.request.POST.keys():
                if self.request.POST['aceitar']:
                    user = models.User.objects.filter(pk = self.request.POST['nome'])
                    self.request.user.amigos.add(user)
                    user.amigos.add(self.request.user)
                else:
                    soli = models.Solicitacao.objects.filter(pk = self.request.POST['nome'])
                    soli.delete()

        print context
        return context

    def post(self, request, *args, **kwargs):
        print request   
        print dir(request)
        try:
            aceitar = self.request.POST['aceitar']
        except:
            pass

        print request.user
        return self.get(request,*args,**kwargs)