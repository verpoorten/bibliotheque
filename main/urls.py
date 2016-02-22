from django.conf.urls import url, include
from django.conf import settings
from . import views
from .models import *
from django.conf.urls import url
from django.contrib.auth.views import login,logout
from django.views.generic import ListView

urlpatterns = [
    url(r'^$', views.home, name='home'),
    # login / logout urls
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^auteur/$', views.auteur_list, name='auteur_list'),

    url(r'^auteur/create/$', views.auteur_create, name='auteur-create'),
    url(r'^/auteur/([0-9]+)/$', views.auteur_form, name='auteur'),
    url(r'^auteur/update/$', views.auteur_update, name='auteur-update'),
    url(r'^auteur/delete/([0-9]+)/$', views.auteur_delete, name='auteur-delete'),

]
