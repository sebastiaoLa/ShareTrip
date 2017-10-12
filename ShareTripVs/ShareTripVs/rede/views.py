from __future__ import unicode_literals
from django.http.response import HttpResponse,HttpResponseForbidden
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render,redirect
from django.views import generic
from django.core.exceptions import PermissionDenied


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

        return context
