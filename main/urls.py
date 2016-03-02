from django.conf.urls import url, include
from django.conf import settings
from . import views, lecture
from .models import *
from django.conf.urls import url
from django.contrib.auth.views import login,logout
from django.views.generic import ListView

urlpatterns = [
    url(r'^$', views.home, name='home'),
    # login / logout urls
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^auteurs/$', views.auteur_list, name='auteur_list'),

    url(r'^auteur/create/$', views.auteur_create, name='auteur-create'),
    url(r'^/auteur/([0-9]+)/$', views.auteur_form, name='auteur'),
    url(r'^auteur/update/$', views.auteur_update, name='auteur-update'),
    url(r'^auteur/delete/([0-9]+)/$', views.auteur_delete, name='auteur-delete'),

    url(r'^livres/$', views.livre_list, name='livre_list'),
    url(r'^livre/create/$', views.livre_create, name='livre-create'),
    url(r'^/livre/([0-9]+)/$', views.livre_form, name='livre'),
    url(r'^/livre/search/$', views.livre_search, name='livre-search'),
    url(r'^meslivres/$', views.livre_my_list, name='meslivres'),

    url(r'^livre/update/$', views.livre_update, name='livre-update'),
    url(r'^livre/delete/([0-9]+)/$', views.livre_delete, name='livre-delete'),
    url(r'^livre/deletea/([0-9]+)/$', views.delete_auteur_livre, name='delete-auteur-livre'),
    url(r'^livre/add/auteurlivre/([0-9]+)/$', views.add_auteur_to_livre, name='add-auteur-to-livre'),
    url(r'^livre/save/auteurlivre/$', views.save_auteur_livre, name='auteur-livre-save'),
    url(r'^livre/add/proprietaire/([0-9]+)/$', views.add_proprietaire_to_livre, name='proprietaire-add-to-livre'),
    url(r'^livre/save/proprietaire/$', views.save_proprietaire, name='proprietaire-save'),
    url(r'^livre/delete/proprietaire/([0-9]+)/$', views.delete_proprietaire, name='proprietaire-remove-from-livre'),
    url(r'^livre/emprunt/([0-9]+)/$', views.proprietaire_emprunt_livre, name='proprietaire-emprunt-livre'),
    url(r'^livre/retour/([0-9]+)/$', views.proprietaire_retour_livre, name='proprietaire-retour-livre'),
    url(r'^livre/retour/lu/([0-9]+)/$', views.proprietaire_retour_lu_livre, name='proprietaire-retour-lu-livre'),

    url(r'^/livre/([0-9]+)/update/$', views.livre_form),

    url(r'^lectures/$', lecture.lecture_list, name='lecture_list'),
    # url(r'^livre/update/$', lecture.lecture_update, name='lecture-update'),
    # url(r'^lecture/create/$', lecture.lecture_create, name='lecture-create'),
    # url(r'^/lecture/([0-9]+)/$', lecture.lecture_form, name='lecture'),
    url(r'^/lecture/search/$', lecture.lecture_search, name='lecture-search'),
    # url(r'^meslectures/$', lecture.lecture_my_list, name='meslectures'),
    url(r'^lecture/delete/([0-9]+)/$', lecture.lecture_delete, name='lecture-delete'),












]
