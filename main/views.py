from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import *
from django.core.urlresolvers import reverse
import os
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import datetime
from django.db import models

def home(request):
    return render(request, 'home.html',
                    {})

def auteur_list(request):
        return render(request, 'auteur_list.html',
                        {'auteurs': Auteur.find_all()})


def auteur_create(request):
    auteur = Auteur()
    return render(request, "auteur_form.html",
                  {'auteur':         auteur})

def auteur_form(request, auteur_id):
    auteur = Auteur.find_auteur(auteur_id)

    return render(request, "auteur_form.html",
                  {'auteur':     auteur})

def auteur_update(request):

    auteur = Auteur()

    if ('add' == request.POST['action'] or 'modify' == request.POST['action']):
        if request.POST['id'] and not request.POST['id'] == 'None':
            auteur = get_object_or_404(Auteur, pk=request.POST['id'])
        else:
            auteur = Auteur()
        auteur.nom = request.POST['nom']
        auteur.prenom = request.POST['prenom']

        auteur.save()

    return render(request, 'auteur_list.html',
                    {'auteurs': Auteur.find_all()})

def auteur_delete(request, id):
    auteur = get_object_or_404(Auteur, pk=id)
    auteur.delete()
    return render(request, 'auteur_list.html',
                    {'auteurs': Auteur.find_all()})




def livre_list(request):
        return render(request, 'livre_list.html',
                        {'livres': Livre.find_all()})


def livre_create(request):
    livre = Livre()
    return render(request, "livre_form.html",
                  {'livre':         livre})

def livre_form(request, livre_id):
    livre = Livre.find_livre(livre_id)

    return render(request, "livre_form.html",
                  {'livre':     livre})

def livre_update(request):
    livre = Livre()

    if ('add' == request.POST['action'] or 'modify' == request.POST['action']):
        if request.POST['id'] and not request.POST['id'] == 'None':
            livre = get_object_or_404(Livre, pk=request.POST['id'])
        else:
            livre = Livre()
        livre.titre = request.POST['titre']
        livre.langue = request.POST['langue']

        livre.save()

    return render(request, 'livre_list.html',
                    {'livres': Livre.find_all()})

def livre_delete(request, id):
    livre = get_object_or_404(Livre, pk=id)
    livre.delete()
    return render(request, 'livre_list.html',
                    {'livres': Livre.find_all()})


def delete_auteur_livre(request, auteur_livre_id):
    auteur_livre = AuteurLivre.find_auteur_livre(auteur_livre_id)
    livre = auteur_livre.livre
    auteur_livre.delete()
    return render(request, "livre_form.html",
                  {'livre': livre})

def add_auteur_livre(request, livre_id):
    livre = get_object_or_404(Livre, pk=livre_id)
    auteur = Auteur()
    auteur.livre= livre

    return render(request, "auteur_form.html",
                  {'auteur':     auteur})

def add_auteur_to_livre(request, livre_id):
    livre = get_object_or_404(Livre, pk=livre_id)
    auteur_livre = AuteurLivre()
    auteur_livre.livre= livre

    return render(request, "auteur_livre_form.html",
                  {'auteur_livre': auteur_livre,
                   'auteurs':      Auteur.find_all(),
                   'livre':        livre})

def save_auteur_livre(request):
    auteur_id=request.POST['auteur_id']
    livre_id=request.POST['livre_id']
    auteur_livre = AuteurLivre()
    auteur = get_object_or_404(Auteur, pk=auteur_id)
    livre = get_object_or_404(Livre, pk=livre_id)
    auteur_livre.livre = livre
    auteur_livre.auteur = auteur
    auteur_livre.save()

    return render(request, "livre_form.html",
                  {'livre': livre})
