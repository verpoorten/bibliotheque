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
