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

def lecture_my_list(request):
    print('lecture_my_list')
    personne = Personne.find_personne_by_user(request.user)
    lectures = Lecteur.find_by_personne(personne.id)
    livres=[]
    for l in lectures:
        livres.append(l.livre)
    return render(request, 'lecture_list.html',
                    {'livres':    livres,
                    'personnes' : Proprietaire.find_distinct(),
                    'auteurs' :   Auteur.objects.all(),
                    'titre' :     None,
                    'auteur':     None,
                    'personne':   personne.id})

def lecture_search(request):
    print('livre_search')
    query = Lecteur.objects.all()
    personne = None
    auteur = None
    livres = Livre.find_all_lecture_by_user(request.user)


    return render(request, 'lecture_list.html',
                    {'livres':    livres,
                    'personnes' : Proprietaire.find_distinct(),
                    'auteurs' :   Auteur.objects.all(),
                    'titre' :     titre,
                    'auteur':     auteur})

def lecture_list(request):
    livres = Livre.find_all_lecture_by_user(request.user)
    return render(request, 'lecture_list.html',
                    {'livres':livres,
                     'personnes' : Lecture.find_distinct(),
                     'auteurs' : Auteur.objects.all()})


def lecture_create(request):
    lecture = Lecteur()
    return render(request, "lecture_form.html",
                  {'lecture':         lecture})

def lecture_form(request, lecture_id):
    lecture = Lecture.find_by_id(lecture_id)
    return render(request, "lecture_form.html",
                  {'lecture':   lecture,
                   'livres' : Livre.find_all})

def lecture_update(request):
    print('livreupdate')
    livre = Livre()

    if ('add' == request.POST['action'] or 'modify' == request.POST['action']):
        if request.POST['id'] and not request.POST['id'] == 'None':
            livre = get_object_or_404(Livre, pk=request.POST['id'])
        else:
            livre = Livre()
        livre.titre = request.POST['titre']
        livre.langue = request.POST['langue']
        if request.POST['categorie'] and not request.POST['categorie'] == 'None':
            categorie = get_object_or_404(Categorie, pk=request.POST['categorie'])
        else:
            categorie = None
        livre.categorie = categorie
        livre.save()
        lu=False
        if request.POST.get('lu',None) == "on":
            lu= True
        if lu:
            lecture = Livre.find_lecture(livre.id,request.user)
            if lecture:
                pass
            else:
                personne = Personne.find_personne_by_user(request.user)
                lecture = Lecture()
                lecture.livre  = livre
                lecture.personne = personne
                lecture.save()

        else:
            lecture = Livre.find_lecture(livre.id,request.user)
            if lecture:
                lecture.delete()

    return render(request, 'lecture_list.html',
                    {'lectures': Lecteur.find_all()})

def lecture_delete(request, livre_id):
    livre = Livre.find_livre(livre_id)
    lectures = Lecture.find_all_by_user_livre(livre_id,request.user)
    for l in lectures:
        l.delete()
    livres = Livre.find_all_lecture_by_user(request.user)
    return render(request, 'lecture_list.html',
                    {'livres': livres})
