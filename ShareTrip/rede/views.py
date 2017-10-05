# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
