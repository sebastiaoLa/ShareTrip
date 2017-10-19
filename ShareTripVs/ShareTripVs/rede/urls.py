# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth import views as auth_views

from rede import views

urlpatterns = [url(r'^$', auth_views.LoginView.as_view(template_name="User/index.html"), name='index'),
    url(r'^help/$', views.HelpView.as_view(), name='help'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(r'^cadastro/$', views.UserCreateView.as_view(), name='cadastro'),
    url(r'^loginfb/$', views.my_view, name='fb-login'),
    url(r'^criarViagem/$', views.BilheteCreateView.as_view(), name='criarViagem'),
    url(r'^criarViagem/(?P<pk>[0-9]+)/$', views.BilheteCreateViewPk.as_view(), name='criaViagemPk'),
    url(r'^editarViagem/(?P<pk>[0-9]+)/$', views.EditBilheteView.as_view(), name='editViagem'),
    url(r'^deleteBilhete/(?P<pk>[0-9]+)/$', views.DeleteBilheteView.as_view(), name='apagaBilhete'),
    url(r'^deleteAmizade/(?P<pk>[0-9]+)/$', views.DeleteAmigoView.as_view(), name='apagaAmigo'),
    url(r'^deleteProfile/(?P<pk>[0-9]+)/$', views.DeleteProfileView.as_view(), name='deletaProfile'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.DetailProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<pk>[0-9]+)/editar/$', views.EditProfileView.as_view(), name='editProfile'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''url(r'^logout/$', views.CustomLogoutView.as_view(), name='logout'),

url(r'^matches/$', views.MatchesView.as_view(), name='match-list'),

url(r'^teams/$', views.TeamsView.as_view(), name='team-list'),
url(r'^teams/(?P<pk>[0-9]+)/$', views.TeamDetailsView.as_view(), name='team-details'),
# url(r'^teams/(?P<name>[\w]+)/$', views.TeamDetails2View.as_view(), name='team-details-2'),
url(r'^teams/create/$', views.TeamCreateView.as_view(), name='team-create'),
url(r'^teams/(?P<pk>[0-9]+)/edit/$', views.TeamUpdateView.as_view(), name='team-edit'),'''
